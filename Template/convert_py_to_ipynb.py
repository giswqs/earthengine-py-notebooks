import os
import glob
import datetime
from pathlib import Path


def extract_py_script(in_file):
    start_index = 0
    with open(in_file) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if 'from ee_plugin import Map' in line:
                start_index = index

                i = 1
                while True:
                    line_tmp = lines[start_index + i].strip()
                    if line_tmp != '':
                        return lines[start_index + i:]
                    else:
                        i = i + 1


def extract_template(in_file, template_file):
    out_py_path = str(in_file).split('/')
    index = out_py_path.index('qgis-earthengine-examples')
    # print(out_py_path)
    # print(index)
    out_py_script_path = '/'.join(out_py_path[index+1:])

    header = []
    footer = []

    template_lines = []
    header_end_index = 0
    footer_start_index = 0

    with open(template_file) as f:
        template_lines = f.readlines()
        for index, line in enumerate(template_lines):
            # line = line.replace('Template/template', out_py_script_path[:-3])
            # header.append(line)
            if '## Add Earth Engine Python script' in line:
                header_end_index = index + 5
            if '## Display Earth Engine data layers' in line:
                footer_start_index = index - 3

    header = template_lines[:header_end_index]
    footer = ['\n'] + template_lines[footer_start_index:]

    header_tmp = []
    for line in header:
        line = line.replace('Template/template', out_py_script_path[:-3])
        header_tmp.append(line)
    header = header_tmp

    # print("header end index: {}".format(header_end_index))
    # print(template_lines[:header_end_index])
    # print(template_lines[footer_start_index:])

    # out_py_script_path = os.path.join(root_dir, out_py_script_path)
    line = 'https://github.com/giswqs/earthengine-py-notebooks/tree/master/Template/template.ipynb'
    line = line.replace('Template/template', out_py_script_path[:-3])
    # print(line)
    return header, footer



root_dir = os.path.dirname(os.path.dirname(__file__))
template_path = os.path.join(root_dir, 'Template/template.py')
# print(template_path)

template_lines = []
with open(template_path) as f:
    template_lines = f.readlines()
# print(len(template_lines))

py_script_dir = os.path.join(root_dir, 'Python')
py_script_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'qgis-earthengine-examples')
print(py_script_dir)

files = list(Path(py_script_dir).rglob('*.py'))[1:]
# print(files)

changed_files = []
changed_files.append('extract_image_by_polygon.py')
changed_files.append('filtering_feature_collection.py')
changed_files.append('filter_range_contains.py')

# loop through dem files to create contours
i = 1
for index, filename in enumerate(files):
    
    # print(filename)
    out_py_path = str(filename).split('/')
    index = out_py_path.index('qgis-earthengine-examples')
    # print(out_py_path)
    # print(index)
    out_py_script_path = '/'.join(out_py_path[index+1:])
    out_py_script_path = os.path.join(root_dir, out_py_script_path)
    # print(out_py_script_path)

    out_dir = os.path.dirname(out_py_script_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    header, footer = extract_template(filename, template_path)
    content = extract_py_script(filename)

    if content != None:
        out_text = header + content + footer 
    else:
        out_text = header + footer

    with open(out_py_script_path, 'w') as f:
        f.writelines(out_text)

    # basename = os.path.basename(out_py_script_path)
    # if basename in changed_files:
    #     print(basename)
    #     out_nb_path = out_py_script_path.replace('.py', '.ipynb')
    #     cmd = 'ipynb-py-convert ' + out_py_script_path + ' ' + out_nb_path
    #     print(os.popen(cmd).read().rstrip())
    #     cmd2 = 'jupyter nbconvert --to notebook --execute ' + out_nb_path + ' --inplace'
    #     print(os.popen(cmd2).read().rstrip())

    # modTimesinceEpoc = os.path.getmtime(out_py_script_path)
    # modificationTime = datetime.datetime.utcfromtimestamp(modTimesinceEpoc).strftime('%Y-%m-%d %H:%M:%S')
    # print("Last Modified Time : ", modificationTime , ' UTC')    
    
    out_nb_path = out_py_script_path.replace('.py', '.ipynb')
    print('{}/{}: {}'.format(i, len(files), out_nb_path))
    i = i + 1
    
    cmd = 'ipynb-py-convert ' + out_py_script_path + ' ' + out_nb_path
    # print(cmd)
    print(os.popen(cmd).read().rstrip())

    cmd2 = 'jupyter nbconvert --to notebook --execute ' + out_nb_path + ' --inplace'
    print(os.popen(cmd2).read().rstrip())


