# NIfTI Workflow Example

This document demonstrates a complete workflow for processing NIfTI files with VesselExpress.

## Example 1: Basic NIfTI Processing

### Step 1: Prepare Your Environment

```bash
# Install Pixi if not already installed
curl -fsSL https://pixi.sh/install.sh | bash

# Clone VesselExpress
git clone https://github.com/farhad-99/VesselExpress.git
cd VesselExpress

# Install dependencies
pixi install

# Activate the environment
pixi shell
```

### Step 2: Inspect Your NIfTI File

Before processing, check your NIfTI file's properties:

```bash
python vesselexpress_cli.py -i /path/to/brain_vessels.nii.gz --info
```

Example output:
```
NIfTI File Information:
  File: brain_vessels.nii.gz
  Shape: (128, 512, 512)
  Data type: float32
  Pixel dimensions (z,y,x): 2.0,0.5,0.5

  Note: Add this to your config.json:
    "graphAnalysis": {"pixel_dimensions": "2.0,0.5,0.5", ...}
```

### Step 3: Update Configuration

Create or edit a configuration file:

```bash
cp VesselExpress/data/config.json my_config.json
```

Edit `my_config.json` and update the pixel dimensions:

```json
{
  "imgFolder": "data",
  "segmentation": "segmentation3D",
  "3D": 1,
  "render": 0,
  "marching_cubes": 0,
  "small_RAM_mode": 0,
  
  "segmentation3D": {
    "smoothing": 1,
    "core_threshold": 3.0,
    "core_vessel_1": 1,
    "gamma_1": 5,
    "sigma_1": 1.0,
    "cutoff_method_1": "threshold_triangle",
    "core_vessel_2": 1,
    "gamma_2": 5,
    "sigma_2": 2.0,
    "cutoff_method_2": "threshold_li",
    "post_closing": 5,
    "post_thinning": 1,
    "thin": 1,
    "min_thickness": 1,
    "post_cleaning": 100
  },
  
  "graphAnalysis": {
    "pixel_dimensions": "2.0,0.5,0.5",  // ← Updated from --info output
    "pruning_scale": 1.5,
    "length_limit": 3,
    "diameter_scale": 2,
    "branching_threshold": 0.25,
    "extended_output": 1,
    "experimental_flag": 0,
    "remove_border_end_pts": 1,
    "remove_end_pts_from_small_filaments": 1,
    "seg_interpolate": 0,
    "spline_degree": 3,
    "cut_neighbor_brpt_segs": 1
  }
}
```

### Step 4: Process the NIfTI File

```bash
python vesselexpress_cli.py -i /path/to/brain_vessels.nii.gz -c my_config.json --cores 4 --verbose
```

### Step 5: Review Results

After processing completes, find results in `VesselExpress/data/`:

```bash
cd VesselExpress/data/brain_vessels/
ls -lh
```

Expected output files:
- `brain_vessels.tiff` - Converted input
- `Binary_brain_vessels.tiff` - Segmented vessels
- `Skeleton_brain_vessels.tiff` - Skeletonized vessels
- `brain_vessels.tiff_Segment_Statistics.csv` - Vessel segment metrics
- `brain_vessels.tiff_Filament_Statistics.csv` - Filament analysis
- `brain_vessels.tiff_BranchesPerBranchPt.csv` - Branch point data
- `brain_vessels_nifti_metadata.txt` - Original NIfTI metadata

## Example 2: Batch Processing Multiple NIfTI Files

If you have multiple NIfTI files to process:

### Option A: Process Files Sequentially

```bash
#!/bin/bash
for file in /path/to/nifti_files/*.nii.gz; do
    echo "Processing: $file"
    python vesselexpress_cli.py -i "$file" -c my_config.json --cores 4
done
```

### Option B: Use Snakemake Directly

Place all `.nii.gz` files in `VesselExpress/data/`:

```bash
cp /path/to/nifti_files/*.nii.gz VesselExpress/data/
cd VesselExpress
snakemake --use-conda --cores all --conda-frontend conda --snakefile ./workflow/Snakefile
```

## Example 3: Processing with Limited Memory

For large NIfTI files on systems with limited RAM:

Update config to enable small RAM mode:

```json
{
  "small_RAM_mode": 1,
  ...
}
```

Then run with fewer cores:

```bash
python vesselexpress_cli.py -i large_brain.nii.gz -c my_config.json --cores 2
```

## Common NIfTI File Sources

### Medical Imaging

NIfTI files are commonly used in medical imaging:

- **Brain imaging**: MRI, fMRI, CT scans
- **Angiography**: MRA (Magnetic Resonance Angiography)
- **Light-sheet microscopy**: 3D tissue imaging

### Converting Other Formats to NIfTI

If you have DICOM files:

```bash
# Using dcm2niix (install separately)
dcm2niix -o output_dir input_dicom_dir/
```

## Tips for NIfTI Processing

### 1. Check Orientation

NIfTI files store orientation information. If your results look wrong:

```python
import nibabel as nib
img = nib.load('your_file.nii.gz')
print(img.header.get_best_affine())
```

### 2. Normalize Intensity

Some NIfTI files have unusual intensity ranges. The converter normalizes to uint16 automatically, but you can adjust in the segmentation config.

### 3. Pixel Dimensions Matter

Always use the `--info` flag first to get correct pixel dimensions. Incorrect dimensions lead to:
- Wrong vessel diameter measurements
- Incorrect branch detection
- Invalid volume calculations

### 4. Memory Usage

NIfTI files can be large. Monitor memory:

```bash
# Check file size first
ls -lh your_file.nii.gz

# For files > 1GB, use small_RAM_mode
```

## Troubleshooting NIfTI Processing

### Issue: Conversion fails

```bash
# Check nibabel installation
python -c "import nibabel; print(nibabel.__version__)"

# If missing:
pip install nibabel
```

### Issue: Wrong orientation

The automatic converter doesn't reorient. If needed, use medical imaging tools:

```bash
# Using FSL (install separately)
fslreorient2std input.nii.gz output.nii.gz
```

### Issue: Segmentation quality

Adjust segmentation parameters:

```json
{
  "segmentation3D": {
    "smoothing": 2,          // Increase for noisy data
    "core_threshold": 2.5,    // Lower for more vessels
    "gamma_1": 3,            // Adjust sensitivity
    "sigma_1": 1.5,          // Change scale
    ...
  }
}
```

## Next Steps

- Visualize results with [Napari plugin](https://www.napari-hub.org/plugins/vessel-express-napari)
- Tune parameters using example data from [Zenodo](https://zenodo.org/record/5733150)
- Read the [full documentation](https://github.com/RUB-Bioinf/VesselExpress/wiki)

## Additional Resources

- [NIfTI Format Specification](https://nifti.nimh.nih.gov/)
- [Nibabel Documentation](https://nipy.org/nibabel/)
- [VesselExpress Parameters Guide](https://github.com/RUB-Bioinf/VesselExpress/wiki/Parameters-for-VesselExpress)
