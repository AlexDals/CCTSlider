
import streamlit as st

def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

def get_cct_range_values(range_name):
    if range_name == "2200K-4000K":
        return 2200, 1.8, [2200, 2700, 3000, 3500, 4000]
    elif range_name == "2700K-6500K":
        return 2700, 3.8, [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]

st.set_page_config(page_title="CCT Slider App", page_icon="💡", layout="centered")

st.title("CCT Slider App")

range_name = st.selectbox("Select CCT Range:", ["2200K-4000K", "2700K-6500K"])
min_cct, cct_per_unit, preset_values = get_cct_range_values(range_name)

slider_value = st.slider("Select slider value (0-1000):", 0, 1000)
cct_result = slider_to_cct(slider_value, min_cct, cct_per_unit)
st.write(f"Corresponding CCT: {cct_result:.2f}K")

cct_value = st.number_input("Enter desired CCT:", float(min_cct), float(min_cct + 1000 * cct_per_unit))
slider_result = cct_to_slider(cct_value, min_cct, cct_per_unit)
st.write(f"Corresponding slider value: {slider_result:.2f}")

st.write("Preset CCT values:")
cols = st.columns(len(preset_values))
for i, preset in enumerate(preset_values):
    if cols[i].button(f"{preset}K"):
        cct_value = preset
        slider_result = cct_to_slider(cct_value, min_cct, cct_per_unit)
        st.slider("Select slider value (0-1000):", 0, 1000, int(slider_result))
        st.write(f"Corresponding CCT: {cct_value:.2f}K")

color_hex = f"#{int((cct_result - 2200) / (6500 - 2200) * 255):02x}00{int((6500 - cct_result) / (6500 - 2200) * 255):02x}"
st.write(f"Color preview: {color_hex}")
st.markdown(f'<div style="width:100px;height:100px;background-color:{color_hex};border-radius:50%;"></div>', unsafe_allow_html=True)
    
