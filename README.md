# 音频批量处理工具

一个用Python开发的音频批量处理工具，能够将短音频文件拼接为满足最小时长要求的音频文件。

## 功能特点

- 批量处理音频文件，自动拼接为满足最小时长要求的文件
- 支持多种音频格式（MP3、WAV、FLAC、OGG、M4A、AAC）
- 提供命令行和图形界面两种使用方式
- 详细的处理日志
- 可自定义最小音频时长

## 安装

1. 克隆仓库到本地：

```bash
git clone [仓库地址]
cd audio_processor
```

2. 安装依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行方式

基本用法：

```bash
python main.py -i [输入目录] -o [输出目录]
```

完整参数：

```bash
python main.py -i [输入目录] -o [输出目录] -d [最小时长(秒)] -v
```

参数说明：
- `-i, --input-dir`：输入音频文件夹路径（必需）
- `-o, --output-dir`：输出音频文件夹路径（必需）
- `-d, --min-duration`：最小音频时长（秒），默认为15秒
- `-v, --verbose`：启用详细日志输出

示例：

```bash
python main.py -i ./audio_input -o ./audio_output -d 20 -v
```

### 图形界面方式

启动图形界面：

```bash
python gui_main.py
```

在图形界面中：
1. 选择输入目录
2. 选择输出目录
3. 设置最小时长（秒）
4. 点击"开始处理"按钮
5. 查看处理日志和结果

## 项目结构

```
audio_processor/
├── main.py             # 命令行入口
├── gui_main.py         # 图形界面入口
├── requirements.txt    # 项目依赖
├── src/                # 源代码
│   ├── __init__.py     
│   ├── audio_processor.py  # 核心处理逻辑
│   ├── cli.py          # 命令行接口
│   └── gui.py          # 图形用户界面
├── tests/              # 单元测试
│   └── test_audio_processor.py
├── data/               # 示例数据
└── output/             # 默认输出目录
```

## 测试

运行单元测试：

```bash
python -m unittest discover -s tests
```

## 依赖

- Python 3.6+
- pydub：音频处理库
- tkinter：GUI库（通常随Python安装）

## 许可证

[MIT许可证](LICENSE)
