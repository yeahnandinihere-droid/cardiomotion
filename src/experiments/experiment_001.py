
import os
import re
import numpy as np

from src.data_loader import (
    load_nifti,
    get_image_metadata,
    validate_image_mask,
    get_segmentation_labels
)

from src.preprocessing import preprocess_volume


def read_cardiac_phases(info_path):
    """Read ED and ES frame numbers from Info.cfg."""

    with open(info_path, "r") as file:
        text = file.read()

    phases = {}

    for phase in ["ED", "ES"]:
        match = re.search(
            rf"^{phase}:\s*(\d+)",
            text,
            flags=re.MULTILINE
        )

        if match is None:
            raise ValueError(f"{phase} phase not found.")

        phases[phase] = int(match.group(1))

    return phases


def calculate_volume(mask, image, label):
    """Calculate exploratory segmented volume in mL."""

    spacing = image.header.get_zooms()[:3]

    voxel_volume = np.prod(spacing)

    voxel_count = np.sum(mask == label)

    return float(voxel_count * voxel_volume / 1000)


def analyse_patient(patient_dir, patient_id="patient001"):
    """Analyse one ACDC patient at ED and ES."""

    info_path = os.path.join(patient_dir, "Info.cfg")

    phases = read_cardiac_phases(info_path)

    results = {}

    for phase, frame in phases.items():

        image_path = os.path.join(
            patient_dir,
            f"{patient_id}_frame{frame:02d}.nii.gz"
        )

        mask_path = os.path.join(
            patient_dir,
            f"{patient_id}_frame{frame:02d}_gt.nii.gz"
        )

        image, image_data = load_nifti(image_path)

        mask_image, mask_data = load_nifti(mask_path)

        valid, message = validate_image_mask(
            image,
            mask_image
        )

        if not valid:
            raise ValueError(message)

        if image_data.shape != mask_data.shape:
            raise ValueError("Image and mask shapes differ.")

        if not np.allclose(
            image.affine,
            mask_image.affine,
            atol=1e-4
        ):
            raise ValueError("Image and mask geometry differ.")

        processed_image = preprocess_volume(image_data)

        results[phase] = {
            "frame": frame,
            "metadata": get_image_metadata(image),
            "labels": get_segmentation_labels(mask_data),
            "lv_volume_ml": calculate_volume(
                mask_data, image, 3
            ),
            "rv_volume_ml": calculate_volume(
                mask_data, image, 1
            ),
            "processed_image": processed_image
        }

    return results


if __name__ == "__main__":

    DATA_ROOT = "data/ACDC/training"

    PATIENT_ID = "patient001"

    PATIENT_DIR = os.path.join(
        DATA_ROOT,
        PATIENT_ID
    )

    if not os.path.isdir(PATIENT_DIR):
        raise FileNotFoundError(
            f"Patient folder not found: {PATIENT_DIR}. "
            "Download and place the ACDC data locally first."
        )

    results = analyse_patient(
        PATIENT_DIR,
        PATIENT_ID
    )

    print("\nCARDIOMOTION — EXPERIMENT 001")

    for phase in ["ED", "ES"]:

        print(f"\n{phase} PHASE")

        print("Frame:", results[phase]["frame"])

        print(
            "LV volume:",
            round(results[phase]["lv_volume_ml"], 2),
            "mL"
        )

        print(
            "RV volume:",
            round(results[phase]["rv_volume_ml"], 2),
            "mL"
        )

        print(
            "Segmentation labels:",
            results[phase]["labels"]
        )
