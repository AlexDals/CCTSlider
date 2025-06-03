import streamlit as st
import math

def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

def get_cct_range_values(range_name):
    if range_name == "2200K-4000K (Warm Whites)":
        return 2200, 1.8, [2200, 2700, 3000, 3500, 4000]
    elif range_name == "2700K-6500K (Full Range)":
        return 2700, 3.8, [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]

def cct_to_rgb(cct):
    """
    Improved CCT to RGB conversion using Tanner Helland's algorithm
    with better accuracy for warm and cool whites
    """
    cct = max(1000, min(40000, cct))
    temp = cct / 100.0
    
    # Calculate Red
    if temp <= 66:
        red = 255
    else:
        red = temp - 60
        red = 329.698727446 * (red ** -0.1332047592)
        red = max(0, min(255, red))
    
    # Calculate Green
    if temp <= 66:
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
        green = max(0, min(255, green))
    else:
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        green = max(0, min(255, green))
    
    # Calculate Blue
    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = temp - 10
        blue = 138.5177312231 * math.log(blue) - 305.0447927307
        blue = max(0, min(255, blue))
    
    # Apply gamma correction for better visual accuracy
    def gamma_correct(value):
        normalized = value / 255.0
        corrected = normalized ** (1.0 / 2.2)
        return int(corrected * 255)
    
    return gamma_correct(red), gamma_correct(green), gamma_correct(blue)

def get_color_description(cct):
    """Get a descriptive name for the color temperature"""
    if cct < 2000:
        return "Candlelight"
    elif cct < 2700:
        return "Very Warm White"
    elif cct < 3000:
        return "Warm White"
    elif cct < 3500:
        return "Soft White"
    elif cct < 4000:
        return "Neutral White"
    elif cct < 5000:
        return "Cool White"
    elif cct < 6000:
        return "Daylight"
    elif cct < 7000:
        return "Cool Daylight"
    else:
        return "Blue Sky"

