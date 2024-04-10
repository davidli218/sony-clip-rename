import argparse
from pathlib import Path

from app import batch_rename


def main():
    parser = argparse.ArgumentParser(description='Batch rename Sony video files.')
    parser.add_argument('work_dir', type=str, help='The directory to work in.')
    parser.add_argument('-a', '--apply', action='store_true', help='Apply the rename.')
    parser.add_argument('-f', '--force', action='store_true', help='Force rename.')
    args = parser.parse_args()

    batch_rename(Path(args.work_dir), strict=not args.force, dry_run=not args.apply)

    if not args.apply:
        print('\nDry run completed. Use -a or --apply to apply the rename.')


if __name__ == '__main__':
    main()
