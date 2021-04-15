import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import VvancitycommunityinvestmentbankItem
from itemloaders.processors import TakeFirst
import requests
from scrapy import Selector

pattern = r'(\xa0)?'

url = "https://vancitycommunityinvestmentbank.ca/wp-admin/admin-ajax.php"

payload = "action=loadmore&query=%7B%22page%22%3A0%2C%22pagename%22%3A%22blog%22%2C%22error%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A0%2C%22post_parent%22%3A%22%22%2C%22subpost%22%3A%22%22%2C%22subpost_id%22%3A%22%22%2C%22attachment%22%3A%22%22%2C%22attachment_id%22%3A0%2C%22name%22%3A%22%22%2C%22page_id%22%3A0%2C%22second%22%3A%22%22%2C%22minute%22%3A%22%22%2C%22hour%22%3A%22%22%2C%22day%22%3A0%2C%22monthnum%22%3A0%2C%22year%22%3A0%2C%22w%22%3A0%2C%22category_name%22%3A%22%22%2C%22tag%22%3A%22%22%2C%22cat%22%3A%22%22%2C%22tag_id%22%3A%22%22%2C%22author%22%3A%22%22%2C%22author_name%22%3A%22%22%2C%22feed%22%3A%22%22%2C%22tb%22%3A%22%22%2C%22paged%22%3A0%2C%22meta_key%22%3A%22%22%2C%22meta_value%22%3A%22%22%2C%22preview%22%3A%22%22%2C%22s%22%3A%22%22%2C%22sentence%22%3A%22%22%2C%22title%22%3A%22%22%2C%22fields%22%3A%22%22%2C%22menu_order%22%3A%22%22%2C%22embed%22%3A%22%22%2C%22category__in%22%3A%5B%5D%2C%22category__not_in%22%3A%5B%5D%2C%22category__and%22%3A%5B%5D%2C%22post__in%22%3A%5B%5D%2C%22post__not_in%22%3A%5B%5D%2C%22post_name__in%22%3A%5B%5D%2C%22tag__in%22%3A%5B%5D%2C%22tag__not_in%22%3A%5B%5D%2C%22tag__and%22%3A%5B%5D%2C%22tag_slug__in%22%3A%5B%5D%2C%22tag_slug__and%22%3A%5B%5D%2C%22post_parent__in%22%3A%5B%5D%2C%22post_parent__not_in%22%3A%5B%5D%2C%22author__in%22%3A%5B%5D%2C%22author__not_in%22%3A%5B%5D%2C%22ignore_sticky_posts%22%3Afalse%2C%22suppress_filters%22%3Afalse%2C%22cache_results%22%3Atrue%2C%22update_post_term_cache%22%3Atrue%2C%22lazy_load_term_meta%22%3Atrue%2C%22update_post_meta_cache%22%3Atrue%2C%22post_type%22%3A%22%22%2C%22posts_per_page%22%3A999%2C%22nopaging%22%3Afalse%2C%22comments_per_page%22%3A%2250%22%2C%22no_found_rows%22%3Afalse%2C%22order%22%3A%22DESC%22%7D&page=1&ids%5B%5D=4655&ids%5B%5D=4596&ids%5B%5D=4604"
headers = {
  'Connection': 'keep-alive',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'Accept': '*/*',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'https://vancitycommunityinvestmentbank.ca',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://vancitycommunityinvestmentbank.ca/blog/',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cookie': 'TiPMix=23.5270528698; x-ms-routing-name=self; ARRAffinity=59ee04e9cdf86f379bb7b7ff32efd152592510d050a476329862fb843f7c8cb5; ARRAffinitySameSite=59ee04e9cdf86f379bb7b7ff32efd152592510d050a476329862fb843f7c8cb5; _ga=GA1.2.1881688300.1618473763; _gid=GA1.2.871817437.1618473763; _fbp=fb.1.1618473763127.437886027; msd365mkttr=TeZHS3KWeD-wMtdpdHoLH0lOGsVTC6Rizj_6cKKQ; msd365mkttrs=hiKOQtjH; _gat_gtag_UA_30390918_2=1; _gat_UA-30390918-2=1'
}



class VvancitycommunityinvestmentbankSpider(scrapy.Spider):
	name = 'vancitycommunityinvestmentbank'
	start_urls = ['https://vancitycommunityinvestmentbank.ca/blog/']

	def parse(self, response):
		data = requests.request("POST", url, headers=headers, data=payload)
		post_links = Selector(text=data.text).xpath('//div[@class="card"]/a/@href').getall() + response.xpath('//div[@class="three_column"]//div[@class="card"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="entry-meta"]/text()').get().split('|')[0].strip()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=VvancitycommunityinvestmentbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
