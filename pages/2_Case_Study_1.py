import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
sys.path.append('..')
from utils.data_generator import DataGenerator
from utils.fraud_detection import FraudDetector
from utils.chatbot import DemoChatbot

# Page config
st.set_page_config(
    page_title="Case Study 1: Fraud Detection",
    page_icon="🕵️",
    layout="wide"
)

# Initialize session state
if 'fraud_data' not in st.session_state:
    st.session_state.fraud_data = None
if 'detector' not in st.session_state:
    st.session_state.detector = None
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = DemoChatbot()
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Header
st.title("Case Study 1: Agent Network Fraud Detection")

st.markdown("---")

# Overview Section
with st.expander("Case Study Overview", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Business Challenge
        
        A **multi-level marketing network** business faced significant challenges with:
        - **Fraudulent agent registrations** using fake identities
        - **Device farming** - one device creating multiple accounts
        - **Rapid mass registrations** from same locations
        - **Duplicate identity abuse** to claim multiple bonuses
        
        **Annual Impact:**
        - Loss: ~Rp 2.5 billion from fraud
        - 15-20% of new agents suspected fraudulent
        - Manual verification taking 10+ hours daily
        """)
    
    with col2:
        st.markdown("""
        ### Solution Delivered
        
        **ML-Powered Fraud Detection System** with:
        - Real-time fraud scoring (0-100 scale)
        - Multi-model ensemble (Rule-based + Random Forest + Isolation Forest)
        - Automatic risk categorization (Low/Medium/High/Critical)
        - Explainable AI - clear fraud indicators
        
        **Business Impact:**
        - 87.5% detection accuracy
        - 70% reduction in fraud
        - 60% cost savings
        - 10x faster verification
        """)

st.markdown("---")

# Data Generation Section
st.subheader("Generate Demo Data")

col1, col2, col3 = st.columns(3)

with col1:
    n_agents = st.slider("Number of Agents", min_value=50, max_value=500, value=100, step=50)

with col2:
    fraud_ratio = st.slider("Fraud Ratio", min_value=0.05, max_value=0.30, value=0.15, step=0.05)

with col3:
    if st.button("Generate Data", use_container_width=True):
        with st.spinner("Generating synthetic data..."):
            # Generate data
            df = DataGenerator.generate_agent_data(n_agents=n_agents, fraud_ratio=fraud_ratio)
            
            # Initialize fraud detector
            detector = FraudDetector()
            
            # Calculate scores
            df = detector.calculate_rule_based_score(df)
            df = detector.assign_risk_level(df)
            
            # Train ML models
            detector.train_ml_models(df)
            df = detector.predict_ml_score(df)
            
            # Get ensemble score
            df = detector.get_ensemble_score(df)
            
            st.session_state.fraud_data = df
            st.session_state.detector = detector

            
            
            # Load to chatbot
            st.session_state.chatbot.set_context('fraud')
            st.session_state.chatbot.load_data(fraud_data=df)
        
        st.success(f"Generated {n_agents} agents with {int(n_agents * fraud_ratio)} potential fraudsters!")

if st.session_state.fraud_data is not None:
    df = st.session_state.fraud_data.copy()

    # ===== FIX DUPLICATE COLUMNS =====
    # Identify duplicated column names
    dup_cols = df.columns[df.columns.duplicated()].tolist()
    if dup_cols:
        st.warning(f"Duplicate columns removed: {dup_cols}")
        df = df.loc[:, ~df.columns.duplicated()]


    st.markdown("---")
    
    # Key Metrics
    st.subheader("Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_agents = len(df)
        st.metric("Total Agents", total_agents, delta=f"+{(fraud_ratio*100):.1f}%")
    
    with col2:
        critical_risk = len(df[df['risk_level'] == 'Critical'])
        st.metric("Critical Risk", critical_risk, delta=f"+{(critical_risk/total_agents*100):.1f}%")
    
    with col3:
        high_risk = len(df[df['risk_level'] == 'High'])
        st.metric("High Risk", high_risk, delta=f"+{(high_risk/total_agents*100):.0f}%")
    
    st.markdown("---")
    

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Distribution", "Agent Details", "Analysis", "AI Chat"])
    
    with tab1:
        st.subheader("Risk Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk Level Distribution
            risk_dist = df['risk_level'].value_counts().reset_index()
            risk_dist.columns = ['Risk Level', 'Count']
            
            # Define color mapping
            color_map = {
                'Low': '#10B981',      # Green
                'Medium': '#F59E0B',   # Yellow
                'High': '#EF4444',     # Red
                'Critical': '#7C3AED'  # Purple
            }
            
            fig1 = px.bar(
                risk_dist, 
                x='Risk Level', 
                y='Count',
                title='Agent Risk Distribution',
                color='Risk Level',
                color_discrete_map=color_map
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Fraud Score Distribution
            fig2 = px.histogram(
                df, 
                x='final_score',
                nbins=30,
                title='Fraud Score Distribution',
                labels={'final_score': 'Fraud Score'},
                color_discrete_sequence=['#6366F1']
            )
            fig2.add_vline(x=50, line_dash="dash", line_color="red", 
                          annotation_text="Risk Threshold")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Correlation Analysis
        st.subheader("Fraud Indicators Correlation")
        
        numeric_cols = ['rule_based_score', 'ml_score', 'final_score',
                'duplicate_devices', 'duplicate_ips', 'same_location_count']

        # Only keep columns that exist in df
        numeric_cols = [col for col in numeric_cols if col in df.columns]

        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig3 = px.imshow(
                corr_matrix,
                title='Feature Correlation Heatmap',
                color_continuous_scale='RdBu_r',
                aspect='auto'
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Not enough numeric columns available to generate correlation matrix.")

        corr_matrix = df[numeric_cols].corr()
        
        fig3 = px.imshow(
            corr_matrix,
            title='Feature Correlation Heatmap',
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.subheader("Agent Details")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                options=['Low', 'Medium', 'High', 'Critical'],
                default=['High', 'Critical']
            )
        
        with col2:
            min_score = st.slider("Minimum Fraud Score", 0, 100, 50)
        
        with col3:
            search_agent = st.text_input("Search Agent ID")
        
        # Apply filters
        filtered_df = df.copy()
        
        if risk_filter:
            filtered_df = filtered_df[filtered_df['risk_level'].isin(risk_filter)]
        
        filtered_df = filtered_df[filtered_df['final_score'] >= min_score]
        
        if search_agent:
            filtered_df = filtered_df[filtered_df['agent_id'].str.contains(search_agent, case=False)]
        
        # Display filtered data
        st.dataframe(
            filtered_df[[
                'agent_id', 'final_score', 'risk_level', 
                'duplicate_devices', 'duplicate_ips', 
                'same_location_count', 'registration_date'
            ]].sort_values('final_score', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Download option
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Filtered Data",
            csv,
            "fraud_detection_results.csv",
            "text/csv",
            key='download-csv'
        )
    
    with tab3:
        st.subheader("Advanced Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Device Farming Detection
            st.markdown("#### Device Farming Analysis")
            device_fraud = df.groupby('device_id').agg({
                'agent_id': 'count',
                'final_score': 'mean'
            }).reset_index()
            device_fraud.columns = ['Device ID', 'Agent Count', 'Avg Fraud Score']
            device_fraud = device_fraud[device_fraud['Agent Count'] > 1].sort_values('Agent Count', ascending=False)
            
            fig4 = px.scatter(
                device_fraud.head(20),
                x='Agent Count',
                y='Avg Fraud Score',
                size='Agent Count',
                hover_data=['Device ID'],
                title='Top 20 Devices by Agent Count',
                color='Avg Fraud Score',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig4, use_container_width=True)
            
            st.dataframe(device_fraud.head(10), use_container_width=True)
        
        with col2:
            # Location-based Fraud
            st.markdown("#### Location-based Fraud")
            location_fraud = df.groupby('location').agg({
                'agent_id': 'count',
                'final_score': 'mean'
            }).reset_index()
            location_fraud.columns = ['Location', 'Agent Count', 'Avg Fraud Score']
            location_fraud = location_fraud.sort_values('Avg Fraud Score', ascending=False)
            
            fig5 = px.bar(
                location_fraud.head(15),
                x='Location',
                y='Avg Fraud Score',
                title='Top 15 High-Risk Locations',
                color='Avg Fraud Score',
                color_continuous_scale='Reds'
            )
            fig5.update_xaxes(tickangle=45)
            st.plotly_chart(fig5, use_container_width=True)
            
            st.dataframe(location_fraud.head(10), use_container_width=True)
        
        # Model Performance
        st.markdown("#### Model Performance Comparison")
        
        # Calculate metrics for each model
        actual_fraud = (df['final_score'] >= 70).astype(int)
        
        rule_based_pred = (df['rule_based_score'] >= 70).astype(int)
        ml_pred = (df['ml_score'] >= 70).astype(int)
        ensemble_pred = (df['final_score'] >= 70).astype(int)
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        models = ['Rule-Based', 'ML Model', 'Ensemble']
        predictions = [rule_based_pred, ml_pred, ensemble_pred]
        
        metrics_data = []
        for model, pred in zip(models, predictions):
            metrics_data.append({
                'Model': model,
                'Accuracy': accuracy_score(actual_fraud, pred),
                'Precision': precision_score(actual_fraud, pred, zero_division=0),
                'Recall': recall_score(actual_fraud, pred, zero_division=0),
                'F1-Score': f1_score(actual_fraud, pred, zero_division=0)
            })
        
        metrics_df = pd.DataFrame(metrics_data)
        
        fig6 = go.Figure()
        
        for metric in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
            fig6.add_trace(go.Bar(
                name=metric,
                x=metrics_df['Model'],
                y=metrics_df[metric],
                text=metrics_df[metric].round(3),
                textposition='auto',
            ))
        
        fig6.update_layout(
            title='Model Performance Comparison',
            xaxis_title='Model',
            yaxis_title='Score',
            barmode='group',
            yaxis_range=[0, 1]
        )
        
        st.plotly_chart(fig6, use_container_width=True)
    
    with tab4:
        st.subheader("AI Assistant")
        
        st.markdown("""
        Ask questions about the fraud detection results. Examples:
        - "How many critical risk agents?"
        - "Show me agents with duplicate devices"
        - "What's the average fraud score?"
        - "Which location has most fraud?"
        """)
        
        # Chat interface
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about fraud detection..."):
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            response = st.session_state.chatbot.get_response(prompt)
            
            # Add assistant message
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_messages = []
            st.rerun()

else:
    st.info("👆 Please generate demo data first using the controls above.")

st.markdown("---")
st.caption("Note: This is a demonstration using synthetic data for portfolio purposes.")