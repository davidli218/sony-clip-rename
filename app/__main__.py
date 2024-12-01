import argparse
from pathlib import Path

from app.task_pipeline import generate_tasks_from_dir
from app.task_pipeline import generate_tasks_from_file
from app.task_pipeline import process_tasks


def main():
    parser = argparse.ArgumentParser(description='Rename Sony camera clips to a more human-readable format.')
    parser.add_argument('work_dest', help='Directory or file to process.')
    parser.add_argument('-d', '--dry', action='store_true', help='Dry run.')
    parser.add_argument('-s', '--strict', action='store_true', help='Strict mode.')
    args = parser.parse_args()

    work_dest = Path(args.work_dest)
    if work_dest.is_dir():
        tasks = generate_tasks_from_dir(work_dest, strict=args.strict)
    elif work_dest.is_file():
        tasks = generate_tasks_from_file(work_dest, strict=args.strict)
    else:
        raise FileNotFoundError(f"File Not Found: {work_dest}")

    process_tasks(tasks, dry_run=args.dry)


if __name__ == '__main__':
    main()
