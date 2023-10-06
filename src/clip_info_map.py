class ClipInfoMap:
    # 机型映射表
    model_name = {
        'ILCE-6400': 'SA640',
        'ILCE-6700': 'SA670',
        'DSC-RX100M7': 'SX107',
        'ZV-E10': 'SZE10',
    }

    # 分辨率映射表
    resolution = {
        (1920, 1080): 'FHD',
        (2560, 1440): 'QHD',
        (3840, 2160): '4K',
        (7680, 4320): '8K',
    }

    # 色域映射表
    color_primaries = {
        'rec709': 'Rec709',
        'rec2020': 'Rec2020',
        's-gamut': 'SGamut',
        's-gamut3': 'SGamut3',
        's-gamut3-cine': 'SGamut3Ci',
    }

    # 传递函数映射表
    gamma_equation = {
        'rec709': 'Rec709',
        'rec709-xvycc': 'xvYCC',
        'rec2100-hlg': 'HLG',
        's-log2': 'SLog2',
        's-log3': 'SLog3',
        's-log3-cine': 'SLog3Ci',
        'nxcam-still': 'Still',
        'ex-cine1': 'Cine1',
        'ex-cine2': 'Cine2',
        's-cinetone': 'SCineT',
        'hlg-slog3ootf': 'HLG',
    }
