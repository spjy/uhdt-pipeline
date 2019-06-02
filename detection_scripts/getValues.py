import argparse
from simple_rest_client.api import API
import os
# from pipeline.models import Metadata

# Script to communicate from the CPP script to python and save the object to the database

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--object", help="object")
    parser.add_argument("--image", help="image file")
    parser.add_argument("--path", help="image path")
    args = parser.parse_args()

    # Metadata.objects.create(
    #   image_name = args.i,
    #   image_path = args.p,
    #   object = args.object
    # )

    api = API(
        api_root_url='http://localhost:8000',
        json_encode_body=True,
        append_slash=True,
    )

    print(args.image)
    print(args.path)
    print(args.object)

    api.add_resource(resource_name='pipeline')
    api.pipeline.create(
      body = {
          'image_name': args.image,
          'image_path': args.path,
          'object': args.object
      }
    )

    os.system('py ..\src\Pipeline.py')

if __name__ == "__main__":
    main()
