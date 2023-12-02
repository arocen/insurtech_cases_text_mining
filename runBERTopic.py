from dotenv import load_dotenv
import os
import loadTxt
import jieba

load_dotenv()

# Set proxy
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

divPattern = "\nThis is a case divider.\n"

def cut(cases:list[str], my_dict_path=None)->list[str]:
    '''Cut cases into words.'''

    if my_dict_path:
        # Load user dict
        jieba.load_userdict(my_dict_path)

    cut_cases = []
    for case in cases:
        tokens = [token for token in jieba.cut(case)]
        result = ' '.join(tokens)
        cut_cases.append(result)
    return cut_cases


def save_cut_results(cut_cases:list[str], save_path=os.environ.get("cut_results"), divPattern=divPattern):
    '''Save cut result list into one txt file.'''

    with open(save_path, "w", encoding="utf-8") as f:
        for i in range(len(cut_cases)):
            f.write(cut_cases[i])
            if i != len(cut_cases) - 1:
                f.write(divPattern)
    return

def load_cut_results():
    # To-do

    return


# Load txt
root_dir = os.environ.get("cases_parent_directory")
txt_paths = loadTxt.get_txt_paths(root_dir)
cases = loadTxt.load_txt_files(txt_paths)

# Cut into words
my_dict_path = ...
cut_cases = cut(cases)
# Save results
save_cut_results(cut_cases)


# Load word embeddings

# Reduce dimensions

# Clustering

# Visualize clustering

# Load stopwords
# Tokenize

# Run BERTopic model
# Save model

# Visualize results