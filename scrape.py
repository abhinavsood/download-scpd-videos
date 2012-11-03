import re
import os
import passwords
import sys
import mechanize
import cookielib
from subprocess import Popen
from BeautifulSoup import BeautifulSoup
from multiprocessing import Pool

def download(work):
	if os.path.exists(work[1]):
		print "Already downloaded", work
		return

	print "Starting", work
	# Put it in a temp file
	if os.system("mimms -c %s %s" % (work[0], "_" + work[1])) == 0:
		# Move the file on success
		os.system("mv %s %s" % ("_" + work[1], work[1]))
	print "Finished", work

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
	#br.set_debug_http(True)
	#br.set_debug_redirects(True)
	#br.set_debug_responses(True)
	
	# User-Agent (this is cheating, ok?)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	
	# Open Stanford Center for Professional Development
	rLogin = br.open("http://scpd.stanford.edu/portal/studentLogin.jsp")

	assert br.viewing_html()

	# Import from a module outside of version control your SUNET id and password
	br.select_form(name="portalLogonFormPanel")
	br["studentNumber"] = passwords.my_username
	br["studentPassword"] = passwords.my_password
	response = br.submit()
	
	# After login, open the page that lists course
	rLoggedIn = br.open("http://scpd.stanford.edu/portal/student/studentHome.do?method=load")
	assert br.viewing_html()
	
	soup = BeautifulSoup(rLoggedIn)
	
	# get the name of the course from the command line arguments
	course = re.compile(sys.argv[1])
	
	# find the link to videos of the requested course
	cell = soup.find(text=course).parent
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
	
	# reached the preloader page, now what?
	br.select_form(nr=0)
	
	br.find_control("AuthInfo").disabled = False
	br.find_control("MAC").disabled = False
	br.find_control("MacKey").disabled = False

	br.form.set_all_readonly(False)
	
	print br.form
	print "\n\n_________________\n\n"
	print br.attrs
	
	# results in authentication error
	#response = br.submit()	
	
	#print response.read()
	
	
	'''
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
		output_name = re.search(r"[a-z]+[0-9]+[a-z]?/[0-9]+",video).group(0).replace("/","_") + ".wmv"
		videos.append((video, output_name))

	# Make a thread pool and download 5 files at a time
	p = Pool(processes=5)
	p.map(download, videos)
	'''
