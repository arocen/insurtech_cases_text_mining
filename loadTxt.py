import os

def get_txt_paths(root_dir):
    '''Get paths of all txt files under a same root directory.'''

    txt_paths = []
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:

            # Types that are filtered out: jpg, jpeg, bmp, mov, png, pptx, wmv, mp4, pdf
            if filename.endswith('.txt'):
                txt_paths.append(os.path.join(foldername, filename))
    
    return txt_paths


# To-do: concatenate contents of txt files that are in a same parent folder while reading.
def load_txt_files(txt_paths):
    '''Load txt files given a list of txt paths.'''
    
    cases = []
    for path in txt_paths:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            cases.append(content)

    return cases