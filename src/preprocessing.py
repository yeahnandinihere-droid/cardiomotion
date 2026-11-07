
import numpy as np


def validate_volume(image):
    """
    Validate a 3D cardiac MRI volume.
    """

    image = np.asarray(image, dtype=np.float32)

    if image.ndim != 3:
        raise ValueError(
            "Expected a 3D MRI volume."
        )

    if not np.isfinite(image).all():
        raise ValueError(
            "Image contains NaN or infinite values."
        )

    return image


def clip_intensity(image, lower_percentile=1, upper_percentile=99):
    """
    Reduce the influence of unusually low and high
    intensity values using percentile clipping.
    """

    image = validate_volume(image)

    nonzero_values = image[image != 0]

    if nonzero_values.size == 0:
        raise ValueError("MRI volume contains no nonzero voxels.")

    lower = np.percentile(nonzero_values, lower_percentile)
    upper = np.percentile(nonzero_values, upper_percentile)

    if upper <= lower:
        raise ValueError("Invalid intensity range.")

    clipped = np.clip(image, lower, upper)

    return clipped.astype(np.float32)


def normalize_intensity(image):
    """
    Apply z-score intensity normalisation.

    Background zero voxels remain zero.
    """

    image = validate_volume(image)

    foreground = image != 0

    if not np.any(foreground):
        raise ValueError("No foreground voxels found.")

    values = image[foreground]

    mean = np.mean(values)
    std = np.std(values)

    if std < 1e-8:
        raise ValueError(
            "Image intensity variation is too small."
        )

    normalized = np.zeros_like(image, dtype=np.float32)

    normalized[foreground] = (
        image[foreground] - mean
    ) / std

    return normalized


def preprocess_volume(image):
    """
    Complete initial preprocessing pipeline.

    1. Validate image
    2. Clip extreme intensities
    3. Normalize intensity
    """

    image = validate_volume(image)

    clipped = clip_intensity(image)

    normalized = normalize_intensity(clipped)

    return normalized
