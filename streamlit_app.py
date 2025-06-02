
import streamlit as st

# Function to convert slider value to CCT
def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

# Function to convert CCT to slider value
def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

# Function to get the color approximation for a given CCT
def cct_to_color(cct):
    # Simplified approximation of color based on CCT
    if cct < 3000:
        return "#FFDDC1"  # Warm light
    elif cct < 4000:
        return "#FFE4B5"  # Neutral light
    else:
        return "#FFFACD"  # Cool light

# Initialize session state
if 'cct_range' not in st.session_state:
    st.session_state.cct_range = "2200-4000"
if 'slider_value' not in st.session_state:
    st.session_state.slider_value = 0
if 'cct_value' not in st.session_state:
    st.session_state.cct_value = 2200

# Define CCT ranges
cct_ranges = {
    "2200-4000": (2200, 4000, 1.8),
    "2700-6500": (2700, 6500, 3.8)
}

# Title
st.title("Slider to CCT Converter")

# CCT range selection
st.session_state.cct_range = st.selectbox("Select CCT range:", cct_ranges.keys())

# Get the selected range values
min_cct, max_cct, cct_per_unit = cct_ranges[st.session_state.cct_range]

# Slider for selecting value
st.session_state.slider_value = st.slider("Select slider value (0-1000):", 0, 1000, int(st.session_state.slider_value))

# Calculate corresponding CCT
st.session_state.cct_value = slider_to_cct(st.session_state.slider_value, min_cct, cct_per_unit)
st.write(f"Corresponding CCT: {st.session_state.cct_value:.2f}K")

# Number input for desired CCT
st.session_state.cct_value = st.number_input(f"Enter desired CCT ({min_cct}K-{max_cct}K):", float(min_cct), float(max_cct), float(st.session_state.cct_value))
st.session_state.slider_value = cct_to_slider(st.session_state.cct_value, min_cct, cct_per_unit)
st.write(f"Corresponding slider value: {st.session_state.slider_value:.2f}")

# Preset buttons
preset_values = {
    "2200-4000": [2200, 2700, 3000, 3500, 4000],
    "2700-6500": [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]
}

st.write("Presets:")
for preset in preset_values[st.session_state.cct_range]:
    if st.button(f"{preset}K"):
        st.session_state.cct_value = preset
        st.session_state.slider_value = cct_to_slider(st.session_state.cct_value, min_cct, cct_per_unit)

# Color preview
color = cct_to_color(st.session_state.cct_value)
st.write("Color Preview:")
st.markdown(f"<div style='width:100%; height:100px; background-color:{color};'></div>", unsafe_allow_html=True)
