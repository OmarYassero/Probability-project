# app.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64

# Page Configuration - MUST BE FIRST
st.set_page_config(
    page_title="CYBER-QUANTUM STAT OS v2.0",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - CYBERPUNK/SCI-FI THEME
# ============================================================================
def inject_custom_css():
    """Inject high-tech cyberpunk CSS with glassmorphism, neon glow, and scanlines"""
    
    # Base64 encoded subtle noise texture (tiny transparent noise)
    noise_svg = "data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E"
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    /* TOTAL BLACKOUT */
    .stApp, .main, .stApp > header, .stApp > footer, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1v0mbdj > div {{
        background: #000000 !important;
        background-color: #000000 !important;
    }}
    
    /* Remove all default padding/margins */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }}
    
    /* Global font cyber */
    html, body, .stApp, div, p, span, label, .stMarkdown {{
        font-family: 'Share Tech Mono', 'Courier New', monospace !important;
        color: #00FFFF !important;
    }}
    
    /* Headers with Orbitron */
    h1, h2, h3, h4, h5, h6, .st-emotion-cache-1y4p8pa {{
        font-family: 'Orbitron', monospace !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        color: #BD00FF !important;
        text-shadow: 0 0 10px #BD00FF, 0 0 20px rgba(189,0,255,0.3) !important;
    }}
    
    /* Glassmorphism containers */
    .cyber-card, [data-testid="stVerticalBlock"] > div, .stPlotlyChart, .stDataFrame, .stTable, [data-testid="stForm"] {{
        background: rgba(0, 10, 20, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1), inset 0 0 20px rgba(0, 255, 255, 0.02) !important;
        margin-bottom: 1rem !important;
        padding: 0.5rem !important;
    }}
    
    /* Sidebar glass */
    [data-testid="stSidebar"] {{
        background: rgba(0, 0, 0, 0.95) !important;
        border-right: 2px solid #00FFFF !important;
        box-shadow: -10px 0 30px rgba(0, 255, 255, 0.2) !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {{
        color: #00FFFF !important;
    }}
    
    /* Cyber button */
    .stButton > button {{
        background: linear-gradient(135deg, #003333, #000000) !important;
        border: 2px solid #00FFFF !important;
        color: #00FFFF !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border-radius: 0px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #006666, #001111) !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.6) !important;
        border-color: #BD00FF !important;
        transform: scale(1.02) !important;
    }}
    
    /* Text area cyber */
    .stTextArea textarea {{
        background: #0a0a0a !important;
        border: 1px solid #00FFFF !important;
        color: #00FFFF !important;
        font-family: 'Share Tech Mono', monospace !important;
        box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.1) !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
        background: #000000;
    }}
    ::-webkit-scrollbar-track {{
        background: #000000;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #00FFFF;
        box-shadow: 0 0 10px #00FFFF;
    }}
    
    /* Scanline overlay */
    .scanline {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 99999;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 255, 255, 0.02) 0px,
            rgba(0, 255, 255, 0.02) 2px,
            transparent 2px,
            transparent 6px
        );
        opacity: 0.5;
    }}
    
    /* Noise overlay */
    .noise {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 99998;
        background-image: url('{noise_svg}');
        opacity: 0.12;
    }}
    
    /* Number input */
    .stNumberInput input {{
        background: #0a0a0a !important;
        border: 1px solid #BD00FF !important;
        color: #BD00FF !important;
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-family: 'Orbitron', monospace !important;
        color: #00FFFF !important;
        text-shadow: 0 0 8px #00FFFF !important;
    }}
    
    /* Dataframe styling */
    .dataframe, .stDataFrame {{
        background: rgba(0, 0, 0, 0.6) !important;
        border-color: #00FFFF !important;
    }}
    
    .dataframe th {{
        background: rgba(0, 255, 255, 0.1) !important;
        color: #BD00FF !important;
        border-color: #00FFFF !important;
    }}
    </style>
    
    <div class="scanline"></div>
    <div class="noise"></div>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# Inject the CSS
inject_custom_css()

# ============================================================================
# STATISTICAL FUNCTIONS
# ============================================================================
def parse_data_input(data_str):
    """Parse comma/semi-colon/space separated numeric data"""
    if not data_str.strip():
        return None
    
    # Replace common separators with comma
    for sep in [';', ' ', '\n', '\t']:
        data_str = data_str.replace(sep, ',')
    
    numbers = []
    for item in data_str.split(','):
        item = item.strip()
        if item:
            try:
                numbers.append(float(item))
            except ValueError:
                continue
    
    return np.array(numbers) if numbers else None

