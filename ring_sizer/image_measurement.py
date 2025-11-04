"""Utilities for collecting measurements from an image interactively."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from .reference_objects import ReferenceObject

Point = Tuple[float, float]


def _prompt_points(message: str, num_points: int) -> Iterable[Point]:
    """Prompt the user to click a number of points on the displayed image."""

    print(message)
    points = plt.ginput(num_points, timeout=-1)
    if len(points) != num_points:
        raise RuntimeError(
            f"Expected {num_points} points but received {len(points)}. "
            "Close the image window and try again."
        )
    return points


def _distance(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two 2D points."""

    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


@dataclass
class MeasurementResult:
    """Outcome of measuring a finger from an image."""

    finger_diameter_mm: float
    finger_pixels: float
    reference_pixels: float
    mm_per_pixel: float


@dataclass
class MeasurementSession:
    """Interactive session that collects the measurements needed for sizing."""

    image_path: Path

    def _load_image(self):
        return mpimg.imread(self.image_path)

    def _show_image(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(self._load_image())
        ax.set_title("Click the requested points and close the window when done")
        ax.axis("off")
        return fig, ax

    def measure(self, reference: ReferenceObject, reference_message: str) -> MeasurementResult:
        """Run the interactive measurement workflow."""

        fig, ax = self._show_image()
        try:
            ref_points = list(_prompt_points(reference_message, 2))
            reference_pixels = _distance(*ref_points)
            finger_points = list(
                _prompt_points(
                    "Click the two points that represent the left and right edges "
                    "of the finger at the spot where the ring will rest.",
                    2,
                )
            )
            finger_pixels = _distance(*finger_points)
        finally:
            plt.close(fig)

        mm_per_pixel = reference.known_mm / reference_pixels
        finger_diameter_mm = finger_pixels * mm_per_pixel
        return MeasurementResult(
            finger_diameter_mm=finger_diameter_mm,
            finger_pixels=finger_pixels,
            reference_pixels=reference_pixels,
            mm_per_pixel=mm_per_pixel,
        )


def compute_scale_from_reference(reference: ReferenceObject, pixel_distance: float) -> float:
    """Return the conversion factor from pixels to millimetres."""

    if pixel_distance <= 0:
        raise ValueError("Pixel distance must be positive.")
    return reference.known_mm / pixel_distance


__all__ = ["MeasurementSession", "MeasurementResult", "compute_scale_from_reference"]
