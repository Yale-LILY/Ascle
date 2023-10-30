ROOT_EHR_DIR = '/lada2/lily/zl379/Year4/EHRTest/MedGen/tutorials/' # set your root MedGen directory here (with the '/' at the end)

import sys
import os
sys.path.append(os.path.dirname(ROOT_EHR_DIR))

OUTPUT_DATA_PATH = ROOT_EHR_DIR + 'data/output_data/'
MIMIC_PATH = ROOT_EHR_DIR + 'data/mimic_data/'



from mimic_icd9_coding.coding_pipeline import codingPipeline
from mimic_icd9_coding.utils.mimic_data_preparation import run_mimic_prep


run_mimic_prep(output_folder = OUTPUT_DATA_PATH, mimic_data_path= MIMIC_PATH)

print("Building basic tfidf pipeline")
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=100, verbose=True)
# Switch max_iter to 100 for better results, but to run for the first time 10 is good
my_mimic_pipeline = codingPipeline(verbose=True, model=clf, data_path = OUTPUT_DATA_PATH)
print("Pipeline complete")

# Let's check out the auroc
auroc = my_mimic_pipeline.auroc
print("Auroc is {:.2f}".format(auroc))


# Here we load the data into the pipeline, this function simply saves the data, we don't want to save the data automatically because it uses more memory
my_mimic_pipeline.load_data()
df = my_mimic_pipeline.data


# We run the algorithm and see that at least for this example our model is pretty good
pred = my_mimic_pipeline.predict(df['TEXT'].iloc[10])
true = df['TARGET'].iloc[10]
print("Predicted ICD9 codes: {}".format(pred))
print("True ICD9 codes: {}".format(true))
