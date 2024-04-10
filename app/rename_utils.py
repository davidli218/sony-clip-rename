from pathlib import Path

from app.xml_parser import parse_xml


def __is_paired_xml(video_file: Path, xml_file: Path, strict: bool) -> bool:
    strict_equal = video_file.stem + 'M01' == xml_file.stem
    common_equal = video_file.stem == xml_file.stem

    return strict_equal or (common_equal and not strict)


def __clip_pair_generator(path: Path, strict: bool):
    if not path.exists() or not path.is_dir():
        raise ValueError(f"{path} is not a valid directory")

    all_files = list(path.glob("*"))
    video_files = [f for f in all_files if f.suffix.lower() == ".mp4"]
    xml_files = [f for f in all_files if f.suffix.lower() == ".xml"]

    for video_file in video_files:
        xml_file = next((f for f in xml_files if __is_paired_xml(video_file, f, strict)), None)
        if xml_file:
            yield video_file, xml_file
        else:
            raise FileNotFoundError(f"No XML file found for {video_file}")


def batch_rename(path: Path, strict: bool, dry_run: bool):
    for video_file, xml_file in __clip_pair_generator(path, strict):
        new_name = parse_xml(xml_file).std_name
        new_video_path = video_file.with_name(new_name + video_file.suffix)
        new_xml_path = xml_file.with_name(new_name + xml_file.suffix)

        print(f"{video_file} -> {new_video_path}")
        print(f"{xml_file} -> {new_xml_path}")

        if not dry_run:
            video_file.rename(new_video_path)
            xml_file.rename(new_xml_path)
