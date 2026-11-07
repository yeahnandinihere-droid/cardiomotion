
import numpy as np


def validate_volume(image):
    image = np.asarray(image, dtype=np.float32)

    if image.ndim != 3:
        raise ValueError("Expected a 3D MRI volume.")

    if not np.isfinite(image).all():
        raise ValueError("Image contains NaN or infinite values.")

    return image


def clip_intensity(image, lower_percentile=1, upper_percentile=99):
    image = validate_volume(image)

    foreground = image != 0

    if not np.any(foreground):
        raise ValueError("MRI volume contains no nonzero voxels.")

    values = image[foreground]

    lower = np.percentile(values, lower_percentile)
    upper = np.percentile(values, upper_percentile)

    if upper <= lower:
        raise ValueError("Invalid intensity range.")

    clipped = np.zeros_like(image, dtype=np.float32)

    clipped[foreground] = np.clip(
        values, lower, upper
    )

    return clipped


def normalize_intensity(image):
    image = validate_volume(image)

    foreground = image != 0

    if not np.any(foreground):
        raise ValueError("No foreground voxels found.")

    values = image[foreground]

    mean = np.mean(values)
    std = np.std(values)

    if std < 1e-8:
        raise ValueError("Image intensity variation is too small.")

    normalized = np.zeros_like(image, dtype=np.float32)

    normalized[foreground] = (values - mean) / std

    return normalized


def preprocess_volume(image):
    image = validate_volume(image)
    clipped = clip_intensity(image)
    normalized = normalize_intensity(clipped)

    return normalized
