# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5039_HLBC_gov"
url = "http://www.harrow.gov.uk/info/100004/council_and_democracy/555/council_spending/2"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
pageLinks = soup.findAll('a', href=True)

for pageLink in pageLinks:
  if 'Spend' in pageLink.contents[0]: # look for the reference to spend in the link contents
  	href = pageLink['href']
	print href
 
  	# add the right prefix onto the url
  	pageUrl = 'http://www.harrow.gov.uk/'+ href
  	html2 = urllib2.urlopen(pageUrl)
  	soup2 = BeautifulSoup(html2)
  	
  	filePages = soup2.findAll('a')
  	
	for filePage in filePages:
	  	if 'Spend Data CSV' in filePage.contents[0]:
	  		subPageUrl = filePage['href']
	  		print subPageUrl
	  		title = filePage.contents[0]
	  		suPageUrl = 'http://www.harrow.gov.uk/'+ href
  			html3 = urllib2.urlopen(subPageUrl)
  			soup3 = BeautifulSoup(html2)
	  		
	  		fileBlocks = soup2.findAll('h3',{'class':'space'})
	  		
	  		for fileBlock in fileBlocks:
				fileUrl = fileBlock.a[href]
				# create the right strings for the new filename
				title = title.upper().strip()
				csvYr = title.split(' ')[0]
				csvMth = title.split(' ')[1][:3]
				csvMth = convert_mth_strings(csvMth);
			
				filename = entity_id + "_" + csvYr + "_" + csvMth
				todays_date = str(datetime.now())
				scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
				print filename
