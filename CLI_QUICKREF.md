# VesselExpress CLI Quick Reference

Quick reference guide for the VesselExpress command-line interface.

## Installation

```bash
# Install Pixi
curl -fsSL https://pixi.sh/install.sh | bash

# Setup VesselExpress
git clone https://github.com/farhad-99/VesselExpress.git
cd VesselExpress
pixi install
pixi shell
```

## Basic Commands

```bash
# Process an image with defaults
python vesselexpress_cli.py -i image.tiff

# Process with custom config
python vesselexpress_cli.py -i image.tiff -c config.json

# Specify output directory
python vesselexpress_cli.py -i image.tiff -o /path/to/output

# Use specific number of cores
python vesselexpress_cli.py -i image.tiff --cores 4

# Dry run (preview without executing)
python vesselexpress_cli.py -i image.tiff --dry-run

# Verbose output
python vesselexpress_cli.py -i image.tiff --verbose
```

## NIfTI-Specific Commands

```bash
# Check NIfTI file information
python vesselexpress_cli.py -i brain.nii.gz --info

# Process NIfTI file
python vesselexpress_cli.py -i brain.nii.gz -c config.json

# Process compressed NIfTI
python vesselexpress_cli.py -i vessels.nii.gz
```

## File Format Support

| Format | Extension | Notes |
|--------|-----------|-------|
| TIFF | `.tif`, `.tiff` | Recommended for 3D |
| PNG | `.png` | 2D images |
| JPG | `.jpg` | 2D images |
| NIfTI | `.nii`, `.nii.gz` | Medical imaging |

## Common Workflows

### 3D Volume Analysis

```bash
# 1. Check NIfTI metadata
python vesselexpress_cli.py -i volume.nii.gz --info

# 2. Update config.json with correct pixel_dimensions

# 3. Process
python vesselexpress_cli.py -i volume.nii.gz --cores 8 --verbose
```

### 2D Image Analysis

```bash
# Edit config.json: set "3D": 0
python vesselexpress_cli.py -i slice.png -c config_2d.json
```

### Batch Processing

```bash
# Process all TIFF files in a directory
for f in /path/to/images/*.tiff; do
    python vesselexpress_cli.py -i "$f" --cores 4
done
```

## Configuration Tips

### Minimal config.json for NIfTI

```json
{
  "3D": 1,
  "render": 0,
  "segmentation": "segmentation3D",
  "graphAnalysis": {
    "pixel_dimensions": "2.0,0.5,0.5"
  }
}
```

### Adjust for noisy data

```json
{
  "segmentation3D": {
    "smoothing": 2,
    "core_threshold": 2.5
  }
}
```

### Memory-constrained systems

```json
{
  "small_RAM_mode": 1
}
```

## Output Files

After processing `image.tiff`, expect:

```
VesselExpress/data/image/
├── image.tiff                              # Original (or converted from NIfTI)
├── Binary_image.tiff                       # Segmented vessels
├── Skeleton_image.tiff                     # Skeletonized vessels
├── image.tiff_Segment_Statistics.csv       # Segment metrics
├── image.tiff_Filament_Statistics.csv      # Filament data
├── image.tiff_BranchesPerBranchPt.csv     # Branch analysis
└── image_nifti_metadata.txt               # NIfTI metadata (if input was NIfTI)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pixi install` and `pixi shell` |
| Out of memory | Use `--cores 2` or set `"small_RAM_mode": 1` |
| Wrong pixel dimensions | Use `--info` flag to get correct values |
| Slow processing | Increase `--cores` value |
| NIfTI conversion fails | Check `pip install nibabel` |

## Performance Tips

1. **Use all cores for faster processing**:
   ```bash
   python vesselexpress_cli.py -i image.tiff --cores all
   ```

2. **Process smaller test region first**:
   - Crop your image to a small test region
   - Tune parameters
   - Then process full image

3. **Monitor resources**:
   ```bash
   # In another terminal
   htop
   ```

## Getting Help

```bash
# CLI help
python vesselexpress_cli.py --help

# View documentation
cat CLI_PIXI_GUIDE.md
cat NIFTI_WORKFLOW.md

# Check NIfTI file
python vesselexpress_cli.py -i file.nii.gz --info
```

## Advanced Usage

### Using Pixi Tasks

```bash
# Run with Pixi task (from project root)
pixi run run

# With specific cores
CORES=4 pixi run run-cores
```

### Direct Snakemake

```bash
cd VesselExpress
snakemake --use-conda --cores 8 --snakefile ./workflow/Snakefile --verbose
```

### Manual NIfTI Conversion

```bash
cd VesselExpress/workflow/scripts
python nifti_utils.py -i input.nii.gz -o output.tiff
```

## Links

- 📖 [Full CLI & Pixi Guide](CLI_PIXI_GUIDE.md)
- 💉 [NIfTI Workflow Examples](NIFTI_WORKFLOW.md)
- 🌐 [VesselExpress Wiki](https://github.com/RUB-Bioinf/VesselExpress/wiki)
- 🐍 [Pixi Documentation](https://prefix.dev/docs/pixi/overview)
