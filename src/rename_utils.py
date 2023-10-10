import os

from clip_info_core import ClipInfoCore


class RenameUtils:

    @classmethod
    def video_pairs_gen(cls, dir_path: str) -> list:

        if not os.path.isdir(dir_path):
            raise IsADirectoryError(f"'{dir_path}' isn't a Directory")

        return cls._video_pairs_gen_single_dir_mode(dir_path)

    @staticmethod
    def _video_pairs_gen_single_dir_mode(dir_path: str) -> list:

        def v2xb_rule(v):
            return os.path.splitext(v)[0] + 'M01'

        print("[PowerRenameUtils - PreCheck] Start")

        *_, fs = os.walk(dir_path).__next__()

        video_list = [fs[i] for i, f in enumerate(fs) if f.endswith(('.MP4', '.mp4'))]
        xml_list = [fs[i] for i, f in enumerate(fs) if f.endswith(('.XML', '.xml'))]
        fs = [f for f in fs if f not in xml_list + video_list]

        video_pairs = []
        unpaired_video = []
        for i, video in enumerate(video_list):
            paired = False
            for j, xml in enumerate(xml_list):
                if os.path.splitext(xml)[0] == v2xb_rule(video):
                    video_pairs.append((
                        os.path.join(dir_path, video_list[i]),
                        os.path.join(dir_path, xml_list.pop(j)),
                    ))
                    paired = True
                    break
            if not paired:
                unpaired_video.append(os.path.join(dir_path, video_list[i]))

        if unpaired_video:
            raise FileExistsError(f"Found Unmatched Video: \n\t{video_list}")
        if xml_list:
            print(f"[Warning] Found Unmatched XML: \n\t{xml_list}")
        if fs:
            print(f"[Warning] Found Unrelated File: \n\t{fs}")

        print(f"[PowerRenameUtils - PreCheck] Done. {len(video_pairs)} videos paired.")

        return video_pairs

    @staticmethod
    def batch_rename(video_pairs: list, dry_run: bool = True):

        if not video_pairs:
            return

        for i, pair in enumerate(video_pairs):
            print(f"[{i + 1}/{len(video_pairs)}]")
            ClipInfoCore(pair).apply_new_name(dry_run)
