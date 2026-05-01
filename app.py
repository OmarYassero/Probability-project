# app.py - FULLY CORRECTED FOR STREAMLIT
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64
import re

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AEGIS STAT ANALYZER | Air-Defense Control",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - AIR DEFENSE SYSTEM AESTHETIC
# ============================================================================
def inject_custom_css():
    """Inject futuristic air-defense control system CSS"""
    
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #050505 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .glass-panel {
        background: rgba(10, 10, 10, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 159, 0.2);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 20px rgba(0, 255, 159, 0.1);
    }
    
    .system-header {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #00ff9f;
        text-shadow: 0 0 10px rgba(0, 255, 159, 0.5);
        border-left: 4px solid #00ff9f;
        padding-left: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00ff9f 0%, #00b8ff 100%);
        color: #0a0a0a;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 255, 159, 0.6);
    }
    
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #00ff9f;
        color: #00ff9f;
        font-family: 'Share Tech Mono', monospace;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        color: #00ff9f;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Share Tech Mono', monospace;
        color: #00eaff;
    }
    
    .dataframe {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid #00ff9f;
    }
    
    .dataframe th {
        background: rgba(0, 255, 159, 0.15);
        color: #00ff9f;
        font-family: 'Orbitron', monospace;
    }
    
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff9f;
        border-radius: 50%;
        box-shadow: 0 0 8px #00ff9f;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    hr {
        border-color: rgba(0, 255, 159, 0.2);
        margin: 1.5rem 0;
    }
    </style>
    
    <div style="position: fixed; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #00ff9f, #00eaff, #00ff9f); z-index: 9999;"></div>
    """
    
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ============================================================================
# STATISTICAL FUNCTIONS
# ============================================================================
def parse_data(input_string):
    """Parse comma-separated input into numpy array"""
    if not input_string or input_string.strip() == "":
        return None
    
    numbers = []
    for item in input_string.split(','):
        item = item.strip()
        if item:
            try:
                numbers.append(float(item))
            except ValueError:
                continue
    
    return np.array(numbers) if numbers else None

def sturges_rule(n):
    """Calculate number of classes using Sturges' Rule"""
    return int(np.ceil(np.log2(n) + 1))

def calculate_class_statistics(data):
    """Calculate all statistical measures required"""
    n = len(data)
    min_val = np.min(data)
    max_val = np.max(data)
    range_val = max_val - min_val
    
    num_classes = sturges_rule(n)
    class_width = range_val / num_classes
    
    intervals = []
    frequencies = []
    cum_frequencies = []
    midpoints = []
    upper_bounds = []
    
    lower_bound = min_val
    
    for i in range(num_classes):
        upper_bound = lower_bound + class_width if i < num_classes - 1 else max_val + 0.0001
        
        if i == num_classes - 1:
            freq = np.sum((data >= lower_bound) & (data <= upper_bound))
        else:
            freq = np.sum((data >= lower_bound) & (data < upper_bound))
        
        frequencies.append(int(freq))
        midpoint = (lower_bound + upper_bound) / 2
        midpoints.append(midpoint)
        upper_bounds.append(upper_bound)
        
        interval_str = f"[{lower_bound:.2f}, {upper_bound:.2f}{']' if i == num_classes - 1 else ')'}"
        intervals.append(interval_str)
        
        lower_bound = upper_bound
    
    cum_frequencies = np.cumsum(frequencies).tolist()
    
    df = pd.DataFrame({
        "Class Interval": intervals,
        "Frequency": frequencies,
        "Cumulative Frequency": cum_frequencies,
        "Midpoint": [round(m, 2) for m in midpoints]
    })
    
    stats = {
        "n": n,
        "min": min_val,
        "max": max_val,
        "range": range_val,
        "num_classes": num_classes,
        "class_width": class_width,
        "mean": np.mean(data),
        "median": np.median(data),
        "std": np.std(data),
        "variance": np.var(data)
    }
    
    return df, stats, frequencies, midpoints, upper_bounds

