# IPython log file

import csv
d14 = []
for row in csv.DictReader(open('output_data/data.csv','r')):
    print row['agency_name']
    break
for row in csv.DictReader(open('output_data/salaries.csv','r')):
    print row
    break
for row in csv.DictReader(open('output_data/salaries.csv','r')):
    print row['agency']
    break
d15 = []
d15 = {}
for row in csv.DictReader(open('output_data/salaries.csv','r')):
    if row['agency'] not in d15:
        d15['agency'] = 0
    d15['agency'] += 1
    
sum(d15[x] for x in d15)
d15
for row in csv.DictReader(open('output_data/salaries.csv','r')):
    if row['agency'] not in d15:
        d15['agency'] = 0
    d15[row['agency']] += 1
    
for row in csv.DictReader(open('output_data/salaries.csv','r')):
    if row['agency'] not in d15:
        d15[row['agency']] = 0
    d15[row['agency']] += 1
    
len(d15)
sum(d15[x] for x in d15)
d15
count = 0
for x in d15:
    count += d15[x]
    
count
get_ipython().magic(u'logstart data_counts.py')
get_ipython().magic(u'll output_data/')
d14 = {}
head output_data/2014.csv
for row in csv.DictReader(open('output_data/2014.csv','r')):
        if row['Employer'] not in d14:
                d14['Employer'] = 0
            d14[row['Employer']] += 1
        
for row in csv.DictReader(open('output_data/2014.csv','r')):
    if row['Employer'] not in d14:
        d14['Employer'] = 0
    d14[row['Employer']] += 1
    
for row in csv.DictReader(open('output_data/2014.csv','r')):
    if row['Employer'] not in d14:
        d14[row['Employer']] = 0
    d14[row['Employer']] += 1
    
len(d14)
missing_agencies = [x for x in d14 if x not in d15]
len(missing_agencies)
missing_agencies
from matt_utils.responses.response_report import *
for ma in missing_agencies:
    a = Agency.objects.get(name=a)
    print a, [r.id for r in a.request_set.all()]
    
for ma in missing_agencies:
    a = Agency.objects.get(name=ma)
    print a, [r.id for r in a.request_set.all()]
    
for ma in missing_agencies:
    try:
        a = Agency.objects.get(name=ma)
        print a, [r.id for r in a.request_set.all()]
    except:
        print 'failed to lookup', ma
        
for ma in missing_agencies:
    try:
        a = Agency.objects.get(name=ma)
        print a, [r.id for r in a.request_set.all() if r.status != 'X']
    except:
        print 'failed to lookup', ma
        
