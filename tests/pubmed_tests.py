import os
import sys
import unittest

# XML_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pubmed', 'xml'))
# PARSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pubmed', 'parsed_articles'))
# XML_DIR = '/data/corpora/pubmed_xml_subset'
# PARSED_DIR = '/data/corpora/pubmed_parsed'

XML_DIR = '../pubmed/xml'
PARSED_DIR = '../pubmed/parsed_articles'

if not os.path.exists(XML_DIR):
    command = 'Error: Directory of PubMed XML files does not exist at ' + XML_DIR + '.'
    sys.exit(command)
if not os.path.exists(PARSED_DIR):
    command = 'Error: Directory of parsed PubMed articles does not exist at ' + PARSED_DIR + '.'
    sys.exit(command)


class tests(unittest.TestCase):
    def setUp(self):
        self.PARSED_DIR = PARSED_DIR
        self.XML_DIR = XML_DIR

class t1(tests):
    # Concerning number of articles in directories
    def test1_1(self):
        print("Number of articles whose introductions have been parsed:")
        command = 'ls ' + os.path.join(self.PARSED_DIR, 'with_just_intros', 'body') + ' | wc -l'
        os.system(command)

    def test1_2(self):
        print("Number of articles whose whole bodies have been parsed:")
        command = 'ls ' + os.path.join(self.PARSED_DIR, 'with_whole_bodies', 'body') + ' | wc -l'
        os.system(command)

    @unittest.skipIf("t1.test1_3" not in sys.argv, "Test 1_3 must be run explicitly due to runtime.")
    def test1_3(self):
        # Takes a few minutes
        print("Number of XML article files (takes a while to run):")
        command = 'find ' + self.XML_DIR + ' -type f | wc -l'
        os.system(command)


class t2(tests):
    # Concerning number of words in files
    def test2_1(self, write=True):
        counts = []
        body_dir = os.path.join(self.PARSED_DIR, 'with_just_intros', 'body')
        for file in os.listdir(body_dir)[:1000]:
            if file.endswith('.src'):
                with open(os.path.join(body_dir, file), "rt") as body_file:
                    data = body_file.read()
                    words = data.split()
                    counts.append(len(words))
        avg = round(sum(counts) / len(counts))
        if write:
            print("Average number of words in introductory section:", avg)
        return avg

    def test2_2(self, write=True):
        counts = []
        body_dir = os.path.join(self.PARSED_DIR, 'with_whole_bodies', 'body')
        for file in os.listdir(body_dir)[:1000]:
            if file.endswith('.src'):
                with open(os.path.join(body_dir, file), "rt") as body_file:
                    data = body_file.read()
                    words = data.split()
                    counts.append(len(words))
        avg = round(sum(counts) / len(counts))
        if write:
            print("Mean number of words in whole body section:", avg)
        return avg

    def test2_3(self, write=True, whole_body=False):
        counts = []
        if whole_body:
            abstract_dir = os.path.join(self.PARSED_DIR, 'with_whole_bodies', 'abstract')
        else:
            abstract_dir = os.path.join(self.PARSED_DIR, 'with_just_intros', 'abstract')
        for file in os.listdir(abstract_dir)[:1000]:
            if file.endswith('.tgt'):
                 with open(os.path.join(abstract_dir, file), "rt") as body_file:
                    data = body_file.read()
                    words = data.split()
                    counts.append(len(words))
        avg = round(sum(counts) / len(counts))
        if write:
            print("Mean number of words in abstract:", avg)
        return avg

    def test2_4(self):
        src_words = self.test2_1(write=False)
        tgt_words = self.test2_3(write=False)
        print("Ratio of body to abstract length (with just body intros):", round(src_words/tgt_words, 1))

    def test2_5(self):
        src_words = self.test2_2(write=False)
        tgt_words = self.test2_3(write=False, whole_body=True)
        print("Ratio of body to abstract length (with whole bodies):", round(src_words/tgt_words, 1))


class t3(tests):
    # Concerning sizes of directories
    @unittest.skipIf("t3.test3_1" not in sys.argv, "Test 3_1 must be run explicitly due to runtime.")
    def test3_1(self):
        print("Size of directory of articles with just body intros (takes a while to run):")
        command = 'du -sh ' + os.path.join(self.PARSED_DIR, 'with_just_intros')
        os.system(command)

    @unittest.skipIf("t3.test3_2" not in sys.argv, "Test 3_2 must be run explicitly due to runtime.")
    def test3_2(self):
        print("Size of directory of articles with whole bodies (takes a while to run):")
        command = 'du -sh ' + os.path.join(self.PARSED_DIR, 'with_whole_bodies')
        os.system(command)

    @unittest.skipIf("t3.test3_3" not in sys.argv, "Test 3_3 must be run explicitly due to runtime.")
    def test3_3(self):
        print("Size of XML file directory (takes a while to run):")
        command = 'du -sh ' + os.path.join(self.XML_DIR)
        os.system(command)


if __name__ == '__main__':
    unittest.main()