def sturges_rule(n):
    """Calculate optimal number of bins using Sturges' Rule"""
    return int(np.ceil(np.log2(n) + 1))

def create_frequency_distribution(data, num_bins=None):
    """Generate frequency distribution table with intervals"""
    if data is None or len(data) == 0:
        return None, None, None
    
    if num_bins is None:
        num_bins = sturges_rule(len(data))
    
    # Calculate histogram
    counts, bin_edges = np.histogram(data, bins=num_bins)
    
    # Create intervals
    intervals = []
    midpoints = []
    for i in range(len(bin_edges) - 1):
        lower = bin_edges[i]
        upper = bin_edges[i + 1]
        intervals.append(f"[{lower:.2f}, {upper:.2f})")
        midpoints.append((lower + upper) / 2)
    
    # Calculate cumulative frequencies
    cumulative = np.cumsum(counts)
    
    # Create DataFrame
    df = pd.DataFrame({
        'INTERVAL': intervals,
        'MIDPOINT': midpoints,
        'FREQUENCY': counts,
        'CUMULATIVE': cumulative
    })
    
    return df, bin_edges, counts

# ============================================================================
# PLOTLY VISUALIZATIONS WITH GLOW & EASING
# ============================================================================
def create_glow_layout(title, x_title="Value", y_title="Frequency"):
    """Create a neon-cyber layout for Plotly figures"""
    return go.Layout(
        title={
            'text': title,
            'font': {'family': 'Orbitron', 'size': 20, 'color': '#BD00FF'},
            'x': 0.05,
            'xanchor': 'left'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font={'family': 'Share Tech Mono', 'size': 12, 'color': '#00FFFF'},
        xaxis={
            'gridcolor': 'rgba(0, 255, 255, 0.1)',
            'linecolor': '#00FFFF',
            'linewidth': 1,
            'mirror': True,
            'title_font': {'color': '#00FFFF'},
            'tickfont': {'color': '#00FFFF'},
            'gridwidth': 0.5
        },
        yaxis={
            'gridcolor': 'rgba(189, 0, 255, 0.1)',
            'linecolor': '#BD00FF',
            'linewidth': 1,
            'mirror': True,
            'title_font': {'color': '#BD00FF'},
            'tickfont': {'color': '#BD00FF'},
            'gridwidth': 0.5
        },
        hoverlabel={
            'bgcolor': 'rgba(0,0,0,0.8)',
            'font_size': 12,
            'font_family': 'Share Tech Mono',
            'bordercolor': '#00FFFF'
        },
        margin=dict(l=50, r=30, t=60, b=50),
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )

def create_histogram_polygon(data, bin_edges, counts):
    """Create combined histogram and frequency polygon with glitch hover"""
    fig = go.Figure()
    
    # Histogram bars with cyan glow
    fig.add_trace(go.Bar(
        x=bin_edges[:-1],
        y=counts,
        width=np.diff(bin_edges),
        name='HISTOGRAM',
        marker=dict(
            color='rgba(0, 255, 255, 0.3)',
            line=dict(color='#00FFFF', width=1.5),
            pattern_shape=".",
        ),
        hovertemplate='<b>Interval</b>: %{x:.2f}<br><b>Freq</b>: %{y}<extra></extra>'
    ))
    
    # Frequency polygon line with purple glow
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    fig.add_trace(go.Scatter(
        x=bin_centers,
        y=counts,
        mode='lines+markers',
        name='POLYGON',
        line=dict(color='#BD00FF', width=3, shape='linear'),
        marker=dict(
            size=8,
            color='#BD00FF',
            symbol='diamond',
            line=dict(color='#00FFFF', width=1)
        ),
        hovertemplate='<b>Midpoint</b>: %{x:.2f}<br><b>Freq</b>: %{y}<extra></extra>'
    ))
    
    layout = create_glow_layout("📊 HISTOGRAM + FREQUENCY POLYGON", "DATA BINS", "FREQUENCY")
    layout.update(
        barmode='overlay',
        bargap=0.05,
        xaxis=dict(tickmode='linear'),
        hovermode='closest'
    )
    
    fig.update_layout(layout)
    
    # Add transition animation
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(
                label="▶ STREAM",
                method="animate",
                args=[None, {"frame": {"duration": 800, "easing": "cubic-in-out"}, "fromcurrent": True}]
            )]
        )]
    )
    
    return fig

