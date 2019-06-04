import sys
sys.path.insert(0, './detection_scripts') # Add detection_scripts to python path

from label_image import main as alphanumeric_recognition
from openCVcolor1 import main as color_recognition
import json
import argparse
import os

# Get environment variables
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('..')
load_dotenv(dotenv_path=env_path)

class Pipeline:
  def __init__(self, image_name, image_path, object):
    self.image_name = image_name
    self.image_path = image_path
    self.metadata = {
      'type': 'standard',
      'latitude': '',
      'longitude': '',
      'orientation': '',
      'shape': object,
      'background_color': '',
      'alphanumeric': '',
      'alphanumeric_color': ''
    }

  """
  Manipulates the class's metadata object.

  Args:
    key (str): The key to modify in the metadata object.
    value (string): The value to set for the key in the metadata object.
  """
  def write_metadata(self, key, value):
    self.metadata[key] = value

  """
  Runs the alphanumeric recognition script and saves the result in the metadata object.
  """
  def run_alphanumeric(self):
    print(f'{self.image_name}: running alphanumeric script')

    # Run alphanumeric script
    result = alphanumeric_recognition(os.path.join(self.image_path, self.image_name))

    # Save result
    self.write_metadata('alphanumeric', result)

    print(f'{self.image_name}: detected alphanumeric "{result}"')

  """
  Runs the color recognition script and saves the result in the metadata object.
  """
  def run_color(self):
    print(f'{self.image_name}: running color script')

    # Run color script on specific image
    result = color_recognition(os.path.join(self.image_path, self.image_name))

    # Save result
    self.write_metadata('background_color', result["shape_color"])
    self.write_metadata('alphanumeric_color', result["alphanumeric_color"])

    print(f'{self.image_name}: detected shape_color {result["shape_color"]}')
    print(f'{self.image_name}: detected alphanumeric_color {result["alphanumeric_color"]}')

  """
  Saves the metadata object into a JSON file.
  """
  def write_json(self):
    print(f'{self.image_name}: writing JSON file')

    output_dir = os.getenv("OUTPUT_DIR")
    name = self.image_name.split('.')[0]
    output = json.dumps(self.metadata)

    with open(f'{os.path.join(output_dir, name)}.json', 'w') as file:
      file.write(output)

    os.rename(os.path.join(self.image_path, self.image_name), output_dir)

def main():
  # Get values from shape recognition script
  parser = argparse.ArgumentParser()
  parser.add_argument("--object", help="object")
  parser.add_argument("--image", help="image file")
  parser.add_argument("--path", help="image path")
  args = parser.parse_args()

  # Initialize pipeline
  pipeline = Pipeline(args.image, args.path, args.object)

  # Run alphanumeric
  pipeline.run_alphanumeric() # store alpha

  # run color
  pipeline.run_color() # store color

  # write object to json in output and mv the image with it to have the same name.
  pipeline.write_json()

if __name__ == '__main__':
  main()
