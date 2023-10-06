# Sony Clip Rename

适用于索尼微单机型的素材自动重命名脚本。

重命名功能依赖于跟随视频生成的XML文件。

## Naming Rule

%y%m%d_%H%M%S-Resolution@FPS-Format-ColorPrimaries-TransferFunc-Model(-Note).MP4

|     占位符     |          解释           |
| :------------: | :---------------------: |
|       %y       | 两位数的年份表示(00-99) |
|       %m       |       月份(01-12)       |
|       %d       |   月内中的一天(0-31)    |
|       %H       |  24小时制小时数(0-23)   |
|       %M       |      分钟数(00-59)      |
|       %S       |        秒(00-59)        |
|   Resolution   |         分辨率          |
|      FPS       |          帧率           |
|     Format     |        视频编码         |
| ColorPrimaries |          原色           |
|  TransferFunc  |        传递函数         |
|     Model      |        拍摄机型         |
|     (Note)     |        可选备注         |

## Example

```
220504_125850-4K@29.97-AVC-Rec709-xvYCC-SX107-乌鸦洗澡.MP4
```

