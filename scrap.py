#!/usr/bin/env python 

import urllib2
import json
import datetime
import csv
import time

# if you haven't had an app_id, sign up one here: https://developers.facebook.com/apps

app_id = "1794678____12"
app_secret = "34e6______d9fc4______d" # DO NOT SHARE WITH ANYONE!

access_token = app_id + "|" + app_secret

#page which analysis is done
page_id = 'chumbakacyberjaya'

#to ping NYT's Facebook page to verify that the access_token works and the page_id is valid
def testFacebookPageData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = json.loads(response.read()) 
    print json.dumps(data, indent=4, sort_keys=True)
    
'''testFacebookPageData(page_id, access_token)'''

#to catch error (such as "HTTP Error 500 (Internal Error)") and try again after a few seconds, which usually works and to consolidates the data retrival code
def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            
            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()

#to return the FB postfeeds by changing the page metadata endpoint to /feed endpoint
def testFacebookPageFeedData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id + "/feed" 
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    print json.dumps(data, indent=4, sort_keys=True)
    

'''testFacebookPageFeedData(page_id, access_token)'''

#to return data of 1 FB postfeed 
def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data
    
test_status = getFacebookPageFeedData(page_id, access_token, 1)["data"][0]
print json.dumps(test_status, indent=4, sort_keys=True)
