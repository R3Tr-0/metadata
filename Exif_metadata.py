#!/usr/bin/python
import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS
###############################################################
def findimages(url):
    print '[+] Finding images on [' + url+']'
    urlcontent = urllib2.urlopen(url).read()
    soup = BeautifulSoup(urlcontent)
    imgtags = soup.findAll('img')
    return imgtags

def downloadimage(imgtag):
    try:
        print '[+] Downloading image....'
        imgsrc = imgtag['src']
        imgcontent = urllib2.urlopen(imgsrc).read()
        imgfilename = basename(urlsplit(imgsrc)[2])
        imgfile = open(imgfilename,'wb')
        imgfile.write(imgcontent)
        imgfile.close()
        return imgfilename
    except:
        return ''
def testforexif(imgfilename):
    try:
        exifdata = {}
        imgfile = Image.open(imgfilename)
        info = imgfile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag,tag)
                exifdata[decoded] = value
            exifgps = exifdata['GPSInfo']
            if exifgps:
                print '[*] ' + imgfilename + ' contains GPS MetaData'
    except:
        pass

def main():
    parser = optparse.OptionParser('usage: -u <TARGET URL>')
    parser.add_option('-u',dest='url', type='string',help='url address')
    (options,args) = parser.parse_args()
    url = options.url
    if url == None:
        print parser.usage
        exit(0)
    else:
        imgtags = findimages(url)
        for imgtag in imgtags:
            imgfilename = downloadimage(imgtag)
            testforexif(imgfilename)
if __name__ == '__main__':
    main()

