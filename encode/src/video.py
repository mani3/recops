import logging
import os
import shutil
import subprocess

from caption import Caption
from program import Program


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

    name, _ = os.path.splitext(os.path.basename(self.m2ts_file))
    self.epg_path = os.path.join(self.title_dir, f"{name}.json")

    if os.path.exists(self.epg_path):
      print(f"Already EPG file exist: {self.epg_path}")
    else:
      shutil.move(json_file, self.epg_path)

    if os.path.exists(json_file):
      os.remove(json_file)

  def extract_epg(self, epg_json_file):
    command = [
      "epgdump",
      "json",
      f'"{self.m2ts_file}"',
      epg_json_file,
    ]

    try:
      command = " ".join(command)
      subprocess.run(command, shell=True)
    except Exception as e:
      logging.error(f"Failed export EPG file: {e}")
      raise e
    return epg_json_file

  def convert(self):
    if not os.path.exists(self.output_file):
      self.convert_to_mp4(self.output_file)
    else:
      print(f"Already converted file exist: {self.output_file}")
    caption = Caption(self.m2ts_file, self.title_dir)
    caption_path = caption.extract_ass()

    if os.path.exists(self.output_file) and os.path.exists(self.epg_path):
      if not os.path.exists(caption_path):
        print(f"Not found ass file: {caption_path}")

      os.remove(self.m2ts_file)
      print(f"Remove m2ts file: {self.m2ts_file}")

  def convert_to_mp4(self, output_file_path):
    # ffmpeg を使用して m2ts ファイルを mp4 に変換
    command = [
      "ffmpeg",
      "-hide_banner",
      "-i",
      f'"{self.m2ts_file}"',
      "-crf",
      "23",
      "-tag:v",
      "hvc1",
      "-c:v",
      self.codec_name(),
      f'"{output_file_path}"',
    ]
    command = " ".join(command)
    print(f"Encode start: {command}")
    subprocess.run(command, shell=True)

  def codec_name(self):
    return "hevc_nvenc"
