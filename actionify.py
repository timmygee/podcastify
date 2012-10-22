# Perform actions based on soup items
import string
import os
import re
import htmlentitydefs

## import urllib2

## try:
##     from bs4 import BeautifulSoup
## except ImportError:
##     from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

from soupify import Soupify

class Action(Soupify):
    """
    Base action class. Perform an arbitrary action on passed in list of items.
    Uses Soupify as a mixin class for url retrieval and BeautifulSoup functions
    """
    items = None

    def __init__(self, items=None):
        if items is not None:
            self.set_items(items)

    def set_items(self, items):
        self.items = items

    def run(self):
        pass

def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.
    
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    Taken from http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def make_nice_title(title):
    """
    Takes an item title, strips out non-printable characters, tokenises and
    then joins tokens together with an underscore as a separator
    """
    new_title = ''
    for char in title:
        if char in string.printable:
            new_title += char

    tokens = []
    for token in new_title.split():
        if len(token) >= 2:
            # Strip out words that start with [ and end with ]
            if token[0] == '[' and token[-1] == ']':
                continue
        tokens.append(token)

    return '_'.join(tokens)
        
class OffworldShowAction(Action):
    """
    Implement visiting of the offworld show pages based on links in the rss
    items, find the download link on the page and download the file alongside
    a text file with the tracklist info
    """
    def __init__(self, items=None, save_path=None):
        Action.__init__(self, items=items)
        self.save_path = save_path

    def parse_page_and_save(self, url, file_name):
        data = self._read_url(url)
        page_soup = self._soupify_html(data)

        # We have the page soup, parse out the download link
        content_div = page_soup.findAll(
            'div', {'class': 'entry-container fix'})[0]
        # Once we have the content div it should be the first link
        anchor = content_div.findNext('a')

        # Cool, supposedly we have the link now. Grab the tracklist and save
        # it in a text file
        div = anchor.parent.parent
        # Should be the text contents of the last p tag in the div
        tracklist_node = div.findAll('p', recursive=False)[-1]

        tracklist = ''.join(
            [unescape(n.string) for n in tracklist_node.contents \
            if n.string is not None])

        tracklist_file_path = os.path.join(self.save_path, file_name + '.txt')
        if os.path.exists(tracklist_file_path):
            print 'Files for %s already exist in path %s. Not saving again' % \
                (file_name, self.save_path)
        else:
            outFile = open(tracklist_file_path, 'w')
            outFile.write(tracklist.encode('utf8'))

            audio_file_path = os.path.join(self.save_path, file_name + '.mp3')
            self._save_url_to_file(anchor['href'], audio_file_path)

    def run(self, items=None):
        if items is None:
            items = self.items
        else:
            self.set_items(items)

        for item in items:
            self.parse_page_and_save(
                item.link.string, make_nice_title(unescape(item.title.string)))

            
if __name__ == '__main__':
    # testing
    action = OffworldShowAction(save_path='/home/tim/projects/podcastify')
    action.parse_page_and_save(
        'http://www.offworldrecordings.com/news/the-offworld-show-with-lm1-oct-15th-2012-bassdrive-download/',
        make_nice_title('The Offworld show with LM1 - Oct 15th 2012 Bassdrive [Download]'))
