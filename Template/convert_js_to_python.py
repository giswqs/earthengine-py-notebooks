''' Convert Google Earth Engine JavaScript to Python script.

To convert one Earth Engine JavaScript to Python script: js_to_python(in_file_path, out_file_path)
To convert all Earth Engine JavaScripts in a folder recursively: js_to_python_dir(in_dir, out_dir)

'''

# Authors: Dr. Qiusheng Wu (https://wetlands.io)
# License: MIT

import os
import random
import string
import argparse
from pathlib import Path
from collections import deque


def random_string(string_length=3):
    """Generate a random string of fixed length. 
    
    Args:
        stringLength (int, optional): Fixed length. Defaults to 3.
    
    Returns:
        str: A random string
    """    
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def find_matching_bracket(lines, start_line_index, start_char_index, matching_char='{'):
    """Finds the position of the matching closing bracket from a list of lines.

    Args:
        lines (list): The input list of lines.
        start_line_index (int): The line index where the starting bracket is located.
        start_char_index (int): The position index of the starting bracket.
        matching_char (str, optional): The starting bracket to search for. Defaults to '{'.

    Returns:
        matching_line_index (int): The line index where the matching closing bracket is located.
        matching_char_index (int): The position index of the matching closing bracket.

    """
    matching_line_index = -1
    matching_char_index = -1

    matching_chars = {
        '{': '}',
        '(': ')',
        '[': ']'
    }
    if matching_char not in matching_chars.keys():
        print("The matching character must be one of the following: {}".format(
            ', '.join(matching_chars.keys())))
        return matching_line_index, matching_char_index

    # Create a deque to use it as a stack.
    d = deque()

    for line_index in range(start_line_index, len(lines)):
        line = lines[line_index]
        # deal with the line where the starting bracket is located.
        if line_index == start_line_index:
            line = lines[line_index][start_char_index:]

        for index, item in enumerate(line):
            # Pops a starting bracket for each closing bracket
            if item == matching_chars[matching_char]:
                d.popleft()
            # Push all starting brackets
            elif item == matching_char:
                d.append(matching_char)

            # If deque becomes empty
            if not d:
                matching_line_index = line_index
                if line_index == start_line_index:
                    matching_char_index = start_char_index + index
                else:
                    matching_char_index = index

                return matching_line_index, matching_char_index

    return matching_line_index, matching_char_index


# extract parameters and wrap them with single/double quotes if needed.
def format_params(line, sep=':'):
    """Formats keys in a dictionary and adds quotes to the keys. 
    For example, {min: 0, max: 10} will result in ('min': 0, 'max': 10)

    Args:
        line (str): A string.
        sep (str, optional): Separator. Defaults to ':'.

    Returns:
        [str]: A string with keys quoted

    """
    # print(line)
    new_line = line
    prefix = ""
    suffix = ""

    if line.strip().startswith('for'):  # skip for loop
        return line

    # find all occurrences of a substring
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1:
                return
            yield start
            start += len(sub)  # use start += 1 to find overlapping matches

    indices = list(find_all(line, sep))
    count = len(indices)

    if "{" in line:
        bracket_index = line.index("{")
        if bracket_index < indices[0]:
            prefix = line[:bracket_index+1]
            line = line[bracket_index+1:]

    if count > 0:
        items = line.split(sep)

        if count == 1:
            for i in range(0, count):
                item = items[i].strip()
                if ('"' not in item) and ("'" not in item):
                    new_item = "'" + item + "'"
                    items[i] = items[i] .replace(item, new_item)
            new_line = ':'.join(items)
        elif count > 1:
            for i in range(0, count):
                item = items[i]
                if ',' in item:
                    subitems = item.split(',')
                    subitem = subitems[-1]
                    if ('"' not in subitem) and ("'" not in subitem):
                        new_subitem = "'" + subitem.strip() + "'"
                        subitems[-1] = subitems[-1].replace(
                            subitem, new_subitem)
                        items[i] = ', '.join(subitems)
                else:
                    if ('"' not in item) and ("'" not in item):
                        new_item = "'" + item.strip() + "'"
                        padding = len(item) - len(item.strip())
                        items[i] = " " * padding + item.replace(item, new_item)

            new_line = ':'.join(items)

    return prefix + new_line


def use_math(lines):
    """Checks if an Earth Engine uses Math library
    
    Args:
        lines (list): An Earth Engine JavaScript.
    
    Returns:
        [bool]: Returns True if the script contains 'Math.'. For example 'Math.PI', 'Math.pow'
    """
    math_import = False
    for line in lines:
        if 'Math.' in line:
            math_import = True
    
    return math_import        


