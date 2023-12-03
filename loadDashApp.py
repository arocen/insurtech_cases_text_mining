import topicwizard
from dotenv import load_dotenv
import os
from wordcloud import WordCloud

load_dotenv()

wordcloud = WordCloud(font_path = os.environ.get("font_path"))
app = topicwizard.load_app(filename=os.environ.get("dashFile"))
app.run(debug=False, port=8050)