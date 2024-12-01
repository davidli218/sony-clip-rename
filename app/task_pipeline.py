from pathlib import Path
from typing import List

from app.xml_parser import parse_xml


def get_video_files(directory: Path, extensions: List[str] = None) -> List[Path]:
    """
    获取指定目录下的所有视频文件

    :param directory: 目录路径
    :param extensions: 视频文件的扩展名列表
    :return: 视频文件的路径列表
    """
    if extensions is None:
        extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv']  # 默认支持的视频格式

    video_files = [file for file in directory.rglob("*") if file.suffix.lower() in extensions]

    return video_files


def find_matching_xml(video_file: Path, strict: bool = True) -> Path | None:
    """
    查找与视频文件匹配的 XML 文件

    - 严格模式：只匹配 f'{视频文件名}M01' 的XML文件
    - 非严格模式：匹配 f'{视频文件名}M01' 或 f'{视频文件名}' 的XML文件

    :param video_file: 视频文件的路径
    :param strict: 是否启用严格模式
    :return: 匹配的 XML 文件路径，如果未找到返回 None
    """
    xml_extensions = [".XML"]
    search_locations = [video_file.parent, video_file.parent / "xml", video_file.parent / "XML"]

    for location in search_locations:
        for ext in xml_extensions:
            original_xml_file = location / (video_file.stem + 'M01' + ext)
            compatible_xml_file = location / (video_file.stem + ext)

            if original_xml_file.exists():
                return original_xml_file
            elif not strict and compatible_xml_file.exists():
                return compatible_xml_file

    return None


def generate_tasks_from_dir(directory: Path, strict: bool = True) -> List[dict]:
    """
    从指定目录中生成任务列表

    :param directory: 目录路径
    :param strict: 是否启用严格模式
    :return: 任务列表
    """
    video_files = get_video_files(directory)

    tasks = []
    for video_file in video_files:
        xml_file = find_matching_xml(video_file, strict=strict)

        if xml_file is not None:
            tasks.append({
                "implicit_dir": directory,
                "video": video_file,
                "xml": xml_file
            })

    print(f"TaskGen[D]: Found {len(video_files)} supported video files in {directory}")
    print(f"TaskGen[D]: Found {len(tasks)} matching video-xml pairs in {directory}")

    return tasks


def generate_tasks_from_file(file: Path, strict: bool = True) -> List[dict]:
    """
    为指定文件生成任务列表

    :param file: 文件路径
    :param strict: 是否启用严格模式
    :return: 任务列表
    """
    xml_file = find_matching_xml(file, strict=strict)

    if xml_file is not None:
        print(f"TaskGen[F]: Found matching video-xml pair for {file}")
        return [{
            "implicit_dir": file.parent,
            "video": file,
            "xml": xml_file
        }]
    else:
        print(f"TaskGen[F]: No matching video-xml pair found for {file}")
        return []


def process_tasks(tasks: List[dict], dry_run: bool = False):
    """
    处理任务列表

    :param tasks: 任务列表，包含 'video' 和 'xml' 的路径信息
    :param dry_run: 是否启用干跑模式，仅打印而不执行实际操作
    """
    if not tasks:
        print("Processor: No tasks to process.")
        return

    print(f"Processor: Starting to process {len(tasks)} tasks...")
    for idx, task in enumerate(tasks, start=1):
        implicit_dir: Path = task["implicit_dir"]
        video_file: Path = task["video"]
        xml_file: Path = task["xml"]

        print(f"Processor: Task [{idx}/{len(tasks)}]", end=' ')
        if dry_run:
            print(f"(DryRun)", end=' ')

        new_name = parse_xml(xml_file).std_name
        new_video_file = video_file.with_stem(new_name)
        new_xml_file = xml_file.with_stem(new_name)

        if not dry_run:
            video_file.rename(new_video_file)
            xml_file.rename(new_xml_file)

        print(f"{video_file.relative_to(implicit_dir)} -> {new_video_file.relative_to(implicit_dir)}")

    print("Processor: All tasks processed.")
