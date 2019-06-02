import sys
sys.path.insert(0, '../detection_scripts') # Add detection_scripts to python path

import label_image as alphanumeric_recognition
import openCVcolor1 as color_recognition
import json
import argparse
import os

class Pipeline:
  def __init__(self, image_name, image_path, object):
    self.image_name = image_name
    self.image_path = image_path
    self.object = {
      'type': 'standard',
      'latitude': '',
      'longitude': '',
      'orientation': '',
      'shape': object,
      'background_color': '',
      'alphanumeric': '',
      'alphanumeric_color': ''
    }

  def write_object(self, key, value):
    self.object[key] = value

  def run_alphanumeric(self):
    print(f'{self.image_name}: running alphanumeric script')

    # Run alphanumeric script
    result = alphanumeric_recognition(os.path.join(self.image_path, self.image_name))

    # Save result
    self.write_object('alphanumeric', result)

    print(f'{self.image_name}: detected alphanumeric "{result}"')

  def run_color(self):
    print(f'{self.image_name}: running color script')

    # Run color script on specific image
    result = color_recognition(os.path.join(self.image_path, self.image_name))

    # Save result
    self.write_object('background_color', result["shape_color"])
    self.write_object('alphanumeric_color', result["alphanumeric_color"])

    print(f'{self.image_name}: detected shape_color {result["shape_color"]}')
    print(f'{self.image_name}: detected alphanumeric_color {result["alphanumeric_color"]}')

  def write_json(self):
    print(f'{self.image_name}: writing JSON file')

    name = self.image_name.split('.')[0]
    output = json.dumps(self.object)

    with open(f'{name}.json', 'w') as file:
      file.write(output)

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
