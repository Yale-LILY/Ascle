import sys, os
import glob
from pathlib import Path

#files2rouge from https://github.com/pltrdy/files2rouge
import files2rouge

class folder2rouge:
    def __init__(self, summaries_dir, references_dir):
        self.summaries_dir = summaries_dir
        self.references_dir = references_dir
        self.allsummaries_path = os.path.join(summaries_dir, 'allsummaries.txt')
        self.allreferences_path = os.path.join(summaries_dir, 'allreferences.txt')

    def compile_all_summaries(self):
        
        allsummaries_file = open(self.allsummaries_path, 'w')
        allreferences_file = open(self.allreferences_path, 'w')

        for filepath in glob.glob(os.path.join(self.summaries_dir, '*.sum')):
            fname = Path(filepath).stem
            ref_path = os.path.join(self.references_dir, fname + ".tgt")
            if not os.path.exists(ref_path):
                print("Target file " + fname + ".tgt does not exist")
                continue
            with open(filepath) as fs:
                summary = fs.readlines()
                if len(summary) < 1:
                    print(fname + " has no summary")
                    continue
                with open(ref_path) as fr:
                    abstract = fr.readlines()
                    if len(summary)!=len(abstract):
                        print("summary and reference " + fname + " must have same number of lines")
                        if os.path.exists(self.allsummaries_path): os.remove(self.allsummaries_path)
                        if os.path.exists( self.allreferences_path): os.remove(self.allreferences_path)
                        sys.exit()
                    for line in abstract:
                        allreferences_file.write("%s\n" % line)
                for line in summary:
                    allsummaries_file.write("%s\n" % summary)           
                
        allsummaries_file.close()
        allreferences_file.close()

    def run(self, saveto=None, keep_compiled_files=False):
        self.compile_all_summaries()
        files2rouge.run(self.allsummaries_path, self.allreferences_path, saveto=saveto)
        if not keep_compiled_files:
            if os.path.exists(self.allsummaries_path): os.remove(self.allsummaries_path)
            if os.path.exists(self.allreferences_path): os.remove(self.allreferences_path)

