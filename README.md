Since Kindle e-readers unfortunately don't come with any Norwegian (Bokmål) dictionaries, here is a simple way for creating one based on [dict.cc](deno.dict.cc) data.
The resulting dictionary can be used like any other Kindle dictionary.
It contains ca. 24.800 uninflected NB > DE entries plus (regularly) inflected forms for most verbs, nouns and adjectives.

With slight changes, these files can be used to create other bilingual dictionaries based on [other dict.cc language pairs](https://browse.dict.cc/).

# Creating and Installing the Dictionary

1. Get the source data from www1.dict.cc/translation_file_request.php and save it as `data/dict.cc_no_de.tsv`.

2. Convert the TSV file into an appropriately formatted HTML file:
```
python transform.py > NB_DE_dict.html
```

3. Install [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) and use it to convert the OPF and HTML files into a MOBI file:

```
kindlegen.exe NB_DE_dict.opf -c2 -verbose -dont_append_source
```

4. (Optional) Use the [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261) to preview the dictionary.
Note that this only allows you to view the dictionary as if it were a regular book, but you unfortunately cannot try it out on an actual book in preview mode.

5. Copy the MOBI file to the directory `documents/dictionaries/` on your Kindle.
You may need to restart the device afterwards (especially if you are updating the dictionary).


To uninstall, go to `documents/dictionaries/` and delete `NB_DE_dict.mobi` as well as `NB_DE_dict.sdr/`.


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

# Features / To Do

- [ ] Generate inflections (nouns, adjectives, verbs).
  - [x] Regular inflections
  - [ ] Irregular inflections
  - [ ] Multi-token entries
- [ ] Deal with parentheses and ellipses in Norwegian entries.
- [x] Merge entries for identical Norwegian words (e.g. `blomsterbutikk`).
  - [ ] Extend this to `[kvinnelig]` entries.
- [ ] Deal with phrases/sentences?
  - [ ] Deal with complex entries such as `dråpen {m} som fikk begeret til å renne over (sjelden: flyte over)`.


# References
- [Dict.cc data](https://www1.dict.cc/translation_file_request.php)
- [Amazon Kindle Publishing Guidelines](https://s3.amazonaws.com/kindlegen/AmazonKindlePublishingGuidelines.pdf#page=71) (version 2018.2)
- [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) (version 2.9)
  - sample files: http://kindlegen.s3.amazonaws.com/samples.zip
- [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261) (version 3.25)
