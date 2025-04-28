import os
import unittest
import tempfile
import shutil
from pathlib import Path
from pydub import AudioSegment
from src.audio_processor import AudioProcessor

class TestAudioProcessor(unittest.TestCase):
    """音频处理器单元测试"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = Path(self.temp_dir) / "input"
        self.output_dir = Path(self.temp_dir) / "output"
        
        # 创建测试目录
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 创建测试音频文件
        self._create_test_audio_files()
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        shutil.rmtree(self.temp_dir)
    
    def _create_test_audio_files(self):
        """创建测试音频文件"""
        # 创建几个不同长度的音频文件用于测试
        # 5秒音频
        self._create_audio_file(self.input_dir / "audio1.wav", 5000)
        # 7秒音频
        self._create_audio_file(self.input_dir / "audio2.wav", 7000)
        # 10秒音频
        self._create_audio_file(self.input_dir / "audio3.wav", 10000)
        # 3秒音频
        self._create_audio_file(self.input_dir / "audio4.wav", 3000)
    
    def _create_audio_file(self, file_path, duration_ms):
        """创建指定长度的测试音频文件"""
        # 创建一个包含静音的音频段
        silent_segment = AudioSegment.silent(duration=duration_ms)
        # 导出为WAV文件
        silent_segment.export(file_path, format="wav")
    
    def test_audio_processor_initialization(self):
        """测试音频处理器初始化"""
        processor = AudioProcessor(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )
        
        self.assertEqual(processor.input_dir, self.input_dir)
        self.assertEqual(processor.output_dir, self.output_dir)
        self.assertEqual(processor.min_duration_ms, 15000)  # 默认值
        
        # 测试自定义最小时长
        custom_min_duration = 20000
        processor = AudioProcessor(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir),
            min_duration_ms=custom_min_duration
        )
        self.assertEqual(processor.min_duration_ms, custom_min_duration)
    
    def test_get_audio_files(self):
        """测试获取音频文件"""
        processor = AudioProcessor(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )
        
        audio_files = processor._get_audio_files()
        
        # 应该找到4个音频文件
        self.assertEqual(len(audio_files), 4)
        
        # 检查文件路径是否正确
        file_names = {file_path.name for file_path in audio_files}
        expected_names = {"audio1.wav", "audio2.wav", "audio3.wav", "audio4.wav"}
        self.assertEqual(file_names, expected_names)
    
    def test_get_audio_info(self):
        """测试获取音频信息"""
        processor = AudioProcessor(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )
        
        audio_files = processor._get_audio_files()
        audio_info = processor._get_audio_info(audio_files)
        
        # 应该有4个音频信息
        self.assertEqual(len(audio_info), 4)
        
        # 检查音频时长是否正确（按时长排序）
        durations = [duration for _, duration in audio_info]
        expected_durations = sorted([3000, 5000, 7000, 10000])
        self.assertEqual(durations, expected_durations)
    
    def test_merge_audio_files(self):
        """测试合并音频文件"""
        processor = AudioProcessor(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir),
            min_duration_ms=15000  # 设置最小时长为15秒
        )
        
        # 处理音频
        merged_count = processor.process()
        
        # 应该生成1个或2个合并后的音频文件
        # 音频总时长：5 + 7 + 10 + 3 = 25秒
        # 可能的组合：
        # 1. 所有音频合并为一个文件 > 15秒
        # 2. 部分音频合并为一个文件 > 15秒，剩余的作为另一个文件，但总共不超过2个文件
        self.assertGreaterEqual(merged_count, 1)
        self.assertLessEqual(merged_count, 2)
        
        # 检查生成的文件
        output_files = list(self.output_dir.glob("*"))
        self.assertEqual(len(output_files), merged_count)
        
        # 检查生成的音频文件是否大于15秒
        for file_path in output_files:
            audio = AudioSegment.from_file(file_path)
            self.assertGreaterEqual(len(audio), 15000)
    
    def test_empty_input_directory(self):
        """测试空输入目录"""
        # 创建一个新的空输入目录
        empty_input_dir = Path(self.temp_dir) / "empty_input"
        os.makedirs(empty_input_dir, exist_ok=True)
        
        processor = AudioProcessor(
            input_dir=str(empty_input_dir),
            output_dir=str(self.output_dir)
        )
        
        # 处理音频
        merged_count = processor.process()
        
        # 应该没有生成音频文件
        self.assertEqual(merged_count, 0)
        
        # 输出目录应该是空的
        output_files = list(self.output_dir.glob("*"))
        self.assertEqual(len(output_files), 0)


if __name__ == "__main__":
    unittest.main() 