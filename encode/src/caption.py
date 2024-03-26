import logging
import os
import subprocess

CAPTION_EXT = "ass"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Caption:
  def __init__(self, m2ts_file, output_dir):
    self.m2ts_file = m2ts_file
    self.output_dir = output_dir
    basename = os.path.basename(m2ts_file)
    name, _ = os.path.splitext(basename)
    self.output_file = os.path.join(output_dir, f"{name}.{CAPTION_EXT}")

  def extract_ass(self):
    command = [
      "ffmpeg",
      "-analyzeduration",
      "10MB",
      "-probesize",
      "10MB",
      "-fix_sub_duration",
      "-i",
      self.m2ts_file,
      "-c:s",
      "ass",
      self.output_file,
    ]

    try:
      subprocess.run(command, check=True)
      logger.info(f"Completed caption file: {self.output_file}")
    except subprocess.CalledProcessError as e:
      logger.error(f"Failed export cation file: {e}")
    return self.output_file
