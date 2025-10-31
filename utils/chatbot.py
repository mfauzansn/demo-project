"""
Simple Rule-Based Chatbot for Demo
"""

import pandas as pd
from datetime import datetime

class DemoChatbot:
    """Simple rule-based chatbot for demo purposes"""
    
    def __init__(self):
        self.context = None
        self.data = {}
    
    def set_context(self, context):
        """Set current context (fraud, pm, demand, quality)"""
        self.context = context
    
    def load_data(self, **kwargs):
        """Load data for current context"""
        self.data = kwargs
    
    def process_message(self, message):
        """
        Process user message and return response
        
        Args:
            message: User's question
        
        Returns:
            Chatbot response string
        """
        message = message.lower().strip()
        
        if self.context == 'fraud':
            return self._handle_fraud_query(message)
        elif self.context == 'pm':
            return self._handle_pm_query(message)
        elif self.context == 'demand':
            return self._handle_demand_query(message)
        elif self.context == 'quality':
            return self._handle_quality_query(message)
        else:
            return "I'm not sure what you're asking about. Please select a specific analysis page first."
    
    def _handle_fraud_query(self, message):
        """Handle fraud detection queries"""
        df = self.data.get('fraud_data')
        
        if df is None:
            return "Please load agent data first to analyze fraud patterns."
        
        # Count queries
        if any(word in message for word in ['berapa', 'jumlah', 'total', 'count', 'how many']):
            if 'fraud' in message or 'critical' in message:
                critical_count = len(df[df['risk_level'] == 'CRITICAL'])
                high_count = len(df[df['risk_level'] == 'HIGH'])
                return f"**Found **{critical_count} CRITICAL** and **{high_count} HIGH** risk agents out of {len(df)} total agents."
            elif 'agent' in message:
                return f"**Total agents in system: **{len(df)}**"
        
        # Risk level queries
        if 'risk' in message or 'status' in message:
            risk_dist = df['risk_level'].value_counts()
            response = "****Risk Distribution:**\n"
            for level, count in risk_dist.items():
                pct = count / len(df) * 100
                response += f"- {level}: {count} ({pct:.1f}%)\n"
            return response
        
        # Top queries
        if 'top' in message or 'tertinggi' in message or 'highest' in message:
            top_5 = df.nlargest(5, 'final_score')[['agent_id', 'name', 'final_score', 'risk_level']]
            response = "****Top 5 Highest Risk Agents:**\n"
            for _, row in top_5.iterrows():
                response += f"- {row['agent_id']}: {row['name']} (Score: {row['final_score']:.1f}, Risk: {row['risk_level']})\n"
            return response
        
        # Pattern queries
        if 'pattern' in message or 'pola' in message:
            device_fraud = df[df['duplicate_device'] > 5]['agent_id'].count()
            ip_fraud = df[df['duplicate_ip'] > 5]['agent_id'].count()
            return f"****Fraud Patterns Detected:**\n- Device farming: {device_fraud} agents\n- IP clustering: {ip_fraud} agents"
        
        # Default
        return "I can help you with:\n- Risk distribution\n- Top risky agents\n- Fraud patterns\n- Agent counts\n\nTry asking: 'Show me top risky agents' or 'What's the risk distribution?'"
    
    def _handle_pm_query(self, message):
        """Handle predictive maintenance queries"""
        df = self.data.get('pm_data')
        
        if df is None:
            return "Please load equipment data first."
        
        # Get latest data
        latest = df.iloc[-1]
        
        # Status queries
        if 'status' in message or 'kondisi' in message or 'bagaimana' in message:
            return f"""****Current Equipment Status:**
- Equipment: {latest['equipment_id']}
- Status: **{latest['status']}**
- Vibration: {latest['vibration']:.2f} mm/s
- Temperature: {latest['temperature']:.1f}°C
- Current: {latest['current']:.1f} A
- Pressure: {latest['pressure']:.1f} bar

{'****Recommendation:** Schedule maintenance within 24-48 hours' if latest['status'] == 'WARNING' else '****URGENT:** Immediate maintenance required!' if latest['status'] == 'CRITICAL' else '****Operating normally**'}
"""
        
        # Vibration queries
        if 'vibration' in message or 'getaran' in message:
            avg_vib = df['vibration'].tail(24).mean()
            max_vib = df['vibration'].tail(24).max()
            return f"****Vibration Analysis (Last 24h):**\n- Current: {latest['vibration']:.2f} mm/s\n- Average: {avg_vib:.2f} mm/s\n- Peak: {max_vib:.2f} mm/s\n- Threshold: 4.0 mm/s (Warning)"
        
        # Temperature queries
        if 'temperature' in message or 'suhu' in message or 'temp' in message:
            avg_temp = df['temperature'].tail(24).mean()
            max_temp = df['temperature'].tail(24).max()
            return f" **Temperature Analysis (Last 24h):**\n- Current: {latest['temperature']:.1f}°C\n- Average: {avg_temp:.1f}°C\n- Peak: {max_temp:.1f}°C\n- Threshold: 85°C (Warning)"
        
        # Trend queries
        if 'trend' in message or 'tren' in message:
            recent_avg = df['vibration'].tail(24).mean()
            older_avg = df['vibration'].tail(48).head(24).mean()
            trend = "increasing" if recent_avg > older_avg else "stable"
            return f"****Trend Analysis:**\n- Vibration trend: {trend}\n- 24h avg: {recent_avg:.2f} mm/s\n- Previous 24h: {older_avg:.2f} mm/s"
        
        # Prediction queries
        if 'predict' in message or 'kapan' in message or 'when' in message or 'fail' in message:
            if latest['status'] == 'CRITICAL':
                return "****Failure Prediction:** High probability of failure within **24-48 hours**. Immediate maintenance recommended!"
            elif latest['status'] == 'WARNING':
                return "****Failure Prediction:** Degradation detected. Estimated **5-7 days** before potential failure. Plan maintenance soon."
            else:
                return "****Failure Prediction:** Equipment operating normally. No immediate maintenance required."
        
        return "I can help you with:\n- Equipment status\n- Vibration analysis\n- Temperature monitoring\n- Trend analysis\n- Failure prediction\n\nTry asking: 'What's the current status?' or 'Show me vibration trend'"
    
    def _handle_demand_query(self, message):
        """Handle demand forecasting queries"""
        df = self.data.get('demand_data')
        
        if df is None:
            return "Please load demand data first."
        
        latest = df.iloc[-1]
        
        # Current demand
        if 'sekarang' in message or 'current' in message or 'hari ini' in message or 'today' in message:
            return f"****Current Demand:**\n- Date: {latest['date'].strftime('%Y-%m-%d')}\n- Demand: **{latest['demand']:.0f} m³/h**\n- Temperature: {latest['temperature']:.1f}°C"
        
        # Average queries
        if 'rata-rata' in message or 'average' in message or 'mean' in message:
            avg_week = df['demand'].tail(7).mean()
            avg_month = df['demand'].tail(30).mean()
            return f"****Average Demand:**\n- Last 7 days: {avg_week:.0f} m³/h\n- Last 30 days: {avg_month:.0f} m³/h"
        
        # Peak queries
        if 'tertinggi' in message or 'peak' in message or 'maximum' in message or 'max' in message:
            peak_week = df['demand'].tail(7).max()
            peak_date = df[df['demand'] == peak_week].iloc[-1]['date']
            return f"****Peak Demand (Last 7 days):**\n- Peak: **{peak_week:.0f} m³/h**\n- Date: {peak_date.strftime('%Y-%m-%d')}"
        
        # Forecast queries
        if 'besok' in message or 'tomorrow' in message or 'prediksi' in message or 'forecast' in message:
            # Simple forecast based on same day last week
            last_week_same_day = df[df['date'] == latest['date'] - pd.Timedelta(days=7)]['demand'].values
            if len(last_week_same_day) > 0:
                forecast = last_week_same_day[0]
                return f"****Demand Forecast (Tomorrow):**\n- Predicted: **{forecast:.0f} m³/h**\n- Based on same day last week pattern\n- Confidence: 85%"
            else:
                return f"****Demand Forecast (Tomorrow):**\n- Predicted: **{latest['demand']:.0f} m³/h** (±100 m³/h)\n- Confidence: 75%"
        
        # Pattern queries
        if 'pattern' in message or 'pola' in message or 'trend' in message:
            weekday_avg = df[df['day_of_week'] < 5]['demand'].mean()
            weekend_avg = df[df['day_of_week'] >= 5]['demand'].mean()
            return f"****Demand Patterns:**\n- Weekday average: {weekday_avg:.0f} m³/h\n- Weekend average: {weekend_avg:.0f} m³/h\n- Weekday/Weekend ratio: {(weekday_avg/weekend_avg):.2f}x"
        
        return "I can help you with:\n- Current demand\n- Average demand\n- Peak demand\n- Demand forecast\n- Usage patterns\n\nTry asking: 'What's today's demand?' or 'Forecast for tomorrow?'"
    
    def _handle_quality_query(self, message):
        """Handle quality anomaly queries"""
        df = self.data.get('quality_data')
        
        if df is None:
            return "Please load quality data first."
        
        latest = df.iloc[-1]
        
        # Current status
        if 'sekarang' in message or 'current' in message or 'status' in message:
            anomaly_status = "**ANOMALY DETECTED" if latest['is_anomaly'] == 1 else "**NORMAL"
            return f"""****Current Water Quality:**
- Status: **{anomaly_status}**
- pH: {latest['ph']:.2f} (normal: 7.0-8.0)
- Turbidity: {latest['turbidity']:.2f} NTU (normal: <1.0)
- Conductivity: {latest['conductivity']:.0f} µS/cm (normal: 400-600)
- Chlorine: {latest['chlorine']:.2f} mg/L (normal: 0.5-1.0)
"""
        
        # pH queries
        if 'ph' in message:
            avg_ph = df['ph'].tail(24).mean()
            return f"****pH Analysis:**\n- Current: {latest['ph']:.2f}\n- 24h average: {avg_ph:.2f}\n- Range: 7.0-8.0 (optimal)"
        
        # Turbidity queries
        if 'turbidity' in message or 'kekeruhan' in message:
            avg_turb = df['turbidity'].tail(24).mean()
            return f"****Turbidity Analysis:**\n- Current: {latest['turbidity']:.2f} NTU\n- 24h average: {avg_turb:.2f} NTU\n- Threshold: <1.0 NTU"
        
        # Anomaly count
        if 'anomaly' in message or 'anomali' in message or 'berapa' in message:
            anomaly_count = df['is_anomaly'].tail(168).sum()  # Last 7 days
            anomaly_pct = anomaly_count / len(df.tail(168)) * 100
            return f"****Anomaly Report (Last 7 days):**\n- Anomalies detected: {int(anomaly_count)}\n- Percentage: {anomaly_pct:.1f}%\n- Status: {'**High anomaly rate' if anomaly_pct > 5 else '**Normal range'}"
        
        # Trend queries
        if 'trend' in message or 'tren' in message:
            recent_anomalies = df['is_anomaly'].tail(24).sum()
            older_anomalies = df['is_anomaly'].tail(48).head(24).sum()
            trend = "increasing" if recent_anomalies > older_anomalies else "decreasing" if recent_anomalies < older_anomalies else "stable"
            return f"****Anomaly Trend:**\n- Last 24h: {int(recent_anomalies)} anomalies\n- Previous 24h: {int(older_anomalies)} anomalies\n- Trend: {trend}"
        
        return "I can help you with:\n- Current water quality\n- pH levels\n- Turbidity analysis\n- Anomaly counts\n- Trend analysis\n\nTry asking: 'What's the current quality?' or 'How many anomalies today?'"
