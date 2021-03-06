#!/usr/bin/env python
####################################################################################################
#
# More information: https://macmule.com/2016/01/11/portfolio-parsing-logs-to-find-troublesome-files
#
# GitRepo: https://github.com/macmule/Portfolio/
#
# License: http://macmule.com/license/
#
####################################################################################################

import logging
import os
import re
import smtplib
import sys
from email.mime.text import MIMEText

# Get Script Name
scriptName =  os.path.basename(sys.argv[0])

# Variables to set manually
serverLogPath = '' 		# Path to Portfolio' Server.log file
mediaDelegateLogPath = '' 	# Path to Portfolio's media-delegate file
logFilePath = '' 		# Path to write this scripts log file to
mailServer = '' 
mailFrom = ''
mailTo = ''

# Set log to name of script
logFileFullPath = os.path.join(logFilePath, os.path.basename(sys.argv[0]) + '.log')

# Empty lists
badFormatFiles = []
corruptFiles = []

# Configure Logging
logging.basicConfig(filename=logFileFullPath,level=logging.INFO,format='%(message)s',filemode='w')

# Send email		
def sendEmail(statusMessage):
	# Open the logFile as email contents
	logFile = open(logFileFullPath, 'rb')
	# Create a text/plain message
	msg = MIMEText(logFile.read())
	logFile.close()

	# Email From, To & Subject
	msg['From'] = mailFrom
	msg['To'] = mailTo
	msg['Subject'] = scriptName + ": " + statusMessage

	# Send the email
	s = smtplib.SMTP(mailServer)
	s.sendmail(mailFrom, mailTo, msg.as_string())
	s.quit()

# Try & read the server.log file
try:
	# Read contents pof the log file
	serverLog = open(serverLogPath, 'r')
# If the file cannot be found
except:
	# If the file cannot be found error
	logging.error('----- Cannot find server.log: %s' % serverLogPath)

# Try & read the media-delegate.log file
try:
	# Read contents pof the log file
	mediaDelegateLog = open(mediaDelegateLogPath, 'r')
# If the file cannot be found Portfolio
except:
	# If the file cannot be found error
	logging.error('----- Cannot find media-delegate.log: %s' % mediaDelegateLogPath)

# Check that the above variables have been defined
try:
	mediaDelegateLog
	serverLog
# If not it will be due to us not being able to find the logs
except:
	# Send email & exit the script
	sendEmail('Logs not found')

# Try & read the contents of serverLog
try:
	# For each entry in the log
	for entry in serverLog:
		# If the entry contains "error processing file"
		if "error processing file" in entry:
				# Grab the files path & add to the badFormatFiles list
				badFormatFiles.append(re.split('::|java', entry)[1])
			
	# Remove duplicates from the list & order
	badFormatFiles = sorted(set(badFormatFiles))
except:
	# If not defined, move on
	pass

# Try & read the contents of the mediaDelegateLog 
try:
	# For each entry in the log
	for entry in mediaDelegateLog:
		# If the entry contains "SourceFile:"
		if entry.strip().startswith('"SourceFile":'):
				# Grab the files path & add to the corruptFiles list
				corruptFiles.append(entry.split(':')[1].rstrip().strip())
		elif 'No workfile produced from' in entry:
			# Grab the files path & add to the corruptFiles list
			corruptFiles.append(entry.split('No workfile produced from')[1].strip().split('Ghostscript output')[0])

	# Remove duplicates from the list & order
	corruptFiles = sorted(set(corruptFiles))
except:
	# If not defined, move on
	pass

# If the list has any entries, log them
if len(badFormatFiles):
	logging.info('----- %s Bad Format Files ------' % (len(badFormatFiles)))
	logging.info('')
	# Log each entry as a new line
	for i in badFormatFiles:
		logging.info(i)
	logging.info('')

# If the list has any entries, log them	
if len(corruptFiles):
	logging.info('----- %s Corrupt Files -----' % (len(corruptFiles)))
	logging.info('')
	# Log each entry as a new line
	for i in corruptFiles:
		logging.info(i)

# If we've found any bad files in the log, email it
if len(badFormatFiles) or len(corruptFiles):
	sendEmail('%s Bad files & %s Corrupt files found' % (len(badFormatFiles), len(corruptFiles)))
