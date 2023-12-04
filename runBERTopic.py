from dotenv import load_dotenv
import os
import loadTxt, cutTxtFiles
import jieba
from sentence_transformers import SentenceTransformer
import umap
from hdbscan import HDBSCAN
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic import BERTopic

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

def load_cut_results(path=os.environ.get("cut_results"), divPattern=divPattern)->list[str]:
    '''Load saved cut results into a list of cut cases.'''
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
        cut_results = contents.split(divPattern)

    return cut_results


def vis_clustering(umap_data, save_path):
    '''Visualize clustering and save png.'''
    result = pd.DataFrame(umap_data, columns=['x', 'y'])
    result['labels'] = cluster.labels_
    fig, ax = plt.subplots(figsize=(25, 15))
    outliers = result.loc[result.labels == -1, :]
    clustered = result.loc[result.labels != -1, :]
    plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=0.05)
    plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=0.05, cmap='hsv_r')
    plt.colorbar()

    # Display the plot
    # plt.show()

    # Save the plot as an image file
    fig.savefig(save_path)
    return


def load_stopwords(stopwords_path:str)->list[str]:
    '''Load stopwords as a list.'''
    stopwords = []
    with open(stopwords_path, "r", encoding="utf-8") as f:
        for line in f:
            # Remove leading and trailing whitespace (including newline characters)
            cleaned_line = line.strip()
    
            # Append the cleaned line to the list
            stopwords.append(cleaned_line)
    return stopwords


def show_and_save(figure, save_path):
    '''Take figure as input and show it, save it to the save_path'''
    figure.show()
    figure.write_html(save_path)
    print(f"A figure saved to {save_path}")
    return




# # Load txt
# root_dir = os.environ.get("cases_parent_directory")
# txt_paths = loadTxt.get_txt_paths(root_dir)
# cases = loadTxt.load_txt_files(txt_paths)

# # Cut into words
# my_dict_path = ...
# cut_cases = cut(cases)
# # Save results
# save_cut_results(cut_cases)

# Load cut txt files
cut_folder = os.environ.get("cutTxtFiles")
cut_cases = cutTxtFiles.loadCutTxtFiles(cut_folder)

# Load word embeddings
sentence_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = sentence_model.encode(cut_cases, show_progress_bar=True)


# Reduce dimensions

# When documents are too few, umap may occur error.
# You can't use spectral initialisation (init='spectral', the default) when n_components is greater or equal to the number of samples.
# Since dataset has 204 samples this is the issue. You can either use 203 instead of 204, or use init='random' for the 204 dimensional case as a workaround.
umap_embeddings = umap.UMAP(n_neighbors=15,
                            n_components=5,
                            min_dist=0.0,
                            metric='cosine',
                            random_state=42).fit_transform(embeddings)


# Clustering
cluster = HDBSCAN(min_cluster_size=5,
                  metric='euclidean',
                  cluster_selection_method='eom', 
                  prediction_data=True).fit(umap_embeddings)


# Visualize clustering

# Load stopwords from 2 files.
stopwords_path1 = os.environ.get("my_stopwords_path")
stopwords_path2 = os.environ.get("other_stopwords_path")
stopwords1 = load_stopwords(stopwords_path1)
stopwords2 = load_stopwords(stopwords_path2)
stopwords = stopwords1 + stopwords2


# Tokenize
token_pattern1 = '([\w\+]+)'                     # 确保'产品+服务'被匹配到
token_pattern2 = r'(?<!\w)(?=\w\w)[\w\+]+(?!\w)' # 确保'产品+服务'被匹配到，且不匹配单个字符长度的词
vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words=stopwords, min_df=2, token_pattern=token_pattern2)


ctfidf_model = ClassTfidfTransformer()

# Run BERTopic model
# nr_topics="auto" 表示自动合并相似主题
topic_model = BERTopic(language="multilingual", 
                       vectorizer_model=vectorizer_model, 
                       top_n_words=30, 
                       calculate_probabilities=True, 
                       ctfidf_model=ctfidf_model, 
                       verbose=True,
                       n_gram_range=[1, 3])
topic = topic_model.fit(cut_cases, embeddings)



# Save model
model_save_path = os.environ.get("bertopic_model_save_path")
topic_model.save(model_save_path)



# Visualize results
print(topic.get_topic_info())    # 查看各主题信息

# visualize_topics1 = topic_model.visualize_topics()
# 可视化结果保存至html中，可以动态显示信息
# visualize_topics1.write_html(os.environ.get("vis_topic"))

# 将所有主题保存到Excel
# excel_save_path = os.environ.get("excel_save_path")
# topic_model.get_topic_info().to_excel(excel_save_path)
# print(f"All information saved to {excel_save_path}")

# 层级可视化
hierarchy_fig = topic_model.visualize_hierarchy()
show_and_save(hierarchy_fig, os.environ.get("hierarchy_topics_vis"))

# Visualize Hierarchical Documents
# hierarchical_topics = topic_model.hierarchical_topics(cut_cases)
# hierarchical_doc_fig = topic_model.visualize_hierarchical_documents(cut_cases, hierarchical_topics, embeddings=umap_embeddings, width=2000, height=1000)
# show_and_save(hierarchical_doc_fig, os.environ.get("heirarchy_docs"))