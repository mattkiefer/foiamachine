from configs import *
from csvkit.utilities.in2csv import In2CSV
import csv

def csvify(att):
    """
    return csv
    open for reading after
    any conversions
    """
    last_four = att.file.name[-4:]

    if last_four in formats:
        if last_four == '.csv':
            infile = open(att.file.path,'r')
            return csv.reader(infile)
        if last_four in ('.xls','xlsx'):
            return convert_xls(att)

    else:
        return None
     

def convert_xls(att):
    if att.file.name[-4:] in ('.xls','xlsx'):
        att_path = att.file.path
        args = [att_path]
        # put the xls->csv output in a tmp file
        tmp_file_name = 'tmp.csv'
        tmp_file = open(tmp_file_name,'w')
        In2CSV(args,output_file=tmp_file).main()
        tmp_file.close()
        infile =  open(tmp_file_name,'r')
        return csv.reader(infile)

