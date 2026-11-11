import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

st.set_page_config(
    page_title="CardioMotion",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ CardioMotion")
st.subheader("Computational Cardiovascular Imaging & Motion Analysis")

st.markdown("""
An experimental platform for 4D cardiac MRI visualisation
and exploratory cardiac motion analysis.
""")
def load_4d_mri(uploaded_file):
    suffix = ".nii.gz" if uploaded_file.name.endswith(".nii.gz") else ".nii"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    try:
        image = nib.load(temp_path)
        image_data = image.get_fdata()
        return image_data

    finally:
        os.remove(temp_path)
st.divider()
st.subheader("Upload Cardiac MRI")

uploaded_file = st.file_uploader(
    "Choose a 4D MRI file",
    type=["nii", "gz"]
)
def next_frame(current_frame, total_frames):
    next_frame = current_frame + 1

    if next_frame >= total_frames:
        next_frame = 0

    return next_frame
if uploaded_file is not None:
    image_data = load_4d_mri(uploaded_file)

    st.success("MRI file loaded successfully!")
    st.write("MRI dimensions:", image_data.shape)
total_frames=image_data.shape[3]
total_slices=image_data.shape[2]
st.write("Total MRI Slices:",total_slices)
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
    col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Play"):
        st.session_state.is_playing = True

with col2:
    if st.button("⏸ Pause"):
        st.session_state.is_playing = False
if image_data.ndim==4:
st.sucess("This is a 4D MRI!")
else 
st.error("this is not a 4D MRI!")
def display_mri_info(image data):
st.write("MRI dimesnions:",image_data.shape)
display_mri_info(image_data)

if uploaded_file is not None:
    image_data = load_4d_mri(uploaded_file)

    st.success("MRI file loaded successfully!")

    st.write("MRI dimensions:", image_data.shape)

    if image_data.ndim == 4:
        st.success("This is a 4D MRI!")

        total_slices = image_data.shape[2]
        total_frames = image_data.shape[3]

        st.write("Total MRI slices:", total_slices)
        st.write("Total cardiac frames:", total_frames)

        frame_number = st.slider(
    "Select Cardiac Frame",
    min_value=1,
    max_value=total_frames,
    value=1
)
        frame_index = frame_number - 1
slice_number = st.slider(
    "Select MRI Slice",
    min_value=1,
    max_value=total_slices,
    value=1
)
slice_index = slice_number - 1
      image_slice = image_data[:, :, slice_index, frame_index]

        st.write("Selected image shape:", image_slice.shape)

        fig, ax = plt.subplots()

        ax.imshow(image_slice, cmap="gray")
        ax.axis("off")

        st.pyplot(fig)

        plt.close(fig)

    else:
        st.error("This is not a 4D MRI!")