def convert_for_loop(line):
    """Convert JavaScript for loop to Python for loop.
    
    Args:
        line (str): Input JavaScript for loop
    
    Returns:
        str: Converted Python for loop.
    """    
    new_line = ''
    if 'var ' in line:
        line = line.replace('var ', '')
    start_index = line.index('(')
    end_index = line.index(')')

    prefix = line[:(start_index)] 
    suffix = line[(end_index + 1):]

    params = line[(start_index + 1): end_index]

    if ' in ' in params and params.count(';') == 0:
        new_line = prefix + '{}:'.format(params) + suffix
        return new_line

    items = params.split('=')
    param_name = items[0].strip()
    items = params.split(';')
  
    subitems = []

    for item in items:
        subitems.append(item.split(' ')[-1])

    start = subitems[0]
    end = subitems[1]    
    step = subitems[2]

    if '++' in step:
        step = 1
    elif '--' in step:
        step = -1

    prefix = line[:(start_index)] 
    suffix = line[(end_index + 1):]
    new_line = prefix + '{} in range({}, {}, {}):'.format(param_name, start, end, step) + suffix

    return new_line


def check_map_functions(input_lines):
    """Extract Earth Engine map function
    
    Args:
        input_lines (list): List of Earth Engine JavaScrips
    
    Returns:
        list: Output JavaScript with map function
    """    
    output_lines = []
    for index, line in enumerate(input_lines):

        if ('.map(function' in line) or ('.map (function') in line:

            bracket_index = line.index("{")
            matching_line_index, matching_char_index = find_matching_bracket(input_lines, index, bracket_index)

            func_start_index = line.index('function')
            func_name = 'func_' + random_string()
            func_header = line[func_start_index:].replace('function', 'function ' + func_name)
            output_lines.append('\n')
            output_lines.append(func_header)

            for sub_index, tmp_line in enumerate(input_lines[index+1: matching_line_index]):
                output_lines.append(tmp_line)
                input_lines[index+1+sub_index] = ''                

            header_line = line[:func_start_index] + func_name 
            header_line = header_line.rstrip()

            func_footer = input_lines[matching_line_index][:matching_char_index+1]
            output_lines.append(func_footer)

            footer_line = input_lines[matching_line_index][matching_char_index+1:].strip()
            if footer_line == ')' or footer_line == ');':
                header_line = header_line + footer_line
                footer_line = ''

            input_lines[matching_line_index] = footer_line

            output_lines.append(header_line)
            output_lines.append(footer_line)
        else: 
            output_lines.append(line)            

    return output_lines


# Convert GEE JavaScripts to Python
def js_to_python(in_file, out_file=None, use_qgis=True, github_repo=None):
    """Converts an Earth Engine JavaScript to Python script.

    Args:
        in_file (str): File path of the input JavaScript.
        out_file (str, optional): File path of the output Python script. Defaults to None.
        use_qgis (bool, optional): Whether to add "from ee_plugin import Map \n" to the output script. Defaults to True.
        github_repo (str, optional): GitHub repo url. Defaults to None.

    Returns:
        list : Python script

    """
    if out_file is None:
        out_file = in_file.replace(".js", ".py")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isfile(in_file):
        in_file = os.path.join(root_dir, in_file)
    if not os.path.isfile(out_file):
        out_file = os.path.join(root_dir, out_file)

    is_python = False
    add_github_url = False
    qgis_import_str = ''
    if use_qgis:
        qgis_import_str = "from ee_plugin import Map \n"

    github_url = ""
    if github_repo is not None:
        github_url = "# GitHub URL: " + github_repo + in_file + "\n\n"

    math_import = False
    math_import_str = ""

    lines = []
    with open(in_file) as f:
        lines = f.readlines()

        math_import = use_math(lines)

        for line in lines:
            line = line.strip()
            if line == 'import ee':
                is_python = True
            
    if math_import:
        math_import_str = "import math\n"

    output = ""

    if is_python:   # only update the GitHub URL if it is already a GEE Python script
        output = github_url + ''.join(map(str, lines))
    else:             # deal with JavaScript

        header = github_url + "import ee \n" + math_import_str + qgis_import_str
        function_defs = []
        output = header + "\n"

        with open(in_file) as f:
            lines = f.readlines()

            print('Processing {}'.format(in_file))
            lines = check_map_functions(lines)

            for index, line in enumerate(lines):

                if ('/* color' in line) and ('*/' in line):
                    line = line[:line.index('/*')].lstrip() + line[(line.index('*/')+2):]
                
                if ("= function" in line) or ("=function" in line) or line.strip().startswith("function"):
                    bracket_index = line.index("{")
                    matching_line_index, matching_char_index = find_matching_bracket(
                        lines, index, bracket_index)

                    line = line[:bracket_index] + line[bracket_index+1:]
                    if matching_line_index == index:
                        line = line[:matching_char_index] + \
                            line[matching_char_index+1:]
                    else:
                        tmp_line = lines[matching_line_index]
                        lines[matching_line_index] = tmp_line[:matching_char_index] + \
                            tmp_line[matching_char_index+1:]

                    line = line.replace(" = function", "").replace(
                        "=function", '').replace("function ", '')
                    line = " " * (len(line) - len(line.lstrip())) + "def " + line.strip() + ":"
                elif "{" in line:
                    bracket_index = line.index("{")
                    matching_line_index, matching_char_index = find_matching_bracket(
                        lines, index, bracket_index)
                    if (matching_line_index == index) and (':' in line):
                        pass
                    elif ('for (' in line) or ('for(' in line):
                        line = convert_for_loop(line)
                        lines[index] = line
                        bracket_index = line.index("{")
                        matching_line_index, matching_char_index = find_matching_bracket(lines, index, bracket_index)
                        tmp_line = lines[matching_line_index]
                        lines[matching_line_index] = tmp_line[:matching_char_index] + tmp_line[matching_char_index+1:]
                        line = line.replace('{', '')

                if line is None:
                    line = ''

                line = line.replace("//", "#")
                line = line.replace("var ", "", 1)
                line = line.replace("/*", '#')
                line = line.replace("*/", '#')
                line = line.replace("true", "True").replace("false", "False")
                line = line.replace("null", "{}")
                line = line.replace(".or", ".Or")
                line = line.replace(".and", '.And')
                line = line.replace(".not", '.Not')
                line = line.replace('visualize({', 'visualize(**{')
                line = line.replace('Math.PI', 'math.pi')
                line = line.replace('Math.', 'math.')
                line = line.replace('= new', '=')
                line = line.rstrip()

                if line.endswith("+"):
                    line = line + " \\"
                elif line.endswith(";"):
                    line = line[:-1]             
                
                if line.lstrip().startswith('*'):
                    line = line.replace('*', '#')

                if (":" in line) and (not line.strip().startswith("#")) and (not line.strip().startswith('def')) and (not line.strip().startswith(".")):
                    line = format_params(line)

                if index < (len(lines) - 1) and line.lstrip().startswith("#") and lines[index+1].lstrip().startswith("."):
                    line = ''               

                if line.lstrip().startswith("."):
                    if "#" in line:
                        line = line[:line.index("#")]
                    output = output.rstrip() + " " + "\\" + "\n" + line + "\n"
                else:
                    output += line + "\n"

    out_dir = os.path.dirname(out_file)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(out_file, 'w') as f:
        f.write(output)

    return output


