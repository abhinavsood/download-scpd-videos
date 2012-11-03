Download online videos from SCPD for the courses you're enrolled in

Installation
============
    git clone git://github.com/abhinavsood/scrape-scpd-videos.git
    sudo easy_install mechanize
    sudo easy_install BeautifulSoup
    sudo port install mimms
    echo "my_username = \"[YOUR SUNETID]\"; my_password = \"[YOUR SUNET PASSWORD]\"" > passwords.py

Running
=======
    python scrape.py [Name of the course as listed on SCPD]

You can leave out your company's name from the name of the course on SCPD. So, for example, if the course name as listed on SCPD is "Your Company Name - Silicon Run Series XOXO1O8 - OO1 ", you can do
    python scrape.py "Silicon Run Series"

Notes
=====
This by default runs 5 concurrent streams, if you want to up this, change the line that says processes=5

This also does no magic encoding because that can be done later (i.e. after Stanford takes everything down) and people might be picky on what format they want anyway.

Until the stream finishes it puts it at a temporary filename prefixed by a "_", that way if everything dies you don't have to go see which one's didn't fully download by opening them.  There's a mimms flag to resume automatically too, but I'm not sure of what happens when there is nothing to resume.

Since this uses multiprocessing, it might be tricky to Ctrl-C out of.  You can always just `killall python`
