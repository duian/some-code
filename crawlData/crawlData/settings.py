# Scrapy settings for crawlData project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawlData'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['crawlData.spiders']
NEWSPIDER_MODULE = 'crawlData.spiders'
DEFAULT_ITEM_CLASS = 'crawlData.items.CrawldataItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