def create_ogive(data, bin_edges, counts):
    """Create cumulative frequency ogive with neon glow"""
    cumulative = np.cumsum(counts)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=bin_centers,
        y=cumulative,
        mode='lines+markers',
        name='CUMULATIVE',
        line=dict(color='#00FFFF', width=3, dash='solid'),
        marker=dict(
            size=8,
            color='#BD00FF',
            symbol='circle',
            line=dict(color='#00FFFF', width=2)
        ),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.05)',
        hovertemplate='<b>Value</b>: %{x:.2f}<br><b>Cumulative Freq</b>: %{y}<extra></extra>'
    ))
    
    layout = create_glow_layout("📈 OGIVE (CUMULATIVE FREQUENCY)", "CLASS MIDPOINTS", "CUMULATIVE FREQUENCY")
    layout.update(
        yaxis=dict(type='linear'),
        xaxis=dict(type='linear')
    )
    
    fig.update_layout(layout)
    return fig

def create_dot_plot(data):
    """Create digital node-style dot plot"""
    # Create jittered positions for dots
    y_jitter = np.random.normal(0, 0.05, len(data))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data,
        y=y_jitter,
        mode='markers',
        name='DATA NODES',
        marker=dict(
            size=8,
            color='#00FFFF',
            symbol='diamond',
            line=dict(color='#BD00FF', width=1.5),
            opacity=0.8
        ),
        hovertemplate='<b>Value</b>: %{x:.2f}<extra></extra>'
    ))
    
    layout = create_glow_layout("⬜ DOT PLOT - DIGITAL NODES", "DATA VALUES", "JITTER")
    layout.update(
        yaxis=dict(showticklabels=False, title_text="", showgrid=False),
        xaxis=dict(showgrid=True),
        showlegend=False
    )
    
    fig.update_layout(layout)
    return fig

