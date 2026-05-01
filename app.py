# app.py
"""
Advanced Statistical Frequency Distribution Dashboard
Theme: Ultra-Dark "Midnight" Mode with Glassmorphism Effects
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import re

# ------------------- PAGE CONFIGURATION -------------------
st.set_page_config(
    page_title="Quantum Statistics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- CUSTOM CSS -------------------
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0A0E17, #03060C);
        font-family: 'Inter', sans-serif;
    }
    
    .glass-card {
        background: rgba(18, 25, 45, 0.55);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(0, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(8, 12, 20, 0.85);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    h1, h2, h3 {
        background: linear-gradient(135deg, #00FFFF, #B026FF);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
        font-weight: 700;
    }
    
    .stTextArea textarea {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        color: #E0E0E0 !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #00B4D8, #0077B6);
        border-radius: 40px;
        color: white;
        width: 100%;
    }
    
    [data-testid="stMetricValue"] { color: #00FFFF !important; }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ------------------- STATISTICAL ENGINE -------------------
def parse_numbers(input_text):
    if not input_text.strip(): return []
    cleaned = re.sub(r'[,\n]+', ' ', input_text)
    numbers = []
    for token in cleaned.split():
        try: numbers.append(float(token.strip()))
        except ValueError: continue
    return numbers

def sturges_rule(n):
    return int(np.ceil(np.log2(n) + 1)) if n > 1 else 1

def generate_frequency_table(data, num_bins):
    counts, bin_edges = np.histogram(data, bins=num_bins)
    df = pd.DataFrame({
        'Class Interval': [f"[{bin_edges[i]:.2f}, {bin_edges[i+1]:.2f})" for i in range(len(counts))],
        'Midpoint (x)': [(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(counts))],
        'Frequency (f)': counts,
        'Cumulative Frequency': np.cumsum(counts),
        'Relative Frequency': counts / len(data)
    })
    return df

def compute_statistics(data):
    n = len(data)
    data_range = np.max(data) - np.min(data) if n > 1 else 0
    bins = sturges_rule(n)
    return {
        'count': n, 'range': data_range, 'optimal_bins': bins,
        'optimal_width': data_range / bins if bins > 0 else 0,
        'mean': np.mean(data), 'std': np.std(data, ddof=1) if n > 1 else 0
    }

# ------------------- VISUALIZATIONS -------------------
def create_histogram(data, stats):
    fig = go.Figure(go.Histogram(x=data, nbinsx=stats['optimal_bins'], marker=dict(color='rgba(0, 255, 255, 0.7)', line=dict(color='#B026FF', width=1.5))))
    fig.update_layout(title="📊 Histogram", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'))
    return fig

def create_frequency_polygon(data, stats):
    counts, bin_edges = np.histogram(data, bins=stats['optimal_bins'])
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    fig = go.Figure(go.Scatter(x=bin_centers, y=counts, mode='lines+markers', line=dict(color='#B026FF', width=3), fill='tozeroy'))
    fig.update_layout(title="📈 Frequency Polygon", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'))
    return fig

def create_ogive(data, stats):
    counts, bin_edges = np.histogram(data, bins=stats['optimal_bins'])
    fig = go.Figure(go.Scatter(x=bin_edges, y=np.insert(np.cumsum(counts), 0, 0), mode='lines+markers', line=dict(color='#00FFFF', width=3)))
    fig.update_layout(title="📉 Ogive Graph", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'))
    return fig

def create_dot_plot(data):
    sorted_data = np.sort(data)
    y_vals = [np.sum(sorted_data[:i] == val) for i, val in enumerate(sorted_data)]
    fig = go.Figure(go.Scatter(x=sorted_data, y=y_vals, mode='markers', marker=dict(size=12, color='#00FFFF')))
    fig.update_layout(title="🔘 Dot Plot", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'), yaxis=dict(showticklabels=False))
    return fig

def create_box_plot(data):
    fig = go.Figure(go.Box(y=data, marker_color='#B026FF', line_color='#00FFFF', fillcolor='rgba(0, 255, 255, 0.2)'))
    fig.update_layout(title="📦 Box Plot", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E0E0E0'))
    return fig

# ------------------- MAIN -------------------
def main():
    st.markdown("<h1 style='text-align: center;'>✦ QUANTUM STATISTICS ✦</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## 🔮 DATA INPUT")
        raw_input = st.text_area("Enter numbers separated by space or comma", height=250)
        analyze = st.button("ANALYZE")

    if analyze and raw_input:
        nums = parse_numbers(raw_input)
        if nums:
            data = np.array(nums)
            stats = compute_statistics(data)
            table = generate_frequency_table(data, stats['optimal_bins'])
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("N", len(data))
            c2.metric("Range", f"{stats['range']:.2f}")
            c3.metric("Bins", stats['optimal_bins'])
            c4.metric("Mean", f"{stats['mean']:.2f}")

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📋 Frequency Table")
            st.dataframe(table.style.format({'Relative Frequency': '{:.2%}'}), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            t1, t2, t3, t4, t5 = st.tabs(["Histogram", "Polygon", "Ogive", "Dot Plot", "Box Plot"])
            with t1: st.plotly_chart(create_histogram(data, stats), use_container_width=True)
            with t2: st.plotly_chart(create_frequency_polygon(data, stats), use_container_width=True)
            with t3: st.plotly_chart(create_ogive(data, stats), use_container_width=True)
            with t4: st.plotly_chart(create_dot_plot(data), use_container_width=True)
            with t5: st.plotly_chart(create_box_plot(data), use_container_width=True)
        else:
            st.error("Invalid input.")
    else:
        st.info("Enter data in the sidebar and click Analyze.")

if __name__ == "__main__":
    main()
