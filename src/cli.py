import argparse
import sys
import logging
from pathlib import Path
from .audio_processor import AudioProcessor

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='音频批量处理工具 - 将短音频拼接成指定最小时长的音频文件',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input-dir', 
        required=True,
        help='输入音频文件夹路径'
    )
    parser.add_argument(
        '-o', '--output-dir', 
        required=True,
        help='输出音频文件夹路径'
    )
    parser.add_argument(
        '-d', '--min-duration', 
        type=float, 
        default=15.0,
        help='最小音频时长（秒）'
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true',
        help='启用详细日志输出'
    )
    
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_args()
    
    # 配置日志级别
    if args.verbose:
        logging.getLogger('AudioProcessor').setLevel(logging.DEBUG)
    
    # 转换秒到毫秒
    min_duration_ms = int(args.min_duration * 1000)
    
    # 检查输入目录是否存在
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"错误: 输入目录 '{args.input_dir}' 不存在", file=sys.stderr)
        return 1
    
    try:
        # 创建处理器并执行
        processor = AudioProcessor(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            min_duration_ms=min_duration_ms
        )
        
        # 开始处理
        print(f"开始处理音频文件...")
        count = processor.process()
        
        if count > 0:
            print(f"处理完成: 成功生成 {count} 个音频文件")
            print(f"输出目录: {args.output_dir}")
            return 0
        else:
            print("未生成任何音频文件，请检查输入文件夹是否包含支持的音频文件")
            return 1
            
    except Exception as e:
        print(f"处理过程中出错: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 