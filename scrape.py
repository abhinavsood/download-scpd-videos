#!/usr/bin/env python

import re
import os
import getpass
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
from multiprocessing import Pool

def download(work):
	if os.path.exists(work[1]):
		print "Already downloaded", work
		return
	
	print "Starting: ", work
	# Put it in a temp file
	if os.system("mimms -c %s %s" % (work[0], "_" + work[1])) == 0:
		# Move the file on success
		os.system("mv %s %s" % ("_" + work[1], work[1]))
	print "Finished: ", work

if __name__ == '__main__':
	# Browser
	br = mechanize.Browser()
	
	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	
	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	
	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	
	# Want debugging messages?
	br.set_debug_http(False)
	br.set_debug_redirects(False)
	br.set_debug_responses(False)
	
	# User-Agent (this is cheating, ok?)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4')]
	
	# Open Stanford Center for Professional Development
	br.open("http://scpd.stanford.edu/portal/studentLogin.jsp")
	assert br.viewing_html()
	
	print "\n## Enter your credentials ##\n"
	br.select_form(name="portalLogonFormPanel")
	br["studentNumber"] = raw_input('Username: ')
	br["studentPassword"] = getpass.getpass()
	response = br.submit()
	
	print "\n## Logged in! ##\n"
	# After login, open the page that lists course
	rLoggedIn = br.open("http://scpd.stanford.edu/portal/student/studentHome.do?method=load")
	
	soup = BeautifulSoup(rLoggedIn)
	
	print "\n## Enter course title ##\n"
	# find the link to videos of the requested course
	cell = soup.find(text=re.compile(raw_input('Course: '))).parent
	while cell.name != 'h3': cell = cell.parent
	videosLink = cell.findNext('a', text=re.compile('Online Videos')).parent
	
	# get onlineResourceId from link to videos of the requested course
	onlineResourceId = re.search(r"\((\d+)\)", videosLink.get('onclick')).group(0)[1:-1]
	
	# select online resource form
	br.select_form(name="portalOnlineResourceForm")
	
	# remove readonly type from onlineResourceId
	br.find_control("onlineResourceId").readonly = False
	
	# set onlineResourceId from link to videos of the requested course
	br["onlineResourceId"] = onlineResourceId
	response = br.submit()
	
	print "\n## Course Found! Loading resources... ##\n"
	# reached the preloader page, now what?
	br.select_form(nr=0)
	br.find_control("AuthInfo").disabled = False
	br.find_control("MAC").disabled = False
	br.find_control("MacKey").disabled = False
	br.form.set_all_readonly(False)
	response = br.submit()
	
	## Rinse and repeat##
	rLoggedInHome = br.open('http://scpd.stanford.edu/portal/student/studentHome.do?method=load')
	
	# select online resource form
	br.select_form(name="portalOnlineResourceForm")
	
	# remove readonly type from onlineResourceId
	br.find_control("onlineResourceId").readonly = False
	
	# set onlineResourceId from link to videos of the requested course
	br["onlineResourceId"] = onlineResourceId
	response = br.submit()
	
	# reached the preloader page, but you know, what?
	br.select_form(nr=0)
	br.find_control("AuthInfo").disabled = False
	br.find_control("MAC").disabled = False
	br.find_control("MacKey").disabled = False
	br.form.set_all_readonly(False)
	response = br.submit()
	
	
	# Build up a list of lectures
	links = []
	for link in br.links(text="WMP"):
		links.append(re.search(r"'(.*)'",link.url).group(1))
	
	videos = []
	# These are done serially purely just to not look suspicious, we could probably parallelize this as well
	for link in links:
		response = br.open(link)
		soup = BeautifulSoup(response.read())
		video = soup.find('object', id='WMPlayer')['data']
		video = re.sub("http","mms",video)
		output_name = os.path.basename(video)
		
		print "## Found video: "+output_name+" ##\n"
		videos.append((video, output_name))
	
	# Make a thread pool and download 5 files at a time
	p = Pool(processes=5)
	p.map(download, videos)