''' Convert GEE JavaScript to Python script to be used in QGIS.

example:
$ python convert_js_to_python.py --input Image/band_math.py 
'''

import os
import argparse


def dict_key_str(line):

    keys = """bands bestEffort bias collection color connectedness eeObject eightConnected format gain gamma
              geometry groupField groupName image iterations kernel labelBand leftField magnitude max maxDistance
              maxOffset maxPixels maxSize minBucketWidth min name normalize opacity palette patchWidth
              radius reducer referenceImage region rightField scale selectors shown sigma size source
              strokeWidth threshold units visParams width""".split()
    for key in keys:
        if ":" in line and key in line:
            line = line.replace(key + ":", "'" + key + "':")
    return line


def js_to_python(in_file):

    root_dir = os.path.dirname(os.path.abspath(__file__))
    in_file_path = os.path.join(root_dir, in_file)

    bool_python = False
    github_url = "# GitHub URL: " + \
        "https://github.com/giswqs/qgis-earthengine-examples/tree/master/" + in_file + "\n\n"

    lines = []
    with open(in_file_path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == 'import ee':
                bool_python = True

    output = ""

    if bool_python:   # only update the GitHub URL if it is already a gee Python script
        output = github_url + ''.join(map(str, lines))
    else:             # deal with JavaScript

        header = github_url + "import ee \n" + "from ee_plugin import Map \n"
        output = header + "\n"

        with open(in_file_path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("//", "#").replace(";",
                                                       "").replace("var ", "")
                line = line.replace("true", "True").replace("false", "False")
                line = line.replace("null", "{}")
                line = line.replace(".or", ".Or")
                line = line.replace(".and", '.And')
                line = line.replace(".not", '.Not')

                line = dict_key_str(line).rstrip()

                if "= function" in line:
                    line = line.replace(" = function", "").replace("{", "")
                    line = "def " + line.rstrip() + ":"
                # if line.strip() == "}":
                #     line = ""

                # print(line)
                if line.lstrip().startswith("."):
                    output = output.rstrip() + " " + "\\" + "\n" + line + "\n"
                else:
                    output += line + "\n"

    # print(output)

    with open(in_file_path, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        help="Path to the input python file")
    # parser.add_argument('--image_path', type=str, help="Path to the input GeoTIFF image")
    # parser.add_argument('--save_path', type=str, help="Path where the output map will be saved")
    args = parser.parse_args()
    js_to_python(args.input)
