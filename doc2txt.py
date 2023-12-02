# Convert docx files to txt.

import pypandoc
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


def docx2txt(docx_paths:list):
    '''Convert docx files to txt.'''
    for path in docx_paths:
        txt_path = path.split(".")[0] + ".txt"
        try:
            output = pypandoc.convert_file(path, 'plain', outputfile=txt_path)
            assert output == ""
        except:
            print("Error convering doc file in this path:", path)
    return


# Replace 'your_root_directory' with the actual root directory
root_directory = os.environ.get("cases_parent_directory")
docx_paths = find_docx_files(root_directory)

# Print the paths of all .docx files
# for docx_path in docx_paths:
#     print(docx_path)

# Convert to txt
docx2txt(docx_paths)
