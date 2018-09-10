Since Kindle e-readers unfortunately don't come with any Norwegian (Bokmål) dictionaries, here is a simple way for creating one based on [dict.cc](deno.dict.cc) data.
The resulting dictionary can be used like any other Kindle dictionary.
It contains ca. 24.800 uninflected NB > DE entries plus (regularly and irregularly) inflected forms for most verbs, nouns and adjectives.

With slight changes, these files can be used to create other bilingual dictionaries based on [other dict.cc language pairs](https://browse.dict.cc/).

# Creating and Installing the Dictionary

1. Get the source data from www1.dict.cc/translation_file_request.php and save it as `data/dict.cc_no_de.tsv`.

2. Convert the TSV file into an appropriately formatted HTML file:
```
python transform.py > NB_DE_dict.html
```

3. Install [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) and use it to convert the dictionary into a `MOBI` file. The conversion requires the following files:

- `NB_DE_dict.opf`: Contains information on the files used for `MOBI` conversion and general metadata about the dictionary.
- `NB_DE_dict.html`: Contains the actual dictionary entries.
- `NB_DE_dict.jpeg`: The cover image (useless, but required for creating the `MOBI` file).

```
kindlegen.exe NB_DE_dict.opf -c2 -verbose -dont_append_source
```

4. (Optional) Use the [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261) to preview the dictionary.
Note that this only allows you to view the dictionary as if it were a regular book, but you unfortunately cannot try it out on an actual book in preview mode.

5. Copy the `MOBI` file to the directory `documents/dictionaries/` on your Kindle.
You may need to restart the device afterwards (especially if you are updating the dictionary).


To uninstall, go to `documents/dictionaries/` and delete `NB_DE_dict.mobi` as well as `NB_DE_dict.sdr/`.

# Building Dictionaries for Other Languages

1. In the [`OPF`](/NB_DE_dict.opf) file, update the dictionary title, languages and all relevant file names.

2. If the dictionary data is **not** in the [dict.cc format](/data/dict.cc/README.md), either re-format it accordingly or change the way the file is parsed in [`transform.py`](/transform.py).

3. Create a class that can generate inflected forms and that extends the `Inflector` class ([`inflector.py`](/inflector.py)). Use it as `Inflector` class in [`transform.py`](/transform.py).

4. Follow the steps above for creating & installing a new dictionary.

# Features / To Do

- [ ] Generate inflections (nouns, adjectives, verbs).
  - [x] Regular inflections
  - [x] Irregular inflections
  - [ ] Multi-token entries
- [ ] Deal with parentheses and ellipses in Norwegian entries.
- [x] Merge entries for identical Norwegian words (e.g. `blomsterbutikk`).
  - [ ] Extend this to `[kvinnelig]` entries.
- [ ] Deal with phrases/sentences?
  - [ ] Deal with complex entries such as `dråpen {m} som fikk begeret til å renne over (sjelden: flyte over)`.


# References and Data

- [Dict.cc data](https://www1.dict.cc/translation_file_request.php)
- [Norsk Ordbank in Norwegian Bokmål 2005](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-5)
- [Amazon Kindle Publishing Guidelines](https://s3.amazonaws.com/kindlegen/AmazonKindlePublishingGuidelines.pdf).
This document describes how to create files that can be converted into `MOBI` files.
There is also a [section on creating dictionaries](https://s3.amazonaws.com/kindlegen/AmazonKindlePublishingGuidelines.pdf#page=71).
- [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) is used for creating `MOBI` files.
  - Sample files: http://kindlegen.s3.amazonaws.com/samples.zip. They give an impression of what `OPF`/`HTML` files should look like so they can be converted into `MOBI` files.
- [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261)
