import random
import sys, os
import re
import shutil
import time
import argparse
from getpass import getpass

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#print(sys.path)
from ehrkit import ehrkit
from ehrkit.summarizers import Lexrank

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(sys.path)

parser = argparse.ArgumentParser()

parser.add_argument('--saveto', action='store', metavar='dir_path', type=str, help='Directory path to store produced summaries', required=True)
parser.add_argument('--ntrain', action='store', type=int, help='First n number of patients to train on. default 100')
parser.add_argument('--ntest', action='store', type=int, help='First n number of patients to produce summaries for. default 20.')
parser.add_argument('--threshold', action='store', type=float, help="default 0.1")

args = parser.parse_args()

saveto_dir = args.saveto
ntrain = args.ntrain or 100
ntest = args.ntest or 20
threshold = args.threshold or 0.1

if not os.path.isdir(saveto_dir):
    print('The saveto directory specified does not exist')
    sys.exit()

# Number of patients in PATIENTS.
NUM_PATIENTS = 46520

start=time.time()
#ehrdb = ehrkit.start_session(USERNAME, PASSWORD)
ehrdb = ehrkit.start_session(input("User?"), getpass("Password?"))
ehrdb.get_patients(ntrain)
ehrdb.get_note_events()

#SUMMARY BY NOTE
print("----Summaries by note----")
new_dir = "script_summary_bynote"
new_dir_path = os.path.join(saveto_dir, new_dir)
if os.path.exists(new_dir_path):
    shutil.rmtree(new_dir_path)
os.mkdir(new_dir_path)

allnotes = [note[1] for patient in ehrdb.patients.values() for note in patient.note_events]
lxr = Lexrank(allnotes, threshold=threshold)

for i, patient in enumerate(ehrdb.patients.values()):
    patient_id = patient.id
    notewise_sum = []
    for note_id, note in patient.note_events:
        if len(note) < 10:
            summary_len = 2
        elif len(note) > 100:
            summary_len = len(note)//20
        else:
            summary_len = len(note)//10
        note_summary = lxr.get_summary(note, summary_size=summary_len)
        notewise_sum.extend(note_summary)
    joined_summary = "\n".join(notewise_sum)
    summary_path = os.path.join(new_dir_path, str(patient_id) + ".sum")
    with open(summary_path, 'w') as sum:
        sum.write(joined_summary)
    if i == ntest:
        break
end1 = time.time()
print("Runtime " + str(end1 - start))

#SUMMARY BY ENTIRE HISTORY
print("----Summaries by entire history----")
new_dir = "script_summary_byetirehistory"
new_dir_path = os.path.join(saveto_dir, new_dir)
if os.path.exists(new_dir_path):
    shutil.rmtree(new_dir_path)
os.mkdir(new_dir_path)

allnotes_bypatient = {}

for patient in ehrdb.patients.values():
    allnotes_bypatient[patient.id] = []
    for note in patient.note_events:
        allnotes_bypatient[patient.id].extend(note)

lxr2 = Lexrank(list(allnotes_bypatient.values()), threshold=threshold)

for i, patient_id in enumerate(allnotes_bypatient):
    if len(allnotes_bypatient[patient_id]) < 4:
        summary_len = 1
    else:
        summary_len = len(allnotes_bypatient[patient_id])//4
    summary = lxr2.get_summary(allnotes_bypatient[patient_id], summary_size=summary_len)
    joined_summary = "\n".join(summary[0])
    summary_path = os.path.join(new_dir_path, str(patient_id) + ".sum")
    with open(summary_path, 'w') as sum:
        sum.write(joined_summary)
    if i == ntest:
        break
end2 = time.time()
print("Runtime " + str(end2-end1))
print("------------------------------")
print("total runtime " + str(end2-start))