def js_to_python_dir(in_dir, out_dir=None, use_qgis=True, github_repo=None):
    """Converts all Earth Engine JavaScripts in a folder recursively to Python scripts

    Args:
        in_dir (str): The input folder containing Earth Engine JavaScripts.
        out_dir (str, optional): The output folder containing Earth Engine Python scripts. Defaults to None.
        use_qgis (bool, optional): Whether to add "from ee_plugin import Map \n" to the output script. Defaults to True.
        github_repo (str, optional): GitHub repo url. Defaults to None.

    """
    if out_dir is None:
        out_dir = in_dir

    for in_file in Path(in_dir).rglob('*.js'):
        out_file = os.path.splitext(in_file)[0] + ".py"
        out_file = out_file.replace(in_dir, out_dir)
        js_to_python(in_file, out_file, use_qgis, github_repo)
    # print("Ouput Python script folder: {}".format(out_dir))


# def dict_key_str(line):

#     keys = """asFloat bands bestEffort bias collection color connectedness crs eeObject eightConnected format gain gamma
#               geometry groupField groupName image iterations kernel labelBand leftField magnitude max maxDistance
#               maxOffset maxPixels maxSize minBucketWidth min name normalize opacity palette patchWidth
#               radius reducer referenceImage region rightField scale selectors shown sigma size source
#               strokeWidth threshold units visParams width""".split()
#     for key in keys:
#         if ":" in line and key in line:
#             line = line.replace(key + ":", "'" + key + "':")
#     return line

if __name__ == '__main__':

    ## Converts an Earth Engine JavaScript to Python script.
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_file_path = os.path.join(root_dir, "JavaScripts/Image/NormalizedDifference.js")  # change this path to your JavaScript file
    out_file_path = os.path.splitext(in_file_path)[0] + ".py"
    js_to_python(in_file_path, out_file_path)
    print("Python script saved at: {}".format(out_file_path))

    # Converts all Earth Engine JavaScripts in a folder recursively to Python scripts.
    in_dir = os.path.join(root_dir, "JavaScripts")
    out_dir = os.path.join(root_dir, "JavaScripts")
    js_to_python_dir(in_dir, out_dir, use_qgis=True)
    print("Python scripts saved at: {}".format(out_dir))


    # parser = argparse.ArgumentParser()
    # parser.add_argument('--input', type=str,
    #                     help="Path to the input JavaScript file")
    # parser.add_argument('--output', type=str,
    #                     help="Path to the output Python file")
    # args = parser.parse_args()
    # js_to_python(args.input, args.output)



