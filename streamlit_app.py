
import streamlit as st

# Function to convert slider value to CCT
def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

# Function to convert CCT to slider value
def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

# Function to get the color approximation for a given CCT
def cct_to_color(cct):
    # Approximate color for given CCT (simplified)
    if cct < 3000:
        return "#FFDDC1"  # Warm white
    elif cct < 4000:
        return "#FFF4E1"  # Soft white
    elif cct < 5000:
        return "#FFFFFF"  # Daylight
    else:
        return "#E0F7FF"  # Cool white

# Define CCT ranges
cct_ranges = {
    "2200K-4000K": (2200, 4000, 1.8),
    "2700K-6500K": (2700, 6500, 3.8)
}

# Streamlit app
st.title("Slider to CCT Converter")

# Select CCT range
cct_range = st.selectbox("Select CCT range:", list(cct_ranges.keys()))
min_cct, max_cct, cct_per_unit = cct_ranges[cct_range]

# Slider for selecting value
slider_value = st.slider("Select slider value (0-1000):", 0, 1000, key="slider")

# Calculate corresponding CCT
cct_result = slider_to_cct(slider_value, min_cct, cct_per_unit)

# Display corresponding CCT
st.write(f"Corresponding CCT: {cct_result:.2f}K")

# Display color preview
color = cct_to_color(cct_result)
st.markdown(f'<div style="width:100%; height:50px; background-color:{color};"></div>', unsafe_allow_html=True)

# Input for desired CCT
cct_value = st.number_input("Enter desired CCT:", float(min_cct), float(max_cct), value=float(cct_result), key="cct_input")

# Calculate corresponding slider value
slider_result = cct_to_slider(cct_value, min_cct, cct_per_unit)

# Update slider value based on CCT input
st.session_state.slider = slider_result

# Preset buttons
st.write("Presets:")
if cct_range == "2200K-4000K":
    presets = [2200, 2700, 3000, 3500, 4000]
else:
    presets = [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]

for preset in presets:
    if st.button(f"{preset}K"):
        st.session_state.slider = cct_to_slider(preset, min_cct, cct_per_unit)
        st.session_state.cct_input = preset
    
