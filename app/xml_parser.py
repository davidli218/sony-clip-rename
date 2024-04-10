import tomllib
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.dom import minidom

specs_mapping_file = Path(__file__).parent / 'specs_mapping.toml'

spec_dict = namedtuple(
    'SpecsDict',
    ['model', 'resolution', 'color_primaries', 'gamma_equation']
)

with specs_mapping_file.open('rb') as f:
    load_dict = tomllib.load(f)
    load_dict['resolution'] = {tuple(map(int, k.split(','))): v for k, v in load_dict['resolution'].items()}

    spec_dict = spec_dict(**load_dict)


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
    s = s.rstrip('0')
    return int(s.rstrip('.')) if s.endswith('.') else float(s)


def parse_xml(xml_file: Path) -> ClipInfo:
    if not xml_file.exists():
        raise FileNotFoundError(f"File Not Found: {xml_file}")

    dom = minidom.parse(str(xml_file))
    root = dom.documentElement

    tag_creation_date = root.getElementsByTagName('CreationDate')[0]
    tag_video_frame = root.getElementsByTagName('VideoFrame')[0]
    tag_video_layout = root.getElementsByTagName('VideoLayout')[0]
    tag_device = root.getElementsByTagName('Device')[0]
    tag_acquisition_record = root.getElementsByTagName('AcquisitionRecord')[0]
    tag_item = tag_acquisition_record.getElementsByTagName('Item')

    att_value = tag_creation_date.getAttribute('value')
    att_model_name = tag_device.getAttribute('modelName')
    att_pixel = tag_video_layout.getAttribute('pixel')
    att_num_of_vertical_line = tag_video_layout.getAttribute('numOfVerticalLine')
    att_capture_fps = tag_video_frame.getAttribute('captureFps')

    d_creation_time = att_value
    d_model_name = att_model_name
    d_resolution = (int(att_pixel), int(att_num_of_vertical_line))
    d_capture_fps = __parse_fps(att_capture_fps[:-1])
    d_gamma_equation = None
    d_color_primaries = None

    for item in tag_item:
        if item.getAttribute('name') == 'CaptureGammaEquation':
            d_gamma_equation = item.getAttribute('value')
        elif item.getAttribute('name') == 'CaptureColorPrimaries':
            d_color_primaries = item.getAttribute('value')

    dom.unlink()

    return ClipInfo(
        creation_time=datetime.fromisoformat(d_creation_time),
        model_name=d_model_name,
        resolution=d_resolution,
        capture_fps=d_capture_fps,
        gamma_equation=d_gamma_equation,
        color_primaries=d_color_primaries,
    )
