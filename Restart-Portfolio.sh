#!/bin/sh
####################################################################################################
#
# More information: https://macmule.com/2016/01/15/restarting-portfolios-services
#
# GitRepo: https://github.com/macmule/Portfolio/
#
# License: http://macmule.com/license/
#
####################################################################################################

#### Stop Portfolio

sudo launchctl unload /Library/LaunchDaemons/com.extensis.dam-server.web.admin.launchd.plist

sleep 5

sudo launchctl unload /Library/LaunchDaemons/com.extensis.portfolio.server.elasticsearch.plist

sleep 5

sudo launchctl unload /Library/LaunchDaemons/com.extensis.portfolio.server.media.delegate.plist

sleep 5

sudo launchctl unload /Library/LaunchDaemons/com.edb.launchd.portfoliodb.plist
 
sleep 30

#### Start Portfolio

sudo launchctl load /Library/LaunchDaemons/com.edb.launchd.portfoliodb.plist 

sleep 5 

sudo launchctl load /Library/LaunchDaemons/com.extensis.portfolio.server.elasticsearch.plist

sleep 5

sudo launchctl load /Library/LaunchDaemons/com.extensis.portfolio.server.media.delegate.plist

sleep 5

sudo launchctl load /Library/LaunchDaemons/com.extensis.dam-server.web.admin.launchd.plist
