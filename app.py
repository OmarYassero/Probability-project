# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64

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
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
    
    /* Global dark background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #050505 100%);
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Glassmorphism panels */
    .glass-panel {
        background: rgba(10, 10, 10, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 159, 0.2);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 20px rgba(0, 255, 159, 0.1);
        transition: all 0.3s ease;
    }
    
    .glass-panel:hover {
        border-color: rgba(0, 255, 159, 0.5);
        box-shadow: 0 0 30px rgba(0, 255, 159, 0.2);
    }
    
    /* Section headers */
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
    
    .system-header-cyan {
        border-left-color: #00eaff;
        color: #00eaff;
        text-shadow: 0 0 10px rgba(0, 234, 255, 0.5);
    }
    
    /* Input area */
    .input-container {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid rgba(0, 255, 159, 0.3);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #00ff9f 0%, #00b8ff 100%);
        color: #0a0a0a;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 255, 159, 0.6);
        background: linear-gradient(135deg, #00eaff 0%, #00ff9f 100%);
    }
    
    /* Text input */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #00ff9f;
        color: #00ff9f;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        border-radius: 4px;
    }
    
    .stTextArea textarea:focus {
        border-color: #00eaff;
        box-shadow: 0 0 10px rgba(0, 234, 255, 0.3);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        color: #00ff9f;
        text-shadow: 0 0 8px rgba(0, 255, 159, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #00eaff;
    }
    
    /* DataFrame styling */
    .dataframe {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid #00ff9f;
        border-radius: 4px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
    }
    
    .dataframe th {
        background: rgba(0, 255, 159, 0.15);
        color: #00ff9f;
        font-family: 'Orbitron', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0.75rem;
    }
    
    .dataframe td {
        color: #00eaff;
        padding: 0.5rem;
    }
    
    /* Status indicators */
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
    
    /* Download button */
    .download-btn {
        background: rgba(0, 255, 159, 0.1);
        border: 1px solid #00ff9f;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .download-btn:hover {
        background: rgba(0, 255, 159, 0.2);
        border-color: #00eaff;
    }
    
    /* Divider */
    hr {
        border-color: rgba(0, 255, 159, 0.2);
        margin: 1.5rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ff9f;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00eaff;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Orbitron', monospace;
        background: rgba(0, 255, 159, 0.05);
        color: #00ff9f;
    }
    </style>
    
    <div style="position: fixed; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #00ff9f, #00eaff, #00ff9f); z-index: 9999;"></div>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# Call CSS injection
inject_custom_css()

# ============================================================================
# STATISTICAL FUNCTIONS
# ============================================================================
def parse_data(input_string):
    """Parse comma-separated input into numpy array"""
    if not input_string or input_string.strip() == "":
        return None
    
    # Split by comma and clean
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
    
    # Number of classes using Sturges' Rule
    num_classes = sturges_rule(n)
    
    # Class width
    class_width = range_val / num_classes
    
    # Create class intervals
    intervals = []
    frequencies = []
    cum_frequencies = []
    midpoints = []
    
    lower_bound = min_val
    
    for i in range(num_classes):
        upper_bound = lower_bound + class_width if i < num_classes - 1 else max_val + 0.0001
        
        # Count frequency in this interval
        if i == num_classes - 1:
            freq = np.sum((data >= lower_bound) & (data <= upper_bound))
        else:
            freq = np.sum((data >= lower_bound) & (data < upper_bound))
        
        frequencies.append(freq)
        midpoints.append((lower_bound + upper_bound) / 2)
        
        # Format interval string
        interval_str = f"[{lower_bound:.2f}, {upper_bound:.2f}{']' if i == num_classes - 1 else ')'}"
        intervals.append(interval_str)
        
        lower_bound = upper_bound
    
    # Calculate cumulative frequencies
    cum_frequencies = np.cumsum(frequencies)
    
    # Create DataFrame
    df = pd.DataFrame({
        "Class Interval": intervals,
        "Frequency": frequencies,
        "Cumulative Frequency": cum_frequencies,
        "Midpoint": [round(m, 2) for m in midpoints]
    })
    
    return df, {
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
    }, frequencies, midpoints, intervals

# ============================================================================
# PLOTLY VISUALIZATIONS
# ============================================================================
def create_dot_plot(data):
    """Generate dot plot visualization"""
    # Create jitter for y-axis
    y_jitter = np.random.normal(0, 0.08, len(data))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data,
        y=y_jitter,
        mode='markers',
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
        title={
            'text': "DOT PLOT - DATA DISTRIBUTION",
            'font': {'family': 'Orbitron', 'size': 18, 'color': '#00ff9f'},
            'x': 0.05
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font={'family': 'Share Tech Mono', 'color': '#00eaff'},
        xaxis=dict(
            title="DATA VALUES",
            gridcolor='rgba(0, 255, 159, 0.1)',
            linecolor='#00ff9f',
            linewidth=2,
            showgrid=True
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

def create_histogram(data, bins):
    """Generate histogram visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=bins,
        marker=dict(
            color='rgba(0, 255, 159, 0.6)',
            line=dict(color='#00eaff', width=2)
        ),
        opacity=0.8,
        hovertemplate='<b>Range:</b> %{x}<br><b>Frequency:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "HISTOGRAM - FREQUENCY DISTRIBUTION",
            'font': {'family': 'Orbitron', 'size': 18, 'color': '#00ff9f'},
            'x': 0.05
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font={'family': 'Share Tech Mono', 'color': '#00eaff'},
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
        line=dict(color='#00eaff', width=3, shape='linear'),
        marker=dict(
            size=10,
            color='#00ff9f',
            symbol='diamond',
            line=dict(color='#00eaff', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(0, 234, 255, 0.1),
        hovertemplate='<b>Midpoint:</b> %{x:.2f}<br><b>Frequency:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "FREQUENCY POLYGON",
            'font': {'family': 'Orbitron', 'size': 18, 'color': '#00ff9f'},
            'x': 0.05
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font={'family': 'Share Tech Mono', 'color': '#00eaff'},
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
        line=dict(color='#00ff9f', width=3, dash='solid'),
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
        title={
            'text': "OGIVE - CUMULATIVE FREQUENCY CURVE",
            'font': {'family': 'Orbitron', 'size': 18, 'color': '#00ff9f'},
            'x': 0.05
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font={'family': 'Share Tech Mono', 'color': '#00eaff'},
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
# CSV DOWNLOAD FUNCTION
# ============================================================================
def download_csv(df):
    """Create CSV download button"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="statistical_analysis.csv" style="text-decoration: none;"><div class="download-btn">📥 DOWNLOAD CSV REPORT</div></a>'
    return href

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Title section
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
    
    # DATA INPUT SECTION
    st.markdown('<div class="system-header">🔓 DATA INPUT</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        data_input = st.text_area(
            "**INPUT DATA STREAM**",
            placeholder="Enter comma-separated numbers...\n\nExample: 12, 15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45",
            height=120,
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            run_analysis = st.button("⚡ RUN ANALYSIS", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if run_analysis:
        # Parse data
        data = parse_data(data_input)
        
        if data is None or len(data) == 0:
            st.error("❌ INVALID INPUT: No valid numbers detected. Please enter comma-separated numeric values.")
            return
        
        with st.spinner("🛰️ PROCESSING DATA STREAM..."):
            # Calculate statistics
            df_stats, stats, frequencies, midpoints, intervals = calculate_class_statistics(data)
            
            # Extract upper bounds for ogive
            upper_bounds = []
            for interval in intervals:
                # Parse interval string to get upper bound
                import re
                match = re.search(r'[\d.]+,\s*([\d.]+)', interval)
                if match:
                    upper_bounds.append(float(match.group(1)))
            
            cum_frequencies = df_stats["Cumulative Frequency"].values
            
            # SUMMARY STATISTICS
            st.markdown('<div class="system-header">📊 SYSTEM STATUS METRICS</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("TOTAL COUNT", stats['n'])
            with col2:
                st.metric("MINIMUM", f"{stats['min']:.2f}")
            with col3:
                st.metric("MAXIMUM", f"{stats['max']:.2f}")
            with col4:
                st.metric("MEAN", f"{stats['mean']:.2f}")
            with col5:
                st.metric("MEDIAN", f"{stats['median']:.2f}")
            with col6:
                st.metric("STD DEV", f"{stats['std']:.2f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("RANGE", f"{stats['range']:.2f}")
            with col2:
                st.metric("NUM CLASSES", stats['num_classes'])
            with col3:
                st.metric("CLASS WIDTH", f"{stats['class_width']:.3f}")
            
            st.markdown("---")
            
            # ANALYSIS TABLE
            st.markdown('<div class="system-header system-header-cyan">📋 ANALYSIS TABLE</div>', unsafe_allow_html=True)
            
            # Display table with custom styling
            st.dataframe(
                df_stats,
                use_container_width=True,
                height=400,
                column_config={
                    "Class Interval": st.column_config.TextColumn("CLASS INTERVAL", width="medium"),
                    "Frequency": st.column_config.NumberColumn("FREQUENCY", format="%d"),
                    "Cumulative Frequency": st.column_config.NumberColumn("CUMULATIVE FREQUENCY", format="%d"),
                    "Midpoint": st.column_config.NumberColumn("MIDPOINT", format="%.2f")
                }
            )
            
            # Download button
            st.markdown(download_csv(df_stats), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # VISUALIZATION SUITE
            st.markdown('<div class="system-header">🛸 VISUAL SYSTEM</div>', unsafe_allow_html=True)
            
            # Row 1: Dot Plot and Histogram
            col1, col2 = st.columns(2)
            
            with col1:
                with st.spinner("🖥️ RENDERING DOT PLOT..."):
                    dot_plot = create_dot_plot(data)
                    st.plotly_chart(dot_plot, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                with st.spinner("📊 RENDERING HISTOGRAM..."):
                    histogram = create_histogram(data, stats['num_classes'])
                    st.plotly_chart(histogram, use_container_width=True, config={'displayModeBar': False})
            
            # Row 2: Frequency Polygon and Ogive
            col3, col4 = st.columns(2)
            
            with col3:
                with st.spinner("📈 RENDERING FREQUENCY POLYGON..."):
                    if len(midpoints) > 0:
                        polygon = create_frequency_polygon(midpoints, frequencies)
                        st.plotly_chart(polygon, use_container_width=True, config={'displayModeBar': False})
            
            with col4:
                with st.spinner("📉 RENDERING OGIVE..."):
                    if len(upper_bounds) > 0:
                        ogive = create_ogive(upper_bounds, cum_frequencies)
                        st.plotly_chart(ogive, use_container_width=True, config={'displayModeBar': False})
            
            # Success message
            st.success("✅ ANALYSIS COMPLETE | All systems operational")
            
    else:
        # Idle state - show placeholder
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(0, 255, 159, 0.05); border: 2px dashed rgba(0, 255, 159, 0.3); border-radius: 8px; margin: 2rem 0;">
            <span style="font-family: 'Orbitron'; font-size: 1.2rem; color: #00ff9f;">
            🎯 SYSTEM ARMED & READY
            </span>
            <br><br>
            <span style="font-family: 'Share Tech Mono'; font-size: 0.9rem; color: #00eaff;">
            Enter comma-separated numerical data above and click "RUN ANALYSIS" to initialize statistical protocols
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.7rem; color: rgba(0, 255, 159, 0.4); padding: 1rem;">
    AEGIS STAT ANALYZER | Powered by Streamlit & Plotly | SECURE AIR-DEFENSE PROTOCOL v2.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
