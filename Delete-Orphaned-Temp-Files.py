#!/usr/bin/env python
####################################################################################################
#
# More information: https://macmule.com/2016/01/16/deleting-portfolios-orphaned-temp-files
#
# GitRepo: https://github.com/macmule/Portfolio/
#
# License: http://macmule.com/license/
#
####################################################################################################

import logging
import os
import shutil
import smtplib
import sys
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText

# Get Script Name
scriptName =  os.path.basename(sys.argv[0])

# Variables
logDir = '/Applications/Extensis/Portfolio Server/logs/'
tmpDir = '/private/var/tmp/'
workDir = '/Applications/Extensis/Portfolio Server/data/work/'
chosenDaysAgo = date.today() - timedelta(5)
logFileFullPath = os.path.join('/private/var/tmp/', os.path.basename(sys.argv[0]) + '.log')
mailServer = ''
mailFrom = ''
mailTo = ''

# Empty Lists
oldWorkFolders = {}
oldMagickFiles = {}
oldLogFiles = {}

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

# Configure Logging
logging.basicConfig(filename=logFileFullPath,level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',filemode='w')

###
#
# logDir
#
###

# For each item in the direcory logDir
for item in os.listdir(logDir):
	# If the file does not being with a . or end with .lock
	if not item.startswith('.') and not item.endswith('.lock') and not item.endswith('.log'):
		# Get the files path
		logPath = os.path.join(logDir, item)
		# Get filess modified time
		modDate = datetime.fromtimestamp(os.stat(logPath).st_mtime)
		# If the date of the modified time is over chosenDaysAgo
		if (chosenDaysAgo > modDate.date()):
			# Add to dict
			oldLogFiles[logPath] = str(modDate)

# If we have oldLogFiles to delete
if len(oldLogFiles):
	# Log the number
	logging.warning('----- %s Log files deleted' % (len(oldLogFiles)))
	# Try so we stop if there's an issue
	try:
		# For each folder in the oldLogFiles dict
		for fileName, fileDate in oldLogFiles.items():
			# Log the file we're deleting, including mod date & path
			logging.info('Deleting %s %s' % (fileDate, fileName))
			# Finally, delete the file
			os.remove(fileName)
	# if there's an issue
	except:
		# Status message to use as subject for sendMail funtion
		statusMessage = 'Deleting %s %s' % (fileDate, fileName)
		# Advise that no devices are to be deleted
		logging.error('-------- ' + statusMessage + ' --------')
		sendEmail(statusMessage)

###
#
# tmpDir
#
###

# For each item in the direcory tmpDir
for item in os.listdir(tmpDir):
	# If the files starts with magick-
	if item.startswith('magick-'):
		# Get he files path
		magickPath = os.path.join(tmpDir, item)
		# Get filess modified time
		modDate = datetime.fromtimestamp(os.stat(magickPath).st_mtime)
		# If the date of the modified time is yesterday
		if (date.today() > modDate.date()):
			# Add to dict
			oldMagickFiles[magickPath] = str(modDate)

# If we have oldWorkFolders to delete
if len(oldMagickFiles):
	# Log the number
	logging.warning('----- %s Magick files deleted' % (len(oldMagickFiles)))
	# Try so we stop if there's an issue
	try:
		# For each file in the oldWorkFolders dict
		for fileName, fileDate in oldMagickFiles.items():
			# Log the file we're deleting, including mod date & path
			logging.info('Deleting %s %s' % (fileDate, fileName))
			# Finally, delete the file
			os.remove(fileName)
	# if there's an issue
	except:
		# Status message to use as subject for sendMail funtion
		statusMessage = 'Deleting %s %s' % (fileDate, fileName)
		# Advise that no devices are to be deleted
		logging.error('-------- ' + statusMessage + ' --------')
		sendEmail(statusMessage)

###
#
# workDir
#
###

# For each directory in the directory workDir
for item in os.listdir(workDir):
	# Get the folders path
	folderPath = os.path.join(workDir, item)
	# Get folders modified time
	modDate = datetime.fromtimestamp(os.stat(folderPath).st_mtime)
	# If the date of the modified time is yesterday
	if (date.today() > modDate.date()):
		# Add to dict
		oldWorkFolders[folderPath] = str(modDate)

# If we have oldWorkFolders to delete
if len(oldWorkFolders):
	# Log the number
	logging.warning('----- %s Work folders deleted' % (len(oldWorkFolders)))
	# Try so we stop if there's an issue
	try:
		# For each folder in the oldWorkFolders dict
		for folderName, folderDate in oldWorkFolders.items():
			# Log the folder we're deleting, including mod date & path
			logging.info('Deleting %s %s' % (folderDate, folderName))
			# Finally, delete the folder
			shutil.rmtree(folderName)
	# if there's an issue
	except:
		# Status message to use as subject for sendMail funtion
		statusMessage = 'Deleting %s %s' % (folderDate, folderName)
		# Advise that no devices are to be deleted
		logging.error('-------- ' + statusMessage + ' --------')
		sendEmail(statusMessage)

###
#
# Email if we have any files or folders found to delete
#
###

# If we've found any bad files in the log, email it
if len(logDir) or len(tmpDir) or len(workDir):
	sendEmail('Old files found')
