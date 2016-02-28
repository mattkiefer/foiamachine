from configs import *
from csvkit.utilities.in2csv import In2CSV
import subprocess, csv


tmp_file_name = 'tmp.csv'


def listify(att):
    """
    return data list
    of csv contents with 
    any conversions
    """
    ext = att.file.name.split('.')[-1].lower()
    
    if ext in formats:
        if ext == 'pdf':
            return tabula_csv(att)
        if ext == 'csv':
            return listify_file(att.file.path)
        if ext in ('xls','xlsx'):
            try:
                return convert_xls(att)
            except Exception, e:
                print 'csvify fail:', att.file.name 
                print e
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
    tmp_file = open(tmp_file_name,'w')
    # In2CSV(args,output_file=tmp_file).main()
    # for some reason the python utility not working so well ...
    # this should also be a standard callback in human.py
    import subprocess
    subprocess.call(['in2csv',
        #'--format',att_path.split('.')[-1].lower(),
        att_path],stdout=tmp_file)
    tmp_file.close()
    return listify_file(tmp_file_name)


def tabula_csv(att,listify=True):
    from parse_attachments import get_attachment_agency
    args = [
                'tabula',
                '--spreadsheet', # use spreadsheet when there are gridlines
                '--pages=all',
                att.file.path,
               ] 
    csv_dir = '/home/ubuntu/foiamachine/repo/foiamachine/media/media/attachments/matthewlkiefer/pdfs/'
    try:
        agency_name = get_attachment_agency(att).name
    except:
        return
    # don't overwrite dupes
    file_name = csv_dir + agency_name + '.csv'
    outfile = open(file_name,'w')
    subprocess.call(args,stdout=outfile)
    outfile.close()
    if listify:
        return listify_file(file_name)
    return file_name
