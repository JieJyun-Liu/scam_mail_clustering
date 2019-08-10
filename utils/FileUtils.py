
'''
	Date: 2019/08/10
	Author: Eleven
	Description: CRUD / Preprocess of raw data.
'''

import tarfile
import numpy as np
import re
import json

from bs4 import BeautifulSoup
from os.path import join

from src.EmailInfo import EmailInfo
from configs import cfg

''' 
	* File Name: 419scam_emails_201401
	* Data:
			#dt,#subject,#url,"<ul>#commands</ul>",
			"<blockquote>#content</blockquote>" (Raw data of email_body, email_from, email_replyto, email_timestamp - dup),
			#scam_type,"#email_body","#email_from",<#email_replyto>,
			"#email_timestamp",
			#email_subject (duplicate with #subject - ignore)
'''
def load_dataset(file_name):
	yearMonth = file_name.split("/")[-1].split("_")[2]

	with open(file_name, 'r') as f:
		f.readline()
		lines = f.read().split(yearMonth)
		errorParsingCount = 0

		for i in range(len(lines)):
			emailInfoDict = parse_raw_data_to_dict(lines[i], yearMonth, i)
			if emailInfoDict is not None:
				emailInfoObj = EmailInfo(emailInfoDict)
				write_data_into_json(file_name, emailInfoObj.toJson())
			else:
				errorParsingCount = errorParsingCount + 1

		print("### [" + file_name + "] # of error parsing: ", errorParsingCount, "/", len(lines))

def write_data_into_json(file_name, json_data):
	outfile_name = join(cfg.output_dir, file_name.split("/")[-1]) + '.json'
	with open(outfile_name, 'a') as f:
		json.dump(json_data, f)
		f.write('\n')
	f.close()
		
# Parse raw data to EmailInfo attributes.
def parse_raw_data_to_dict(raw_data, yearMonth, id):
	attributes = {}
	try:
		firstThreeTuples = raw_data.split(",",3)
		attributes['date'] = yearMonth + firstThreeTuples[0]
		attributes['subject'] = firstThreeTuples[1]
		attributes['url'] = firstThreeTuples[2]
		
		tmp = firstThreeTuples[3].split("blockquote")[2].split(",",2)
		attributes['scam_type'] = tmp[1]
		attributes['email_body'] = tmp[2].split("\",")[0][1:].replace('\n','')
		attributes['email_body'] = preprocess_email_body(attributes['email_body'])
		attributes['email_from'] = tmp[2].split("\",")[1][1:]
		
		if(len(attributes['email_from'].split(",", 2)) > 1):
			emailInfo = attributes['email_from'].split(",", 2)
			attributes['email_from'] = extract_email(emailInfo[0])
			attributes['email_replyto'] = extract_email(emailInfo[1])
			attributes['email_timestamp'] = extract_time(emailInfo[-1])
		else:
			attributes['email_from'] = extract_email(attributes['email_from'])
			attributes['email_replyto'] = extract_email(tmp[2].split("\",")[2].split(",")[0])
			attributes['email_timestamp'] = extract_time(tmp[2].split("\",")[2].split(",\"")[-1])

		attributes['id'] = attributes['date'] + "_" + str(id)
	except:
		return None

	return attributes


# TODO: Replace punctuation to <EOS> I will do this at ana.
def preprocess_email_body(text):
	# remove all text in (), []
	text = re.sub("[\(\[].*?[\)\]]", "", text)
	text = remove_non_ascii(text)

	return text

def remove_all_non_word_chars(text):
	return re.sub(r'[^\w\s]', '', text)

def remove_non_ascii(text):
	text = re.sub(r'[^\x00-\x7F]', ' ', text)
	return re.sub('\s+', ' ', text).strip()

def remove_html_tags(markup):
	soup = BeautifulSoup(markup)
	text = soup.get_text()

	return re.sub('\s+', ' ', text).strip()

def extract_email(text):
	text = re.sub(r'[\\\"]', '', text)
	text = re.sub("<i>.*?</i>", "", text)
	try:
		email = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', text)[0]
	except:
		email = ''

	name = remove_all_non_word_chars(text.replace(email, "")).strip()

	return {"name": name, "email": email}

# Output: 31 Dec 2013 21:32:55 +0530
def extract_time(text):
	text = re.sub("[\(\[].*?[\)\]]", "", text)
	datetime = text.split(",")[-1].strip()
	return datetime