# ASTC Encoder/Decoder

A Python-based command-line tool for ASTC texture compression and decompression. ASTC (Adaptive Scalable Texture Compression) is a lossy texture compression format that supports a wide range of block sizes to control the compression ratio and quality.

## Features

- Compress/decompress images using configurable 2D and 3D block sizes
- Support for different color profiles (linear, sRGB)
- Generate quality metrics (PSNR, SSIM) to evaluate compression
- Simple command-line interface

## Installation

```bash
# Install dependencies
pip install numpy pillow scipy scikit-image opencv-python
```

## Usage

### Compress an image to ASTC format

```bash
python astc.py compress input.png output.astc --block-size 4x4 --color-profile srgb --quality 75
```

### Decompress an ASTC file to image

```bash
python astc.py decompress input.astc output.png --color-profile srgb
```

### Test compression quality

```bash
python astc.py test input.png --block-size 6x6 --output test_output.png
```

## Block Sizes

Supported 2D block sizes: `4x4`, `5x4`, `5x5`, `6x5`, `6x6`, `8x5`, `8x6`, `8x8`, `10x5`, `10x6`, `10x8`, `10x10`, `12x10`, `12x12`

Supported 3D block sizes: `3x3x3`, `4x3x3`, `4x4x3`, `4x4x4`, `5x4x4`, `5x5x4`, `5x5x5`, `6x5x5`, `6x6x5`, `6x6x6`

Smaller block sizes provide better quality but lower compression, while larger block sizes increase compression at the cost of quality.

## Example Results

For a test pattern image (256×256 RGBA):

| Block Size | PSNR (dB) | SSIM    | Compression Ratio |
|------------|-----------|---------|-------------------|
| 4x4        | 24.23     | 0.9460  | 0.02x            |
| 6x6        | 17.00     | 0.7758  | 0.05x            |
| 8x8        | 18.52     | 0.8976  | 0.09x            |
| 12x12      | 13.23     | 0.6748  | 0.19x            |

## Implementation Notes

- Pure Python implementation with optional Cython optimizations
- Simplified encoding/decoding that focuses on the core principles of ASTC
- Support for both 2D and 3D textures

## Project Structure

- `astc.py`: Main entry point
- `astc_encoder/cli.py`: Command-line interface
- `astc_encoder/encoder.py`: Image compression functions
- `astc_encoder/decoder.py`: Image decompression functions
- `astc_encoder/core.py`: Core ASTC algorithms
- `astc_encoder/utils.py`: Utility functions
- `astc_encoder/metrics.py`: Quality metrics
- `astc_encoder/color_profiles.py`: Color profile conversions
- `astc_encoder/optimizations.pyx`: Optional Cython optimizations (if available)
