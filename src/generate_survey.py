# https://csatlas.com/python-import-file-module/

outfolder = './instruments/'
outname = 'R01_ObesityCancerChemo_Shreoder-Neuner'
template = 'GPCDataReadinessSurvey'
domain_lst = ['NAACCR Registry Data','Pathologic Complete Response', 'Ejection Fraction']

# generate individual surveys
domain_lst_nowhite = []
for subject in domain_lst:
    subject_idx = domain_lst.index(subject) + 1
    survey = redcap_template(template,subject,subject_idx)
    survey.modify_template()
    domain_lst_nowhite.append(survey.subjectnowhite)

# integrate survey chunks into one
outfile = open(outfolder + template + '_' + outname + ".csv", "a", newline='')
# first file:
for line in open(outfolder + template + '_' + domain_lst_nowhite[0] + ".csv"):
    outfile.write(line)
# now the rest:  
domain_lst_nowhite.pop(0)  
for domain in domain_lst_nowhite:
    infile = open(outfolder + template + '_' + domain+".csv")
    next(infile) # skip the header
    next(infile) # skip first row, redundant info
    next(infile) # skip second row, redundant info
    for line in infile:
        # update form name
        outfile.write(line)
outfile.close()
