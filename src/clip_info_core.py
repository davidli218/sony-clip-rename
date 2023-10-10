import os
from dataclasses import dataclass
from xml.dom import minidom

from clip_info_map import ClipInfoMap


@dataclass
class ClipInfoData:
    creation_time: str = None
    model_name: str = None
    resolution: tuple = None
    capture_fps: int | float = None
    video_codec: str = None
    gamma_equation: str = None
    color_primaries: str = None

    @property
    def std_name(self) -> str:
        return '-'.join([
            self._short_creation_time(self.creation_time),
            f"{ClipInfoMap.resolution[self.resolution]}@{self.capture_fps}",
            self.video_codec,
            ClipInfoMap.color_primaries[self.color_primaries],
            ClipInfoMap.gamma_equation[self.gamma_equation],
            ClipInfoMap.model_name[self.model_name],
        ])

    @staticmethod
    def _short_creation_time(t) -> str:
        return '_'.join([t[2:10].replace('-', ''), t[11:19].replace(':', '')])


class ClipInfoCore:
    def __init__(self, video_pair: tuple):
        self._data = ClipInfoData()

        self._input_mp4 = os.path.split(video_pair[0])
        self._input_xml = os.path.split(video_pair[1])

        self._parse_xml()

    def _parse_xml(self):
        dom = minidom.parse(os.path.join(*self._input_xml))
        root = dom.documentElement

        tag_creation_date = root.getElementsByTagName('CreationDate')[0]
        tag_video_frame = root.getElementsByTagName('VideoFrame')[0]
        tag_video_layout = root.getElementsByTagName('VideoLayout')[0]
        tag_device = root.getElementsByTagName('Device')[0]
        tag_acquisition_record = root.getElementsByTagName('AcquisitionRecord')[0]
        tag_item = tag_acquisition_record.getElementsByTagName('Item')

        att_value: str = tag_creation_date.getAttribute('value')
        att_model_name: str = tag_device.getAttribute('modelName')
        att_pixel: str = tag_video_layout.getAttribute('pixel')
        att_num_of_vertical_line: str = tag_video_layout.getAttribute('numOfVerticalLine')
        att_capture_fps: str = tag_video_frame.getAttribute('captureFps')
        att_video_codec: str = tag_video_frame.getAttribute('videoCodec')

        self._data.creation_time = att_value
        self._data.model_name = att_model_name
        self._data.resolution = (int(att_pixel), int(att_num_of_vertical_line))
        self._data.capture_fps = self._str2num(att_capture_fps[:-1])
        self._data.video_codec = att_video_codec.split('_')[0]

        for item in tag_item:
            if item.getAttribute('name') == 'CaptureGammaEquation':
                self._data.gamma_equation = item.getAttribute('value')
            elif item.getAttribute('name') == 'CaptureColorPrimaries':
                self._data.color_primaries = item.getAttribute('value')

        dom.unlink()

    @staticmethod
    def _str2num(s: str) -> int | float:
        s = s.rstrip('0')
        return int(s.rstrip('.')) if s.endswith('.') else float(s)

    def print_debug_info(self):
        line_len = 68
        info_strs = [
            f"{self._input_mp4[1]} ({self._input_xml[1]})",
            f"Creation Date: {self._data.creation_time}",
            f"Device: {self._data.model_name}",
            f"Resolution: {self._data.resolution}",
            f"Video Codec: {self._data.video_codec}",
            f"Capture FPS: {self._data.capture_fps}",
            f"Capture Gamma Equation: {self._data.gamma_equation}",
            f"Capture Color Primaries: {self._data.color_primaries}",
            f"STD Name: {self._data.std_name}",
        ]

        # Printer
        print('<'.join('-' * (line_len // 2)))
        print(f"| {info_strs[0]: ^{line_len - 4}} |")
        for info in info_strs[1:]:
            print(f"| {info: <{line_len - 4}} |")
        print('>'.join('-' * (line_len // 2)))

    def apply_new_name(self, debug=True):
        new_video_path = os.path.join(self._input_mp4[0], self._data.std_name + '.' + self._input_mp4[1].split('.')[-1])
        new_xml_path = os.path.join(self._input_xml[0], self._data.std_name + '.' + self._input_xml[1].split('.')[-1])

        print(f"{os.path.join(*self._input_mp4)} -> {new_video_path}")
        print(f"{os.path.join(*self._input_xml)} -> {new_xml_path}")

        if not debug:
            os.rename(os.path.join(*self._input_mp4), new_video_path)
            os.rename(os.path.join(*self._input_xml), new_xml_path)
        else:
            print(f"Info: Working in debug mode, the rename will not be applied!")
