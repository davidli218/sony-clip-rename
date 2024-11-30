import tomllib

from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

SPEC_MAPPING_FILE = Path(__file__).parent / 'res' / 'specs_mapping.toml'

SpecsDict = namedtuple('SpecsDict', ['model', 'resolution', 'color_primaries', 'gamma_equation'])

with SPEC_MAPPING_FILE.open('rb') as f:
    load_dict = tomllib.load(f)

    # Convert resolution from string to tuple
    load_dict['resolution'] = {tuple(map(int, k.split(','))): v for k, v in load_dict['resolution'].items()}

    spec_dict = SpecsDict(**load_dict)


@dataclass
class ClipInfo:
    creation_time: datetime
    model_name: str
    resolution: tuple
    capture_fps: int | float
    gamma_equation: str
    color_primaries: str

    @property
    def std_name(self) -> str:
        return '-'.join([
            self.creation_time.strftime('%y%m%d_%H%M%S'),
            f"{spec_dict.resolution[self.resolution]}@{self.capture_fps}",
            spec_dict.color_primaries[self.color_primaries],
            spec_dict.gamma_equation[self.gamma_equation],
            spec_dict.model[self.model_name],
        ])


def __parse_fps(s: str) -> int | float:
    s = s.rstrip('0p')
    return int(s[:-1]) if s.endswith('.') else float(s)


def parse_xml(xml_file: Path) -> ClipInfo:
    if not xml_file.exists():
        raise FileNotFoundError(f"File Not Found: {xml_file}")

    tree = ElementTree.parse(str(xml_file))
    root = tree.getroot()

    namespaces = {
        '': 'urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.20',
        'lib': 'urn:schemas-professionalDisc:lib:ver.2.10',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    }

    # 提取 CreationDate 中的 value
    creation_date = root.find('CreationDate', namespaces).get('value')

    # 提取 VideoFormat.VideoLayout 中的 pixel 和 numOfVerticalLine
    video_layout = root.find('VideoFormat/VideoLayout', namespaces)
    pixel_h = video_layout.get('pixel')
    pixel_v = video_layout.get('numOfVerticalLine')

    # 提取 VideoFormat.VideoFrame 中的 captureFps
    video_frame = root.find('VideoFormat/VideoFrame', namespaces)
    capture_fps = video_frame.get('captureFps')

    # 提取 Device 中的 modelName
    device = root.find('Device', namespaces)
    device_model = device.get('modelName')

    # 提取 AcquisitionRecord 中的 CaptureGammaEquation 和 CaptureColorPrimaries
    metadata_set = root.find("AcquisitionRecord/Group[@name='CameraUnitMetadataSet']", namespaces)
    capture_gamma_equation = metadata_set.find("Item[@name='CaptureGammaEquation']", namespaces).get('value')
    capture_color_primaries = metadata_set.find("Item[@name='CaptureColorPrimaries']", namespaces).get('value')

    return ClipInfo(
        creation_time=datetime.fromisoformat(creation_date),
        model_name=device_model,
        resolution=(int(pixel_h), int(pixel_v)),
        capture_fps=__parse_fps(capture_fps),
        gamma_equation=capture_gamma_equation,
        color_primaries=capture_color_primaries,
    )
