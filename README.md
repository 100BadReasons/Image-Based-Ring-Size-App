# Image-Based Ring Size App

This project provides a lightweight Python application that estimates a person's ring size from a photo of their hand placed next to a reference object. The workflow is intentionally simple so it can run on most laptops without additional dependencies beyond `matplotlib`.

## Features

- Supports multiple reference objects with known physical dimensions (US quarter, credit card) and custom ruler segments.
- Interactive point selection directly on the photo to capture the reference object and finger width.
- Converts the measured finger diameter into a US ring size using data based on the ISO 8653:2016 standard.
- Outputs millimetre measurements for transparency.

## Requirements

- Python 3.9+
- `matplotlib`

Install the dependency with:

```bash
pip install matplotlib
```

## Usage

1. Capture or upload a clear photo of the hand with one of the supported reference objects in the same plane as the finger.
2. Run the CLI, pointing it at the image and indicating which reference object is present. For example:

```bash
python app.py path/to/photo.jpg --reference quarter
```

For a credit card:

```bash
python app.py path/to/photo.jpg --reference credit_card
```

For a custom ruler segment, specify the exact length in millimetres:

```bash
python app.py path/to/photo.jpg --reference custom_ruler --custom-length-mm 20
```

3. A window will open showing the photo. Follow the on-screen prompts:
   - Click the left and right edges of the reference object (e.g., the diameter of the quarter).
   - Click the left and right edges of the finger where the ring will sit.
   - Close the window once the clicks are registered.

4. The console output will display the finger diameter, estimated US ring size, equivalent circumference, and the calculated pixel density.

## How It Works

- The application computes the ratio of millimetres to pixels using the known size of the reference object.
- It then multiplies the pixel distance between the finger edges by this ratio to recover the finger's diameter in millimetres.
- Finally, the diameter is converted to a US ring size through linear interpolation of a standard ring size chart.

## Limitations

- The accuracy depends on the clarity of the photo and how well the reference object is aligned with the finger.
- For best results, ensure the finger and reference object are on the same plane and the photo is taken perpendicular to that plane to minimise perspective distortion.
- The user must click accurately; consider zooming into the image if the default resolution makes precise clicks difficult.

## Testing

The repository ships with a small automated test suite that checks the pixel-to-millimetre conversion helpers and the ring size interpolation logic. To run it locally:

1. *(Optional but recommended)* Create and activate a virtual environment.
2. Install the project dependencies, which also include the testing tools:

   ```bash
   pip install -r requirements.txt
   ```

   > If you are working in an environment without internet access, make sure the required wheels (notably `matplotlib` and `pytest`) are available from a local package index before running the command above.

3. Execute the tests from the repository root:

   ```bash
   python -m pytest
   ```

You should see `pytest` collect the `tests/` directory and report passing results. Any failures will point to the specific helper that needs attention.
