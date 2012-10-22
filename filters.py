from copy import deepcopy

# A collection of utilities to filter beautiful soup data

## Some average rss:
## <?xml version="1.0"?>
## <rss version="2.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:media="http://search.yahoo.com/mrss/" xmlns:yt="http://gdata.youtube.com/schemas/2007" xmlns:atom="http://www.w3.org/2005/Atom">
## <channel>
##   <title>Offworld Show</title>
##   <description>Pipes Output</description>
##   <link>http://pipes.yahoo.com/pipes/pipe.info?_id=e7c9e97eeb12e65d8108c6f7bb9ba47c</link>
##   <atom:link rel="next" href="http://pipes.yahoo.com/pipes/pipe.run?_id=e7c9e97eeb12e65d8108c6f7bb9ba47c&amp;_render=rss&amp;page=2"/>
##   <pubDate>Mon, 22 Oct 2012 02:54:04 +0000</pubDate>
##   <generator>http://pipes.yahoo.com/pipes/</generator>
##   <item>
##     <title>The Offworld show with LM1 - Oct 15th 2012 Bassdrive [Download]</title>
##     <link>http://www.offworldrecordings.com/news/the-offworld-show-with-lm1-oct-15th-2012-bassdrive-download/</link>
##     <description>blahblah</description>
##     <guid isPermaLink="false">http://www.offworldrecordings.com/?p=2168</guid>
##     <pubDate>Sun, 21 Oct 2012 14:58:18 +0000</pubDate>
##     <category>News</category>
##   </item>
## </channel>
## </rss>

class SoupFilter:
    """
    Filters soup content
    """
    soup = None
    filter_kw = {}
    include = True
    items = None
    
    def __init__(self, soup, include=True, **filter_kw):
        self.set_soup(soup)
        self.set_include(include)
        self.filter_kw = deepcopy(filter_kw)

    def set_include(self, include):
        self.include = include

    def set_soup(self, soup):
        self.soup = soup

    def filter(self, include=None, **filter_kw):
        """
        Override in child class.
        Filter based on kwargs. include=True means that any matches dictate the
        item should be included. include=False is effectively an exclude of
        the same items.
        Should alwas reset self.items to an empty list when invoked
        """
        pass

    def get_soup(self):
        return self.soup

    def get_markup(self):
        return self.get_soup().prettify()

    def get_items(self):
        """
        Returns a list of the soupified items of interest
        """
        return self.items

class RssSoupFilter(SoupFilter):
    """
    Class to provide filtering actions for RSS soup
    """
    def filter(self, include=None, **filter_kw):
        """
        kwargs can be:

        title_all_keywords: [keyword, keyword, ...]
        """
        if not filter_kw:
            filter_kw = deepcopy(self.filter_kw)

        if include is None:
            include = self.include

        self.items = []

        channel = self.get_soup().rss.channel

        for item in channel.findAllNext('item'):
            if 'title_all_keywords' in filter_kw:
                tokens = item.title.string.lower().split()

                matches = []

                for search_word in filter_kw['title_all_keywords']:
                    for token in tokens:
                        if search_word.lower() == token:
                            matches.append(search_word)

                if include and \
                       len(matches) != len(filter_kw['title_all_keywords']):
                    # To be included if all keywords matched. They didn't so we
                    # remove the item node from the markup
                    print 'include and not enough matches'
                    item.extract()
                elif (not include) and \
                       len(matches) == len(filter_kw['title_all_keywords']):
                    # To be excluded if there are matches. There is so remove
                    # item node from markup
                    print '(not include) and all matched keywords'
                    item.extract()
                else:
                    self.items.append(item)
                    
        print len(self.items)
