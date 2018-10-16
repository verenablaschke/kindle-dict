Since Kindle ebook readers unfortunately don't come with any Norwegian (Bokmål) dictionaries, here is a simple way for creating one based on [dict.cc](deno.dict.cc) data.
The resulting dictionary can be used like any other Kindle dictionary (in-document word look-up (also of inflected forms), vocabulary trainer, browsing the dictionary).
It contains ca. 24.800 uninflected NB > DE entries plus (regularly and irregularly) inflected forms for most verbs, nouns and adjectives.

With slight changes, these files can be used to create bilingual dictionaries based on [other dict.cc language pairs](https://browse.dict.cc/).

# Creating and Installing the Dictionary

1. Get the dictionary source data from [dict.cc's download page](www1.dict.cc/translation_file_request.php) and save it as `data/dict.cc/dict.cc.tsv`.

2. Get the files `lemma.txt` and `fullformsliste.txt` from [Språkbankens ressurskatalog](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-5) and save them in `data/spraakbanken/`.
If, **instead** you would only like to use automatically generated regular inflection forms, open [`transform.py`](/transform.py) and change `inflector = SpraakbankenInflector()` to `inflector = RegularInflector()`.

3. Get a list of Bokmål stop words (for instance via [ranks.nl](https://www.ranks.nl/stopwords/norwegian)) and save it as `data/stopwords/stopwords.txt` (one word per line).

4. Convert the TSV file into an appropriately formatted HTML file:
```
python transform.py > NB_DE_dict.html
```

5. Install [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) and use it to convert the dictionary into a `MOBI` file. The conversion requires the following files:

- `NB_DE_dict.opf`: Contains information on the files used for `MOBI` conversion and general metadata about the dictionary.
- `NB_DE_dict.html`: Contains the actual dictionary entries.
- `NB_DE_dict.jpeg`: The cover image (useless, but required for creating the `MOBI` file).

```
kindlegen.exe NB_DE_dict.opf -c2 -verbose -dont_append_source
```

6. (Optional) Use the [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261) to preview the dictionary.
Note that this only allows you to view the dictionary as if it were a regular book, but you unfortunately cannot try it out on an actual book in preview mode.

7. Copy the `MOBI` file to the directory `documents/dictionaries/` on your Kindle.
You may need to restart the device afterwards (especially if you are updating the dictionary).


If you are using Windows, you can execute steps 4 and 5 at once by running [`run.bat`](/run.bat). 


To uninstall, go to `documents/dictionaries/` and delete `NB_DE_dict.mobi` as well as `NB_DE_dict.sdr/`.

## Building Dictionaries for Other Languages

1. In the [`OPF`](/NB_DE_dict.opf) file, update the dictionary title, languages and all relevant file names.

2. If the dictionary data is **not** in the [dict.cc format](/data/dict.cc/README.md), either re-format it accordingly or change the way the file is parsed in [`transform.py`](/transform.py).

3. Create a class that can generate inflected forms and that extends the `Inflector` class ([`inflector.py`](/inflector.py)). Use it as `Inflector` class in [`transform.py`](/transform.py).

4. Follow the steps above for creating & installing a new dictionary.

# Features / To Do

- [ ] Generate inflections (nouns, adjectives, verbs).
  - [x] Regular inflections (from Språkbanken where available, otherwise generated according to regular inflection paradigms)
  - [x] Irregular inflections (from Språkbanken's list)
  - [ ] Genitive forms
  - [ ] Multi-token entries (in particular: phrasal verbs)
- [ ] Deal with parentheses and ellipses in Norwegian entries.
- [x] Merge entries for identical Norwegian words (e.g. `blomsterbutikk`).
  - [x] Extend this to `[kvinnelig]` entries.
- [x] Show relevant multi-token entries when looking up single-token entries (e.g. the entry for `blå` (blue) also contains information on the phrase `å være i det blå` (to be in the dark), which is also a distinct entry).
  - I don't check for POS tags when creating these references; therefore, there are some false positives here. Since I find them quite interesting, I don't plan on refining this.
- [ ] Extend the dictionary.
  - Note: Unless compound nouns are in the dictionary, it's not possible to look them (or their constituents) up. Since I cannot change the way the dictionary is used to look up entries, there is not much I can do.
  - [ ] Look into adding Wiktionary data. Specifically from the English or Norwegian versions of Wiktionary.
  - The best (monolingual) Norwegian dictionary I know is https://ordbok.uib.no/, whose database I unfortunately cannot download and use. But maybe there are other good monolingual dictionaries out there that I can use?
  - Written Danish and Bokmål are very similar. If I can find a large DA>EN or DA>DE dictionary, it could be worth looking into adding these entries where no Norwegian entries are present.


# References and Data

- [Dict.cc data](https://www1.dict.cc/translation_file_request.php).
NB > DE translation data.
- [Norsk Ordbank in Norwegian Bokmål 2005](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-5) (Språkbankens ressurskatalog).
Lists of Norwegian lemmas and inflected forms.
- [Norwegian stop words](https://www.ranks.nl/stopwords/norwegian) (Ranks NL).
- [Amazon Kindle Publishing Guidelines](https://s3.amazonaws.com/kindlegen/AmazonKindlePublishingGuidelines.pdf).
This document describes how to create files that can be converted into `MOBI` files.
There is also a [section on creating dictionaries](https://s3.amazonaws.com/kindlegen/AmazonKindlePublishingGuidelines.pdf#page=71).
- [KindleGen](https://www.amazon.com/gp/feature.html?docId=1000765211) is used for creating `MOBI` files.
  - Sample files: http://kindlegen.s3.amazonaws.com/samples.zip. They give an impression of what `OPF`/`HTML` files should look like so they can be converted into `MOBI` files.
- [Kindle Previewer](https://www.amazon.com/gp/feature.html/?docId=1000765261)
