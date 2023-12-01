# Convert docx files to txt.

import docx2txt
import glob
from dotenv import load_dotenv
import os

load_dotenv()

directory = glob.glob(os.environ.get(""))

for file_name in directory:
    with open(file_name, 'rb') as infile:
        with open(file_name[:-5]+'.txt', 'w', encoding='utf-8') as outfile:
            doc = docx2txt.process(infile)
            outfile.write(doc)

print("=========")
print("All done!")