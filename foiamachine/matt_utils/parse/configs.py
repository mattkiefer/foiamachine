from datetime import datetime


now                  = datetime.now()  
now_str              = now.strftime('%Y-%m-%d-%R')
repo_path            = '/home/ubuntu/foiamachine/repo/foiamachine/'
outfile_path         = repo_path + 'output_data/'
outfile_name         = 'data.csv'
outfile_file_path    = outfile_path + outfile_name
error_log_path       = repo_path + 'data_output_logs/'
error_log_name       = 'error.log'
error_log_file_path  = error_log_path + error_log_name + now_str 
formats              = ['csv', 'xls', 'xlsx','pdf'] # last split on '.'
