## SciSpacy

In this tutorial, we will use [scispacy](https://allenai.github.io/scispacy/) for various extraction tasks on MIMIC notes. Here we use named entity extraction as a detailed example.
##### Named Entities
```get_named_entities.py```

Arguments:
- ```--mimic_dir```: directory to mimic data that includes NOTEEVENTS.csv, default to data/mimic\_data in the tutorials directory
- ```--model```: spaCy model to use, default to en_core_sci_sm
- ```--row_id```: the row_id of the row whose NOTE field will be processed, default to 178
- ```--output_file```: output file to save identified named entities default to ./output_named_entities.txt

Commands:
```sh
python get_named_entities.py
python get_named_entities.py --model en_core_sci_scibert --row_id 174
```
*Remark: if running with custom model, need to download the corresponding model using ```pip install <model url>``` where model urls can be found [here](https://allenai.github.io/scispacy/).

A list of named entities will be written to the file specified by --ouput_file. 

##### Abbreviations
```get_abbreviations.py```
##### Hyponyms
```get_hyponyms.py```
##### Linked Entities
```get_linked_entities.py ```

The arguments for these 3 tasks are the same as get_named_entities.py. Use the following commands to run in default values.

```sh
python get_abbreviations.py 
python get_hyponyms.py
python get_linked_entities.py 
```

## Translation with MarianMT
We use [MarianMT](https://huggingface.co/transformers/model_doc/marian.html) to translate clinical notes to another language.

```get_translation.py```

Arguments:
- ```--mimic_dir```: directory to mimic data that includes NOTEEVENTS.csv, default to data/mimic\_data in the tutorials directory
- ```--target_language```: supported languages are {Spanish, French, Portuguese, Italian, Romanian, Malay_written_with_Latin, Mauritian_Creole, Haitian, Papiamento, Asturian, Catalan, Indonesian, Galician, Walloon, Occitan, Aragonese, Minangkabau}, default to Spanish
- ```--row_id```: the row_id of the row whose NOTE field will be processed, default to 178
- ```--output_file```: output file to save original and translated notes, default to ./output_translation.txt

Commands:
```sh
python get_translation.py
python get_translation.py --target_language French --row_id 2000 --output_file ./output_French.txt
```
