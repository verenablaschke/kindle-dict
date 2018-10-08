:: Use UTF-8 as encoding.
chcp 65001
set pythonioencoding=utf8
:: Conversion TSV > HTML.
python transform.py > NB_DE_dict.html
:: Conversion HTML/OPF > MOBI.
kindlegen.exe NB_DE_dict.opf -c2 -verbose -dont_append_source
