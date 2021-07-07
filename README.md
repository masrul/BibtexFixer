BibtexFixer 
-----
A command line tool for  removing duplicate entries from Bibtex file. 



### Installation
---
```bash 
git clone https://github.com/masrul/BibtexFixer 
cd BibtexFixer
pip install . 
```

### Usage
---

BibtexFixer [-h] -i  [-o]

+  -h, --help          show this help message and exit
+  -i , --inputFile    Name of the input file
+  -o , --outputFile   Name of the output file [Default: Clean.bib]
+  -r , --ref-tex      If provided, then bibtex will contain relevent citations

**Example:** 
```bash 
BibtexFixer -i Examples/references.bib -o clean.bib 
```