# ============================================================================
# PLOTLY VISUALIZATIONS - ALL CORRECTED
# ============================================================================
def create_dot_plot(data):
    """Generate dot plot visualization"""
    y_jitter = np.random.normal(0, 0.08, len(data))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data,
        y=y_jitter,
        mode='markers',
        name='Data Points',
        marker=dict(
            size=12,
            color='#00ff9f',
            symbol='circle',
            line=dict(color='#00eaff', width=2),
            opacity=0.8
        ),
        hovertemplate='<b>Value:</b> %{x:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="DOT PLOT - DATA DISTRIBUTION",
            font=dict(family='Orbitron', size=18, color='#00ff9f'),
            x=0.05
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(family='Share Tech Mono', color='#00eaff'),
        xaxis=dict(
            title="DATA VALUES",
            gridcolor='rgba(0, 255, 159, 0.1)',
            linecolor='#00ff9f',
            linewidth=2,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="",
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        hovermode='closest',
        height=400,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig

def create_histogram(data, num_bins):
    """Generate histogram visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=num_bins,
        name='Frequency',
        marker=dict(
            color='rgba(0, 255, 159, 0.6)',
            line=dict(color='#00eaff', width=2)
        ),
        opacity=0.8,
        hovertemplate='<b>Range:</b> %{x}<br><b>Frequency:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="HISTOGRAM - FREQUENCY DISTRIBUTION",
            font=dict(family='Orbitron', size=18, color='#00ff9f'),
            x=0.05
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(family='Share Tech Mono', color='#00eaff'),
        xaxis=dict(
            title="CLASS INTERVALS",
            gridcolor='rgba(0, 255, 159, 0.1)',
            linecolor='#00ff9f',
            linewidth=2
        ),
        yaxis=dict(
            title="FREQUENCY",
            gridcolor='rgba(0, 234, 255, 0.1)',
            linecolor='#00eaff',
            linewidth=2
        ),
        bargap=0.05,
        height=400,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig

def create_frequency_polygon(midpoints, frequencies):
    """Generate frequency polygon visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=midpoints,
        y=frequencies,
        mode='lines+markers',
        name='Frequency Polygon',
        line=dict(color='#00eaff', width=3),
        marker=dict(
            size=10,
            color='#00ff9f',
            symbol='diamond',
            line=dict(color='#00eaff', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(0, 234, 255, 0.1)',
        hovertemplate='<b>Midpoint:</b> %{x:.2f}<br><b>Frequency:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="FREQUENCY POLYGON",
            font=dict(family='Orbitron', size=18, color='#00ff9f'),
            x=0.05
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(family='Share Tech Mono', color='#00eaff'),
        xaxis=dict(
            title="CLASS MIDPOINTS",
            gridcolor='rgba(0, 255, 159, 0.1)',
            linecolor='#00ff9f',
            linewidth=2
        ),
        yaxis=dict(
            title="FREQUENCY",
            gridcolor='rgba(0, 234, 255, 0.1)',
            linecolor='#00eaff',
            linewidth=2
        ),
        height=400,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig

def create_ogive(upper_bounds, cum_frequencies):
    """Generate ogive (cumulative frequency curve)"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=upper_bounds,
        y=cum_frequencies,
        mode='lines+markers',
        name='Cumulative Frequency',
        line=dict(color='#00ff9f', width=3),
        marker=dict(
            size=10,
            color='#00eaff',
            symbol='circle',
            line=dict(color='#00ff9f', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 159, 0.1)',
        hovertemplate='<b>Upper Bound:</b> %{x:.2f}<br><b>Cumulative Freq:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="OGIVE - CUMULATIVE FREQUENCY CURVE",
            font=dict(family='Orbitron', size=18, color='#00ff9f'),
            x=0.05
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(family='Share Tech Mono', color='#00eaff'),
        xaxis=dict(
            title="CLASS UPPER BOUNDS",
            gridcolor='rgba(0, 255, 159, 0.1)',
            linecolor='#00ff9f',
            linewidth=2
        ),
        yaxis=dict(
            title="CUMULATIVE FREQUENCY",
            gridcolor='rgba(0, 234, 255, 0.1)',
            linecolor='#00eaff',
            linewidth=2
        ),
        height=400,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="status-online"></span>
        <span style="font-family: 'Orbitron'; font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #00ff9f, #00eaff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        AEGIS STATISTICAL ANALYZER
        </span>
        <br>
        <span style="font-family: 'Share Tech Mono'; font-size: 0.85rem; color: #00eaff;">
        AIR-DEFENSE CONTROL SYSTEM v2.0 | DATA ANALYSIS MODULE
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown('<div class="system-header">🔓 DATA INPUT</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        data_input = st.text_area(
            "**INPUT DATA STREAM**",
            placeholder="Enter comma-separated numbers...\n\nExample: 12, 15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45",
            height=120,
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            run_analysis = st.button("⚡ RUN ANALYSIS", use_container_width=True)
    
    if run_analysis:
        data = parse_data(data_input)
        
        if data is None or len(data) == 0:
            st.error("❌ INVALID INPUT: No valid numbers detected.")
            return
        
        with st.spinner("🛰️ PROCESSING DATA STREAM..."):
            df_stats, stats, frequencies, midpoints, upper_bounds = calculate_class_statistics(data)
            
            # Summary Statistics
            st.markdown('<div class="system-header">📊 SYSTEM STATUS METRICS</div>', unsafe_allow_html=True)
            
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            with m1:
                st.metric("TOTAL COUNT", stats['n'])
            with m2:
                st.metric("MINIMUM", f"{stats['min']:.2f}")
            with m3:
                st.metric("MAXIMUM", f"{stats['max']:.2f}")
            with m4:
                st.metric("MEAN", f"{stats['mean']:.2f}")
            with m5:
                st.metric("MEDIAN", f"{stats['median']:.2f}")
            with m6:
                st.metric("STD DEV", f"{stats['std']:.2f}")
            
            s1, s2, s3 = st.columns(3)
            with s1:
                st.metric("RANGE", f"{stats['range']:.2f}")
            with s2:
                st.metric("NUM CLASSES", stats['num_classes'])
            with s3:
                st.metric("CLASS WIDTH", f"{stats['class_width']:.3f}")
            
            st.markdown("---")
            
            # Analysis Table
            st.markdown('<div class="system-header">📋 ANALYSIS TABLE</div>', unsafe_allow_html=True)
            
            st.dataframe(
                df_stats,
                use_container_width=True,
                height=400
            )
            
            # CSV Download
            csv = df_stats.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            download_link = f'<a href="data:file/csv;base64,{b64}" download="statistical_analysis.csv" style="text-decoration: none; display: inline-block; margin: 1rem 0; padding: 0.5rem 1rem; background: rgba(0, 255, 159, 0.1); border: 1px solid #00ff9f; border-radius: 4px; color: #00ff9f;">📥 DOWNLOAD CSV REPORT</a>'
            st.markdown(download_link, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Visualizations
            st.markdown('<div class="system-header">🛸 VISUAL SYSTEM</div>', unsafe_allow_html=True)
            
            # Row 1
            c1, c2 = st.columns(2)
            with c1:
                dot_plot = create_dot_plot(data)
                st.plotly_chart(dot_plot, use_container_width=True, config={'displayModeBar': False})
            
            with c2:
                histogram = create_histogram(data, stats['num_classes'])
                st.plotly_chart(histogram, use_container_width=True, config={'displayModeBar': False})
            
            # Row 2
            c3, c4 = st.columns(2)
            with c3:
                if len(midpoints) > 0:
                    polygon = create_frequency_polygon(midpoints, frequencies)
                    st.plotly_chart(polygon, use_container_width=True, config={'displayModeBar': False})
            
            with c4:
                if len(upper_bounds) > 0:
                    ogive = create_ogive(upper_bounds, df_stats['Cumulative Frequency'].tolist())
                    st.plotly_chart(ogive, use_container_width=True, config={'displayModeBar': False})
            
            st.success("✅ ANALYSIS COMPLETE | All systems operational")
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(0, 255, 159, 0.05); border: 2px dashed rgba(0, 255, 159, 0.3); border-radius: 8px; margin: 2rem 0;">
            <span style="font-family: 'Orbitron'; font-size: 1.2rem; color: #00ff9f;">
            🎯 SYSTEM ARMED & READY
            </span>
            <br><br>
            <span style="font-family: 'Share Tech Mono'; font-size: 0.9rem; color: #00eaff;">
            Enter comma-separated numerical data above and click "RUN ANALYSIS"
            </span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
