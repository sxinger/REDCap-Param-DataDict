import csv #https://stackoverflow.com/questions/62139040/python-csv-module-vs-pandas
import re

class redcap_template:
    
    infolder = './templates/'
    outfolder = './instruments/'

    def __init__(self, template, subject, subject_idx=1, start_pos='<#', end_pos='#>'):
        self.template = template
        self.placeholder = start_pos + '[^(' + start_pos + ')]*' + end_pos
        self.subject = subject
        self.subject_idx = subject_idx
        self.subjectnowhite = re.sub(r"\s+", "", subject)

    def modify_template(self):
        # csv file name
        filename_r = self.infolder + self.template + '.csv'
        filename_w = self.outfolder + self.template + '_' + self.subjectnowhite + '.csv'
        
        # initializing the titles and rows list
        cols = []
        rows = []
        
        # open one csv file in read mode and another in write mode
        with open(filename_r, 'r') as infile, open(filename_w, 'w', newline='') as outfile:
            # create a csv reader and a writer object
            r = csv.reader(infile, delimiter = ',')
            w = csv.writer(outfile, delimiter = ',')

            # extract field names through first row
            cols = next(r)
            # write new header to outfile
            w.writerow(cols)
             
            # Iterate over each row in the csv using reader object
            for row in r:
                # update parametrized string portion everywhere
                row_update = [re.sub(self.placeholder, self.subject, str(row_item)) for row_item in row]
                # modify Variable/Field Name
                row_update[0] = row[0] + '_' + str(self.subject_idx)
                # modify Branching Logic corresponding to updated Variable/Field name
                row_update[11] = re.sub('\]', '_' + str(self.subject_idx) + ']', row[11])
                # write to output file
                w.writerow(row_update)


