import os
import jieba
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()


def cutTxtFiles(folder, dest_folder):
    '''Cut txt files in a same folder'''
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

folder = os.environ.get("txtFiles")
dest_folder = os.environ.get("cutTxtFiles")
cutTxtFiles(folder, dest_folder)