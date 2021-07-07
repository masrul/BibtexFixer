import bibtexparser
import  io 
import requests 
from pylatexenc.latexencode import unicode_to_latex 
lines=open("bib.bib","r").readlines() 

string='' 
for line in lines:
    string  +=line.strip() 

with io.StringIO(string) as FH:
    bib_database = bibtexparser.load(FH)

doi=bib_database.entries[0]["doi"].split("/")[-2:]
doi = "/".join(doi)
print(doi)

base_url = "http://api.crossref.org/"
url = "{}works/{}/transform/application/x-bibtex"
url = url.format(base_url, doi)
print(url)
r = requests.get(url)
found = False if r.status_code != 200 else True
bib = r.content
bib = str(bib, "utf-8")
bib = unicode_to_latex(bib,unknown_char_policy='ignore',non_ascii_only=True)
print(bib)
