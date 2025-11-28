"""
Two-dimensional cross correlation
"""

import numpy as np
from scipy import signal
from astropy.modeling import models, fitting

FITTER = fitting.LMLSQFitter()


def max_location_indices(arr: np.ndarray) -> tuple[int, ...]:
    """Return array indices of maximum value in `arr`

    This behaves like maxloc() in Fortran
    """
    return np.unravel_index(np.argmax(arr), arr.shape)  # type: ignore


def regularize(a):
    mean = np.mean(a)
    std = np.std(a)
    return (a - mean) / std


def measure_shift_integer(
    img_ref: np.ndarray, img_new: np.ndarray
) -> tuple[float, float]:
    """
    Measure (dy, dx) that best aligns img_new onto img_ref using 2D cross-correlation.

    Convention:
        img_new(y + dy, x + dx) ≈ img_ref(y, x)
    so positive dy, dx mean img_new must be shifted down/right to match img_ref.
    """

    assert len(img_ref.shape) == 2, "Images must be two-dimensional"
    assert img_ref.shape == img_new.shape, "Images mut be the same shape"

    # 2D cross-correlation: slide img_new over img_ref
    corr = signal.correlate2d(
        regularize(img_ref),
        regularize(img_new),
        mode="full",
        boundary="fill",
        fillvalue=0.0,
    )

    # Location of maximum correlation
    max_y, max_x = max_location_indices(corr)

    # Zero-lag position in 'full' correlation
    # For correlate2d(ref, new): zero lag is at (ref_shape - 1)
    y0 = img_new.shape[0] - 1
    x0 = img_new.shape[1] - 1

    # Lags (dy, dx)
    dy = max_y - y0
    dx = max_x - x0

    return float(dy), float(dx)


def measure_shift_gfit(
    img_ref: np.ndarray, img_new: np.ndarray
) -> tuple[models.Gaussian2D, np.ndarray]:
    """
    Measure (dy, dx) that best aligns img_new onto img_ref using 2D cross-correlation with 2D Gaussian fitting.

    Convention:
        img_new(y + dy, x + dx) ≈ img_ref(y, x)
    so positive dy, dx mean img_new must be shifted down/right to match img_ref.
    """

    # 2D cross-correlation: slide img_new over img_ref
    corr = signal.correlate2d(
        regularize(img_ref),
        regularize(img_new),
        mode="full",
        boundary="fill",
        fillvalue=0.0,
    )
    # Location of maximum correlation
    max_y, max_x = max_location_indices(corr)

    # Pixel grid for corr array indices
    ny, nx = corr.shape
    y, x = np.mgrid[0:ny, 0:nx]
    # Fit a 2d gaussian to the cross-correlation image
    g_init = models.Gaussian2D(
        amplitude=1.0,
        x_mean=max_x,
        y_mean=max_y,
        x_stddev=2.0,
        y_stddev=2.0,
    )
    g = FITTER(g_init, x, y, corr)
    # Return both the fit and the fitted image
    return g, g(x, y)
