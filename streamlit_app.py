import streamlit as st
import math

def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

def get_cct_range_values(range_name):
    if range_name == "2200K-4000K":
        return 2200, 1.8, [2200, 2700, 3000, 3500, 4000]
    elif range_name == "2700K-6500K":
        return 2700, 3.8, [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]

def cct_to_rgb(cct):
    """
    Improved CCT to RGB conversion using Tanner Helland's algorithm
    with better accuracy for warm and cool whites
    """
    # Clamp CCT to reasonable bounds
    cct = max(1000, min(40000, cct))
    
    # Convert to temperature in hundreds of Kelvin
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

st.set_page_config(page_title="CCT Slider App", page_icon="💡", layout="centered")

# Enhanced CSS with better dark mode support and improved styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base styling */
    .stApp {
        background-color: #f8f9fa;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
        max-width: 900px;
    }
    
    /* Main title styling */
    .main-title {
        background: linear-gradient(135deg, #2c5aa0 0%, #1e3d72 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(44, 90, 160, 0.2);
    }
    
    .main-title h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-title p {
        margin: 0.75rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #ffffff 0%, #f1f3f4 100%);
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border-left: 4px solid #2c5aa0;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        color: #1a1a1a;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Form controls styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        transition: border-color 0.2s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #2c5aa0;
        box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
    }
    
    .stSlider > div > div > div {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stNumberInput > div > div {
        background: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        transition: border-color 0.2s ease;
    }
    
    .stNumberInput > div > div:focus-within {
        border-color: #2c5aa0;
        box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: white;
        color: #2c5aa0;
        border: 2px solid #2c5aa0;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stButton > button:hover {
        background: #2c5aa0;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(44, 90, 160, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Current value display */
    .current-value {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .current-value-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c5aa0;
        margin-bottom: 0.5rem;
    }
    
    .current-value-text {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    /* Color swatch enhancement */
    .color-swatch {
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        border: 3px solid white;
        margin: 0 auto;
    }
    
    .color-swatch:hover {
        transform: scale(1.05) translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.2);
    }
    
    /* Reference colors grid */
    .reference-grid {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid #e1e5e9;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .reference-item {
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .reference-item:hover {
        transform: translateY(-2px);
    }
    
    .reference-swatch {
        width: 80px;
        height: 60px;
        border-radius: 12px;
        margin: 0 auto 12px auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 2px solid white;
        transition: all 0.2s ease;
    }
    
    .reference-swatch:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }
    
    /* RGB/Hex display */
    .tech-info {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .tech-info-label {
        font-weight: 600;
        color: #2c5aa0;
        margin-bottom: 0.25rem;
    }
    
    .tech-info-value {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 6px;
        border: 1px solid #e1e5e9;
        font-size: 0.9rem;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e1e5e9, transparent);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 2rem;
        }
        
        .main-title p {
            font-size: 1rem;
        }
        
        .reference-swatch {
            width: 60px;
            height: 45px;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
    <h1>💡 CCT Control Center</h1>
    <p>Professional color temperature visualization and control</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "slider_value" not in st.session_state:
    st.session_state.slider_value = 0

# Range selection
st.markdown('<div class="section-header">📊 Range Selection</div>', unsafe_allow_html=True)
range_name = st.selectbox("Select CCT Range:", ["2200K-4000K", "2700K-6500K"], key="range_select")
min_cct, cct_per_unit, preset_values = get_cct_range_values(range_name)

# CCT Control section
st.markdown('<div class="section-header">🔧 CCT Control</div>', unsafe_allow_html=True)

# Create two columns for slider and number input
ctrl_col1, ctrl_col2 = st.columns([3, 2])

with ctrl_col1:
    st.session_state.slider_value = st.slider(
        "Slider value (0-1000):",
        0, 1000, st.session_state.slider_value,
        key="slider"
    )

with ctrl_col2:
    cct_result = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
    cct_input = st.number_input(
        "CCT value:",
        float(min_cct),
        float(min_cct + 1000 * cct_per_unit),
        value=float(cct_result),
        key="cct_input",
        step=50.0
    )
    
    # Update slider if CCT input changes
    if abs(cct_input - cct_result) > 0.1:
        if min_cct <= cct_input <= min_cct + 1000 * cct_per_unit:
            st.session_state.slider_value = int(cct_to_slider(cct_input, min_cct, cct_per_unit))
            st.rerun()

# Update final values
cct_result = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
color_description = get_color_description(cct_result)

# Current setting display
st.markdown(f'''
<div class="current-value">
    <div class="current-value-title">Current Setting</div>
    <div class="current-value-text">{cct_result:.0f}K - {color_description}</div>
</div>
''', unsafe_allow_html=True)

# Preset buttons section
st.markdown('<div class="section-header">🎯 Quick Presets</div>', unsafe_allow_html=True)

preset_cols = st.columns(len(preset_values))
for i, preset in enumerate(preset_values):
    if preset_cols[i].button(f"{preset}K", key=f"preset_{preset}"):
        st.session_state.slider_value = int(cct_to_slider(preset, min_cct, cct_per_unit))
        st.rerun()

# Color preview section
st.markdown('<div class="section-header">🎨 Color Preview</div>', unsafe_allow_html=True)

r, g, b = cct_to_rgb(cct_result)
color_hex = f"#{r:02x}{g:02x}{b:02x}"

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f'''
    <div class="tech-info">
        <div class="tech-info-label">RGB Values</div>
        <div class="tech-info-value">({r}, {g}, {b})</div>
        <br>
        <div class="tech-info-label">Hex Color</div>
        <div class="tech-info-value">{color_hex}</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    # Large color swatch with enhanced styling
    text_color = 'white' if sum([r, g, b]) < 400 else '#1a1a1a'
    st.markdown(
        f'''
        <div class="color-swatch" style="
            width: 180px; 
            height: 100px; 
            background-color: {color_hex}; 
            display: flex;
            align-items: center;
            justify-content: center;
            color: {text_color};
            font-weight: 700;
            font-size: 1.3rem;
            text-shadow: 0 2px 4px {'rgba(0,0,0,0.3)' if sum([r, g, b]) > 400 else 'rgba(255,255,255,0.3)'};
        ">
            {cct_result:.0f}K
        </div>
        ''',
        unsafe_allow_html=True
    )

# Reference color comparison
st.markdown('<div class="section-header">🌡️ Reference Colors</div>', unsafe_allow_html=True)

st.markdown('<div class="reference-grid">', unsafe_allow_html=True)
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
                <div style="font-weight: 600; color: #2c5aa0; font-size: 1rem;">{ref_temp}K</div>
                <div style="color: #6c757d; font-size: 0.85rem; margin-top: 0.25rem;">{ref_desc}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
