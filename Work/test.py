from pylatexenc.latexencode import unicode_to_latex 
lines=open("test.bib","r").readlines() 



for line in lines:
    print(unicode_to_latex(line,unknown_char_policy="ignore"))
