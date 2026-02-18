#!/usr/bin/env python3
"""
VesselExpress Command Line Interface

A simplified CLI wrapper for running VesselExpress analyses on vessel imaging data.
Supports TIFF, PNG, JPG, and NIfTI (.nii, .nii.gz) formats.
"""

import os
import sys
import argparse
import json
import subprocess
from pathlib import Path
import shutil


def setup_workspace(input_file, config_file=None, output_dir=None):
    """
    Set up the workspace for VesselExpress processing.
    
    Parameters:
    -----------
    input_file : str
        Path to input image file
    config_file : str, optional
        Path to configuration JSON file
    output_dir : str, optional
        Output directory (default: creates 'data' directory)
        
    Returns:
    --------
    workspace_dir : Path
        Path to the prepared workspace directory
    """
    # Get the VesselExpress directory
    script_dir = Path(__file__).resolve().parent
    vesselexpress_dir = script_dir / "VesselExpress"
    
    # Prepare workspace
    if output_dir:
        workspace_dir = Path(output_dir).resolve()
    else:
        workspace_dir = vesselexpress_dir / "data"
    
    workspace_dir.mkdir(exist_ok=True, parents=True)
    
    # Copy input file to workspace
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    target_file = workspace_dir / input_path.name
    if target_file != input_path:
        shutil.copy2(input_path, target_file)
        print(f"Copied input file to: {target_file}")
    
    # Handle config file
    if config_file:
        config_path = Path(config_file).resolve()
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        target_config = workspace_dir / "config.json"
        shutil.copy2(config_path, target_config)
        print(f"Using config file: {target_config}")
    else:
        # Check if config.json exists in workspace
        target_config = workspace_dir / "config.json"
        if not target_config.exists():
            # Copy default config
            default_config = vesselexpress_dir / "data" / "config.json"
            if default_config.exists():
                shutil.copy2(default_config, target_config)
                print(f"Using default config file: {target_config}")
            else:
                print("Warning: No config file found. Using Snakemake defaults.")
    
    return workspace_dir


def run_vesselexpress(workspace_dir, cores="all", dry_run=False, verbose=False):
    """
    Run VesselExpress using Snakemake.
    
    Parameters:
    -----------
    workspace_dir : Path
        Path to the workspace directory
    cores : str or int
        Number of cores to use (default: "all")
    dry_run : bool
        If True, perform a dry run without executing
    verbose : bool
        If True, show verbose output
        
    Returns:
    --------
    int
        Exit code (0 for success, non-zero for failure)
    """
    # Get the VesselExpress directory
    script_dir = Path(__file__).resolve().parent
    vesselexpress_dir = script_dir / "VesselExpress"
    
    # Build snakemake command
    cmd = [
        "snakemake",
        "--use-conda",
        "--cores", str(cores),
        "--conda-frontend", "conda",
        "--snakefile", str(vesselexpress_dir / "workflow" / "Snakefile"),
        "--directory", str(vesselexpress_dir)
    ]
    
    if dry_run:
        cmd.append("--dry-run")
    
    if verbose:
        cmd.extend(["--verbose", "--printshellcmds"])
    
    # Run snakemake
    print(f"\nRunning VesselExpress...")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        # Run with stderr visible to user for diagnostics
        result = subprocess.run(cmd, check=True, stderr=None)
        print("\n✓ VesselExpress completed successfully!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n✗ VesselExpress failed with exit code {e.returncode}")
        print("Check the error messages above for details.")
        return e.returncode


def print_nifti_info(input_file):
    """Print information about a NIfTI file."""
    try:
        # Use absolute path for import
        script_dir = Path(__file__).parent
        scripts_path = script_dir / "VesselExpress" / "workflow" / "scripts"
        sys.path.insert(0, str(scripts_path))
        
        from nifti_utils import load_nifti, get_pixel_dimensions_from_nifti
        
        data, affine, header = load_nifti(input_file)
        dims = get_pixel_dimensions_from_nifti(input_file)
        
        print(f"\nNIfTI File Information:")
        print(f"  File: {input_file}")
        print(f"  Shape: {data.shape}")
        print(f"  Data type: {data.dtype}")
        print(f"  Pixel dimensions (z,y,x): {dims}")
        print(f"\n  Note: Add this to your config.json:")
        print(f'    "graphAnalysis": {{"pixel_dimensions": "{dims}", ...}}')
        
    except ImportError:
        print("Error: nibabel not installed. Install with: pip install nibabel")
    except Exception as e:
        print(f"Error reading NIfTI file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="VesselExpress CLI - Blood vessel analysis in 3D image volumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run on a TIFF file with default settings
  %(prog)s -i sample.tiff
  
  # Run on a NIfTI file with custom config
  %(prog)s -i brain_vessels.nii.gz -c custom_config.json
  
  # Run with 4 cores and verbose output
  %(prog)s -i sample.tiff --cores 4 --verbose
  
  # Check NIfTI file information
  %(prog)s -i brain.nii.gz --info
  
  # Dry run to see what would be executed
  %(prog)s -i sample.tiff --dry-run

Supported formats: TIFF (.tif, .tiff), PNG (.png), JPG (.jpg), NIfTI (.nii, .nii.gz)
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='Input image file (TIFF, PNG, JPG, or NIfTI format)')
    parser.add_argument('-c', '--config', default=None,
                        help='Configuration JSON file (default: uses default config)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output directory (default: VesselExpress/data)')
    parser.add_argument('--cores', default='all',
                        help='Number of CPU cores to use (default: all)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform a dry run without executing')
    parser.add_argument('--verbose', action='store_true',
                        help='Show verbose output')
    parser.add_argument('--info', action='store_true',
                        help='Show information about input file (useful for NIfTI files)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    # If --info flag, just print information and exit
    if args.info:
        if args.input.endswith(('.nii', '.nii.gz')):
            print_nifti_info(args.input)
        else:
            print(f"File: {args.input}")
            print(f"Size: {os.path.getsize(args.input)} bytes")
        return 0
    
    try:
        # Set up workspace
        workspace_dir = setup_workspace(args.input, args.config, args.output)
        
        # Run VesselExpress
        return run_vesselexpress(
            workspace_dir, 
            cores=args.cores,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
