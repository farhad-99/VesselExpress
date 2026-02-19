# Summary of Changes for Pixi and NIfTI Support

This document summarizes the changes made to VesselExpress to add Pixi compatibility and NIfTI file support.

## Files Added

### 1. `pixi.toml`
- Main Pixi configuration file
- Defines project dependencies (Python, Snakemake, scientific packages)
- Includes nibabel for NIfTI support
- Defines tasks for running VesselExpress
- Supports multiple platforms (Linux, macOS, macOS ARM)

### 2. `vesselexpress_cli.py`
- New command-line interface wrapper
- Simplifies VesselExpress usage
- Features:
  - Automatic workspace setup
  - Support for all image formats (TIFF, PNG, JPG, NIfTI)
  - Configuration file management
  - NIfTI file information display
  - Dry-run capability
  - Flexible core count specification

### 3. `VesselExpress/workflow/scripts/nifti_utils.py`
- NIfTI file handling utilities
- Functions:
  - `load_nifti()`: Load NIfTI files
  - `nifti_to_tiff()`: Convert NIfTI to TIFF
  - `get_pixel_dimensions_from_nifti()`: Extract spacing information
- Automatically normalizes float data to uint16
- Saves metadata for reference

### 4. Documentation Files

#### `CLI_PIXI_GUIDE.md`
Comprehensive guide covering:
- Pixi installation and setup
- CLI usage instructions
- NIfTI file workflow
- Configuration tips
- Troubleshooting

#### `NIFTI_WORKFLOW.md`
Detailed NIfTI workflow examples:
- Basic NIfTI processing
- Batch processing
- Memory-constrained processing
- Common NIfTI sources
- Troubleshooting specific to NIfTI

#### `CLI_QUICKREF.md`
Quick reference with:
- Common commands
- File format table
- Configuration snippets
- Output file descriptions
- Performance tips

## Files Modified

### 1. `VesselExpress/workflow/Snakefile`
**Modified function: `get_files_and_extensions()`**

Changes:
- Added support for `.nii` and `.nii.gz` file extensions
- Automatic NIfTI to TIFF conversion during file discovery
- Proper handling of `.nii.gz` double extension
- Imports and uses `nifti_utils` for conversion

### 2. `README.md`
**Added new section: "CLI Version with Pixi (Recommended for Local Use)"**

Additions:
- Quick start guide for Pixi
- List of supported file formats including NIfTI
- CLI usage examples
- Link to detailed documentation
- Positioned before "Local Version" section

### 3. `.gitignore`
**Added Pixi-related entries:**
- `.pixi/` - Pixi environment directory
- `pixi.lock` - Pixi lock file (optional, could be committed for reproducibility)

## Feature Summary

### Pixi Support
✅ Full Pixi integration with `pixi.toml`
✅ Conda and PyPI dependencies properly configured
✅ Pixi tasks for running VesselExpress
✅ Cross-platform support (Linux, macOS)

### CLI Enhancement
✅ User-friendly command-line interface
✅ Automatic workspace management
✅ Configuration file handling
✅ Progress reporting and verbose output
✅ Dry-run capability

### NIfTI Support
✅ Native `.nii` and `.nii.gz` file support
✅ Automatic format conversion
✅ Pixel dimension extraction
✅ Metadata preservation
✅ Float to uint16 normalization

## Usage Examples

### Using Pixi

```bash
# Install dependencies
pixi install

# Activate environment
pixi shell

# Run VesselExpress
python vesselexpress_cli.py -i image.nii.gz
```

### Using CLI

```bash
# Basic usage
python vesselexpress_cli.py -i vessels.nii.gz

# With configuration
python vesselexpress_cli.py -i vessels.nii.gz -c config.json --cores 4

# Check file info
python vesselexpress_cli.py -i vessels.nii.gz --info
```

### Processing Workflow

1. Check NIfTI metadata: `python vesselexpress_cli.py -i file.nii.gz --info`
2. Update config.json with correct pixel_dimensions
3. Process: `python vesselexpress_cli.py -i file.nii.gz -c config.json`
4. Results appear in `VesselExpress/data/`

## Technical Details

### NIfTI Conversion
- Converts NIfTI volumes to TIFF for processing
- Handles both uncompressed (.nii) and compressed (.nii.gz)
- Normalizes intensity values to uint16 range
- Preserves original metadata in text file
- Extracts and reports pixel dimensions

### Pixi Integration
- Uses conda-forge and defaults channels
- Manages both conda and PyPI packages
- Creates isolated, reproducible environments
- Faster than traditional conda/mamba
- Cross-platform compatibility

### Backward Compatibility
- All existing functionality preserved
- Docker workflows unaffected
- Snakemake direct usage still supported
- Web interface unchanged

## Testing Recommendations

Before deploying, test:

1. **Pixi installation**: `pixi install` in repository
2. **CLI help**: `python vesselexpress_cli.py --help`
3. **NIfTI info**: With sample `.nii.gz` file
4. **TIFF processing**: Existing workflow should work
5. **Dry run**: `--dry-run` flag verification

## Future Enhancements

Potential additions:
- Direct integration with neuroimaging libraries (nilearn, etc.)
- Support for additional medical imaging formats (DICOM, etc.)
- GUI for parameter tuning
- Cloud processing integration
- Pre-built Pixi binary distributions

## Dependencies Added

### Core (via Pixi/conda)
- numpy, scipy, scikit-image
- pandas, matplotlib, networkx
- pillow, tifffile, imageio
- pyyaml, dask

### PyPI packages
- aicsimageio, aicssegmentation
- numpy-stl, dask-image
- **nibabel** (for NIfTI)
- itk, itk-io
- geomdl, zarr, xarray

## Documentation Structure

```
VesselExpress/
├── README.md                    # Updated with Pixi section
├── pixi.toml                    # Pixi configuration
├── vesselexpress_cli.py         # CLI wrapper
├── CLI_PIXI_GUIDE.md           # Comprehensive guide
├── CLI_QUICKREF.md             # Quick reference
├── NIFTI_WORKFLOW.md           # NIfTI examples
└── VesselExpress/
    └── workflow/
        ├── Snakefile            # Modified for NIfTI
        └── scripts/
            └── nifti_utils.py   # NIfTI utilities
```

## Backward Compatibility

All changes are backward compatible:
- Existing TIFF/PNG/JPG workflows unchanged
- Docker images not affected
- Snakemake direct usage preserved
- Configuration files compatible
- No breaking changes to APIs

## Migration Path

For existing users:
1. Optional: Install Pixi (`curl -fsSL https://pixi.sh/install.sh | bash`)
2. Optional: Use new CLI (`python vesselexpress_cli.py`)
3. Continue using existing workflows if preferred
4. NIfTI support available but not required

## Conclusion

These changes add modern package management (Pixi), a user-friendly CLI, and NIfTI support while maintaining full backward compatibility with existing VesselExpress workflows.
