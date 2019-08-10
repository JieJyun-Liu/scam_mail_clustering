# Scam Mail Clustering
## Data (English / with punctuations)

#### Attributes
1. dt: date (Reported date?)
2. subject
3. url: html file name
4. comments: comments of this email (with html tags)
5. content: (~ email_body, email_from, email_replyto, email_timestamp)
6. scam_type: types (ex. next-to-kin, 419)
7. email_body: email content (text)
8. email_from: Name <email>
9. email_replyto: <email>
10. email_timestamp: email date (ex. Fri, 31 Jan 2014 22:10:10 +0700)
11. email_subject: subject (dup with 2)

#### Split
1. Train / Val (2014-2018, 60)
2. Test (2019, 4)

## Target
## Flow
### Data cleaning: parse raw data to json (drop 4, 5 & 11)

```
	{
		"url": "00810674.1.htm",
		"email_body": "FBI Headquarters ...",
		"scam_type": "419", 
		"email_from": { 
						"name": "fbi ag***t",
						"email": ""
					},
		"email_timestamp": "31 Dec 2017 17:48:34 +0200",
		"date": "20180101",
		"email_replyto": {
							"name": "",
							"email": "atm****@rep***tative.com"
						  },
		"id": "20180101_1",
		"subject": "Re: ..."
	}

```

### 
Ref. 
[1] 419scam.org