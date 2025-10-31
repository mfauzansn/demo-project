import streamlit as st
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Data Analytics Portfolio",
    page_icon="📊",  # Keep simple chart icon for browser tab only
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #64748B;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .case-card {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .case-card-2 {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 2rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #1E3A8A;
    }
    .tech-badge {
        display: inline-block;
        background: #F1F5F9;
        color: #1E293B;
        padding: 0.4rem 0.9rem;
        border-radius: 4px;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Data Analytics Portfolio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Machine Learning & AI Solutions Showcase</div>', unsafe_allow_html=True)

st.markdown("---")

# Introduction
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### Welcome
    
    This portfolio demonstrates **end-to-end data analytics solutions** across different industries,
    showcasing expertise in:
    - **Fraud Detection & Risk Analytics**
    - **Industrial IoT & Predictive Analytics**
    - **Machine Learning & AI Implementation**
    - **Real-time Dashboard & Visualization**
    """)

st.markdown("---")

# Case Studies Overview
st.markdown("### Case Studies")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="case-card">
        <h2>Case Study 1</h2>
        <h3>Agent Network Fraud Detection</h3>
        <p><strong>Industry:</strong> Multi-Level Marketing / Network Business</p>
        <p><strong>Challenge:</strong> Detect fraudulent agents and prevent system abuse</p>
        <p><strong>Solution:</strong> ML-powered fraud detection with real-time scoring</p>
        <br>
        <p><strong>Impact:</strong></p>
        <ul>
            <li>87.5% Detection Accuracy</li>
            <li>70% Reduction in Fraud</li>
            <li>Real-time Risk Assessment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Explore Case Study 1", use_container_width=True, key="case1"):
        st.switch_page("pages/2_Case_Study_1.py")

with col2:
    st.markdown("""
    <div class="case-card-2">
        <h2>Case Study 2</h2>
        <h3>Industrial IoT Analytics</h3>
        <p><strong>Industry:</strong> Water Treatment & Distribution</p>
        <p><strong>Challenge:</strong> Optimize operations and prevent equipment failures</p>
        <p><strong>Solution:</strong> Predictive maintenance & demand forecasting</p>
        <br>
        <p><strong>Impact:</strong></p>
        <ul>
            <li>95% Prediction Accuracy</li>
            <li>30-40% Reduced Downtime</li>
            <li>15-20% Energy Savings</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Explore Case Study 2", use_container_width=True, key="case2"):
        st.switch_page("pages/3_Case_Study_2.py")

st.markdown("---")

# Technical Capabilities
st.markdown("### Technical Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Data Engineering")
    st.markdown("""
    <span class="tech-badge">Python</span>
    <span class="tech-badge">Pandas</span>
    <span class="tech-badge">SQL</span>
    <span class="tech-badge">ETL Pipelines</span>
    <span class="tech-badge">Data Warehouse</span>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("#### Machine Learning")
    st.markdown("""
    <span class="tech-badge">Scikit-learn</span>
    <span class="tech-badge">XGBoost</span>
    <span class="tech-badge">Prophet</span>
    <span class="tech-badge">Random Forest</span>
    <span class="tech-badge">Isolation Forest</span>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("#### Visualization & Deployment")
    st.markdown("""
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Plotly</span>
    <span class="tech-badge">Docker</span>
    <span class="tech-badge">API Development</span>
    <span class="tech-badge">Cloud Deploy</span>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key Metrics
st.markdown("### Portfolio Highlights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h2 style="color: #1E3A8A; margin: 0;">2</h2>
        <p style="margin: 0; color: #64748B;">Industries Covered</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h2 style="color: #1E3A8A; margin: 0;">5+</h2>
        <p style="margin: 0; color: #64748B;">ML Models</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h2 style="color: #1E3A8A; margin: 0;">90%+</h2>
        <p style="margin: 0; color: #64748B;">Accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h2 style="color: #1E3A8A; margin: 0;">Real-time</h2>
        <p style="margin: 0; color: #64748B;">Analytics</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 2rem;">
    <p><strong>Interactive Demo</strong> - Click on case studies above to explore full functionality</p>
    <p>Built with Streamlit | Powered by Python & Machine Learning</p>
</div>
""", unsafe_allow_html=True)
