"""
various logging stuff
"""
import csv
from configs import *




def init_error_log(error_log_file_path):
    """
    sets up error log
    """
    error_file = open(error_log_file_path,'w') # don't need old errors
    error_csv = csv.writer(error_file)
    return error_csv

error_log = init_error_log(error_log_file_path)


def log_invalid_line(line, attachment, error_log=error_log):
    """
    each invalid line 
    gets written to this file with
    attachment ID
    """
    line['attachment_id'] = attachment.id
    line = [(key, line[key]) for key in line]
    error_log.writerow(line)


def read_in_outfile(outfile):
    """
    reads in outfile
    to use when checking if line
    was already run
    """
    return [x for x in open(outfile,'r')] # eventually want to remove timestamp[:-1] to check if line processed


outfile_read = read_in_outfile(outfile_file_path)


def check_if_line_processed(line,outfile):
    """
    checking if line was 
    already processed prior
    ... doesn't check timestamp
    """
    # TODO: need to select columns to check and use appending data outfile
    if line in outfile:
        return True




