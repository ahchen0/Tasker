from pyspider.libs.base_handler import *

class Handler(BaseHandler):
	crawl_config = {
	}

	@every(minutes=24 * 60)
	def on_start(self):
		self.crawl('http://scrapy.org/', callback=self.index_page)

	@config(age=10 * 24 * 60 * 60)
	def index_page(self, response):
		return {
			"url": response.url,
			"title": response.doc('title').text()
		}
