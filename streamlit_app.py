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

# Custom CSS for Dals.com inspired theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title styling */
    .main-title {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Professional color scheme */
    .stSelectbox > div > div {
        margin-bottom: 0.5rem;
        border-radius: 8px;
    }
    
    .stSlider > div > div > div {
        margin-bottom: 0.5rem;
    }
    
    .stNumberInput > div > div {
        margin-bottom: 0.5rem;
        border-radius: 8px;
    }
    
    .stButton > button {
        margin-bottom: 0.25rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background: white;
        color: #333;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #f8f9fa;
        border-color: #007bff;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,123,255,0.15);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #ddd, transparent);
    }
    
    /* Color swatch enhancement */
    .color-swatch {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }
    
    .color-swatch:hover {
        transform: scale(1.02);
    }
    
    /* Reference colors grid */
    .reference-grid {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
    }
    
    /* Professional text styling */
    .current-value {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
    <h1 style="margin:0; font-size: 2.2rem; font-weight: 600;">💡 CCT Control Center</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem;">Professional color temperature visualization and control</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "slider_value" not in st.session_state:
    st.session_state.slider_value = 0

range_name = st.selectbox("Select CCT Range:", ["2200K-4000K", "2700K-6500K"])
min_cct, cct_per_unit, preset_values = get_cct_range_values(range_name)

# Combined slider and CCT control
st.divider()
st.markdown('<div class="section-header">🔧 CCT Control</div>', unsafe_allow_html=True)

# Create two columns for slider and number input
ctrl_col1, ctrl_col2 = st.columns([2, 1])

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
        key="cct_input"
    )
    
    # Update slider if CCT input changes
    if abs(cct_input - cct_result) > 0.1:
        if min_cct <= cct_input <= min_cct + 1000 * cct_per_unit:
            st.session_state.slider_value = int(cct_to_slider(cct_input, min_cct, cct_per_unit))
            st.rerun()

# Update final values
cct_result = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
color_description = get_color_description(cct_result)

# Combined preset buttons and color preview
st.divider()
st.markdown('<div class="section-header">🎯 Presets & Color Preview</div>', unsafe_allow_html=True)

# Preset buttons
preset_cols = st.columns(len(preset_values))
for i, preset in enumerate(preset_values):
    if preset_cols[i].button(f"{preset}K"):
        st.session_state.slider_value = int(cct_to_slider(preset, min_cct, cct_per_unit))
        st.rerun()

# Color preview
r, g, b = cct_to_rgb(cct_result)
color_hex = f"#{r:02x}{g:02x}{b:02x}"

st.markdown(f'<div class="current-value"><strong>Current Setting:</strong> {cct_result:.0f}K ({color_description})</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.write(f"**RGB:** ({r}, {g}, {b})")
    st.write(f"**Hex:** `{color_hex}`")

with col2:
    # Large color swatch with enhanced styling
    st.markdown(
        f'''
        <div class="color-swatch" style="
            width: 150px; 
            height: 80px; 
            background-color: {color_hex}; 
            border: 2px solid #e9ecef; 
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: {'black' if sum([r, g, b]) > 400 else 'white'};
            font-weight: 600;
            font-size: 1.1rem;
            text-shadow: 1px 1px 2px {'rgba(255,255,255,0.8)' if sum([r, g, b]) > 400 else 'rgba(0,0,0,0.8)'};
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        ">
            {cct_result:.0f}K
        </div>
        ''',
        unsafe_allow_html=True
    )

# Reference color comparison
st.divider()
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
            <div style="text-align: center;">
                <div style="
                    width: 70px; 
                    height: 50px; 
                    background-color: {hex_ref}; 
                    border: 2px solid #e9ecef; 
                    border-radius: 8px;
                    margin: 0 auto 8px auto;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    transition: transform 0.2s ease;
                " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"></div>
                <small style="font-weight: 500; color: #2c3e50;"><strong>{ref_temp}K</strong><br><span style="color: #6c757d;">{ref_desc}</span></small>
            </div>
            ''',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