# Page configuration
st.set_page_config(
    page_title="CCT Color Temperature Tool",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional, clean design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Card styling */
    .stContainer > div {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        color: #1e293b !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stSelectbox label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #ff6b35, #f7931e, #ffff00, #87ceeb, #4169e1);
        height: 8px;
        border-radius: 4px;
    }
    
    .stSlider > div > div > div > div > div {
        background: white;
        border: 3px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        width: 24px;
        height: 24px;
    }
    
    /* Slider value display box - make transparent */
    .stSlider > div > div > div[data-testid="stSliderTickBarMin"],
    .stSlider > div > div > div[data-testid="stSliderTickBarMax"],
    .stSlider > div > div > div > div[data-testid="stMarkdownContainer"] {
        background: transparent !important;
    }
    
    .stSlider .stMarkdown {
        background: transparent !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: #1e293b !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stNumberInput label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        color: #374151;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        border-color: #3b82f6;
        background: #f0f9ff;
        color: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    /* Color swatch */
    .color-swatch {
        width: 200px;
        height: 120px;
        border-radius: 15px;
        border: 3px solid #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.3rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 0 auto;
    }
    
    /* Temperature display */
    .current-temp {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .temp-description {
        font-size: 1.3rem;
        color: #3b82f6;
        font-weight: 500;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Info display */
    .info-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 0.5rem;
    }
    
    .info-label {
        font-weight: 600;
        color: #374151;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .info-value {
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        color: #1e293b;
        font-weight: 500;
    }
    
    /* Reference colors */
    .reference-item {
        text-align: center;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .reference-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .reference-swatch {
        width: 100%;
        height: 60px;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        margin-bottom: 0.5rem;
    }
    
    /* General text color fixes */
    .stApp, .stApp p, .stApp span, .stApp div {
        color: #1e293b !important;
    }
    
    /* Slider label styling */
    .stSlider label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    /* Fix any white text on white background */
    .stMarkdown p {
        color: #1e293b !important;
    }
    
    /* Ensure all input labels are visible */
    label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    /* Remove extra padding */
    .stMarkdown {
        margin-bottom: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "slider_value" not in st.session_state:
    st.session_state.slider_value = 0

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">💡 CCT Color Temperature Tool</div>
    <div class="main-subtitle">Professional color temperature visualization with accurate warm and cool white rendering</div>
</div>
""", unsafe_allow_html=True)

# Range Selection
with st.container():
    st.markdown('<div class="section-header">🎛️ Range Selection</div>', unsafe_allow_html=True)
    range_name = st.selectbox(
        "CCT Range:",
        ["2200K-4000K (Warm Whites)", "2700K-6500K (Full Range)"],
        label_visibility="collapsed"
    )

min_cct, cct_per_unit, preset_values = get_cct_range_values(range_name)

# Temperature Control
with st.container():
    st.markdown('<div class="section-header">🔄 Temperature Control</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.33, 1], gap="medium")
    
    with col1:
        st.session_state.slider_value = st.slider(
            "Slider value (0-1000):",
            0, 1000, st.session_state.slider_value,
            key="slider"
        )
    
    with col2:
        cct_result = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
        cct_input = st.number_input(
            "CCT value:",
            float(min_cct),
            float(min_cct + 1000 * cct_per_unit),
            value=float(cct_result),
            key="cct_input"
        )
        
        # Update slider if CCT input changes
        if abs(cct_input - cct_result) > 0.1:
            if min_cct <= cct_input <= min_cct + 1000 * cct_per_unit:
                st.session_state.slider_value = int(cct_to_slider(cct_input, min_cct, cct_per_unit))
                st.rerun()

# Quick Presets
with st.container():
    st.markdown('<div class="section-header">🎯 Quick Presets</div>', unsafe_allow_html=True)
    
    # Create preset buttons
    cols = st.columns(len(preset_values))
    for i, preset in enumerate(preset_values):
        if cols[i].button(f"{preset}K", key=f"preset_{preset}"):
            st.session_state.slider_value = int(cct_to_slider(preset, min_cct, cct_per_unit))
            st.rerun()

# Update final values
cct_result = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
color_description = get_color_description(cct_result)
r, g, b = cct_to_rgb(cct_result)
color_hex = f"#{r:02x}{g:02x}{b:02x}"

# Color Preview
with st.container():
    st.markdown('<div class="section-header">🎨 Color Preview</div>', unsafe_allow_html=True)
    
    # Temperature display
    st.markdown(f'<div class="current-temp">{cct_result:.0f}K</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="temp-description">{color_description}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Color information
        st.markdown(f"""
        <div class="info-item">
            <div class="info-label">RGB Values</div>
            <div class="info-value">({r}, {g}, {b})</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-item">
            <div class="info-label">Hex Code</div>
            <div class="info-value">{color_hex}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-item">
            <div class="info-label">Temperature</div>
            <div class="info-value">{cct_result:.0f}K</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Color swatch
        text_color = 'black' if sum([r, g, b]) > 400 else 'white'
        st.markdown(
            f'''
            <div class="color-swatch" style="
                background-color: {color_hex}; 
                color: {text_color};
            ">
                {cct_result:.0f}K
            </div>
            ''',
            unsafe_allow_html=True
        )

# Reference Colors
with st.container():
    st.markdown('<div class="section-header">🌡️ Reference Temperatures</div>', unsafe_allow_html=True)
    
    reference_temps = [2700, 3000, 4000, 5000, 6500]
    ref_cols = st.columns(len(reference_temps))
    
    for i, ref_temp in enumerate(reference_temps):
        r_ref, g_ref, b_ref = cct_to_rgb(ref_temp)
        hex_ref = f"#{r_ref:02x}{g_ref:02x}{b_ref:02x}"
        ref_desc = get_color_description(ref_temp)
        
        with ref_cols[i]:
            st.markdown(
                f'''
                <div class="reference-item">
                    <div class="reference-swatch" style="background-color: {hex_ref};"></div>
                    <div style="font-weight: 600; color: #374151; margin-bottom: 0.25rem;">{ref_temp}K</div>
                    <div style="font-size: 0.85rem; color: #6b7280;">{ref_desc}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
