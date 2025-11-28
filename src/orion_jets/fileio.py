"""
I/O utilities for Orion Jets project

Includes functions for reading FITS files and DS9 region files
"""

from astropy.io import fits
import regions as rg
from pathlib import Path


def get_first_data_hdu(fitsfile: Path) -> fits.PrimaryHDU | fits.ImageHDU:
    """Try each of the HDUs in turn in a FITS file until we find a data array"""
    hdu_list = fits.open(fitsfile)
    for hdu in hdu_list:
        if hdu.data is not None:
            return hdu
    # Case of no data found
    raise IOError(f"No image data found in {fitsfile.name}")


def get_box_region_masks(regions_file) -> dict[str, rg.RegionMask]:
    """
    Read regions from file in DS9 format

    Coordinates should be in "image" frame (pixel coordinates)

    Returns a dict of RegionMask objects with keys taken from the region text labels
    """
    regs: rg.Regions = rg.Regions.read(regions_file)
    boxes: dict[str, rg.RegionMask] = {}
    unlabeled_index = 1
    for reg in regs:
        # Use region text as label if it exists
        try:
            label = reg.meta["text"]
        except KeyError:
            # Otherwise, just call it "Box 001", etc
            label = f"Box {unlabeled_index:03d}"
            unlabeled_index += 1
        mask: rg.RegionMask = reg.to_mask()
        boxes[label] = mask
    return boxes
