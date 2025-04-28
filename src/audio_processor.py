import os
import logging
from pydub import AudioSegment
from pathlib import Path
from typing import List, Tuple, Optional, Callable
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AudioProcessor')

class AudioProcessor:
    """音频批量处理工具，将短音频拼接成大于指定时长的音频文件"""
    
    def __init__(self, input_dir: str, output_dir: str, min_duration_ms: int = 15000):
        """
        初始化音频处理器
        
        Args:
            input_dir: 输入音频文件夹路径
            output_dir: 输出音频文件夹路径
            min_duration_ms: 最小音频时长（毫秒），默认15000ms即15秒
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.min_duration_ms = min_duration_ms
        
        logger.info(f"初始化音频处理器: 输入目录={self.input_dir}, 输出目录={self.output_dir}, 最小时长={self.min_duration_ms/1000}秒")
        
        # 创建输出目录（如果不存在）
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 支持的音频格式
        self.supported_formats = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac'}
        logger.info(f"支持的音频格式: {', '.join(self.supported_formats)}")
        
    def process(self) -> int:
        """
        处理音频文件：读取、拼接并保存
        
        Returns:
            生成的音频文件数量
        """
        logger.info("开始处理音频文件...")
        
        # 获取所有音频文件
        audio_files = self._get_audio_files()
        
        if not audio_files:
            logger.warning(f"未在 {self.input_dir} 找到支持的音频文件")
            return 0
        
        logger.info(f"找到 {len(audio_files)} 个音频文件")
        for file in audio_files:
            logger.info(f"  - {file.name}")
            
        # 获取所有音频的长度并排序
        logger.info("开始分析音频文件时长...")
        audio_info = self._get_audio_info(audio_files)
        
        if not audio_info:
            logger.warning("音频分析异常")
            return 0
        
        # 拼接音频
        logger.info("开始拼接音频文件...")
        merged_count = self._merge_audio_files(audio_info)
        
        if merged_count > 0:
            logger.info(f"处理完成: 成功生成 {merged_count} 个音频文件")
        else:
            logger.warning("未生成任何合并文件，可能是处理发生错误")
            
        return merged_count
    
    def _get_audio_files(self) -> List[Path]:
        """获取所有支持的音频文件路径"""
        logger.info(f"扫描目录: {self.input_dir}")
        audio_files = []
        
        if not self.input_dir.exists():
            logger.error(f"输入目录 {self.input_dir} 不存在")
            return audio_files
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                audio_files.append(file_path)
                logger.info(f"找到音频文件: {file_path.name}")
            elif file_path.is_file():
                logger.info(f"跳过不支持的文件: {file_path.name}")
        
        return audio_files
    
    def _get_audio_info(self, audio_files: List[Path]) -> List[Tuple[Path, int]]:
        """
        获取音频文件信息（路径和时长）
        
        Args:
            audio_files: 音频文件路径列表
            
        Returns:
            包含(文件路径, 时长)的列表
        """
        audio_info = []
        
        for file_path in audio_files:
            try:
                logger.info(f"分析音频: {file_path.name}")
                
                # 加载音频文件
                audio = AudioSegment.from_file(file_path)
                    
                audio_info.append((file_path, len(audio)))
                logger.info(f"音频 {file_path.name} 时长: {len(audio)/1000:.2f}秒")
            except Exception as e:
                logger.error(f"处理音频 {file_path} 时出错: {str(e)}")
        
        # 按时长排序（从短到长）
        sorted_info = sorted(audio_info, key=lambda x: x[1])
        logger.info("音频文件按时长排序:")
        for path, duration in sorted_info:
            logger.info(f"  - {path.name}: {duration/1000:.2f}秒")
        
        return sorted_info
    
    def _merge_audio_files(self, audio_info: List[Tuple[Path, int]]) -> int:
        """
        合并音频文件，保证每个合并后的文件时长大于最小时长
        
        Args:
            audio_info: 包含(文件路径, 时长)的列表
            
        Returns:
            生成的音频文件数量
        """
        if not audio_info:
            return 0
        
        merged_count = 0
        current_segment = None
        current_duration = 0
        current_files = []
        
        for file_path, duration in audio_info:
            try:
                logger.info(f"处理音频: {file_path.name} (时长: {duration/1000:.2f}秒)")
                
                # 加载当前音频
                audio = AudioSegment.from_file(file_path)
                
                # 如果是第一个音频或当前音频段为空
                if current_segment is None:
                    logger.info(f"开始新的拼接段，第一个文件: {file_path.name}")
                    current_segment = audio
                    current_duration = duration
                    current_files = [file_path.name]
                else:
                    # 拼接音频
                    logger.info(f"拼接音频: {file_path.name} 到当前段 (当前段时长: {current_duration/1000:.2f}秒)")
                    current_segment += audio
                    current_duration += duration
                    current_files.append(file_path.name)
                    logger.info(f"拼接后时长: {current_duration/1000:.2f}秒")
                
                # 如果当前拼接段长度已超过最小时长，保存并重置
                if current_duration >= self.min_duration_ms:
                    output_filename = f"merged_{uuid.uuid4().hex[:8]}_{current_duration/1000:.1f}s{file_path.suffix}"
                    output_path = self.output_dir / output_filename
                    
                    logger.info(f"当前段时长({current_duration/1000:.2f}秒)已超过最小时长({self.min_duration_ms/1000}秒)，准备导出")
                    logger.info(f"拼接段包含的文件: {', '.join(current_files)}")
                    
                    current_segment.export(output_path, format=file_path.suffix.lstrip('.'))
                    merged_count += 1
                    logger.info(f"成功生成音频: {output_filename} (时长: {current_duration/1000:.2f}秒)")
                    
                    # 重置当前段
                    current_segment = None
                    current_duration = 0
                    current_files = []
            
            except Exception as e:
                logger.error(f"处理音频 {file_path} 时出错: {str(e)}")
        
        # 处理剩余音频段（如果有）
        if current_segment is not None:
            # 如果剩余段太短，需要使用最后一个文件的格式
            suffix = audio_info[-1][0].suffix
            output_filename = f"merged_{uuid.uuid4().hex[:8]}_{current_duration/1000:.1f}s{suffix}"
            output_path = self.output_dir / output_filename
            
            logger.info(f"处理剩余音频段 (时长: {current_duration/1000:.2f}秒)")
            logger.info(f"剩余段包含的文件: {', '.join(current_files)}")
            
            current_segment.export(output_path, format=suffix.lstrip('.'))
            merged_count += 1
            logger.info(f"成功生成音频: {output_filename} (时长: {current_duration/1000:.2f}秒)")
        
        return merged_count 