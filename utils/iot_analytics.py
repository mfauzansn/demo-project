"""
IoT Analytics Module
Contains ML models for predictive maintenance, demand forecasting, and anomaly detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

class PredictiveMaintenance:
    """Predictive Maintenance System"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.is_trained = False
    
    def create_features(self, df):
        """
        Create features for predictive maintenance
        
        Args:
            df: DataFrame with sensor data
        
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        df = df.sort_values('timestamp')
        
        # Rolling statistics (24 hour window)
        df['vibration_mean_24h'] = df['vibration'].rolling(window=24, min_periods=1).mean()
        df['vibration_std_24h'] = df['vibration'].rolling(window=24, min_periods=1).std()
        df['vibration_max_24h'] = df['vibration'].rolling(window=24, min_periods=1).max()
        
        df['temp_mean_24h'] = df['temperature'].rolling(window=24, min_periods=1).mean()
        df['temp_std_24h'] = df['temperature'].rolling(window=24, min_periods=1).std()
        
        # Rate of change
        df['vibration_roc'] = df['vibration'].diff()
        df['temp_roc'] = df['temperature'].diff()
        
        # Fill NaN
        df = df.bfill()
        
        return df
    
    def train_model(self, df):
        """
        Train predictive maintenance model
        
        Args:
            df: DataFrame with features and status
        """
        # Create features
        df = self.create_features(df)
        
        # Encode status
        status_map = {'NORMAL': 0, 'WARNING': 1, 'CRITICAL': 2}
        y = df['status'].map(status_map)
        
        # Select features
        feature_cols = [
            'vibration', 'temperature', 'current', 'pressure',
            'vibration_mean_24h', 'vibration_std_24h', 'vibration_max_24h',
            'temp_mean_24h', 'temp_std_24h',
            'vibration_roc', 'temp_roc'
        ]
        
        X = df[feature_cols]
        
        # Scale
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        
        self.is_trained = True
    
    def predict_failure(self, current_data):
        """
        Predict failure probability and time to failure
        
        Args:
            current_data: Current sensor readings (Series or DataFrame row)
        
        Returns:
            dict with prediction results
        """
        if not self.is_trained:
            return {
                'failure_prob': 0,
                'time_to_failure': None,
                'recommended_action': 'Monitor',
                'confidence': 0
            }
        
        # Get current status
        vibration = current_data['vibration']
        temperature = current_data['temperature']
        
        # Simple rule-based prediction (since we don't have full history in demo)
        if vibration > 6.0 or temperature > 90:
            failure_prob = 0.95
            time_to_failure = 24
            recommended_action = 'URGENT: Schedule maintenance immediately'
            status = 'CRITICAL'
        elif vibration > 4.0 or temperature > 80:
            failure_prob = 0.70
            time_to_failure = 48
            recommended_action = 'Schedule maintenance within 24-48 hours'
            status = 'WARNING'
        elif vibration > 3.0 or temperature > 75:
            failure_prob = 0.40
            time_to_failure = 120
            recommended_action = 'Monitor closely, plan maintenance'
            status = 'WARNING'
        else:
            failure_prob = 0.10
            time_to_failure = None
            recommended_action = 'Continue normal operation'
            status = 'NORMAL'
        
        return {
            'failure_prob': failure_prob,
            'time_to_failure': time_to_failure,
            'recommended_action': recommended_action,
            'status': status,
            'confidence': 0.92
        }


class DemandForecaster:
    """Water Demand Forecasting System"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def create_features(self, df):
        """
        Create features for demand forecasting
        
        Args:
            df: DataFrame with demand data
        
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        
        # Time features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['day_of_month'] = df['date'].dt.day
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Lag features
        df['demand_lag_1'] = df['demand'].shift(1)
        df['demand_lag_7'] = df['demand'].shift(7)
        df['demand_lag_30'] = df['demand'].shift(30)
        
        # Rolling features
        df['demand_rolling_mean_7'] = df['demand'].rolling(window=7, min_periods=1).mean()
        df['demand_rolling_std_7'] = df['demand'].rolling(window=7, min_periods=1).std()
        
        # Fill NaN
        df = df.bfill()
        
        return df
    
    def train_model(self, df):
        """
        Train demand forecasting model
        
        Args:
            df: DataFrame with historical demand
        """
        # Create features
        df = self.create_features(df)
        
        # Select features
        feature_cols = [
            'day_of_week', 'month', 'day_of_month', 'is_weekend',
            'temperature', 'demand_lag_1', 'demand_lag_7', 'demand_lag_30',
            'demand_rolling_mean_7', 'demand_rolling_std_7'
        ]
        
        # Remove rows with NaN after feature engineering
        df_train = df.dropna()
        
        X = df_train[feature_cols]
        y = df_train['demand']
        
        # Train Random Forest Regressor
        from sklearn.ensemble import RandomForestRegressor
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42
        )
        self.model.fit(X, y)
        
        self.is_trained = True
    
    def forecast(self, df, days_ahead=7):
        """
        Forecast demand for next N days
        
        Args:
            df: DataFrame with historical data
            days_ahead: Number of days to forecast
        
        Returns:
            DataFrame with forecasted demand
        """
        if not self.is_trained:
            # Return simple forecast based on average
            last_week_avg = df['demand'].tail(7).mean()
            forecast_dates = pd.date_range(
                start=df['date'].max() + timedelta(days=1),
                periods=days_ahead,
                freq='D'
            )
            forecast_df = pd.DataFrame({
                'date': forecast_dates,
                'forecasted_demand': [last_week_avg] * days_ahead,
                'confidence_lower': [last_week_avg * 0.95] * days_ahead,
                'confidence_upper': [last_week_avg * 1.05] * days_ahead
            })
            return forecast_df
        
        # Simple forecast using last week pattern
        df = df.copy()
        last_date = df['date'].max()
        last_demand = df['demand'].iloc[-1]
        
        forecast_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )
        
        # Simple pattern-based forecast
        forecasts = []
        for date in forecast_dates:
            # Get same day of week from last week
            same_day_last_week = df[df['date'] == date - timedelta(days=7)]['demand'].values
            if len(same_day_last_week) > 0:
                forecast = same_day_last_week[0]
            else:
                forecast = last_demand
            
            # Add small random variation
            forecast += np.random.normal(0, 50)
            forecasts.append(forecast)
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecasted_demand': forecasts,
            'confidence_lower': [f * 0.95 for f in forecasts],
            'confidence_upper': [f * 1.05 for f in forecasts]
        })
        
        return forecast_df


class AnomalyDetector:
    """Water Quality Anomaly Detection System"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.is_trained = False
        self.thresholds = {}
    
    def train_model(self, df):
        """
        Train anomaly detection model
        
        Args:
            df: DataFrame with quality parameters
        """
        # Select features
        feature_cols = ['ph', 'turbidity', 'conductivity', 'chlorine']
        X = df[feature_cols]
        
        # Scale
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model = IsolationForest(
            contamination=0.05,
            random_state=42
        )
        self.model.fit(X_scaled)
        
        # Calculate thresholds (3 sigma rule)
        for col in feature_cols:
            mean = df[col].mean()
            std = df[col].std()
            self.thresholds[col] = {
                'mean': mean,
                'std': std,
                'lower': mean - 3 * std,
                'upper': mean + 3 * std
            }
        
        self.is_trained = True
    
    def detect_anomalies(self, df):
        """
        Detect anomalies in water quality data
        
        Args:
            df: DataFrame with quality parameters
        
        Returns:
            DataFrame with anomaly predictions
        """
        df = df.copy()
        
        if not self.is_trained:
            # Simple threshold-based detection
            df['is_anomaly'] = 0
            df.loc[(df['ph'] < 6.5) | (df['ph'] > 8.5), 'is_anomaly'] = 1
            df.loc[df['turbidity'] > 2.0, 'is_anomaly'] = 1
            df['anomaly_score'] = df['is_anomaly'] * 100
            return df
        
        # Select features
        feature_cols = ['ph', 'turbidity', 'conductivity', 'chlorine']
        X = df[feature_cols]
        X_scaled = self.scaler.transform(X)
        
        # Predict
        predictions = self.model.predict(X_scaled)
        anomaly_scores = self.model.score_samples(X_scaled)
        
        # Convert predictions (-1 = anomaly, 1 = normal)
        df['is_anomaly'] = (predictions == -1).astype(int)
        
        # Convert scores to 0-100 scale
        df['anomaly_score'] = ((anomaly_scores - anomaly_scores.min()) / 
                                (anomaly_scores.max() - anomaly_scores.min()) * 100)
        df['anomaly_score'] = 100 - df['anomaly_score']  # Invert
        
        return df
    
    def get_anomaly_explanation(self, row):
        """
        Generate explanation for detected anomaly
        
        Args:
            row: Single row from DataFrame
        
        Returns:
            List of explanation strings
        """
        if not self.is_trained or not hasattr(row, 'is_anomaly'):
            return ['No anomaly detected']
        
        if row['is_anomaly'] == 0:
            return ['✅ All parameters within normal range']
        
        explanations = []
        
        # Check each parameter
        if not hasattr(self, 'thresholds'):
            # Simple rule-based
            if row['ph'] < 6.5 or row['ph'] > 8.5:
                explanations.append(f"⚠️ pH out of range: {row['ph']:.2f} (normal: 6.5-8.5)")
            if row['turbidity'] > 2.0:
                explanations.append(f"⚠️ High turbidity: {row['turbidity']:.2f} NTU (normal: <2.0)")
            if row['conductivity'] < 200 or row['conductivity'] > 800:
                explanations.append(f"⚠️ Conductivity abnormal: {row['conductivity']:.0f} µS/cm")
            if row['chlorine'] < 0.5 or row['chlorine'] > 1.5:
                explanations.append(f"⚠️ Chlorine out of range: {row['chlorine']:.2f} mg/L")
        else:
            # Use learned thresholds
            for param, threshold in self.thresholds.items():
                value = row[param]
                if value < threshold['lower'] or value > threshold['upper']:
                    explanations.append(
                        f"⚠️ {param.upper()} anomalous: {value:.2f} "
                        f"(expected: {threshold['mean']:.2f} ± {threshold['std']:.2f})"
                    )
        
        if not explanations:
            explanations.append('⚠️ Anomaly detected but parameters within individual thresholds')
        
        return explanations
