from ring_sizer.ring_chart import RING_SIZE_CHART, diameter_to_ring_size


def test_ring_chart_is_sorted():
    diameters = [entry.diameter_mm for entry in RING_SIZE_CHART]
    assert diameters == sorted(diameters)


def test_interpolation_between_sizes():
    # Midpoint between size 6 (16.51 mm) and 6.5 (16.92 mm)
    diameter = (16.51 + 16.92) / 2
    result = diameter_to_ring_size(diameter)
    assert abs(result.size - 6.25) < 1e-6
    assert abs(result.diameter_mm - diameter) < 1e-6
