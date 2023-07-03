## Download and Parse PubMed Articles

PubMed is a corpus of over 30 million citations for biomedical literature from MEDLINE, life science journals, and online books. These scripts download and parse thousands of medical research papers from the[Open Access Subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/). 

##### Downloading Pubmed
To dowload the [Pubmed dataset](ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/) in XML format, run the following bash script:
```
> bash download_pubmed.sh
```
This shell script will a while to run, so we recommend running it in a separate Linux screen. It will parse the files to pubmed/xml/.

##### Parsing Pubmed Articles
From another directory, you can then parse each article to 3 plaintext files: one containing its abstract, one containing its body, and one containing both. For the body, you will choose to parse either the whole body or just its introduction section. Up to 757123 articles can be parsed using their whole bodies, and 45,655 with just their intros. 

```
> python parse_articles.py
Path to XML files: /PATH/TO/EHRKIT/pubmed/xml/
Path to parsed PubMed files: /PATH/TO/EHRKIT/pubmed/parsed_articles/
Parse the whole body section of each article or just the body introduction? [w=whole body, j=just intro]: j
Number of files to parse [press Enter to parse all]: 300
Number of files parsed: 100
Number of files parsed: 200
Number of files parsed: 300
Successfully parsed 300 files. 
```
All paragraphs with fewer than 20 words are removed. The parsed articles are in pubmed/parsed_articles/with_whole_bodies/ or pubmed/parsed_articles/with_just_intros/, depending on which type is selected. Inside this directory, the abstracts are in abstract/, the body sections are in body/, and the whole texts are in merged/.

In addition, it also generates a random summary of the same length as the abstract for each article. This creates a useful baseline for summarization models. These summaries are in random_summary/.

**/tests/pubmed_tests.py** runs unit tests on the parsed files and the original XML corpus. For example:
```
> python pubmed_tests.py t2.test2_4
Ratio of body to abstract length (with just body intros): 3.6

> python pubmed_tests.py t3.test3_2
Size of directory of articles with just body intros:
1002M	/PATH/TO/EHRKIT/pubmed/parsed_articles/with_just_intros

```