# Convert docx files to txt.

import docx2txt
import glob
from dotenv import load_dotenv
import os

load_dotenv()



def find_docx_files(root_dir):
    '''
    Get all paths of docx files given a root directort.
    '''
    docx_files = []
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:

            # Types that are filtered out: jpg, jpeg, bmp, mov, png, pptx, wmv, mp4, pdf
            if filename.endswith('.docx') or filename.endswith('.doc'):
                docx_files.append(os.path.join(foldername, filename))
    return docx_files

# Replace 'your_root_directory' with the actual root directory
root_directory = os.environ.get("cases_parent_directory")
docx_paths = find_docx_files(root_directory)

# Print the paths of all .docx files
for docx_path in docx_paths:
    print(docx_path)

