"""
Fraud Detection Module
Contains ML models and scoring logic for fraud detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle

class FraudDetector:
    """Fraud Detection System"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.rf_model = None
        self.iso_forest = None
        self.is_trained = False
    
    def calculate_rule_based_score(self, df):
        """
        Calculate fraud score using rule-based approach
        
        Args:
            df: DataFrame with agent data
        
        Returns:
            DataFrame with fraud_score column
        """
        df = df.copy()
        
        # Initialize score
        df['fraud_score'] = 0
        
        # Rule 1: Duplicate device (30 points)
        df.loc[df['duplicate_device'] > 5, 'fraud_score'] += 30
        df.loc[df['duplicate_device'] > 10, 'fraud_score'] += 10  # Extra
        
        # Rule 2: Duplicate IP (25 points)
        df.loc[df['duplicate_ip'] > 5, 'fraud_score'] += 25
        df.loc[df['duplicate_ip'] > 10, 'fraud_score'] += 10  # Extra
        
        # Rule 3: Duplicate email domain (20 points)
        df.loc[df['duplicate_email'] > 0, 'fraud_score'] += 20
        
        # Rule 4: Duplicate phone (20 points)
        df.loc[df['duplicate_phone'] > 0, 'fraud_score'] += 20
        
        # Rule 5: Rapid registration (15 points)
        df.loc[df['rapid_registration'] > 10, 'fraud_score'] += 15
        df.loc[df['rapid_registration'] > 20, 'fraud_score'] += 10  # Extra
        
        # Rule 6: Suspicious email patterns (15 points)
        suspicious_domains = ['tempmail.com', 'guerrillamail.com', 'temp.com']
        for domain in suspicious_domains:
            df.loc[df['email'].str.contains(domain, na=False), 'fraud_score'] += 15
        
        # Rule 7: Low transaction activity (10 points)
        df.loc[df['total_transactions'] < 3, 'fraud_score'] += 10
        
        # Rule 8: Round number transactions (10 points)
        # Check if avg_transaction is a round million
        is_round = df['avg_transaction'] % 1000000 == 0
        df.loc[is_round, 'fraud_score'] += 10
        
        # Cap at 100
        df['fraud_score'] = df['fraud_score'].clip(upper=100)
        
        return df
    
    def assign_risk_level(self, df):
        """
        Assign risk level based on fraud score using numpy.select
        
        Args:
            df: DataFrame with fraud_score column
        
        Returns:
            DataFrame with risk_level column
        """
        import numpy as np
        
        df = df.copy()
        
        # Extract fraud_score as numpy array to ensure 1D
        scores = df['fraud_score'].values
        
        # Define conditions using numpy
        conditions = [
            scores >= 70,
            scores >= 50,
            scores >= 30
        ]
        
        choices = ['CRITICAL', 'HIGH', 'MEDIUM']
        
        # Use numpy.select for vectorized assignment
        df['risk_level'] = np.select(conditions, choices, default='LOW')
        
        return df
    
    def train_ml_models(self, df):
        """
        Train ML models on the data
        
        Args:
            df: DataFrame with features and is_fraud label
        """
        # Select features
        feature_cols = [
            'duplicate_device', 'duplicate_ip', 'duplicate_email', 
            'duplicate_phone', 'rapid_registration', 'total_transactions',
            'avg_transaction'
        ]
        
        X = df[feature_cols]
        y = df['is_fraud']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.rf_model.fit(X_scaled, y)
        
        # Train Isolation Forest
        self.iso_forest = IsolationForest(
            contamination=0.15,
            random_state=42
        )
        self.iso_forest.fit(X_scaled)
        
        self.is_trained = True
    
    def predict_ml_score(self, df):
        """
        Predict fraud using ML models
        
        Args:
            df: DataFrame with features
        
        Returns:
            DataFrame with ml_fraud_prob and anomaly_score columns
        """
        if not self.is_trained:
            raise ValueError("Models not trained. Call train_ml_models first.")
        
        df = df.copy()
        
        # Select features
        feature_cols = [
            'duplicate_device', 'duplicate_ip', 'duplicate_email', 
            'duplicate_phone', 'rapid_registration', 'total_transactions',
            'avg_transaction'
        ]
        
        X = df[feature_cols]
        X_scaled = self.scaler.transform(X)
        
        # Random Forest prediction
        df['ml_fraud_prob'] = self.rf_model.predict_proba(X_scaled)[:, 1] * 100
        
        # Isolation Forest prediction (-1 = anomaly, 1 = normal)
        iso_pred = self.iso_forest.predict(X_scaled)
        iso_score = self.iso_forest.score_samples(X_scaled)
        
        # Convert to 0-100 score (more negative = more anomalous)
        df['anomaly_score'] = ((iso_score - iso_score.min()) / (iso_score.max() - iso_score.min()) * 100)
        df['anomaly_score'] = 100 - df['anomaly_score']  # Invert so higher = more anomalous
        
        return df
    
    def get_ensemble_score(self, df):
        """
        Calculate ensemble score from all methods
        
        Args:
            df: DataFrame with fraud_score, ml_fraud_prob, anomaly_score
        
        Returns:
            DataFrame with final_score column
        """
        df = df.copy()
        
        # Weighted average
        df['final_score'] = (
            df['fraud_score'] * 0.4 +  # Rule-based: 40%
            df['ml_fraud_prob'] * 0.4 +  # ML prediction: 40%
            df['anomaly_score'] * 0.2  # Anomaly detection: 20%
        )
        
        # Re-assign risk level based on final score
        df = self.assign_risk_level(df.rename(columns={'final_score': 'fraud_score'}))
        df = df.rename(columns={'fraud_score': 'final_score'})
        
        return df
    
    def generate_explanation(self, agent_row):
        """
        Generate human-readable explanation for fraud score
        
        Args:
            agent_row: Single row from DataFrame
        
        Returns:
            List of explanation strings
        """
        explanations = []
        
        if agent_row['duplicate_device'] > 5:
            explanations.append(f"⚠️ Device used by {agent_row['duplicate_device']} agents")
        
        if agent_row['duplicate_ip'] > 5:
            explanations.append(f"⚠️ IP address shared with {agent_row['duplicate_ip']} agents")
        
        if agent_row['duplicate_email'] > 0:
            explanations.append(f"⚠️ Email domain duplicated")
        
        if agent_row['duplicate_phone'] > 0:
            explanations.append(f"⚠️ Phone number pattern duplicated")
        
        if agent_row['rapid_registration'] > 10:
            explanations.append(f"⚠️ Part of rapid registration batch ({agent_row['rapid_registration']} agents)")
        
        if '@tempmail.com' in agent_row['email'] or '@temp.com' in agent_row['email']:
            explanations.append(f"⚠️ Temporary email service detected")
        
        if agent_row['total_transactions'] < 3:
            explanations.append(f"⚠️ Very low transaction activity ({agent_row['total_transactions']} transactions)")
        
        if agent_row['avg_transaction'] % 1000000 == 0:
            explanations.append(f"⚠️ Suspicious round-number transactions")
        
        if not explanations:
            explanations.append("✅ No major risk indicators detected")
        
        return explanations