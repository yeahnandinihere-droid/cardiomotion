
import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CardioMotion",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ CardioMotion")

st.subheader(
    "Experimental Cardiovascular Imaging Research Tool"
)

st.info(
    "An experimental platform for cardiovascular imaging "
    "visualization and computational motion analysis."
)


# --------------------------------------------------
# 2. MRI FILE UPLOAD
# --------------------------------------------------

st.divider()

st.header("Upload Cardiac MRI")

uploaded_file = st.file_uploader(
    "Choose a 4D cardiac MRI file",
    type=["nii", "gz"]
)


# --------------------------------------------------
# 3. LOAD MRI DATA
# --------------------------------------------------

def load_4d_mri(uploaded_file):

    suffix = (
        ".nii.gz"
        if uploaded_file.name.lower().endswith(".nii.gz")
        else ".nii"
    )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False
        ) as temp_file:

            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        image = nib.load(temp_path)

        image_data = image.get_fdata(
            dtype=np.float32
        )

        return image, image_data

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# --------------------------------------------------
# 4. MRI IMAGE INFORMATION
# --------------------------------------------------

def display_mri_info(image, image_data):

    st.subheader("MRI Image Information")

    dimensions = image_data.shape
    spacing = image.header.get_zooms()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Image Dimensions",
            str(dimensions)
        )

    with col2:
        st.metric(
            "Number of Slices",
            dimensions[2]
        )

    with col3:
        st.metric(
            "Cardiac Frames",
            dimensions[3] if len(dimensions) == 4 else 0
        )

    st.write("Voxel spacing:", spacing)
    st.write("Data type:", image_data.dtype)


# --------------------------------------------------
# 5. 4D CARDIAC MRI VIEWER WITH CINE PLAYBACK
# --------------------------------------------------

def display_4d_image(image_data):

    if image_data.ndim != 4:

        st.error(
            "Expected a 4D cardiac MRI volume."
        )

        return

    total_slices = image_data.shape[2]
    total_frames = image_data.shape[3]

    st.divider()

    st.header("4D Cardiac MRI Viewer")

    # Initialize playback state

    if "cine_frame" not in st.session_state:
        st.session_state.cine_frame = 1

    if "cine_playing" not in st.session_state:
        st.session_state.cine_playing = False

    # Playback controls

    st.subheader("Cine Playback Controls")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "▶ Play",
            disabled=st.session_state.cine_playing
        ):

            st.session_state.cine_playing = True

    with col2:

        if st.button(
            "⏸ Pause",
            disabled=not st.session_state.cine_playing
        ):

            st.session_state.cine_playing = False

    with col3:

        if st.button("↺ Restart"):

            st.session_state.cine_playing = False
            st.session_state.cine_frame = 1

    # Playback speed

    fps = st.select_slider(
        "Playback Speed (Frames per Second)",
        options=[1, 2, 5, 10],
        value=5
    )

    # MRI slice selection

    slice_number = st.slider(
        "MRI Slice",
        min_value=1,
        max_value=total_slices,
        value=total_slices // 2 + 1,
        key="cine_slice"
    )

    slice_index = slice_number - 1

    # Automatic playback refresh

    playback_interval = (
        1 / fps
        if st.session_state.cine_playing
        else None
    )

    @st.fragment(run_every=playback_interval)
    def cine_display():

        # Move to the next frame during playback

        if st.session_state.cine_playing:

            st.session_state.cine_frame = (
                st.session_state.cine_frame % total_frames
            ) + 1

        # Manual frame selection

        frame_number = st.slider(
            "Cardiac Frame",
            min_value=1,
            max_value=total_frames,
            key="cine_frame"
        )

        frame_index = frame_number - 1

        # Extract MRI image

        image_slice = image_data[
            :, :, slice_index, frame_index
        ].T

        # Display MRI image

        fig, ax = plt.subplots(figsize=(7, 7))

        ax.imshow(
            image_slice,
            cmap="gray",
            origin="lower"
        )

        ax.set_title(
            f"Cardiac Frame {frame_number}/{total_frames} "
            f"| Slice {slice_number}/{total_slices}"
        )

        ax.axis("off")

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            f"Displaying frame {frame_number} "
            f"of {total_frames}"
        )

    cine_display()


# --------------------------------------------------
# 6. MAIN APPLICATION
# --------------------------------------------------

if uploaded_file is not None:

    try:

        with st.spinner("Loading cardiac MRI..."):

            image, image_data = load_4d_mri(
                uploaded_file
            )

        if image_data.ndim != 4:

            st.error(
                "This application currently requires "
                "a 4D cardiac MRI file."
            )

        else:

            st.success(
                "4D Cardiac MRI loaded successfully!"
            )

            display_mri_info(
                image,
                image_data
            )

            display_4d_image(
                image_data
            )

    except Exception as error:

        st.error(
            f"Unable to load MRI file: {error}"
        )

else:

    st.info(
        "Upload a NIfTI cardiac MRI file to begin "
        "exploring cardiac frames."
    )

    st.caption(
        "Supported formats: .nii and .nii.gz"
    )


# --------------------------------------------------
# 7. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CardioMotion | Cardiovascular Imaging "
    "Visualization and Motion Analysis"
)
