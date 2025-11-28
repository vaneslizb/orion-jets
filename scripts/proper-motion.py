import cyclopts
from pathlib import Path
from orion_jets import fileio, xcorr2d
from astropy.wcs import WCS
from astropy.wcs import WCSCOMPARE_ANCILLARY  # type: ignore


def main(
    epoch1_file: Path,
    epoch2_file: Path,
    regions_file: Path,
    verbose: bool = False,
) -> None:
    """
    Calculate proper motions by the cross-correlation method

    The peak of the spatial cross-correlation between the epochs is calculated for
    each box region that is specified

    Parameters
    ----------
    epoch1_file
        FITS image file of first epoch
    epoch2_file
        FITS image file of second epoch
    regions_file
        DS9 regions file containing list of boxes
    """

    # Read in the FITS image for each epoch
    hdu1 = fileio.get_first_data_hdu(epoch1_file)
    hdu2 = fileio.get_first_data_hdu(epoch2_file)

    # Require that the WCS are equivalent, so we can just work with pixels
    assert WCS(hdu1.header).wcs.compare(WCS(hdu2.header).wcs, cmp=WCSCOMPARE_ANCILLARY)

    # Read in regions from file and convert to dict of RegionMask
    boxes = fileio.get_box_region_masks(regions_file)
    if verbose:
        print(*[(k, v.bbox) for k, v in boxes.items()])

    for label, box in boxes.items():
        image1 = box.cutout(hdu1.data)
        image2 = box.cutout(hdu2.data)
        jshift, ishift = xcorr2d.measure_shift_integer(image1, image2)
        if verbose:
            print(label, "shift = ", jshift, ishift)


if __name__ == "__main__":
    cyclopts.run(main)
