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

# Custom CSS for tighter spacing
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    .stSelectbox > div > div {
        margin-bottom: 0.5rem;
    }
    .stSlider > div > div > div {
        margin-bottom: 0.5rem;
    }
    .stNumberInput > div > div {
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        margin-bottom: 0.25rem;
    }
    hr {
        margin: 1rem 0;
    }
    .stSubheader {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("💡 CCT Slider App")
st.caption("Accurate color temperature visualization with improved warm and cool white rendering")

# Initialize session state
if "slider_value" not in st.session_state:
    st.session_state.slider_value = 0

range_name = st.selectbox("Select CCT Range:", ["2200K-4000K", "2700K-6500K"])
min_cct, cct_per_unit, preset_values = get_cct_range_values(range_name)

# Slider and CCT display
st.divider()
st.subheader("🔁 Slider to CCT Conversion")
st.session_state.slider_value = st.slider(
    "Select slider value (0-1000):",
    0, 1000, st.session_state.slider_value,
    key="slider"
)
cct_result = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
color_description = get_color_description(cct_result)
st.write(f"Corresponding CCT: **{cct_result:.2f}K** ({color_description})")

# CCT input and validation
st.divider()
st.subheader("🔁 CCT to Slider Conversion")
cct_input = st.number_input(
    "Enter desired CCT:",
    float(min_cct),
    float(min_cct + 1000 * cct_per_unit),
    value=float(cct_result)
)

if min_cct <= cct_input <= min_cct + 1000 * cct_per_unit:
    slider_result = cct_to_slider(cct_input, min_cct, cct_per_unit)
    st.write(f"Slider value: **{slider_result:.2f}**")
else:
    st.error("CCT value is out of range for the selected range.")

# Preset buttons
st.divider()
st.subheader("🎯 Preset CCT Values")
cols = st.columns(len(preset_values))
for i, preset in enumerate(preset_values):
    if cols[i].button(f"{preset}K"):
        st.session_state.slider_value = int(cct_to_slider(preset, min_cct, cct_per_unit))
        st.rerun()

# Color preview with enhanced display
st.divider()
st.subheader("🎨 Color Preview")
r, g, b = cct_to_rgb(cct_result)
color_hex = f"#{r:02x}{g:02x}{b:02x}"

col1, col2 = st.columns([1, 1])

with col1:
    st.write(f"**RGB:** ({r}, {g}, {b})")
    st.write(f"**Hex:** `{color_hex}`")
    st.write(f"**Type:** {color_description}")

with col2:
    # Large color swatch
    st.markdown(
        f'''
        <div style="
            width: 150px; 
            height: 80px; 
            background-color: {color_hex}; 
            border: 2px solid #ccc; 
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: {'black' if sum([r, g, b]) > 400 else 'white'};
            font-weight: bold;
            text-shadow: 1px 1px 2px {'white' if sum([r, g, b]) > 400 else 'black'};
        ">
            {cct_result:.0f}K
        </div>
        ''',
        unsafe_allow_html=True
    )

# Reference color comparison
st.divider()
st.subheader("🌡️ Reference Colors")
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
                    border: 1px solid #ccc; 
                    border-radius: 5px;
                    margin: 0 auto 3px auto;
                "></div>
                <small><strong>{ref_temp}K</strong><br>{ref_desc}</small>
            </div>
            ''',
            unsafe_allow_html=True
        )
