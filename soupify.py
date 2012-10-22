# Tools to turn internet resources into BeautifulSoup soup objects
import urllib2

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

class Soupify:
    """
    Class to define soupify common functionality
    """
    soup = None
    data = None

    def soupify(self):
        """
        Runs internal soupify method then returns result
        """
        self._soupify()
        return self.get_soup()

    def get_soup(self):
        """
        Returns internal self.soup
        """
        return self.soup

    def _soupify_xml(self, data=None):
        """
        Sets self.soup to the soupified version of the inputted xml data.
        """
        if data is None:
            data = self.data
            
        #soup = BeautifulSoup(data, ['lxml', 'xml'])
        self.soup = BeautifulStoneSoup(data)
        return self.soup

    def _soupify_html(self, data=None):
        """
        Sets self.soup to the soupified version of the inputted html data.
        """
        if data is None:
            data = self.data
            
        self.soup = BeautifulSoup(data)
        return self.soup

    def _read_url(self, url):
        """
        Reads data at url and returns it
        """
        #headers = {'User-Agent': config.USER_AGENT}
        headers = {}
        
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print 'HTTP Error %s fetching %s' % (e.code, url)
            raise
        except urllib2.URLError, e:
            print 'Error %s fetching  %s' % (e.reason, url)
            raise
        self.data = response.read()
        return self.data

    def _save_url_to_file(self, url, file_path):
        """
        Reads data at url and saves it to file_path. Unlike the _read_url
        method this saves the data to file chunk by chunk to avoid rediculous
        memory usage when downloading large files
        """
        #headers = {'User-Agent': config.USER_AGENT}
        headers = {}
        
        request = urllib2.Request(url, headers=headers)
        CHUNK_SIZE = 64 * 1024
        try:
            response = urllib2.urlopen(request)
            with open(file_path, 'wb') as fp:
                bytes = 0
                while True:
                    print 'Saved %s bytes' % bytes
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    fp.write(chunk)
                    bytes += len(chunk)
        except urllib2.HTTPError, e:
            print 'HTTP Error %s fetching %s' % (e.code, url)
            raise
        except urllib2.URLError, e:
            print 'Error %s fetching  %s' % (e.reason, url)
            raise

class SoupifyFeed(Soupify):
    """
    Takes a feed url upon initialisation and stores a beautifulsoup version of
    the content complete with methods to display and manipulate the soup
    """
    feed_url = None
    data = None
    
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self._read_url(self.feed_url)
        self._soupify_xml()
