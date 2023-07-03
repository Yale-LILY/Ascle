# De-Identification

## Testing de-identification software package using gold standard corpus
Download gold standard corpus [here](https://physionet.org/content/deidentifiedmedicaltext/1.0/).

Download deidentification software package [here](https://www.physionet.org/content/deid/1.1/).

Copy id.text from the directory of gold standard corpus to the directory of software package. 

Make sure that you have [perl](https://www.perl.org) installed. 

Run the following command to generate output file id.phi 
```sh
perl deid.pl id deid.config
```
Performance statistics can be derived by running the following command.
```sh
perl runStat.pl id.deid id.phi
```
For example, for the gold standard corpus, the performance should be the following.
```sh
==========================

Num of true positives = 1720

Num of false positives = 546

Num of false negatives = 59

Sensitivity/Recall = 0.967

PPV/Specificity = 0.748

==========================
```

## De-identify any text
Check software package page for more information about the ```deid``` package and how to configure the tool. We provide a simple example for demonstration purpose here.

Download ```test.text``` here to software package directory.

Open ```deid.config``` in text editor, comment out ```Gold standard comparison = 1``` and uncomment ```Gold standard comparison = 0``` to use output mode.

Use the command of the format ```perl deid.pl input_file config``` to generate output file input\_file.phi. Note that input\_file should have the extension text but the extension should be omitted in the command. For example, we have the input file as test.text here, but we use the following command where input file is notated as ```test```.
```sh
perl deid.pl test deid.config
```
Output files:
- ```test.phi```: contains the numerical spans of sensitive fields
- ```test.info```: contains the neumerical spans of sensitive fields AND corresponding tokens AND types
- ```test.res```: scrubbed text with sensitive fields removed
