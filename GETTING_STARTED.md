# Getting Started with VesselExpress CLI

This quick start guide will get you up and running with VesselExpress CLI in minutes.

## Prerequisites

- Linux or macOS (Windows users: use Docker or WSL2)
- Python 3.7 or later
- At least 4 GB RAM (8 GB recommended)

## Installation (5 minutes)

### Step 1: Install Pixi

```bash
# One-line installation
curl -fsSL https://pixi.sh/install.sh | bash

# Restart your shell or run:
source ~/.bashrc  # or ~/.zshrc on macOS
```

### Step 2: Get VesselExpress

```bash
git clone https://github.com/farhad-99/VesselExpress.git
cd VesselExpress
```

### Step 3: Install Dependencies

```bash
# This will take a few minutes the first time
pixi install

# Activate the environment
pixi shell
```

That's it! You're ready to process vessel images.

## Quick Start: Process Your First Image

### Example 1: TIFF Image

```bash
# Process a TIFF file with defaults
python vesselexpress_cli.py -i /path/to/your/vessels.tiff

# Results will be in: VesselExpress/data/vessels/
```

### Example 2: NIfTI Image

```bash
# Step 1: Check the file information
python vesselexpress_cli.py -i /path/to/brain.nii.gz --info

# Output shows:
#   Pixel dimensions (z,y,x): 2.0,0.5,0.5
#   Note: Add this to your config.json

# Step 2: Update config (if needed)
# Edit VesselExpress/data/config.json
# Set: "pixel_dimensions": "2.0,0.5,0.5"

# Step 3: Process the file
python vesselexpress_cli.py -i /path/to/brain.nii.gz --cores 4
```

## Understanding the Output

After processing completes, you'll find these files:

```
VesselExpress/data/your_image/
├── your_image.tiff                      # Converted input (if NIfTI)
├── Binary_your_image.tiff               # Segmented vessels
├── Skeleton_your_image.tiff             # Vessel skeleton
├── your_image.tiff_Segment_Statistics.csv     # Segment data
├── your_image.tiff_Filament_Statistics.csv    # Filament metrics
└── your_image.tiff_BranchesPerBranchPt.csv   # Branch analysis
```

### Key Files:

1. **Binary_*.tiff** - Segmented blood vessels (binary mask)
2. **Skeleton_*.tiff** - Vessel centerlines/skeleton
3. **Segment_Statistics.csv** - Detailed measurements per segment
4. **Filament_Statistics.csv** - Per-filament analysis
5. **BranchesPerBranchPt.csv** - Branch point information

## Common Use Cases

### Adjust Processing Quality

```bash
# More thorough (slower)
python vesselexpress_cli.py -i image.tiff --cores 8 --verbose

# Quick preview (faster)
python vesselexpress_cli.py -i image.tiff --cores 2
```

### Use Custom Configuration

```bash
# Copy default config
cp VesselExpress/data/config.json my_config.json

# Edit my_config.json to adjust parameters
# Then run:
python vesselexpress_cli.py -i image.tiff -c my_config.json
```

### Process Multiple Files

```bash
# Create a simple script
for file in /path/to/images/*.nii.gz; do
    echo "Processing: $file"
    python vesselexpress_cli.py -i "$file" --cores 4
done
```

## Troubleshooting

### Out of Memory

```bash
# Use fewer cores
python vesselexpress_cli.py -i image.tiff --cores 2

# Or enable small RAM mode in config.json:
# "small_RAM_mode": 1
```

### Slow Processing

```bash
# Use all available cores
python vesselexpress_cli.py -i image.tiff --cores all

# Or specify exact number
python vesselexpress_cli.py -i image.tiff --cores 8
```

### Module Not Found

```bash
# Make sure you're in the pixi environment
pixi shell

# Or reinstall
pixi install
```

### NIfTI Files Not Converting

```bash
# Check if nibabel is installed
python -c "import nibabel; print('OK')"

# If not, install it:
pip install nibabel
```

## Configuration Guide

### Basic Config for 3D Images

Edit `VesselExpress/data/config.json`:

```json
{
  "3D": 1,
  "render": 0,
  "segmentation": "segmentation3D",
  "graphAnalysis": {
    "pixel_dimensions": "2.0,1.0,1.0"
  }
}
```

### For 2D Images

```json
{
  "3D": 0,
  "segmentation": "segmentation2D"
}
```

### For Noisy Data

```json
{
  "segmentation3D": {
    "smoothing": 2,
    "core_threshold": 2.5
  }
}
```

## Next Steps

### Visualize Results

You can view the output TIFF files with:
- **ImageJ/Fiji** - Free, powerful image viewer
- **Napari** - Modern Python-based viewer
- **VesselExpress Napari Plugin** - Specialized for vessel data

### Analyze Results

The CSV files contain quantitative data:
- Vessel lengths
- Vessel diameters
- Branch point counts
- Network connectivity

Open them in Excel, Python (pandas), or R for analysis.

### Fine-Tune Parameters

Read the parameter guide:
```bash
cat CLI_PIXI_GUIDE.md
```

Or visit the [wiki](https://github.com/RUB-Bioinf/VesselExpress/wiki/Parameters-for-VesselExpress).

## Example Workflow

Here's a complete example workflow:

```bash
# 1. Setup (one time)
curl -fsSL https://pixi.sh/install.sh | bash
git clone https://github.com/farhad-99/VesselExpress.git
cd VesselExpress
pixi install

# 2. Activate environment
pixi shell

# 3. Check your NIfTI file
python vesselexpress_cli.py -i ~/data/brain_vessels.nii.gz --info

# Output:
# Pixel dimensions (z,y,x): 2.0,0.5,0.5

# 4. Update config (optional)
# Edit VesselExpress/data/config.json if needed

# 5. Process
python vesselexpress_cli.py -i ~/data/brain_vessels.nii.gz --cores 4 --verbose

# 6. Check results
ls -lh VesselExpress/data/brain_vessels/

# 7. View with ImageJ or Napari
# fiji VesselExpress/data/brain_vessels/Binary_brain_vessels.tiff
```

## Tips

1. **Start Small**: Test with a small region or low-resolution version first
2. **Monitor Resources**: Use `htop` or Activity Monitor to watch CPU/RAM
3. **Save Configs**: Keep multiple config files for different data types
4. **Document Settings**: Note which parameters work best for your data
5. **Read Docs**: Check the guides in this repository for advanced features

## Getting Help

- **Documentation**: Read `CLI_PIXI_GUIDE.md` for detailed info
- **Examples**: See `NIFTI_WORKFLOW.md` for NIfTI-specific examples
- **Quick Ref**: Use `CLI_QUICKREF.md` for command reference
- **Issues**: Report problems on [GitHub Issues](https://github.com/farhad-99/VesselExpress/issues)

## Resources

- [VesselExpress Wiki](https://github.com/RUB-Bioinf/VesselExpress/wiki)
- [Pixi Documentation](https://prefix.dev/docs/pixi/overview)
- [Example Data](https://zenodo.org/record/5733150)

## Success!

You're now ready to analyze blood vessel networks with VesselExpress. Happy analyzing! 🎉
