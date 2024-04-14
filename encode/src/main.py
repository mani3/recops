import argparse
import glob
import logging
import os

from video import Video


def main(args):
  input_dir = args.input_dir
  output_dir = args.output_dir

  os.makedirs(output_dir, exist_ok=True)
  file_paths = glob.glob(os.path.join(input_dir, "*.m2ts")).sort()

  if len(file_paths) == 0:
    print("No files found in the input directory")
    return

  for path in file_paths:
    try:
      video = Video(path, output_dir)
      video.convert()
    except Exception as e:
      logging.error(f"Convert error: {path}, {e}")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--input_dir", type=str, help="Input file")
  parser.add_argument("--output_dir", type=str, help="Output file")
  args = parser.parse_args()
  main(args)
