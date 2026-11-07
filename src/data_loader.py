import nibabel as nib
import numpy as np
from pathlib import Path


def load_nifti(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    image = nib.load(str(file_path))
    image_data = image.get_fdata()

    return image, image_data


def get_image_metadata(image):
    return {
        "dimensions": image.shape,
        "voxel_spacing": image.header.get_zooms()[:3],
        "orientation_affine": image.affine,
        "data_type": str(image.get_data_dtype())
    }


def validate_image_mask(image, mask):
    if image.shape[:3] != mask.shape[:3]:
        return False, "Image and mask dimensions do not match."

    if not np.allclose(image.affine, mask.affine, atol=1e-4):
        return False, "Image and mask spatial geometry do not match."

    return True, "Image and mask geometry validated."


def get_segmentation_labels(mask):
    return np.unique(mask).astype(int).tolist()


def calculate_voxel_volume(image):
    spacing = image.header.get_zooms()[:3]
    return float(np.prod(spacing))