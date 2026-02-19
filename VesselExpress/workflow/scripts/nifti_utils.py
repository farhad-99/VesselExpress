"""
Utility functions for handling NIfTI files in VesselExpress pipeline.
Converts NIfTI files to TIFF format for processing.
"""

import numpy as np
import nibabel as nib
from tifffile import imsave
import os
from pathlib import Path


def load_nifti(filepath):
    """
    Load a NIfTI file (.nii or .nii.gz).
    
    Parameters:
    -----------
    filepath : str
        Path to the NIfTI file
        
    Returns:
    --------
    data : np.ndarray
        Image data as numpy array
    affine : np.ndarray
        Affine transformation matrix
    header : nibabel header
        NIfTI header containing metadata
    """
    img = nib.load(filepath)
    data = img.get_fdata()
    affine = img.affine
    header = img.header
    return data, affine, header


def nifti_to_tiff(input_path, output_path=None):
    """
    Convert a NIfTI file to TIFF format.
    
    Parameters:
    -----------
    input_path : str
        Path to input NIfTI file (.nii or .nii.gz)
    output_path : str, optional
        Path to output TIFF file. If None, creates output in same directory
        with .tiff extension
        
    Returns:
    --------
    output_path : str
        Path to the created TIFF file
    """
    # Load NIfTI file
    data, affine, header = load_nifti(input_path)
    
    # Convert to appropriate dtype if needed
    # Many vessel segmentation algorithms expect uint8 or uint16
    if data.dtype == np.float32 or data.dtype == np.float64:
        # Normalize to 0-65535 range for uint16
        data_min = data.min()
        data_max = data.max()
        if data_max > data_min:
            data = ((data - data_min) / (data_max - data_min) * 65535).astype(np.uint16)
        else:
            data = data.astype(np.uint16)
    
    # Determine output path
    if output_path is None:
        input_path_obj = Path(input_path)
        # Remove .gz if present, then remove .nii, then add .tiff
        stem = input_path_obj.stem
        if stem.endswith('.nii'):
            stem = stem[:-4]
        output_path = str(input_path_obj.parent / f"{stem}.tiff")
    
    # Save as TIFF
    # Using 'minisblack' photometric interpretation for grayscale medical imaging data
    # This is standard for single-channel intensity images like vessel scans
    imsave(output_path, data, photometric='minisblack')
    
    # Save metadata as a text file for reference
    metadata_path = output_path.replace('.tiff', '_nifti_metadata.txt')
    with open(metadata_path, 'w') as f:
        f.write("NIfTI Metadata\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Original file: {input_path}\n")
        f.write(f"Shape: {data.shape}\n")
        f.write(f"Data type: {data.dtype}\n")
        f.write(f"\nAffine matrix:\n{affine}\n")
        f.write(f"\nPixel dimensions (mm): {header.get_zooms()}\n")
        f.write(f"\nHeader:\n{header}\n")
    
    return output_path


def get_pixel_dimensions_from_nifti(filepath):
    """
    Extract pixel dimensions from NIfTI header.
    
    Parameters:
    -----------
    filepath : str
        Path to NIfTI file
        
    Returns:
    --------
    dimensions : str
        Comma-separated pixel dimensions in format "z,y,x" matching VesselExpress convention
        
    Note:
    -----
    NIfTI zooms are in (x, y, z) order by default, but we return (z, y, x) to match
    VesselExpress's expected format for 3D image processing.
    """
    img = nib.load(filepath)
    zooms = img.header.get_zooms()
    
    # Return in z,y,x format as expected by VesselExpress
    # NIfTI zooms are typically (x, y, z), so we reverse for VesselExpress
    if len(zooms) >= 3:
        return f"{zooms[2]},{zooms[1]},{zooms[0]}"
    else:
        # Default if not 3D
        return "1.0,1.0,1.0"


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert NIfTI files to TIFF for VesselExpress processing"
    )
    parser.add_argument('-i', '--input', required=True, 
                        help='Input NIfTI file (.nii or .nii.gz)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output TIFF file (optional, default: same name with .tiff extension)')
    
    args = parser.parse_args()
    
    output = nifti_to_tiff(args.input, args.output)
    print(f"Converted {args.input} to {output}")
    
    # Also print pixel dimensions
    dims = get_pixel_dimensions_from_nifti(args.input)
    print(f"Pixel dimensions (z,y,x): {dims}")
    print(f"Note: Update config.json graphAnalysis.pixel_dimensions to: {dims}")
