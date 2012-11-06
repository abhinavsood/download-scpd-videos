Download online videos from Stanford Center for Professional Development for the courses that you're enrolled in using your my*stanford*connection account.

Installation
============

To be able to use this Python script, you'll need mechanize, BeautifulSoup and mimmms.

### On Mac

    sudo easy_install mechanize
    sudo easy_install BeautifulSoup
    sudo port install mimms

( using MacPorts to install mimms here)

### On Linux / Windows

Download and manually install from sources.


Running
=======
    python scrape.py

The script will prompt you for your username, password and the course that you're looking for. You can enter a part of the course name. You can leave out your company's name or course code from the name of the course on SCPD. So, for example, if the course name as listed on SCPD is "Your Company Name - Silicon Run Series XOXO1O8 - OO1 ", you can just enter 'Silicon Run' when prompted for course name.

Notes
=====
scrape-scpd-videos runs 5 concurrent streams, by default. To change this, modify the number in the line that says `processes=5`.

This script does no magic encoding on the downloaded videos.

Until the stream finishes it puts it at a temporary filename prefixed by a "_", that way if everything dies you don't have to go see which one's didn't fully download by opening them.  There's a mimms flag to resume automatically too, but I'm not sure of what happens when there is nothing to resume.

Since this uses multiprocessing, it might be tricky to Ctrl-C out of. You can always just `killall python`
