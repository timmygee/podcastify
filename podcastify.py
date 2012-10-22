import os

from filters import RssSoupFilter
from soupify import SoupifyFeed
from actionify import OffworldShowAction

if __name__ == '__main__':
    PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
    soupified = SoupifyFeed('http://www.offworldrecordings.com/feed/')
    rss_filter = RssSoupFilter(
        soupified.get_soup(), title_all_keywords=['offworld', 'show'])
    rss_filter.filter()
    action = OffworldShowAction(
        items=rss_filter.get_items(), save_path=PROJECT_PATH)
    action.run()
    
