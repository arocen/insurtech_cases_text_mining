# Visualize BERTopic with topicwizard
from bertopic import BERTopic
import topicwizard
import os
from dotenv import load_dotenv
import loadTxt

load_dotenv()

# Chinese font added in source code of topicwizard. Caution if it needs update.


# Load corpus
root_dir = os.environ.get("cases_parent_directory")
txt_paths = loadTxt.get_txt_paths(root_dir)
cases = loadTxt.load_txt_files(txt_paths)

# Load BERTopic model from saved pickle file
model_path = os.environ.get("bertopic_model_save_path")
model = BERTopic.load(model_path)

pipeline = topicwizard.bertopic_pipeline(model)
topicwizard.visualize(pipeline=pipeline, corpus=cases)