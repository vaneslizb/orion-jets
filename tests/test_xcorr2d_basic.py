import numpy as np

from orion_jets.xcorr2d import measure_shift_integer, max_location_indices


# ---------------------------------------------------------------
# Helper function for test images
# ---------------------------------------------------------------


def make_gaussian_image(x0, y0, shape=(40, 40), sigma=3.0):
    """Simple 2D Gaussian for testing."""
    ny, nx = shape
    y, x = np.mgrid[0:ny, 0:nx]
    dx = (x - x0) / sigma
    dy = (y - y0) / sigma
    return np.exp(-0.5 * (dx * dx + dy * dy))


# ---------------------------------------------------------------
# Test 1: basic behaviour of max_location_indices
# ---------------------------------------------------------------


def test_max_location_indices_finds_peak():
    arr = np.array([[1, 2, 3], [4, 9, 5]])
    i, j = max_location_indices(arr)

    # The maximum value (9) is at row 1, column 1
    assert i == 1
    assert j == 1


# ---------------------------------------------------------------
# Test 2: measure_shift_integer recovers zero shift
# ---------------------------------------------------------------


def test_measure_shift_integer_zero_shift():
    img = make_gaussian_image(20, 20)

    dy, dx = measure_shift_integer(img, img)

    assert dy == 0
    assert dx == 0


# ---------------------------------------------------------------
# Test 3: measure_shift_integer recovers a small integer shift
# ---------------------------------------------------------------


def test_measure_shift_integer_simple_shift():
    img_ref = make_gaussian_image(20, 20)
    img_new = make_gaussian_image(22, 18)  # dx = +2, dy = -2

    dy, dx = measure_shift_integer(img_ref, img_new)

    # Allow exact equality here because this is a simple synthetic case
    assert (dx, dy) == (2, -2)
