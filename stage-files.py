#
# This script can be executed with a command like the following:
#
#    python stage-files.py \ 
#        --baseDownloadUrl http://yourserver.com/yourfolder/ \
#        --localTempFolder /tmp/ \                                                           noms-site$
#        --bucket your-bucket \
#        --fileList file1.zip,file2.csv,file3.zip,file4.csv
#

import os, sys, getopt
import boto3
import urllib.request
import shutil
import logging

session = boto3.Session(profile_name='usgs')
s3_client = session.client('s3')

help_string = 'stage-files.py --baseDownloadUrl <value> --localTempFolder <value> --bucket <value> --fileList <comma delimited list of file names to download>'

def main(argv):
	"""main entry point into the script

	:param argv command line parameters in the format --baseDownloadUrl <value> --localTempFolder <value> --bucket <value> --fileList <comma delimited list of file names to download>
	"""
	# parse command line parameters
	try:
		opts, args = getopt.getopt(argv,"",["help","baseDownloadUrl=","localTempFolder=","bucket=","fileList="])
	except getopt.GetoptError:
		print('arguments are invalid')
		print(help_string)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--help':
			print(help_string)
			sys.exit()
		elif opt == '--baseDownloadUrl':
			base_url = arg
		elif opt == '--localTempFolder': 
			temp_folder = arg
		elif opt == '--bucket':
			bucket_name = arg
		elif opt == '--fileList':
			files = arg.split(',')

	# Loop through and process each of the requested files
	for file in files:
		process_file(file, base_url, bucket_name, temp_folder)

def download_file(url, tmp_file):
	"""Download a file from a url

	:param url: url of the file to download
	:param tmp_file: the temporary file to create
	:return True if the file was downloaded, False otherwise
	"""
	try:
		with urllib.request.urlopen(url) as response, open(tmp_file, 'wb') as out_file:
		    shutil.copyfileobj(response, out_file)
	except:
		e = sys.exc_info()
		logging.error(e[0])
		logging.error(e[1])
		return False
	return True

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def process_file(file_name, base_url, bucket_name, temp_folder):
	"""Process a file

	:param file_name the file to process
	:param base_url the base url to download the file from
	:param bucket_name the name of the s3 bucket to upload to
	:param temp_folder the name of the temp folder to use
	"""
	print('  downloading file ' + file_name)
	if (download_file(base_url + file_name, temp_folder + file_name)):
		print('  downloaded ' + file_name)
		print('  uploading file ' + file_name)
		if (upload_file(temp_folder + file_name, bucket_name, file_name)):
			print('  uploaded ' + file_name)

if __name__ == "__main__":
   main(sys.argv[1:])
