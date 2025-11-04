"""Metadata for supported reference objects."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReferenceObject:
    """Representation of a physical object that can be used for scaling.

    Attributes
    ----------
    name:
        Human-friendly name of the object.
    known_mm:
        The physical length in millimetres that corresponds to the user-selected
        measurement on the object.
    instructions:
        Text that explains how the object should be measured in the photo.
    """

    name: str
    known_mm: float
    instructions: str


SUPPORTED_REFERENCE_OBJECTS: Dict[str, ReferenceObject] = {
    "quarter": ReferenceObject(
        name="US Quarter",
        known_mm=24.26,
        instructions=(
            "Click the leftmost and rightmost edges of the quarter so the "
            "selection spans its diameter."
        ),
    ),
    "credit_card": ReferenceObject(
        name="Credit Card (ISO/IEC 7810 ID-1)",
        known_mm=85.6,
        instructions=(
            "Click the leftmost and rightmost edges of the card so the "
            "selection spans its width."
        ),
    ),
}
"""Lookup of built-in reference objects keyed by identifier."""


def describe_reference_objects() -> str:
    """Return a formatted description of supported reference objects."""

    lines = ["Supported reference objects:"]
    for key, obj in SUPPORTED_REFERENCE_OBJECTS.items():
        lines.append(f"- {key}: {obj.name} ({obj.known_mm:.2f} mm)")
    lines.append(
        "- custom_ruler: Use a ruler segment. You will be prompted to enter its length."
    )
    return "\n".join(lines)


__all__ = ["ReferenceObject", "SUPPORTED_REFERENCE_OBJECTS", "describe_reference_objects"]
