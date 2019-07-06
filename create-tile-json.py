import argparse
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument("metadata_json", help="The relative path to the metadata.json file created by tippecanoe")
parser.add_argument("url_path", help="The full URL to the place you'll be hosting these tiles e.g. http://mydomain.com/map/")
args = parser.parse_args()

if os.path.isfile(args.metadata_json):
    with open(args.metadata_json, "r") as f:
        metadata = json.load(f)

        # Write the URL path to the tiles so Mapbox knows where to fetch them
        url_path = args.url_path[:-1] if args.url_path[-1:] == "/" else args.url_path
        relative_dir = os.path.dirname(args.metadata_json).replace(os.getcwd(), "")
        relative_dir = "/{}".format(relative_dir) if relative_dir[:1] != "/" else relative_dir
        metadata["tiles"] = ["{url}{dir}/{{z}}/{{x}}/{{y}}.pbf".format(url=url_path, dir=relative_dir)]

        # Parse the vector layers from written-as-text blob of JSON in the metadata.json file
        json_pkg = json.loads(metadata["json"])

        if "vector_layers" not in json_pkg:
            raise Exception("Your metadata.json file doesn't contain a 'vector_layers' property in its 'json' package")

        metadata["vector_layers"] = json_pkg["vector_layers"]
        del metadata["json"]

        with open(args.metadata_json.replace("metadata.json", "tile.json"), "w") as f:
            f.write(json.dumps(metadata, indent=4, sort_keys=True))
