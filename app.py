# app.py
"""
Advanced Statistical Frequency Distribution Dashboard
Author: Expert Full-Stack Python Developer & Data Scientist
Theme: Ultra-Dark "Midnight" Mode with Glassmorphism Effects
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import re
from typing import List, Tuple, Dict, Optional

# ------------------- PAGE CONFIGURATION -------------------
st.set_page_config(
    page_title="Quantum Statistics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- CUSTOM CSS (Glassmorphism + Midnight Theme) -------------------
def inject_custom_css():
    st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono&display=swap');
    
    /* Global background and font */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0A0E17, #03060C);
        font-family: 'Inter', sans-serif;
    }
    
    /* Glassmorphism effect for cards and containers */
    .glass-card {
        background: rgba(18, 25, 45, 0.55);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(0, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(8, 12, 20, 0.85);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding: 1rem;
    }
    
    /* Headers with neon accents */
    h1, h2, h3 {
        background: linear-gradient(135deg, #00FFFF, #B026FF);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.5rem;
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
        display: inline-block;
        padding-bottom: 0.25rem;
    }
    
    /* Input fields */
    .stTextArea textarea, .stNumberInput input {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 16px !important;
        color: #E0E0E0 !important;
        font-family: 'Roboto Mono', monospace !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #00B4D8, #0077B6);
        border: none;
        border-radius: 40px;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 180, 216, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 180, 216, 0.5);
        background: linear-gradient(135deg, #00E5FF, #0096C7);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #00FFFF !important;
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #B0B8D0 !important;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 16px;
        background: rgba(255, 75, 75, 0.15);
        backdrop-filter: blur(8px);
        border-left: 4px solid #FF4B4B;
    }
    
    /* Dataframes */
    .dataframe {
        background: rgba(10, 15, 25, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(0, 255, 255, 0.15);
        font-family: 'Roboto Mono', monospace;
    }
    
    .dataframe th {
        background: rgba(0, 255, 255, 0.1);
        color: #00FFFF;
    }
    
    /* Hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ------------------- STATISTICAL ENGINE -------------------
def parse_numbers(input_text: str) -> List[float]:
    """Parse comma, space, or newline separated numbers."""
    if not input_text.strip():
        return []
    # Replace commas and newlines with spaces
    cleaned = re.sub(r'[,\n]+', ' ', input_text)
    # Split by whitespace and convert to float
    numbers = []
    for token in cleaned.split():
        try:
            numbers.append(float(token.strip()))
        except ValueError:
            continue
    return numbers

def sturges_rule(n: int) -> int:
    """Calculate optimal number of bins using Sturges' Rule."""
    if n <= 1:
        return 1
    return int(np.ceil(np.log2(n) + 1))

def generate_frequency_table(data: np.ndarray, num_bins: int) -> pd.DataFrame:
    """Generate comprehensive frequency distribution table."""
    if len(data) == 0:
        return pd.DataFrame()
    
    counts, bin_edges = np.histogram(data, bins=num_bins)
    bin_width = bin_edges[1] - bin_edges[0]
    
    class_intervals = []
    midpoints = []
    frequencies = []
    cumulative_freq = []
    relative_freq = []
    
    cumulative = 0
    for i in range(len(counts)):
        lower = bin_edges[i]
        upper = bin_edges[i + 1]
        class_intervals.append(f"[{lower:.2f}, {upper:.2f})")
        midpoints.append((lower + upper) / 2)
        frequencies.append(counts[i])
        cumulative += counts[i]
        cumulative_freq.append(cumulative)
        relative_freq.append(counts[i] / len(data) if len(data) > 0 else 0)
    
    df = pd.DataFrame({
        'Class Interval': class_intervals,
        'Midpoint (x)': midpoints,
        'Frequency (f)': frequencies,
        'Cumulative Frequency': cumulative_freq,
        'Relative Frequency': relative_freq
    })
    return df

def compute_statistics(data: np.ndarray) -> Dict:
    """Compute key statistics with optimal bin width."""
    n = len(data)
    data_range = np.max(data) - np.min(data) if n > 1 else 0
    optimal_bins = sturges_rule(n)
    optimal_width = data_range / optimal_bins if optimal_bins > 0 else 1.0
    
    return {
        'count': n,
        'min': np.min(data) if n > 0 else 0,
        'max': np.max(data) if n > 0 else 0,
        'range': data_range,
        'mean': np.mean(data) if n > 0 else 0,
        'median': np.median(data) if n > 0 else 0,
        'std': np.std(data, ddof=1) if n > 1 else 0,
        'optimal_bins': optimal_bins,
        'optimal_width': optimal_width,
        'q1': np.percentile(data, 25) if n > 0 else 0,
        'q3': np.percentile(data, 75) if n > 0 else 0,
    }

