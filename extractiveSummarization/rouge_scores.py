import sys, os
import argparse

from summarizers.evaluate import folder2rouge

parser = argparse.ArgumentParser()

parser.add_argument('--summaries', action='store', metavar='path', type=str, help='directory path containing summaries', required=True)
parser.add_argument('--references', action='store', metavar='path', type=str, help='directory path containing target references', required=True)
parser.add_argument('--save', action='store', metavar='path', type=str, help='file path for saving scores produced')

args = parser.parse_args()

summaries_dir = args.summaries
references_dir = args.references
saveto_file_path = args.save

if not os.path.isdir(summaries_dir):
    print('The summaries directory specified does not exist')
    sys.exit()

if not os.path.isdir(references_dir):
    print('The references directory specified does not exist')
    sys.exit()

if saveto_file_path and not os.access(os.path.dirname(saveto_file_path), os.W_OK):
    print('Invalid file path for saving')

rouge = folder2rouge(summaries_dir, references_dir)
rouge.run(saveto=saveto_file_path)
