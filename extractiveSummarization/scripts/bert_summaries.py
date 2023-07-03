import sys, os
import glob
import shutil
from pathlib import Path
import time
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(sys.path)

from summarizer import Summarizer

parser = argparse.ArgumentParser()

parser.add_argument('--source', action='store', metavar='dir_path', type=str, help='directory path containing source', required=True)
parser.add_argument('--saveto', action='store', metavar='dir_path', type=str, help='directory path to store produced summaries', required=True)
parser.add_argument('--threshold', action='store', type=float, help="default 0.03")
parser.add_argument('--ratio', action='store', type=int, help='ratio of summary size to source size (based on number of sentences). default 0.05')
parser.add_argument('--n', action='store', metavar='ndocs', type=int, help='number of documents to produce summaries of. default 2.')

args = parser.parse_args()

source_dir = args.source
saveto_dir = args.saveto
ratio = args.ratio or 0.05
ndocs = args.n or 2

if not os.path.isdir(source_dir):
    print('The source directory specified does not exist')
    sys.exit()

if not os.path.isdir(saveto_dir):
    print('The saveto directory specified does not exist')
    sys.exit()

start=time.time()
documents = {}
model = Summarizer() 

for i, filepath in enumerate(glob.glob(os.path.join(source_dir, '*.src'))):
	with open(filepath) as fp:
		fname = Path(filepath).stem
		documents[fname] = fp.read()
	summary = model(documents[fname], ratio=ratio)
	
	joined_summary = ''.join(summary).replace('\n', '')
	summary_path = os.path.join(saveto_dir, fname + ".sum")
	with open(summary_path, 'w') as sum:
		sum.write(joined_summary)
	if i == ndocs - 1:
		break
end = time.time()
print("----Bert summary----")
# print(saveto_dir)
print("Num docs: " + str(ndocs) + " sentence ratio: " + str(ratio))
print("Runtime " + str(end - start))
