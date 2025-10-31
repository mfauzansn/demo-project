"""
Data Generator for Synthetic Data
Generates realistic data for both case studies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataGenerator:
    """Generate synthetic data for demos"""
    
    @staticmethod
    def generate_agent_data(n_agents=100, fraud_ratio=0.15):
        """
        Generate synthetic agent registration data for fraud detection
        
        Args:
            n_agents: Number of agents to generate
            fraud_ratio: Ratio of fraudulent agents
        
        Returns:
            DataFrame with agent data
        """
        np.random.seed(42)
        random.seed(42)
        
        n_fraud = int(n_agents * fraud_ratio)
        n_normal = n_agents - n_fraud
        
        # Generate normal agents
        normal_agents = []
        for i in range(n_normal):
            agent = {
                'agent_id': f'AGT{1000 + i:04d}',
                'name': f'Agent {i+1}',
                'email': f'agent{i+1}@email.com',
                'phone': f'08{random.randint(10, 99)}{random.randint(10000000, 99999999)}',
                'device_id': f'DEV{random.randint(1000, 9999)}',
                'ip_address': f'192.168.{random.randint(1, 255)}.{random.randint(1, 255)}',
                'city': random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang']),
                'registration_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'duplicate_device': random.randint(0, 2),
                'duplicate_ip': random.randint(0, 2),
                'duplicate_email': 0,
                'duplicate_phone': 0,
                'rapid_registration': random.randint(0, 3),
                'total_transactions': random.randint(5, 50),
                'avg_transaction': round(random.uniform(200000, 800000), 2),
                'is_fraud': 0
            }
            normal_agents.append(agent)
        
        # Generate fraud agents
        fraud_agents = []
        fraud_devices = [f'DEV{random.randint(1000, 1100)}' for _ in range(5)]
        fraud_ips = [f'103.{random.randint(10, 50)}.1.1' for _ in range(5)]
        
        for i in range(n_fraud):
            agent = {
                'agent_id': f'AGT{1000 + n_normal + i:04d}',
                'name': f'Agent{i+100}',  # Suspicious name
                'email': f'test{i}@tempmail.com',  # Temp email
                'phone': f'081111111{i:02d}',  # Pattern phone
                'device_id': random.choice(fraud_devices),  # Shared device
                'ip_address': random.choice(fraud_ips),  # Shared IP
                'city': random.choice(['Jakarta', 'Tangerang']),
                'registration_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'duplicate_device': random.randint(5, 15),
                'duplicate_ip': random.randint(5, 15),
                'duplicate_email': random.randint(0, 3),
                'duplicate_phone': random.randint(0, 3),
                'rapid_registration': random.randint(10, 30),
                'total_transactions': random.randint(1, 5),
                'avg_transaction': round(random.choice([1000000, 2000000, 5000000]), 2),  # Round numbers
                'is_fraud': 1
            }
            fraud_agents.append(agent)
        
        # Combine and shuffle
        all_agents = normal_agents + fraud_agents
        random.shuffle(all_agents)
        
        df = pd.DataFrame(all_agents)

        # Rename to match Streamlit app expected columns
        df.rename(columns={
            'duplicate_device': 'duplicate_devices',
            'duplicate_ip': 'duplicate_ips'
        }, inplace=True)

        # Add columns expected by app but not generated here
        df['same_location_count'] = df.groupby('city')['city'].transform('count') - 1

        # Placeholder model scores (to avoid KeyError before fraud detector runs)
        df['rule_based_score'] = np.nan
        df['ml_score'] = np.nan

        return df
    
    @staticmethod
    def generate_iot_sensor_data(n_days=90, equipment='PUMP_01'):
        """
        Generate synthetic IoT sensor data for predictive maintenance
        
        Args:
            n_days: Number of days of data
            equipment: Equipment name
        
        Returns:
            DataFrame with sensor data
        """
        np.random.seed(42)
        
        # Generate timestamps
        end_date = datetime.now()
        start_date = end_date - timedelta(days=n_days)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='1h')
        
        n_points = len(timestamps)
        
        # Simulate degradation pattern
        # Normal operation (first 70% of time)
        normal_period = int(n_points * 0.7)
        degradation_period = int(n_points * 0.2)
        critical_period = n_points - normal_period - degradation_period
        
        # Vibration (mm/s)
        vibration_normal = np.random.normal(2.0, 0.3, normal_period)
        vibration_degrad = np.linspace(2.0, 4.5, degradation_period) + np.random.normal(0, 0.5, degradation_period)
        vibration_critical = np.linspace(4.5, 8.0, critical_period) + np.random.normal(0, 0.8, critical_period)
        vibration = np.concatenate([vibration_normal, vibration_degrad, vibration_critical])
        
        # Temperature (°C)
        temp_normal = np.random.normal(65, 3, normal_period)
        temp_degrad = np.linspace(65, 85, degradation_period) + np.random.normal(0, 4, degradation_period)
        temp_critical = np.linspace(85, 100, critical_period) + np.random.normal(0, 5, critical_period)
        temperature = np.concatenate([temp_normal, temp_degrad, temp_critical])
        
        # Current (A)
        current_normal = np.random.normal(45, 2, normal_period)
        current_degrad = np.linspace(45, 55, degradation_period) + np.random.normal(0, 3, degradation_period)
        current_critical = np.linspace(55, 65, critical_period) + np.random.normal(0, 4, critical_period)
        current = np.concatenate([current_normal, current_degrad, current_critical])
        
        # Pressure (bar)
        pressure = np.random.normal(8.5, 0.5, n_points)
        
        # Status
        status = ['NORMAL'] * normal_period + ['WARNING'] * degradation_period + ['CRITICAL'] * critical_period
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'equipment_id': equipment,
            'vibration': vibration,
            'temperature': temperature,
            'current': current,
            'pressure': pressure,
            'status': status
        })
        
        return df
    
    @staticmethod
    def generate_demand_data(n_days=365):
        """
        Generate synthetic water demand data
        
        Args:
            n_days: Number of days of data
        
        Returns:
            DataFrame with demand data
        """
        np.random.seed(42)
        
        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=n_days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Base demand
        base_demand = 2500  # m³/h
        
        # Weekly seasonality (weekday vs weekend)
        weekly_pattern = []
        for date in dates:
            if date.weekday() < 5:  # Weekday
                weekly_pattern.append(1.0)
            else:  # Weekend
                weekly_pattern.append(0.8)
        
        # Monthly seasonality (simplified)
        monthly_pattern = np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 0.1 + 1.0
        
        # Trend (slight increase)
        trend = np.linspace(1.0, 1.05, len(dates))
        
        # Combine patterns
        demand = base_demand * np.array(weekly_pattern) * monthly_pattern * trend
        
        # Add noise
        demand += np.random.normal(0, 100, len(dates))
        
        # Temperature correlation
        temperature = 20 + 10 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.normal(0, 3, len(dates))
        
        df = pd.DataFrame({
            'date': dates,
            'demand': demand,
            'temperature': temperature,
            'day_of_week': [d.weekday() for d in dates],
            'month': [d.month for d in dates]
        })
        
        return df
    
    @staticmethod
    def generate_quality_data(n_days=30):
        """
        Generate synthetic water quality data for anomaly detection
        
        Args:
            n_days: Number of days of data
        
        Returns:
            DataFrame with quality data
        """
        np.random.seed(42)
        
        # Generate timestamps (hourly)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=n_days)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='h')
        
        n_points = len(timestamps)
        
        # Normal parameters
        ph = np.random.normal(7.5, 0.2, n_points)
        turbidity = np.random.normal(0.5, 0.1, n_points)
        conductivity = np.random.normal(500, 50, n_points)
        chlorine = np.random.normal(0.8, 0.1, n_points)
        
        # Inject anomalies (5% of data)
        n_anomalies = int(n_points * 0.05)
        anomaly_indices = np.random.choice(n_points, n_anomalies, replace=False)
        
        for idx in anomaly_indices:
            ph[idx] += np.random.choice([-1, 1]) * np.random.uniform(1, 2)
            turbidity[idx] += np.random.uniform(2, 5)
            conductivity[idx] += np.random.choice([-1, 1]) * np.random.uniform(200, 500)
        
        # Mark anomalies
        is_anomaly = np.zeros(n_points)
        is_anomaly[anomaly_indices] = 1
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'ph': ph,
            'turbidity': turbidity,
            'conductivity': conductivity,
            'chlorine': chlorine,
            'is_anomaly': is_anomaly
        })
        
        return df
