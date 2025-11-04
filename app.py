"""Command-line tool for estimating US ring size from a photo."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from ring_sizer.image_measurement import MeasurementSession
from ring_sizer.reference_objects import (
    ReferenceObject,
    SUPPORTED_REFERENCE_OBJECTS,
    describe_reference_objects,
)
from ring_sizer.ring_chart import diameter_to_ring_size


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to the hand photo to analyse.")
    parser.add_argument(
        "--reference",
        choices=[*SUPPORTED_REFERENCE_OBJECTS.keys(), "custom_ruler"],
        default="quarter",
        help="Reference object present in the image.",
    )
    parser.add_argument(
        "--custom-length-mm",
        type=float,
        default=None,
        help=(
            "Length in millimetres of the ruler segment selected when using the "
            "'custom_ruler' reference."
        ),
    )
    return parser.parse_args()


def _resolve_reference(reference_key: str, custom_length: Optional[float]) -> ReferenceObject:
    if reference_key == "custom_ruler":
        if custom_length is None or custom_length <= 0:
            raise SystemExit(
                "When using 'custom_ruler' you must provide --custom-length-mm > 0."
            )
        return ReferenceObject(
            name="Custom Ruler Segment",
            known_mm=custom_length,
            instructions=(
                "Click the start and end of the ruler segment whose length you provided."
            ),
        )

    return SUPPORTED_REFERENCE_OBJECTS[reference_key]


def main() -> None:
    args = _parse_args()
    reference = _resolve_reference(args.reference, args.custom_length_mm)

    print(describe_reference_objects())
    print()
    print(f"Selected reference object: {reference.name} ({reference.known_mm:.2f} mm)")
    print(reference.instructions)

    session = MeasurementSession(args.image)
    result = session.measure(reference, reference.instructions)

    ring_entry = diameter_to_ring_size(result.finger_diameter_mm)
    circumference = ring_entry.circumference_mm

    print("\nResults")
    print("-------")
    print(f"Finger diameter: {result.finger_diameter_mm:.2f} mm")
    print(f"Estimated ring size (US): {ring_entry.size:.2f}")
    print(f"Equivalent inner circumference: {circumference:.2f} mm")
    print(f"Pixels per millimetre: {1 / result.mm_per_pixel:.4f}")


if __name__ == "__main__":
    main()
