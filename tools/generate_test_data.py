#!/usr/bin/env python3
"""
测试数据生成脚本 - 创建多个不同长度的测试音频文件
"""
import os
import argparse
import random
from pathlib import Path
from pydub import AudioSegment
from pydub.generators import Sine

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='生成测试音频文件',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '-o', '--output-dir', 
        default='../data',
        help='输出目录'
    )
    parser.add_argument(
        '-n', '--num-files', 
        type=int, 
        default=10,
        help='生成文件数量'
    )
    parser.add_argument(
        '-f', '--format', 
        choices=['mp3', 'wav', 'ogg', 'flac'],
        default='wav',
        help='音频格式'
    )
    
    return parser.parse_args()

def generate_audio_file(file_path, format_type, min_duration=1, max_duration=10):
    """
    生成一个测试音频文件
    
    Args:
        file_path: 保存路径
        format_type: 音频格式
        min_duration: 最小时长(秒)
        max_duration: 最大时长(秒)
    """
    # 随机选择时长（秒）
    duration_s = random.uniform(min_duration, max_duration)
    duration_ms = int(duration_s * 1000)
    
    # 随机选择频率（赫兹）
    frequency = random.choice([440, 880, 220, 330])
    
    # 生成正弦波
    sine_wave = Sine(frequency)
    audio = sine_wave.to_audio_segment(duration=duration_ms)
    
    # 导出文件
    audio.export(file_path, format=format_type)
    
    print(f"生成音频: {file_path.name} (时长: {duration_s:.2f}秒, 频率: {frequency}Hz)")

def main():
    """主函数"""
    args = parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成音频文件
    print(f"开始生成 {args.num_files} 个测试音频文件...")
    
    for i in range(args.num_files):
        file_name = f"test_audio_{i+1}.{args.format}"
        file_path = output_dir / file_name
        generate_audio_file(file_path, args.format)
    
    print(f"完成生成 {args.num_files} 个测试音频文件")
    print(f"输出目录: {output_dir}")

if __name__ == "__main__":
    main() 