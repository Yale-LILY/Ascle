import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)
from ehrkit import ehrkit
from getpass import getpass

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import json

# this should be the row ID in NOTEEVENTS
doc_id=int(input("MIMIC Document ID: "))

USERNAME = input('DB_username: ')
PASSWORD = getpass('DB_password: ')

ehrdb = ehrkit.start_session(USERNAME, PASSWORD)
text = ehrdb.get_document(doc_id)

predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/ner-model-2020.02.10.tar.gz")
prediction=predictor.predict(
  text
)

with open(str(doc_id)+'.json', 'w', encoding='utf-8') as f:
	json.dump(prediction, f, ensure_ascii=False, indent=4)