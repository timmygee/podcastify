import os

from filters import RssSoupFilter
from soupify import SoupifyFeed
from actionify import OffworldShowAction

if __name__ == '__main__':
    PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
    # Step 1: Make soup from feed
    soupified = SoupifyFeed('http://www.offworldrecordings.com/feed/')
    # Step 2: Filter feed if necessary
    rss_filter = RssSoupFilter(
        soupified.get_soup(), title_all_keywords=['offworld', 'show'])
    rss_filter.filter()
    # Step 3: Perform an action on the feed. In this case, we're scraping the
    # blog page for the offworld show download and tracklist
    action = OffworldShowAction(
        items=rss_filter.get_items(), save_path=PROJECT_PATH)
    action.run()
    
