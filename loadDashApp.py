import topicwizard
from dotenv import load_dotenv
import os

load_dotenv()


app = topicwizard.load_app(filename=os.environ.get("dashFile"))
app.run(debug=False, port=8050)