
import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# --------------------------------------------------
# CARDIOMOTION
# Experimental Cardiovascular Imaging Research Tool
# --------------------------------------------------

st.set_page_config(
    page_title="CardioMotion",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ CardioMotion")
st.subheader("Computational Cardiovascular Imaging & Motion Analysis")

st.markdown("""
**CardioMotion** is an experimental research platform for cardiac MRI
visualisation, ventricular segmentation analysis, and exploratory
cardiac measurements.

Current development stage: **Experiment 001 — ACDC Dataset**
""")

st.warning(
    "Research prototype only. Measurements are exploratory and "
    "must not be used for clinical diagnosis or treatment decisions."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Research Controls")

uploaded_image = st.sidebar.file_uploader(
    "Upload cardiac MRI image (.nii or .nii.gz)",
    type=["nii", "gz"]
)

uploaded_mask = st.sidebar.file_uploader(
    "Upload segmentation mask (.nii or .nii.gz)",
    type=["nii", "gz"]
)

phase = st.sidebar.selectbox(
    "Cardiac phase",
    ["End-Diastole (ED)", "End-Systole (ES)"]
)

# --------------------------------------------------
# IMAGE LOADING
# --------------------------------------------------
def load_nifti(uploaded_file):

    if uploaded_file is None:
        return None, None

    import tempfile

    suffix = ".nii.gz" if uploaded_file.name.endswith(".nii.gz") else ".nii"

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

# --------------------------------------------------
# IMAGE VISUALISATION
# --------------------------------------------------

def display_image(image_data, mask_data=None):

    if image_data.ndim != 3:
        st.error("Expected a 3D cardiac MRI volume.")
        return

    if mask_data is not None and mask_data.shape != image_data.shape:
        st.error("Image and segmentation mask dimensions do not match.")
        return

    lv_area = (
        np.sum(mask_data == 3, axis=(0, 1))
        if mask_data is not None
        else np.zeros(image_data.shape[2])
    )

    slice_index = (
        int(np.argmax(lv_area))
        if mask_data is not None and np.any(lv_area)
        else image_data.shape[2] // 2
    )

    image_slice = np.rot90(image_data[:, :, slice_index])

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.imshow(image_slice, cmap="gray")

    if mask_data is not None:

        mask_slice = np.rot90(mask_data[:, :, slice_index])

        overlay = np.ma.masked_where(
            mask_slice == 0,
            mask_slice
        )

        ax.imshow(
            overlay,
            cmap="tab10",
            vmin=1,
            vmax=3,
            alpha=0.4
        )

    ax.set_title(f"Cardiac MRI — Slice {slice_index}")
    ax.axis("off")

    st.pyplot(fig)
    plt.close(fig)


# --------------------------------------------------
# VOLUME CALCULATION
# --------------------------------------------------

def calculate_volume(mask, spacing, label):

    voxel_count = np.sum(mask == label)

    voxel_volume = np.prod(spacing)

    volume_ml = voxel_count * voxel_volume / 1000

    return volume_ml


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

if uploaded_image is not None:

    try:

        image = load_nifti(uploaded_image)
        image_data = image.get_fdata()

        st.success("Cardiac MRI image loaded successfully.")

        st.write("### Image Information")

        col1, col2, col3 = st.columns(3)

        col1.metric("Image dimensions", str(image_data.shape))
        col2.metric(
            "Voxel spacing",
            str(tuple(round(x, 3) for x in image.header.get_zooms()[:3]))
        )
        col3.metric("Data type", str(image_data.dtype))

        mask = None

st.success("Segmentation mask loaded successfully.")
           mask_image, mask_data = load_nifti(uploaded_mask)
mask = mask_data.astype(np.uint8)

            if mask.shape != image_data.shape:
                st.error(
                    "Image and mask dimensions differ. "
                    "Please upload matching files."
                )
                st.stop()

            st.success("Segmentation mask loaded successfully.")

            st.write("### Segmentation Labels")

            st.write({
                "0": "Background",
                "1": "Right Ventricle (RV)",
                "2": "Myocardium (MYO)",
                "3": "Left Ventricle (LV)"
            })

            st.write(
                "Labels found in uploaded mask:",
                np.unique(mask).tolist()
            )

        st.write("### Cardiac MRI Visualisation")

        display_image(image_data, mask)

        # ------------------------------------------
        # EXPLORATORY MEASUREMENTS
        # ------------------------------------------

        if mask is not None:

            st.write("### Exploratory Ventricular Measurements")

            spacing = image.header.get_zooms()[:3]

            lv_volume = calculate_volume(mask, spacing, 3)
            rv_volume = calculate_volume(mask, spacing, 1)

            col1, col2 = st.columns(2)

            col1.metric("LV segmented volume", f"{lv_volume:.2f} mL")
            col2.metric("RV segmented volume", f"{rv_volume:.2f} mL")

            st.info(
                "These are single-volume estimates from the uploaded "
                "segmentation. They are not EDV/ESV or ejection fraction "
                "unless the corresponding cardiac phase and full-volume "
                "acquisition are correctly established. Verify slice "
                "spacing, gaps, orientation, and acquisition metadata."
            )

    except Exception as error:

        st.error(f"Unable to process the uploaded file: {error}")

else:

    st.info(
        "Upload a cardiac MRI NIfTI volume to begin the experiment."
    )

    st.write("### Planned Research Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **1. Cardiac Segmentation**

        - LV segmentation
        - RV segmentation
        - Myocardial segmentation

        **2. Cardiac Motion Analysis**

        - Motion tracking
        - Displacement estimation
        - Temporal analysis
        """)

    with col2:
        st.markdown("""
        **3. Myocardial Strain Analysis**

        - Regional deformation
        - Strain maps
        - 2D and 3D analysis

        **4. Quality & Validation**

        - Tracking reliability
        - Measurement uncertainty
        - Cross-dataset validation
        """)

st.divider()

st.caption(
    "CardioMotion | Experimental Research Software | "
    "Not intended for clinical use"
)
