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

The script will prompt you for your username, password and the course that you're looking for. You can enter a part of the course name. You can leave out your company's name or course code from the name of the course on SCPD. So, for example, if the course name as listed on SCPD is "ABC Company - Programming Basics Series ABC123 - OO1 ", you can just enter `Programming Basics` when prompted for course name.

Notes
=====
scrape-scpd-videos runs 5 concurrent streams, by default. To change this, modify the number in the line that says `processes=5`.

This script does no magic encoding on the downloaded videos.

Until the stream finishes it puts it at a temporary filename prefixed by a "_", that way if everything dies you don't have to go see which one's didn't fully download by opening them.  There's a mimms flag to resume automatically too, but I'm not sure of what happens when there is nothing to resume.

Since this uses multiprocessing, it might be tricky to Ctrl-C out of. You can always just `killall python`

Disclaimer
==========

The code is provided "as is" without any express or implied warranty of any kind including warranties of merchantability, non-infringement of intellectual property, or fitness for any particular purpose. In no event shall I be liable for any damages whatsoever (including, without limitation, damages for loss of profits, business interruption, loss of information, injury or death) arising out of the use of or inability to use the code, even if I have been advised of the possibility of such loss or damages.

Piracy is bad. Very bad. And, I do not support or encourage piracy. Do not download a video that you're not allowed or entitled to. You are urged to use this script with good judgment, common sense, discretion, and assume full responsibility for misuse. I accept NO responsibility for your use of this tool.
