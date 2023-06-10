import os
from scrapy import cmdline

# Change directory to the Scrapper app
os.chdir('scrapper')

# Run the Scrapy spider using the cmdline utility
cmdline.execute(['scrapy', 'crawl', 'loopnet'])
