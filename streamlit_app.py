
import streamlit as st

def slider_to_cct(slider_value, min_cct, cct_per_unit):
    return min_cct + slider_value * cct_per_unit

def cct_to_slider(cct_value, min_cct, cct_per_unit):
    return (cct_value - min_cct) / cct_per_unit

def get_cct_range_and_unit(selected_range):
    if selected_range == "2200K-4000K":
        return 2200, 1.8
    elif selected_range == "2700K-6500K":
        return 2700, 3.8

def get_color_from_cct(cct):
    # Approximate color representation for the given CCT
    if cct < 2700:
        return "#FFDDC1"  # Warm white
    elif cct < 3500:
        return "#FFF4E1"  # Soft white
    elif cct < 4500:
        return "#FFFFFB"  # Neutral white
    elif cct < 5500:
        return "#F1FAFF"  # Cool white
    else:
        return "#E1F5FF"  # Daylight

st.title("Slider to CCT Converter")

selected_range = st.selectbox("Select CCT range:", ["2200K-4000K", "2700K-6500K"])
min_cct, cct_per_unit = get_cct_range_and_unit(selected_range)

preset_ccts = {
    "2200K-4000K": [2200, 2700, 3000, 3500, 4000],
    "2700K-6500K": [2700, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]
}

preset_buttons = preset_ccts[selected_range]

preset_cct = st.radio("Select a preset CCT:", preset_buttons, index=0)

slider_value = cct_to_slider(preset_cct, min_cct, cct_per_unit)
cct_value = slider_to_cct(slider_value, min_cct, cct_per_unit)

slider_value = st.slider("Select slider value (0-1000):", 0, 1000, int(slider_value))
cct_value = st.number_input("Enter desired CCT:", float(min_cct), float(min_cct + 1000 * cct_per_unit), float(cct_value))

# Update slider and CCT input based on preset button selection
if st.button("Update from preset"):
    slider_value = cct_to_slider(preset_cct, min_cct, cct_per_unit)
    cct_value = slider_to_cct(slider_value, min_cct, cct_per_unit)

# Update slider and CCT input based on user input
slider_value = cct_to_slider(cct_value, min_cct, cct_per_unit)
cct_value = slider_to_cct(slider_value, min_cct, cct_per_unit)

st.write(f"Corresponding CCT: {cct_value:.2f}K")
st.write(f"Corresponding slider value: {slider_value:.2f}")

# Display color preview
color = get_color_from_cct(cct_value)
st.markdown(f'<div style="width:100%; height:100px; background-color:{color};"></div>', unsafe_allow_html=True)
