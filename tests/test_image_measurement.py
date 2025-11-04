from ring_sizer.image_measurement import compute_scale_from_reference
from ring_sizer.reference_objects import ReferenceObject


def test_compute_scale_from_reference():
    reference = ReferenceObject(
        name="Test",
        known_mm=10.0,
        instructions="",
    )
    scale = compute_scale_from_reference(reference, 20.0)
    assert scale == 0.5


def test_compute_scale_from_reference_requires_positive_distance():
    reference = ReferenceObject(
        name="Test",
        known_mm=10.0,
        instructions="",
    )
    try:
        compute_scale_from_reference(reference, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for zero distance")
