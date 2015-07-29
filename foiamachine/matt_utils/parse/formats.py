from configs import *
from csvkit.utilities.in2csv import In2CSV
import csv

def listify(att):
    """
    return data list
    of csv contents with 
    any conversions
    """
    ext = att.file.name.split('.')[-1]
    
    if ext in formats:
        if ext == 'csv':
            return listify_file(att.file.path)
        if ext in ('xls','xlsx'):
            try:
                return convert_xls(att)
            except:
                print 'csvify fail:', att.file.name 
                return None # TODO: investigate this
        else:
            print 'ext fail', att.file.name
    else:
        print 'format fail', att.file.name
        return None
     
def listify_file(csv_file_path):
    infile = open(csv_file_path,'r')
    incsv = csv.reader(infile)
    data = []
    for row in incsv:
        # rows with empty cells hopefully get tossed
        if len(','.join(row)) > 10:
            data.append(row)
    infile.close()
    #import ipdb; ipdb.set_trace()
    return data

def convert_xls(att):
    att_path = att.file.path
    args = [att_path]
    # put the xls->csv output in a tmp file
    tmp_file_name = 'tmp.csv'
    tmp_file = open(tmp_file_name,'w')
    In2CSV(args,output_file=tmp_file).main()
    tmp_file.close()
    return listify_file(tmp_file_name)
