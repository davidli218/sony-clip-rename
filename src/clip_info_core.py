import os
import xml.etree.ElementTree as xmlET

from clip_info_map import ClipInfoMap


class ClipInfoCore:
    _creation_time = None  # 录制日期&时间
    _model_name = None  # 录制机型
    _resolution = None  # 素材分辨率
    _format_fps = None  # 素材帧率
    _video_codec = None  # 素材编码
    _gamma_equation = None  # 素材传递函数
    _color_primaries = None  # 素材原色

    def __init__(self, video_pair: tuple):
        """
        :param video_pair: Tuple(mp4_path, xml_path)
        """
        self._input_mp4 = os.path.split(video_pair[0])
        self._input_xml = os.path.split(video_pair[1])

        func_map_list = [
            ("'CreationDate' in elem.tag", self._set_creation_date),
            ("'Device' in elem.tag", self._set_model_name),
            ("'VideoLayout' in elem.tag", self._set_resolution),
            ("'VideoFrame' in elem.tag", self._set_fps_and_codec),
            ("elem.attrib.get('name') == 'CaptureGammaEquation'", self._set_gamma_equation),
            ("elem.attrib.get('name') == 'CaptureColorPrimaries'", self._set_color_primaries),
        ]

        for elem in xmlET.parse(video_pair[1]).getroot().iter():
            for condition, func in func_map_list:
                func(elem) if eval(condition) else ...

    def _set_creation_date(self, elem):
        """
        @Example:
            {'date': '2022-05-07', 'time': '08:41:00'} -> self._creation_time
        """
        val = elem.attrib.get('value')

        self._creation_time = {'date': val[:10], 'time': val[11:19]}

    def _set_model_name(self, elem):
        """
        @Example:
            'SX107' -> self._model_name
        """
        val = elem.attrib.get('modelName')

        try:
            self._model_name = ClipInfoMap.model_name[val]
        except KeyError:
            raise ValueError(f'[ERROR] model_name: {val} can not be recognized!')

    def _set_resolution(self, elem):
        """
        @Example:
            (1920, 1080) -> self._resolution
        """
        self._resolution = ClipInfoMap.resolution[
            (int(elem.attrib.get('pixel')), int(elem.attrib.get('numOfVerticalLine')))
        ]

    def _set_fps_and_codec(self, elem):
        """
        @Example:
            23.98 -> self._format_fps
            'AVC_HP@L51' -> self._video_codec
        """
        codec = elem.attrib.get('videoCodec').split('_')

        self._format_fps = elem.attrib.get('formatFps')[:-1]
        self._video_codec = f"{codec[0]}"

    def _set_gamma_equation(self, elem):
        """
        @Example:
            'HLG' -> self._gamma_equation
        """
        self._gamma_equation = ClipInfoMap.gamma_equation[elem.attrib.get('value')]

    def _set_color_primaries(self, elem):
        """
        @Example:
            'Rec709' -> self._color_primaries
        """
        self._color_primaries = ClipInfoMap.color_primaries[elem.attrib.get('value')]

    @property
    def std_name(self) -> str:
        d = self._creation_time['date'].replace('-', '')[2:]
        t = self._creation_time['time'].replace(':', '')

        return '-'.join([
            '_'.join([d, t]), f"{self._resolution}@{self._format_fps}",
            self._video_codec, self._color_primaries,
            self._gamma_equation, self._model_name,
        ])

    def print_debug_info(self):
        line_len = 68
        info_strs = [
            f"{self._input_mp4[1]} ({self._input_xml[1]})",
            f"Creation Date: [{self._creation_time['date']}] ({self._creation_time['time']})",
            f"Device: {self._model_name}",
            f"Resolution: {self._resolution}",
            f"Video Codec: {self._video_codec}",
            f"Capture FPS: {self._format_fps}",
            f"Capture Gamma Equation: {self._gamma_equation}",
            f"Capture Color Primaries: {self._color_primaries}",
            f"STD Name: {self.std_name}",
        ]

        ''' Printer '''
        print('<'.join('-' * (line_len // 2)))
        print(f"| {info_strs[0]: ^{line_len - 4}} |")
        for info in info_strs[1:]:
            print(f"| {info: <{line_len - 4}} |")
        print('>'.join('-' * (line_len // 2)))

    def apply_new_name(self, debug=True):
        new_video_path = os.path.join(self._input_mp4[0],
                                      self.std_name + '.' + self._input_mp4[1].split('.')[-1])
        new_xml_path = os.path.join(self._input_xml[0],
                                    self.std_name + '.' + self._input_xml[1].split('.')[-1])

        print(f"{os.path.join(*self._input_mp4)} -> {new_video_path}")
        print(f"{os.path.join(*self._input_mp4)} -> {new_xml_path}")

        if not debug:
            os.rename(os.path.join(*self._input_mp4), new_video_path)
            os.rename(os.path.join(*self._input_xml), new_xml_path)
        else:
            print(f"Info: Working in debug mode, the rename will not be applied!")
