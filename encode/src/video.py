import logging
import os
import shutil
import subprocess

from caption import Caption
from program import Program

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Video:
  def __init__(self, m2ts_file, output_dir):
    self.m2ts_file = m2ts_file
    self.output_dir = output_dir
    json_file = "/tmp/tmp.json"
    self.extract_epg(json_file)

    program = Program(json_file, self.m2ts_file)
    directory_name, output_filename = program.get_output_info()

    self.title_dir = os.path.join(output_dir, directory_name)
    self.output_file = os.path.join(self.title_dir, output_filename)
    os.makedirs(self.title_dir, exist_ok=True)
    name, _ = os.path.splitext(m2ts_file)
    shutil.move(json_file, os.path.join(self.title_dir, f"{name}.json"))

  def extract_epg(self, epg_json_file):
    command = [
      "epgdump",
      "json",
      self.m2ts_file,
      epg_json_file,
    ]

    try:
      command = " ".join(command)
      subprocess.run(command, shell=True)
    except subprocess.CalledProcessError as e:
      logger.error(f"Failed export EPG file: {e}")

    return epg_json_file

  def convert(self):
    if not os.path.exists(self.output_file):
      self.convert_to_mp4(self.output_file)
    else:
      logger.info(f"Already converted file exist: {self.output_file}")
    caption = Caption(self.m2ts_file, self.title_dir)
    caption.extract_ass()

  def convert_to_mp4(self, output_file_path):
    # ffmpeg を使用して m2ts ファイルを mp4 に変換
    command = [
      "ffmpeg",
      "-i",
      self.m2ts_file,
      "-crf",
      "23",
      "-tag:v",
      "hvc1",
      "-c:v",
      self.codec_name(),
      output_file_path,
    ]
    command = " ".join(command)
    subprocess.run(command, shell=True)

  def codec_name(self):
    return "hevc_nvenc"
