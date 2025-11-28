# scripts/fetch_data.py

import argparse
import pathlib
from orion_jets import remote_data


def parse_args():
    """
    Parse options from the command line
    """
    parser = argparse.ArgumentParser(
        description=(
            "Download example FITS files from the orion-jets-data repository "
            "into a local data directory."
        )
    )

    parser.add_argument(
        "--dest",
        type=pathlib.Path,
        default=pathlib.Path("data"),
        help="Destination directory for downloaded files (default: %(default)s).",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download files even if they already exist.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not download; just print what would be done.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("Destination directory:", args.dest.resolve())

    remote_files = remote_data.list_remote_fits_files()
    if not remote_files:
        print("No FITS files found in remote folder.")
        return

    print(f"Found {len(remote_files)} FITS file(s) in remote folder.")

    if args.dry_run:
        print("Dry run: no files will be downloaded.\n")

    for filename, url in remote_files:
        dest_path = args.dest / filename

        if dest_path.exists() and not args.force:
            print(f"Skipping {filename} (already exists).")
            continue

        if args.dry_run:
            print(f"Would download {url} → {dest_path}")
        else:
            remote_data.download_file(url, dest_path)


if __name__ == "__main__":
    main()
