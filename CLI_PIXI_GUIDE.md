# VesselExpress CLI and Pixi Guide

This guide explains how to use VesselExpress with the CLI interface and Pixi package manager, including support for NIfTI files.

## Table of Contents
- [Installation with Pixi](#installation-with-pixi)
- [Using the CLI](#using-the-cli)
- [Working with NIfTI Files](#working-with-nifti-files)
- [Configuration](#configuration)
- [Examples](#examples)

## Installation with Pixi

[Pixi](https://prefix.dev/) is a fast, modern package manager built on top of conda. It provides reproducible environments and fast dependency resolution.

### 1. Install Pixi

```bash
# Linux and macOS
curl -fsSL https://pixi.sh/install.sh | bash

# Or using Homebrew (macOS)
brew install pixi

# Windows
iwr -useb https://pixi.sh/install.ps1 | iex
```

### 2. Clone and Setup VesselExpress

```bash
git clone https://github.com/farhad-99/VesselExpress.git
cd VesselExpress
```

### 3. Install Dependencies with Pixi

Pixi will automatically read the `pixi.toml` file and create an isolated environment:

```bash
# Install all dependencies
pixi install

# Activate the environment
pixi shell
```

### 4. Alternative: Use Pixi Tasks

You can run VesselExpress directly using pixi tasks without manually activating the environment:

```bash
# Run with all cores
pixi run run

# Run with specific number of cores
CORES=4 pixi run run-cores
```

## Using the CLI

VesselExpress now includes a simplified command-line interface that makes it easy to process vessel images.

### Basic Usage

```bash
# Activate pixi environment first
pixi shell

# Run VesselExpress on an image
python vesselexpress_cli.py -i /path/to/your/image.tiff
```

### CLI Options

```
-i, --input    : Input image file (required)
                 Supported formats: TIFF (.tif, .tiff), PNG (.png), JPG (.jpg), 
                 NIfTI (.nii, .nii.gz)

-c, --config   : Configuration JSON file (optional)
                 Default: uses VesselExpress/data/config.json

-o, --output   : Output directory (optional)
                 Default: VesselExpress/data

--cores        : Number of CPU cores to use (optional)
                 Default: all available cores

--dry-run      : Perform a dry run to see what would be executed
                 No files are processed

--verbose      : Show verbose output and commands

--info         : Show information about the input file
                 Useful for NIfTI files to see pixel dimensions
```

### Examples

```bash
# Process a TIFF file with default settings
python vesselexpress_cli.py -i sample.tiff

# Process with custom configuration
python vesselexpress_cli.py -i sample.tiff -c my_config.json

# Use 4 cores with verbose output
python vesselexpress_cli.py -i sample.tiff --cores 4 --verbose

# Dry run to see the pipeline steps
python vesselexpress_cli.py -i sample.tiff --dry-run

# Process a NIfTI file
python vesselexpress_cli.py -i brain_vessels.nii.gz

# Check NIfTI file information
python vesselexpress_cli.py -i brain_vessels.nii.gz --info
```

## Working with NIfTI Files

NIfTI (Neuroimaging Informatics Technology Initiative) is a common medical imaging format. VesselExpress now supports both `.nii` and `.nii.gz` (compressed) files.

### Automatic Conversion

When you provide a NIfTI file as input, VesselExpress automatically:
1. Converts it to TIFF format for processing
2. Extracts pixel dimensions from the NIfTI header
3. Saves metadata for reference

### Getting NIfTI File Information

Before processing, you can check the NIfTI file's properties:

```bash
python vesselexpress_cli.py -i brain_vessels.nii.gz --info
```

This shows:
- Image dimensions (shape)
- Data type
- Pixel dimensions (spacing)
- Suggested configuration for pixel_dimensions

### Configuring for NIfTI Files

NIfTI files include pixel dimension metadata. Use the `--info` command to get the correct values:

```bash
python vesselexpress_cli.py -i your_file.nii.gz --info
```

Output example:
```
NIfTI File Information:
  File: brain_vessels.nii.gz
  Shape: (100, 512, 512)
  Data type: float32
  Pixel dimensions (z,y,x): 2.0,0.5,0.5

  Note: Add this to your config.json:
    "graphAnalysis": {"pixel_dimensions": "2.0,0.5,0.5", ...}
```

Then update your `config.json`:

```json
{
  "graphAnalysis": {
    "pixel_dimensions": "2.0,0.5,0.5",
    ...
  }
}
```

### Manual NIfTI to TIFF Conversion

You can also manually convert NIfTI files:

```bash
cd VesselExpress/workflow/scripts
python nifti_utils.py -i /path/to/file.nii.gz -o /path/to/output.tiff
```

## Configuration

### Default Configuration

VesselExpress uses `VesselExpress/data/config.json` for default settings. You can:
1. Edit this file directly
2. Create a custom config and use `-c` flag
3. Copy and modify the example: `config_standard.json`

### Key Configuration Parameters

```json
{
  "3D": 1,                    // 1 for 3D images, 0 for 2D
  "render": 0,                // Enable 3D rendering (requires Blender)
  "segmentation": "segmentation3D",  // Segmentation method
  
  "segmentation3D": {
    "smoothing": 1,
    "core_threshold": 3.0,
    ...
  },
  
  "graphAnalysis": {
    "pixel_dimensions": "2.0,1.015625,1.015625",  // z,y,x spacing
    "pruning_scale": 1.5,
    ...
  }
}
```

### Important Notes for NIfTI Files

1. **Pixel Dimensions**: Always update `pixel_dimensions` based on your NIfTI file's spacing
2. **3D Processing**: NIfTI files are typically 3D, so ensure `"3D": 1` in config
3. **Data Type**: The conversion handles float32/float64 by normalizing to uint16

## Complete Workflow Example

Here's a complete example processing a NIfTI file:

```bash
# 1. Install Pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# 2. Clone and setup VesselExpress
git clone https://github.com/farhad-99/VesselExpress.git
cd VesselExpress

# 3. Install dependencies
pixi install

# 4. Activate environment
pixi shell

# 5. Check your NIfTI file
python vesselexpress_cli.py -i /path/to/brain_vessels.nii.gz --info

# 6. Update config.json with correct pixel_dimensions
# (Edit VesselExpress/data/config.json or create custom config)

# 7. Process the file
python vesselexpress_cli.py -i /path/to/brain_vessels.nii.gz --cores 4 --verbose

# 8. Find results in VesselExpress/data/
ls VesselExpress/data/
```

## Output Files

After processing, you'll find in the output directory:

- `Binary_[filename].tiff` - Segmented vessel image
- `Skeleton_[filename].tiff` - Skeletonized vessels
- `[filename].tiff_Segment_Statistics.csv` - Segment analysis
- `[filename].tiff_Filament_Statistics.csv` - Filament metrics
- `[filename].tiff_BranchesPerBranchPt.csv` - Branching information
- `[filename]_nifti_metadata.txt` - Original NIfTI metadata (if input was NIfTI)

## Troubleshooting

### Pixi Installation Issues

If `pixi install` fails:
```bash
# Try updating pixi
pixi self-update

# Or clear cache
pixi clean
```

### Memory Issues

For large images, use fewer cores:
```bash
python vesselexpress_cli.py -i large_image.nii.gz --cores 2
```

Or enable small RAM mode in config.json:
```json
{
  "small_RAM_mode": 1
}
```

### NIfTI Conversion Issues

If automatic conversion fails:
```bash
# Manual conversion
cd VesselExpress/workflow/scripts
python nifti_utils.py -i your_file.nii.gz

# Then process the TIFF
cd ../../..
python vesselexpress_cli.py -i VesselExpress/workflow/scripts/your_file.tiff
```

## Additional Resources

- [VesselExpress Wiki](https://github.com/RUB-Bioinf/VesselExpress/wiki)
- [Pixi Documentation](https://prefix.dev/docs/pixi/overview)
- [NIfTI Format](https://nifti.nimh.nih.gov/)
- [Snakemake Documentation](https://snakemake.readthedocs.io/)
