"""Conversion utilities between physical measurements and US ring sizes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple


@dataclass(frozen=True)
class RingSizeEntry:
    """Mapping between a ring size and its inner diameter and circumference."""

    size: float
    diameter_mm: float

    @property
    def circumference_mm(self) -> float:
        from math import pi

        return self.diameter_mm * pi


RING_SIZE_CHART: Tuple[RingSizeEntry, ...] = tuple(
    RingSizeEntry(size, diameter)
    for size, diameter in [
        (1.0, 12.37),
        (1.5, 12.76),
        (2.0, 13.06),
        (2.5, 13.46),
        (3.0, 14.07),
        (3.5, 14.48),
        (4.0, 14.86),
        (4.5, 15.27),
        (5.0, 15.70),
        (5.5, 16.10),
        (6.0, 16.51),
        (6.5, 16.92),
        (7.0, 17.32),
        (7.5, 17.73),
        (8.0, 18.14),
        (8.5, 18.54),
        (9.0, 18.95),
        (9.5, 19.35),
        (10.0, 19.76),
        (10.5, 20.17),
        (11.0, 20.57),
        (11.5, 20.98),
        (12.0, 21.39),
        (12.5, 21.79),
        (13.0, 22.20),
        (13.5, 22.61),
        (14.0, 23.01),
        (14.5, 23.42),
        (15.0, 23.83),
    ]
)
"""Lookup table derived from the ISO 8653:2016 standard."""


def _interpolate_ring_size(diameter_mm: float) -> float:
    """Linearly interpolate the ring size for a given diameter."""

    entries: List[RingSizeEntry] = list(RING_SIZE_CHART)
    if diameter_mm <= entries[0].diameter_mm:
        return entries[0].size
    if diameter_mm >= entries[-1].diameter_mm:
        return entries[-1].size

    for lower, upper in zip(entries, entries[1:]):
        if lower.diameter_mm <= diameter_mm <= upper.diameter_mm:
            span = upper.diameter_mm - lower.diameter_mm
            if span == 0:
                return lower.size
            fraction = (diameter_mm - lower.diameter_mm) / span
            return lower.size + fraction * (upper.size - lower.size)

    # Fallback, although the loop should always return before this point.
    return entries[-1].size


def diameter_to_ring_size(diameter_mm: float) -> RingSizeEntry:
    """Return the closest ring size entry for the given diameter.

    The returned entry uses linear interpolation and reports the interpolated
    diameter while keeping the circumference consistent with the interpolated
    size.
    """

    interpolated_size = _interpolate_ring_size(diameter_mm)
    return RingSizeEntry(size=interpolated_size, diameter_mm=diameter_mm)


__all__ = ["RingSizeEntry", "RING_SIZE_CHART", "diameter_to_ring_size"]