# ------------------- PLOTLY VISUALIZATIONS (Animated) -------------------
def create_histogram(data: np.ndarray, stats: Dict) -> go.Figure:
    """Animated histogram with optimal bins."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=stats['optimal_bins'],
        marker=dict(
            color='rgba(0, 255, 255, 0.7)',
            line=dict(color='#B026FF', width=1.5),
            opacity=0.85
        ),
        name='Frequency',
        hovertemplate='Bin Range: %{x}<br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='📊 Histogram with Optimal Bins', font=dict(size=24, color='#00FFFF')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#E0E0E0'),
        xaxis=dict(title='Value', gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Frequency', gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        hoverlabel=dict(bgcolor='#0A0E17', font_size=12, font_family='Inter'),
        transition=dict(duration=500, easing='cubic-in-out')
    )
    
    # Animation on load
    fig.update_traces(marker=dict(line=dict(width=1.5)), selector=dict(type='histogram'))
    fig.layout.updatemenus = []
    return fig

def create_frequency_polygon(data: np.ndarray, stats: Dict) -> go.Figure:
    """Animated frequency polygon overlay."""
    counts, bin_edges = np.histogram(data, bins=stats['optimal_bins'])
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=bin_centers,
        y=counts,
        mode='lines+markers',
        line=dict(color='#B026FF', width=3, shape='spline'),
        marker=dict(size=8, color='#00FFFF', symbol='circle', line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor='rgba(176, 38, 255, 0.15)',
        name='Frequency Polygon',
        hovertemplate='Midpoint: %{x:.2f}<br>Frequency: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='📈 Frequency Polygon', font=dict(size=24, color='#B026FF')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#E0E0E0'),
        xaxis=dict(title='Class Midpoint', gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Frequency', gridcolor='rgba(255,255,255,0.05)'),
        hoverlabel=dict(bgcolor='#0A0E17'),
        transition=dict(duration=600)
    )
    
    return fig

def create_ogive(data: np.ndarray, stats: Dict) -> go.Figure:
    """Cumulative frequency ogive with smooth curve."""
    counts, bin_edges = np.histogram(data, bins=stats['optimal_bins'])
    cumulative = np.cumsum(counts)
    # Add starting point at lower bound
    x_vals = np.insert(bin_edges, 0, bin_edges[0])
    y_vals = np.insert(cumulative, 0, 0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines+markers',
        line=dict(color='#00FFFF', width=3, shape='spline', smoothing=1.2),
        marker=dict(size=6, color='#B026FF', symbol='diamond'),
        name='Cumulative Frequency',
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.08)',
        hovertemplate='Upper Bound: %{x:.2f}<br>Cumulative: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='📉 Ogive (Cumulative Frequency)', font=dict(size=24, color='#00FFFF')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#E0E0E0'),
        xaxis=dict(title='Class Upper Bound', gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Cumulative Frequency', gridcolor='rgba(255,255,255,0.05)'),
        transition=dict(duration=500)
    )
    
    return fig

def create_dot_plot(data: np.ndarray) -> go.Figure:
    """Modern stacked dot plot using scatter with jitter."""
    # Create jittered positions for dot plot effect
    sorted_data = np.sort(data)
    y_jitter = []
    for i, val in enumerate(sorted_data):
        # Count occurrences for stacking
        count = np.sum(sorted_data == val)
        if count > 1:
            # Stack vertically
            idx = np.where(sorted_data == val)[0]
            pos = np.where(idx == i)[0][0] if i in idx else 0
            y_jitter.append(pos * 0.2)
        else:
            y_jitter.append(0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sorted_data,
        y=y_jitter,
        mode='markers',
        marker=dict(
            size=12,
            color='#00FFFF',
            symbol='circle',
            line=dict(width=1, color='#B026FF'),
            opacity=0.8
        ),
        text=[f'Value: {v:.2f}' for v in sorted_data],
        hovertemplate='<b>Dot Plot</b><br>Value: %{x:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='🔘 Modern Dot Plot (Stacked)', font=dict(size=24, color='#B026FF')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#E0E0E0'),
        xaxis=dict(title='Data Values', gridcolor='rgba(255,255,255,0.05)', showline=True),
        yaxis=dict(title='', showticklabels=False, showgrid=False, zeroline=False),
        showlegend=False,
        transition=dict(duration=400)
    )
    
    return fig

def create_box_plot(data: np.ndarray) -> go.Figure:
    """Vertical box plot with quartiles and outliers."""
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=data,
        name='Distribution',
        boxmean='sd',
        marker=dict(
            color='#B026FF',
            outliercolor='#FF4B4B',
            line=dict(width=2, color='#00FFFF')
        ),
        line=dict(color='#00FFFF', width=2),
        fillcolor='rgba(0, 255, 255, 0.2)', # Corrected the quote here
        hovertemplate='<b>Box Plot</b><br>Q1: %{q1:.2f}<br>Median: %{median:.2f}<br>Q3: %{q3:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='📦 Box Plot (with Quartiles)', font=dict(size=24, color='#00FFFF')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#E0E0E0'),
        yaxis=dict(title='Value', gridcolor='rgba(255,255,255,0.05)'),
        xaxis=dict(showticklabels=False),
        transition=dict(duration=500)
    )
    
    return fig

def create_dashboard_grid(data: np.ndarray, stats: Dict, freq_table: pd.DataFrame):
    """Orchestrate all visualizations in a professional grid."""
    if len(data) == 0:
        st.warning("⚠️ No valid data to visualize. Please enter numbers.")
        return
    
    # First row: Key Metrics with glassmorphism
    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("📊 N", stats['count']),
        ("🎯 Range", f"{stats['range']:.2f}"),
        ("📐 Optimal Bins", stats['optimal_bins']),
        ("📏 Class Width", f"{stats['optimal_width']:.3f}"),
        ("⚖️ Mean ± Std", f"{stats['mean']:.2f} ± {stats['std']:.2f}")
    ]
    for col, (label, value) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.metric(label=label, value=value)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row: Frequency Table in a glass card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📋 Frequency Distribution Table")
    if not freq_table.empty:
        # Format for display
        display_table = freq_table.copy()
        display_table['Relative Frequency'] = display_table['Relative Frequency'].apply(lambda x: f"{x:.2%}")
        st.dataframe(display_table, use_container_width=True, height=350)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Third row: Visualization Tabs
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Histogram", "📈 Frequency Polygon", "📉 Ogive", "🔘 Dot Plot", "📦 Box Plot"
    ])
    
    with tab1:
        st.plotly_chart(create_histogram(data, stats), use_container_width=True, config={'displayModeBar': False})
    with tab2:
        st.plotly_chart(create_frequency_polygon(data, stats), use_container_width=True, config={'displayModeBar': False})
    with tab3:
        st.plotly_chart(create_ogive(data, stats), use_container_width=True, config={'displayModeBar': False})
    with tab4:
        st.plotly_chart(create_dot_plot(data), use_container_width=True, config={'displayModeBar': False})
    with tab5:
        st.plotly_chart(create_box_plot(data), use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- MAIN APP -------------------
def main():
    # Animated title
    st.markdown("""
    <h1 style='text-align: center; font-size: 3rem;'>
        ✦ QUANTUM STATISTICS DASHBOARD ✦
    </h1>
    <p style='text-align: center; color: #A0A8C0; margin-bottom: 2rem;'>
        Advanced Frequency Distribution | Interactive Visualizations | Midnight Glassmorphism UI
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar for data input
    with st.sidebar:
        st.markdown("## 🔮 DATA INPUT")
        st.markdown("Paste your numeric list below (comma, space, or newline separated):")
        raw_input = st.text_area(
            "Numbers",
            placeholder="Example: 12, 15, 18, 22, 25, 25, 30, 32, 35, 40",
            height=200,
            label_visibility="collapsed"
        )
        
        process_btn = st.button("✨ ANALYZE DISTRIBUTION", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📌 Instructions")
        st.caption("• Accepts integers & decimals\n• Automatically detects separators\n• Sturges' Rule for optimal bins\n• Interactive animated graphs")
        
        st.markdown("---")
        st.markdown("<p style='font-size: 0.7rem; text-align: center;'>⚡ Powered by Streamlit & Plotly</p>", unsafe_allow_html=True)
    
    # Main content area
    if process_btn:
        numbers = parse_numbers(raw_input)
        
        if len(numbers) == 0:
            st.error("❌ No valid numeric data detected. Please enter at least one number.")
            return
        
        data = np.array(numbers)
        stats = compute_statistics(data)
        freq_table = generate_frequency_table(data, stats['optimal_bins'])
        
        # Display success message
        st.success(f"✅ Successfully parsed {len(numbers)} data points. Optimal bins: {stats['optimal_bins']} | Class width: {stats['optimal_width']:.4f}")
        
        # Render the full dashboard
        create_dashboard_grid(data, stats, freq_table)
        
    else:
        # Show placeholder / welcome visualization
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.info("👋 **Welcome to the Quantum Statistics Dashboard**\n\nEnter your numeric data in the sidebar and click **ANALYZE DISTRIBUTION** to generate:\n\n- 📊 Interactive Histogram\n- 📈 Frequency Polygon\n- 📉 Ogive (Cumulative Frequency)\n- 🔘 Modern Dot Plot\n- 📦 Box Plot with Outliers\n- 📋 Complete Frequency Table with Class Intervals, Midpoints, and Relative Frequencies")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample demonstration
        with st.expander("🔍 View Sample Analysis (Click to preview)"):
            sample_data = np.array([15, 18, 22, 25, 25, 27, 30, 32, 32, 35, 38, 40, 42, 45, 45, 48, 50])
            sample_stats = compute_statistics(sample_data)
            sample_table = generate_frequency_table(sample_data, sample_stats['optimal_bins'])
            st.markdown("**Sample Data:** " + ", ".join(map(str, sample_data)))
            st.markdown(f"**Statistics:** N={sample_stats['count']}, Range={sample_stats['range']:.2f}, Bins={sample_stats['optimal_bins']}, Width={sample_stats['optimal_width']:.3f}")
            st.dataframe(sample_table, use_container_width=True)

if __name__ == "__main__":
    main()