def create_box_plot(data):
    """Create minimalist vertical box plot with neon aesthetics"""
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=data,
        name='DISTRIBUTION',
        boxmean='sd',
        marker=dict(
            color='#00FFFF',
            line=dict(color='#BD00FF', width=2),
            outliercolor='#BD00FF',
            symbol='x'
        ),
        line=dict(color='#00FFFF', width=2),
        fillcolor='rgba(0, 255, 255, 0.1)',
        whiskerwidth=0.8,
        boxpoints='outliers',
        jitter=0.3,
        pointpos=0,
        hovertemplate='<b>Value</b>: %{y:.2f}<extra></extra>'
    ))
    
    layout = create_glow_layout("📦 BOX PLOT - QUANTUM DISTRIBUTION", "", "VALUES")
    layout.update(
        xaxis=dict(showticklabels=True, title_text=""),
        yaxis=dict(title_text="DATA VALUES", title_font_color='#BD00FF'),
        showlegend=False
    )
    
    fig.update_layout(layout)
    return fig

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Cyber header with ASCII art
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="font-family: 'Orbitron'; font-size: 28px; color: #00FFFF; text-shadow: 0 0 20px #00FFFF;">
        ⚡ CYBER-QUANTUM STATISTICAL OS v2.0 ⚡
        </span><br>
        <span style="font-family: 'Share Tech Mono'; font-size: 12px; color: #BD00FF;">
        [ SECURE DATA UPLINK TERMINAL // QUANTUM ANALYTICS ENGINE ]
        </span>
    </div>
    <hr style="border-color: #00FFFF; box-shadow: 0 0 10px #00FFFF;">
    """, unsafe_allow_html=True)
    
    # Sidebar - Input Portal
    with st.sidebar:
        st.markdown("### 🔐 DATA UPLINK PORTAL")
        st.markdown("---")
        
        data_input = st.text_area(
            "QUANTUM DATA STREAM",
            placeholder="Enter numbers separated by commas, spaces, or semicolons...\nExample: 12, 15, 18, 22, 25, 28, 30, 32, 35",
            height=150,
            key="data_input"
        )
        
        st.markdown("---")
        
        # Custom cyber button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uplink_btn = st.button("🚀 INITIATE UPLINK", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### ⚙️ SYSTEM PARAMS")
        
        manual_bins = st.number_input("BIN COUNT (0 = AUTO)", min_value=0, max_value=50, value=0, step=1)
        
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 10px; text-align: center; opacity: 0.6;">
        [ STURGES' RULE ENGAGED ]<br>
        [ QUANTUM-READY v2.0 ]
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if uplink_btn:
        data = parse_data_input(data_input)
        
        if data is None or len(data) == 0:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; border: 1px solid #FF0000; background: rgba(255,0,0,0.1);">
            <span style="color: #FF0000; font-family: 'Orbitron';">⚠ UPLINK FAILED: NO VALID DATA DETECTED ⚠</span>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Display data metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("TOTAL ENTRIES", f"{len(data)}", delta=None)
        with col2:
            st.metric("MEAN", f"{np.mean(data):.3f}")
        with col3:
            st.metric("STD DEV", f"{np.std(data):.3f}")
        with col4:
            st.metric("RANGE", f"{np.max(data) - np.min(data):.3f}")
        
        # Determine bins
        num_bins = manual_bins if manual_bins > 0 else sturges_rule(len(data))
        
        # Create frequency distribution
        freq_df, bin_edges, counts = create_frequency_distribution(data, num_bins)
        
        if freq_df is not None:
            # Frequency Distribution Table with cyber styling
            st.markdown("### 📋 FREQUENCY DISTRIBUTION MATRIX")
            
            # Style the dataframe
            styled_df = freq_df.style.background_gradient(cmap='Blues', subset=['FREQUENCY', 'CUMULATIVE'])
            styled_df = styled_df.set_properties(**{
                'background-color': 'rgba(0,0,0,0.6)',
                'border-color': '#00FFFF',
                'color': '#00FFFF',
                'font-family': 'Share Tech Mono'
            })
            
            st.dataframe(styled_df, use_container_width=True, height=300)
            
            # Visualization Suite
            st.markdown("---")
            st.markdown("### 🎛️ QUANTUM VISUALIZATION SUITE")
            
            # Row 1: Histogram + Polygon and Ogive
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = create_histogram_polygon(data, bin_edges, counts)
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                fig2 = create_ogive(data, bin_edges, counts)
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            
            # Row 2: Dot Plot and Box Plot
            col3, col4 = st.columns(2)
            
            with col3:
                fig3 = create_dot_plot(data)
                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            
            with col4:
                fig4 = create_box_plot(data)
                st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
            
            # Statistical summary in cyber style
            st.markdown("---")
            st.markdown("### 📊 QUANTUM STATISTICAL MATRIX")
            
            # Calculate quartiles
            q1, q2, q3 = np.percentile(data, [25, 50, 75])
            
            stats_cols = st.columns(5)
            with stats_cols[0]:
                st.metric("MIN", f"{np.min(data):.3f}")
            with stats_cols[1]:
                st.metric("Q1 (25%)", f"{q1:.3f}")
            with stats_cols[2]:
                st.metric("MEDIAN", f"{q2:.3f}")
            with stats_cols[3]:
                st.metric("Q3 (75%)", f"{q3:.3f}")
            with stats_cols[4]:
                st.metric("MAX", f"{np.max(data):.3f}")
            
            # Skewness and Kurtosis
            skew_val = pd.Series(data).skew()
            kurt_val = pd.Series(data).kurtosis()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("SKEWNESS", f"{skew_val:.3f}", 
                         delta="SYMMETRIC" if abs(skew_val) < 0.5 else "SKEWED")
            with col2:
                st.metric("KURTOSIS", f"{kurt_val:.3f}",
                         delta="MESOKURTIC" if abs(kurt_val) < 1 else "EXTREME")
    
    else:
        # Idle state - show cyber interface waiting for input
        st.markdown("""
        <div style="text-align: center; padding: 4rem; border: 1px solid #00FFFF; border-radius: 8px; background: rgba(0, 255, 255, 0.02);">
            <span style="font-family: 'Orbitron'; font-size: 20px; color: #00FFFF;">
            ⚡ SYSTEM READY ⚡
            </span><br><br>
            <span style="font-family: 'Share Tech Mono'; font-size: 14px; color: #BD00FF;">
            [ AWAITING DATA UPLINK ]
            </span><br>
            <span style="font-family: 'Share Tech Mono'; font-size: 11px; opacity: 0.6;">
            Input numeric data in the sidebar portal and press "INITIATE UPLINK"
            </span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
