import numpy as np
import pytest

from src.preprocessing import (
    validate_volume,
    clip_intensity,
    normalize_intensity,
    preprocess_volume
)


def sample_volume():
    image = np.zeros((10, 10, 5), dtype=np.float32)
    image[2:8, 2:8, :] = np.arange(180).reshape(6, 6, 5)
    return image


def test_volume_validation():
    image = sample_volume()
    assert validate_volume(image).shape == (10, 10, 5)


def test_background_remains_zero():
    result = preprocess_volume(sample_volume())
    assert np.all(result[0, :, :] == 0)


def test_preprocessing_output_is_finite():
    result = preprocess_volume(sample_volume())
    assert np.isfinite(result).all()


def test_preprocessing_preserves_shape():
    result = preprocess_volume(sample_volume())
    assert result.shape == (10, 10, 5)


def test_invalid_dimensions():
    with pytest.raises(ValueError):
        validate_volume(np.zeros((10, 10)))


def test_empty_volume():
    with pytest.raises(ValueError):
        preprocess_volume(np.zeros((10, 10, 5)))