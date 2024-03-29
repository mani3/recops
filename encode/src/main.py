import argparse
import glob
import logging
import os

from video import Video

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(args):
  input_dir = args.input_dir
  output_dir = args.output_dir

  os.makedirs(output_dir, exist_ok=True)
  file_paths = glob.glob(os.path.join(input_dir, "*.m2ts"))

  if len(file_paths) == 0:
    logger.info("No files found in the input directory")
    return

  for path in file_paths:
    video = Video(path, output_dir)
    video.convert()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input_dir", type=str, help="Input file")
  parser.add_argument("--output_dir", type=str, help="Output file")
  args = parser.parse_args()
  main(args)
