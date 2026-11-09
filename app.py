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

st.subheader("4D Cardiac MRI Analysis Platform")

st.info(
    "Experimental Research Software | "
    "Not intended for clinical use"
)

st.write(
    "Explore cardiac MRI across multiple slices "
    "and cardiac time frames."
)

st.divider()
st.header("Upload Cardiac MRI")

uploaded_file = st.file_uploader(
    "Choose a 4D cardiac MRI file",
    type=["nii", "gz"]
)
def load_4d_mri(uploaded_file):
    suffix = (
    ".nii.gz"
    if uploaded_file.name.lower().endswith(".nii.gz")
    else ".nii"
)
    with tempfile.NamedTemporaryFile(
    suffix=suffix,
    delete=False
) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name
    try:
    image = nib.load(temp_path)
    image_data = image.get_fdata()

    return image, image_data
    finally:
    if os.path.exists(temp_path):
        os.remove(temp_path)
        if uploaded_file is not None:

    try:
        image, image_data = load_4d_mri(uploaded_file)
                if image_data.ndim != 4:
            st.error(
                "This is not a 4D MRI volume. "
                "Please upload a 4D cardiac MRI."
            )
                            else:
            st.success("4D Cardiac MRI loaded successfully!")
                    st.subheader("MRI Information")

            st.write("Image dimensions:", image_data.shape)

            st.write("Data type:", image_data.dtype)

            st.write(
                "Voxel spacing:",
                image.header.get_zooms()
            )
                    total_slices = image_data.shape[2]
            total_frames = image_data.shape[3]
                    slice_number = st.slider(
                "Select MRI Slice",
                min_value=1,
                max_value=total_slices,
                value=min(5, total_slices)
            )
                    slice_index = slice_number - 1
                    frame_number = st.slider(
                "Select Cardiac Frame",
                min_value=1,
                max_value=total_frames,
                value=1
            )
                    image_slice = image_data[
                :, :, slice_index, frame_index
            ]
                    vmin = np.percentile(image_slice, 2)
            vmax = np.percentile(image_slice, 98)
                    if vmax <= vmin:
                vmax = vmin + 1
                                    midpoint = (vmin + vmax) / 2
                                    half_range = (vmax - vmin) / 2
                                    contrast = st.slider(
                "Adjust Contrast",
                min_value=50,
                max_value=200,
                value=100
            )
                                    contrast_factor = 100 / contrast
                                    brightness = st.slider(
                "Adjust Brightness",
                min_value=-50,
                max_value=50,
                value=0
            )
                                    brightness_shift = (
                brightness / 100
            ) * (vmax - vmin)
                                    adjusted_vmin = (
                midpoint
                - (half_range * contrast_factor)
                - brightness_shift
            )

            adjusted_vmax = (
                midpoint
                + (half_range * contrast_factor)
                - brightness_shift
            )
                    fig, ax = plt.subplots(figsize=(8, 8))

            ax.imshow(
                image_slice,
                cmap="gray",
                vmin=adjusted_vmin,
                vmax=adjusted_vmax
            )

            ax.set_title(
                f"Cardiac Frame {frame_number} | "
                f"Slice {slice_number}"
            )

            ax.axis("off")

            st.pyplot(fig)

            plt.close(fig)
        
