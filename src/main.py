from rename_utils import RenameUtils

if __name__ == '__main__':
    work_dir = r'Input working directory here'

    RenameUtils.batch_rename(
        RenameUtils.video_pairs_gen(work_dir), dry_run=False
    )
