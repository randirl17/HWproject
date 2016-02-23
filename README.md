# HWproject

Web-scraping project, using the BeautifulSoup package to parse teachers' websites for the most recent homework assignments.

sites.txt is the most comprehensive list of teacher websites.

HWpull.py is the umbrella script.  It requests the website HTML and saves as local text files in ./sitefiles.  For each class website there is a different routine to parse and find the HW assignment.  These are then consolidated by calling HWhtml.py, which presents the findings in a local HTML file called "HWpost.html".