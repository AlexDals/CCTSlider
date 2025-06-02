
import streamlit as st

def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

def get_cct_per_unit(min_cct, max_cct, slider_max):
    return (max_cct - min_cct) / slider_max

st.title("Dals Connect Slider CCT Converter")

# Dropdown to select CCT range
cct_range = st.selectbox("Select CCT range:", ["2200K-4000K", "2700K-6500K"])

if cct_range == "2200K-4000K":
    min_cct = 2200
    max_cct = 4000
    presets = [2200, 2700, 3000, 3500, 4000]
else:
    min_cct = 2700
    max_cct = 6500
    presets = [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]

slider_max = 1000
cct_per_unit = get_cct_per_unit(min_cct, max_cct, slider_max)

# Slider to select value
slider_value = st.slider("Select slider value (0-1000):", 0, slider_max)
cct_result = slider_to_cct(slider_value, min_cct, cct_per_unit)
st.write(f"Corresponding CCT: {cct_result:.2f}K")

# Number input to enter desired CCT
cct_value = st.number_input(f"Enter desired CCT ({min_cct}K-{max_cct}K):", min_cct, max_cct)
slider_result = cct_to_slider(cct_value, min_cct, cct_per_unit)
st.write(f"Corresponding slider value: {slider_result:.2f}")

# Preset buttons
st.write("Preset CCT values:")
cols = st.columns(len(presets))
for i, preset in enumerate(presets):
    if cols[i].button(f"{preset}K"):
        slider_value = cct_to_slider(preset, min_cct, cct_per_unit)
        st.slider("Select slider value (0-1000):", 0, slider_max, int(slider_value))
        st.write(f"Corresponding CCT: {preset:.2f}K")
        st.write(f"Corresponding slider value: {slider_value:.2f}")

# Real-time color preview
color_hex = f"#{int((cct_result - min_cct) / (max_cct - min_cct) * 255):02x}0000"
st.write(f"Color preview: {color_hex}")
st.markdown(f'<div style="width:100px;height:100px;background-color:{color_hex};"></div>', unsafe_allow_html=True)
