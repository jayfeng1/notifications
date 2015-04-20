# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:55:41 2015

@author: Jay

"""

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import smtplib
import csv

def connect(email, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    return server

def email(sender, receivers, listings, server):
    for listing in listings:
        message = """From: From Person <from@fromdomain.com>
        To: To Person <to@todomain.com>
        Subject: NEW CRAIGSLIST POSTING
        """ + listing.text
        try:
           server.sendmail(sender, receivers, message)         
           print "Successfully sent email"
        except:
           print "Error: unable to send email"

def apartments(num, soup, seen):
    results = []
    #Find the list of craigslist postings
    for listing in soup.find_all('p',{'class':'row'}):
        #Check to see if they have pictures and coordinate locations as well as if they've been sent out before
        if listing.find('span',{'class':'p'}).text == ' pic map' and listing.get("data-pid") not in seen:
            text = listing.text.split("  $")[1]
            price, beds = text.split(" ")[0], text.split(" ")[2][0]
            #Divide to check if it's within the proper range on a per bedroom basis
            if float(price)/float(beds) < num and float(price)/float(beds) > float(num)/2:
                results.append(listing.text)
                #Add ID to the SET to make sure it's been seen
                seen.add(listing.get("data-pid"))
    return results

def getSoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content)

def openSet(path):
    reader = csv.reader(open(path,'rb'))
    return set(list(reader)[0])
    
if __name__=='__main__':
    URL = 'http://sfbay.craigslist.org/search/sfc/apa?hasPic=1&nh=25&nh=1&bedrooms=2'
    path = 'set1.csv'
    soup = getSoup(URL)
    seen = openSet(path)
    listings = apartments(1800, soup, seen)
    if len(listings) > 0:
        server = connect("YOUR_EMAIL", "YOUR_PASSWORD")
        email("YOUR_EMAIL", ['jayfeng1@uw.edu'], listings, server)
    cw = csv.writer(open("set1.csv",'wb'))
    cw.writerow(listings)
    
        
