# Files

- `NB_DE_dict.opf`: contains information on the files used for MOBI conversion and general metadata about the dictionary
- `NB_DE_dict.html`: contains the actual dictionary entries
- `NB_DE_dict.jpeg`: cover image (useless, but required for creating the MOBI file)
- `data/dict.cc_no_de.tsv`: contains entries from dict.cc (NO-DE) in the following format:

```
# comment
Norwegian\tGerman\t(POS)\t(comment)
```

Norwegian (and German) entries can contain optional gender/number information and comments:

```
entry {gender} <comment> [comment]
```

# Creating and Installing the Dictionary

```
python transform.py > NB_DE_dict.html
kindlegen.exe NB_DE_dict.opf -c2 -verbose -dont_append_source
```

Copy the MOBI file to the directory `documents/dictionaries/` on your Kindle.
Especially if you are updating the dictionary, you may need to restart the device afterwards.

To uninstall, go to `documents/dictionaries/` and delete `NB_DE_dict.mobi` as well as `NB_DE_dict.spr\`.

# To Do

- Generate inflections (nouns, adjectives, verbs).
  - regular inflections
  - irregular inflections
- Deal with parentheses and ellipses in Norwegian entries.
- Merge entries for identical Norwegian words (e.g. 'blomsterbutikk').
- Deal with phrases/sentences?
- Deal with complex entries such as 'dråpen {m} som fikk begeret til å renne over (sjelden: flyte over)'.

# References
- [Dict.cc data](https://www1.dict.cc/translation_file_request.php)
- [Amazon Kindle Publishing Guidelines](https://s3.amazonaws.com/kindlegen/AmazonKindlePublishingGuidelines.pdf#page=71) (version 2018.2)
- [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) (version 2.9)
  - sample files: http://kindlegen.s3.amazonaws.com/samples.zip
- [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261) (version 3.25)
