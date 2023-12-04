import os
import jieba
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()


def cutTxtFiles(folder, dest_folder, dictinoary=os.environ.get("dict1")):
    '''Cut txt files in a same folder'''

    jieba.load_userdict(dictinoary) # This may be invalid. Go check results.
    filenames = [f for f in os.listdir(folder) if f.endswith(".txt")]
    filepaths = [os.path.join(folder, filename) for filename in filenames]
    
    for path in tqdm(filepaths):
        basename = os.path.basename(path)
        dst = os.path.join(dest_folder, basename)
        with open(path, 'r', encoding="utf-8") as f1:
            case = f1.read()
            tokens = [token for token in jieba.cut(case)]
            result = ' '.join(tokens)
            result = result.replace("\n", " ")
            with open(dst, 'w', encoding='utf-8') as f2:
                f2.write(result)
    return

def loadCutTxtFiles(parent_folder)->list[str]:
    '''Load txt files in a same parent folder.'''
    filenames = [f for f in os.listdir(parent_folder) if f.endswith(".txt")]
    filepaths = sorted([os.path.join(parent_folder, filename) for filename in filenames])

    cases = []
    for path in filepaths:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            cases.append(content)
    
    return cases

# folder = os.environ.get("txtFiles")
# dest_folder = os.environ.get("cutTxtFiles")
# cutTxtFiles(folder, dest_folder)