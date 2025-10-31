import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from utils.data_generator import DataGenerator
from utils.iot_analytics import PredictiveMaintenance, DemandForecaster, AnomalyDetector
from utils.chatbot import DemoChatbot

# Page config
st.set_page_config(
    page_title="Case Study 2: Industrial IoT",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'pm_data' not in st.session_state:
    st.session_state.pm_data = None
if 'demand_data' not in st.session_state:
    st.session_state.demand_data = None
if 'quality_data' not in st.session_state:
    st.session_state.quality_data = None
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = DemoChatbot()
if 'iot_chat_messages' not in st.session_state:
    st.session_state.iot_chat_messages = []

# Header
st.title("Case Study 2: Industrial IoT Analytics")
st.markdown("---")

# Overview Section
with st.expander("Case Study Overview", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Business Challenge
        
        A **water treatment & distribution facility** faced operational challenges:
        - **Unplanned equipment downtime** costing millions
        - **Inefficient production planning** leading to energy waste
        - **Quality issues** detected too late
        - **Manual monitoring** unable to scale with growth
        
        **Annual Impact:**
        - Downtime cost: ~Rp 5 billion
        - Energy waste: 20-25% of operational costs
        - Quality incidents: 12-15 per year
        - Reactive maintenance approach
        """)
    
    with col2:
        st.markdown("""
        ### Solution Delivered
        
        **End-to-End IoT Analytics Platform** featuring:
        ****Predictive Maintenance** - predict failures 48h in advance
        ****Demand Forecasting** - optimize production planning
        ****Real-time Anomaly Detection** - quality monitoring
        ****Command Center Dashboard** - unified operations view
        
        **Business Impact:**
        **30-40% reduction in downtime
        **15-20% energy savings
        **95% prediction accuracy
        **Real-time alerting system
        """)

st.markdown("---")

# Main Tabs
main_tab1, main_tab2, main_tab3 = st.tabs([
    "Predictive Maintenance",
    "Demand Forecasting", 
    "Quality Monitoring"
])

# ========== TAB 1: PREDICTIVE MAINTENANCE ==========
with main_tab1:
    st.subheader("Predictive Maintenance")
    
    # Data generation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        days_pm = st.slider("Historical Data (days)", min_value=30, max_value=180, value=90, step=30, key='pm_days')
    
    with col2:
        if st.button("Generate PM Data", use_container_width=True):
            with st.spinner("Generating sensor data..."):
                df = DataGenerator.generate_iot_sensor_data(n_days=days_pm, equipment='PUMP_01')
                st.session_state.pm_data = df
                
                # Train model
                pm_model = PredictiveMaintenance()
                pm_model.train_model(df)
                st.session_state.pm_model = pm_model
                
                # Load to chatbot
                st.session_state.chatbot.set_context('pm')
                st.session_state.chatbot.load_data(pm_data=df)
            
            st.success("Success: Predictive maintenance data generated!")
    
    if st.session_state.pm_data is not None:
        df = st.session_state.pm_data
        pm_model = st.session_state.pm_model
        
        # Get latest reading
        latest = df.iloc[-1]
        
        # Predict failure
        prediction = pm_model.predict_failure(latest)
        
        # Key Metrics
        st.markdown("#### Status: Equipment Status")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            status_color = {
                'NORMAL': '[OK]',
                'WARNING': '[WARNING]',
                'CRITICAL': '[CRITICAL]'
            }
            st.metric("Status", f"{status_color[prediction['status']]} {prediction['status']}")
        
        with col2:
            st.metric("Vibration", f"{latest['vibration']:.2f} mm/s", 
                     delta=f"{latest['vibration'] - df['vibration'].mean():.2f}")
        
        with col3:
            st.metric("Temperature", f"{latest['temperature']:.1f}°C",
                     delta=f"{latest['temperature'] - df['temperature'].mean():.1f}°C")
        
        with col4:
            st.metric("Failure Probability", f"{prediction['failure_prob']*100:.0f}%")
        
        with col5:
            if prediction['time_to_failure']:
                st.metric("Time to Failure", f"~{prediction['time_to_failure']}h")
            else:
                st.metric("Time to Failure", "N/A")
        
        # Alert box
        if prediction['status'] == 'CRITICAL':
            st.error(f"CRITICAL ALERT: {prediction['recommended_action']}")
        elif prediction['status'] == 'WARNING':
            st.warning(f"WARNING: {prediction['recommended_action']}")
        else:
            st.success(f"Success: **NORMAL:** {prediction['recommended_action']}")
        
        st.markdown("---")
        
        # Visualizations
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "Time Series", "Correlation", "Statistics", "AI Chat"
        ])
        
        with sub_tab1:
            st.markdown("### Sensor Data Over Time")
            
            # Vibration trend
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['vibration'],
                mode='lines',
                name='Vibration',
                line=dict(color='#636EFA')
            ))
            
            # Add threshold lines
            fig.add_hline(y=4.0, line_dash="dash", line_color="orange", annotation_text="Warning Threshold")
            fig.add_hline(y=6.0, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
            
            # Color background by status
            for status in ['NORMAL', 'WARNING', 'CRITICAL']:
                status_data = df[df['status'] == status]
                if len(status_data) > 0:
                    fig.add_vrect(
                        x0=status_data['timestamp'].min(),
                        x1=status_data['timestamp'].max(),
                        fillcolor={'NORMAL': 'green', 'WARNING': 'yellow', 'CRITICAL': 'red'}[status],
                        opacity=0.1,
                        layer="below",
                        line_width=0
                    )
            
            fig.update_layout(
                title="Vibration Trend",
                xaxis_title="Timestamp",
                yaxis_title="Vibration (mm/s)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Temperature trend
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['temperature'],
                mode='lines',
                name='Temperature',
                line=dict(color='#EF553B')
            ))
            
            fig.add_hline(y=85, line_dash="dash", line_color="orange", annotation_text="Warning Threshold")
            fig.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
            
            fig.update_layout(
                title="Temperature Trend",
                xaxis_title="Timestamp",
                yaxis_title="Temperature (°C)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Multi-parameter view
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Vibration', 'Temperature', 'Current', 'Pressure')
            )
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['vibration'], name='Vibration', line=dict(color='#636EFA')),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['temperature'], name='Temperature', line=dict(color='#EF553B')),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['current'], name='Current', line=dict(color='#00CC96')),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['pressure'], name='Pressure', line=dict(color='#AB63FA')),
                row=2, col=2
            )
            
            fig.update_layout(height=600, title_text="All Parameters")
            st.plotly_chart(fig, use_container_width=True)
        
        with sub_tab2:
            st.markdown("###  Parameter Correlation Analysis")
            
            # Correlation matrix
            corr_data = df[['vibration', 'temperature', 'current', 'pressure']].corr()
            
            fig = px.imshow(
                corr_data,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title="Correlation Matrix"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Scatter plots
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(
                    df,
                    x='vibration',
                    y='temperature',
                    color='status',
                    title="Vibration vs Temperature",
                    trendline="ols"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(
                    df,
                    x='vibration',
                    y='current',
                    color='status',
                    title="Vibration vs Current",
                    trendline="ols"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with sub_tab3:
            st.markdown("### Status: Statistical Summary")
            
            # Statistics by status
            stats_df = df.groupby('status')[['vibration', 'temperature', 'current', 'pressure']].agg(['mean', 'std', 'min', 'max'])
            
            st.dataframe(stats_df.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
            
            # Distribution plots
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.box(
                    df,
                    x='status',
                    y='vibration',
                    color='status',
                    title="Vibration Distribution by Status"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.box(
                    df,
                    x='status',
                    y='temperature',
                    color='status',
                    title="Temperature Distribution by Status"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Histograms
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    df,
                    x='vibration',
                    color='status',
                    title="Vibration Histogram",
                    nbins=30,
                    barmode='overlay',
                    opacity=0.7
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(
                    df,
                    x='temperature',
                    color='status',
                    title="Temperature Histogram",
                    nbins=30,
                    barmode='overlay',
                    opacity=0.7
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with sub_tab4:
            st.markdown("### AI Assistant - Predictive Maintenance")
            
            # Chat interface
            for message in st.session_state.iot_chat_messages:
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI:** {message['content']}")
                st.markdown("---")
            
            # Chat input
            col1, col2 = st.columns([4, 1])
            
            with col1:
                pm_chat_input = st.text_input("Ask about equipment status...", key="pm_chat_input",
                                             placeholder="e.g., 'What's the current status?'")
            
            with col2:
                if st.button("Send", key="pm_send"):
                    if pm_chat_input:
                        st.session_state.iot_chat_messages.append({'role': 'user', 'content': pm_chat_input})
                        response = st.session_state.chatbot.process_message(pm_chat_input)
                        st.session_state.iot_chat_messages.append({'role': 'bot', 'content': response})
                        st.rerun()
            
            if st.button("Clear Chat", key="pm_clear"):
                st.session_state.iot_chat_messages = []
                st.rerun()
    
    else:
        st.info("Please generate predictive maintenance data to start analysis")

# ========== TAB 2: DEMAND FORECASTING ==========
with main_tab2:
    st.subheader("📈 Water Demand Forecasting")
    
    # Data generation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        days_demand = st.slider("Historical Data (days)", min_value=90, max_value=730, value=365, step=30, key='demand_days')
    
    with col2:
        if st.button("Generate Demand Data", use_container_width=True):
            with st.spinner("Generating demand data..."):
                df = DataGenerator.generate_demand_data(n_days=days_demand)
                st.session_state.demand_data = df
                
                # Train model
                forecaster = DemandForecaster()
                forecaster.train_model(df)
                st.session_state.forecaster = forecaster
                
                # Load to chatbot
                st.session_state.chatbot.set_context('demand')
                st.session_state.chatbot.load_data(demand_data=df)
            
            st.success("Success: Demand forecasting data generated!")
    
    if st.session_state.demand_data is not None:
        df = st.session_state.demand_data
        forecaster = st.session_state.forecaster
        
        # Get forecast
        forecast_days = st.slider("Forecast horizon (days)", min_value=1, max_value=30, value=7, key='forecast_days')
        forecast_df = forecaster.forecast(df, days_ahead=forecast_days)
        
        # Key Metrics
        st.markdown("#### Status: Demand Summary")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            current_demand = df['demand'].iloc[-1]
            st.metric("Current Demand", f"{current_demand:.0f} m³/h")
        
        with col2:
            avg_7d = df['demand'].tail(7).mean()
            st.metric("7-Day Avg", f"{avg_7d:.0f} m³/h",
                     delta=f"{((current_demand - avg_7d) / avg_7d * 100):.1f}%")
        
        with col3:
            peak_7d = df['demand'].tail(7).max()
            st.metric("7-Day Peak", f"{peak_7d:.0f} m³/h")
        
        with col4:
            next_day_forecast = forecast_df['forecasted_demand'].iloc[0]
            st.metric("Tomorrow's Forecast", f"{next_day_forecast:.0f} m³/h")
        
        with col5:
            forecast_change = ((next_day_forecast - current_demand) / current_demand * 100)
            st.metric("Forecast Change", f"{forecast_change:+.1f}%")
        
        st.markdown("---")
        
        # Visualizations
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Historical & Forecast", "Patterns", "AI Chat"])
        
        with sub_tab1:
            st.markdown("### Demand Trend & Forecast")
            
            # Historical + Forecast
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['demand'],
                mode='lines',
                name='Historical Demand',
                line=dict(color='#636EFA')
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['forecasted_demand'],
                mode='lines',
                name='Forecasted Demand',
                line=dict(color='#EF553B', dash='dash')
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_df['date'].tolist() + forecast_df['date'].tolist()[::-1],
                y=forecast_df['confidence_upper'].tolist() + forecast_df['confidence_lower'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(239, 85, 59, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence'
            ))
            
            fig.update_layout(
                title="Water Demand: Historical & Forecast",
                xaxis_title="Date",
                yaxis_title="Demand (m³/h)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recent 30 days
            fig = px.line(
                df.tail(30),
                x='date',
                y='demand',
                title="Recent 30 Days Demand",
                labels={'demand': 'Demand (m³/h)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with sub_tab2:
            st.markdown("### Status: Demand Patterns")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Weekly pattern
                weekly_avg = df.groupby('day_of_week')['demand'].mean().reset_index()
                weekly_avg['day_name'] = weekly_avg['day_of_week'].map({
                    0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'
                })
                
                fig = px.bar(
                    weekly_avg,
                    x='day_name',
                    y='demand',
                    title="Average Demand by Day of Week",
                    labels={'demand': 'Avg Demand (m³/h)', 'day_name': 'Day'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Monthly pattern
                monthly_avg = df.groupby('month')['demand'].mean().reset_index()
                monthly_avg['month_name'] = monthly_avg['month'].map({
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                })
                
                fig = px.bar(
                    monthly_avg,
                    x='month_name',
                    y='demand',
                    title="Average Demand by Month",
                    labels={'demand': 'Avg Demand (m³/h)', 'month_name': 'Month'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Temperature correlation
            fig = px.scatter(
                df.tail(90),
                x='temperature',
                y='demand',
                title="Demand vs Temperature Correlation (Last 90 Days)",
                trendline="ols",
                labels={'temperature': 'Temperature (°C)', 'demand': 'Demand (m³/h)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with sub_tab3:
            st.markdown("### AI Assistant - Demand Forecasting")
            
            # Chat interface
            for message in st.session_state.iot_chat_messages:
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI:** {message['content']}")
                st.markdown("---")
            
            # Chat input
            col1, col2 = st.columns([4, 1])
            
            with col1:
                demand_chat_input = st.text_input("Ask about demand...", key="demand_chat_input",
                                                 placeholder="e.g., 'What's the forecast for tomorrow?'")
            
            with col2:
                if st.button("Send", key="demand_send"):
                    if demand_chat_input:
                        st.session_state.iot_chat_messages.append({'role': 'user', 'content': demand_chat_input})
                        response = st.session_state.chatbot.process_message(demand_chat_input)
                        st.session_state.iot_chat_messages.append({'role': 'bot', 'content': response})
                        st.rerun()
            
            if st.button("Clear Chat", key="demand_clear"):
                st.session_state.iot_chat_messages = []
                st.rerun()
    
    else:
        st.info("Please generate demand data to start analysis")

# ========== TAB 3: QUALITY MONITORING ==========
with main_tab3:
    st.subheader("Water Quality Anomaly Detection")
    
    # Data generation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        days_quality = st.slider("Historical Data (days)", min_value=7, max_value=90, value=30, step=7, key='quality_days')
    
    with col2:
        if st.button("Generate Quality Data", use_container_width=True):
            with st.spinner("Generating quality data..."):
                df = DataGenerator.generate_quality_data(n_days=days_quality)
                st.session_state.quality_data = df
                
                # Train model
                detector = AnomalyDetector()
                detector.train_model(df)
                df = detector.detect_anomalies(df)
                st.session_state.quality_data = df
                st.session_state.quality_detector = detector
                
                # Load to chatbot
                st.session_state.chatbot.set_context('quality')
                st.session_state.chatbot.load_data(quality_data=df)
            
            st.success("Success: Quality monitoring data generated!")
    
    if st.session_state.quality_data is not None:
        df = st.session_state.quality_data
        detector = st.session_state.quality_detector
        
        # Get latest reading
        latest = df.iloc[-1]
        
        # Key Metrics
        st.markdown("#### Status: Water Quality Status")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            status = "[ANOMALY]" if latest['is_anomaly'] == 1 else "[NORMAL]"
            st.metric("Status", status)
        
        with col2:
            st.metric("pH", f"{latest['ph']:.2f}",
                     delta=f"{latest['ph'] - 7.5:.2f}")
        
        with col3:
            st.metric("Turbidity", f"{latest['turbidity']:.2f} NTU",
                     delta=f"{latest['turbidity'] - 0.5:.2f}")
        
        with col4:
            st.metric("Conductivity", f"{latest['conductivity']:.0f} µS/cm")
        
        with col5:
            anomaly_count = df['is_anomaly'].tail(168).sum()  # Last 7 days
            st.metric("Anomalies (7d)", int(anomaly_count))
        
        # Alert box
        if latest['is_anomaly'] == 1:
            explanations = detector.get_anomaly_explanation(latest)
            st.error("ANOMALY DETECTED:")
            for exp in explanations:
                st.write(exp)
        else:
            st.success("Success: **All parameters within normal range**")
        
        st.markdown("---")
        
        # Visualizations
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Parameter Trends", "Anomaly Analysis", "AI Chat"])
        
        with sub_tab1:
            st.markdown("### Quality Parameters Over Time")
            
            # All parameters
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('pH', 'Turbidity', 'Conductivity', 'Chlorine')
            )
            
            # Mark anomalies
            anomaly_times = df[df['is_anomaly'] == 1]['timestamp']
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['ph'], name='pH', line=dict(color='#636EFA')),
                row=1, col=1
            )
            fig.add_hline(y=7.5, line_dash="dash", line_color="green", row=1, col=1)
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['turbidity'], name='Turbidity', line=dict(color='#EF553B')),
                row=1, col=2
            )
            fig.add_hline(y=1.0, line_dash="dash", line_color="orange", row=1, col=2)
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['conductivity'], name='Conductivity', line=dict(color='#00CC96')),
                row=2, col=1
            )
            fig.add_hline(y=500, line_dash="dash", line_color="green", row=2, col=1)
            
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['chlorine'], name='Chlorine', line=dict(color='#AB63FA')),
                row=2, col=2
            )
            fig.add_hline(y=0.8, line_dash="dash", line_color="green", row=2, col=2)
            
            fig.update_layout(height=600, title_text="Water Quality Parameters", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Anomaly timeline
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['is_anomaly'],
                mode='markers',
                name='Anomaly',
                marker=dict(size=8, color=df['is_anomaly'], colorscale='Reds')
            ))
            
            fig.update_layout(
                title="Anomaly Timeline",
                xaxis_title="Timestamp",
                yaxis_title="Anomaly (1=Yes, 0=No)",
                yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Normal', 'Anomaly'])
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with sub_tab2:
            st.markdown("### Anomaly Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Anomaly distribution
                anomaly_counts = df['is_anomaly'].value_counts()
                fig = px.pie(
                    values=anomaly_counts.values,
                    names=['Normal', 'Anomaly'],
                    title="Anomaly Distribution",
                    color_discrete_sequence=['#00CC96', '#EF553B']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Anomaly score distribution
                fig = px.histogram(
                    df,
                    x='anomaly_score',
                    color='is_anomaly',
                    title="Anomaly Score Distribution",
                    nbins=30,
                    labels={'is_anomaly': 'Type'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Parameter comparison
            st.markdown("#### Parameter Statistics: Normal vs Anomaly")
            
            normal_stats = df[df['is_anomaly'] == 0][['ph', 'turbidity', 'conductivity', 'chlorine']].describe()
            anomaly_stats = df[df['is_anomaly'] == 1][['ph', 'turbidity', 'conductivity', 'chlorine']].describe()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Normal Conditions**")
                st.dataframe(normal_stats, use_container_width=True)
            
            with col2:
                st.markdown("**Anomaly Conditions**")
                st.dataframe(anomaly_stats, use_container_width=True)
        
        with sub_tab3:
            st.markdown("### AI Assistant - Quality Monitoring")
            
            # Chat interface
            for message in st.session_state.iot_chat_messages:
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI:** {message['content']}")
                st.markdown("---")
            
            # Chat input
            col1, col2 = st.columns([4, 1])
            
            with col1:
                quality_chat_input = st.text_input("Ask about water quality...", key="quality_chat_input",
                                                  placeholder="e.g., 'What's the current pH?'")
            
            with col2:
                if st.button("Send", key="quality_send"):
                    if quality_chat_input:
                        st.session_state.iot_chat_messages.append({'role': 'user', 'content': quality_chat_input})
                        response = st.session_state.chatbot.process_message(quality_chat_input)
                        st.session_state.iot_chat_messages.append({'role': 'bot', 'content': response})
                        st.rerun()
            
            if st.button("Clear Chat", key="quality_clear"):
                st.session_state.iot_chat_messages = []
                st.rerun()
    
    else:
        st.info("Please generate quality data to start analysis")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Note: This is a demonstration using synthetic data for portfolio purposes</p>
</div>
""", unsafe_allow_html=True)
