import scrapy

from PeaceEliteFirearms.items import PeaceelitefirearmsItem


class GpQqSpider(scrapy.Spider):
    name = 'gp.qq'
    allowed_domains = ['gp.qq.com']
    start_urls = ['https://gp.qq.com/cp/a20190522gamedata/pc_list.shtml']

    def parse_detail(self, response):
        item = response.meta['item']
        name = response.xpath("//div[@class='top']/h4[@class='wea_name']/text()")[0].extract()
        youdian = response.xpath("//div[@class='merit_text']/p[@class='merit_cont']/text()")[0].extract()
        quedian = response.xpath("//div[@class='merit_text']/p[@class='merit_cont merit_cont2']/text()")[0].extract()
        item['name'] = name
        item['youdian'] = youdian
        item['quedian'] = quedian
        yield item

    def parse(self, response):
        item = PeaceelitefirearmsItem()
        uls = response.xpath("///div[@class='weapons-data']/div[@id='section-container']/ul")
        for ul in uls:
            for li in ul.xpath('./li'):
                # name = li.xpath("./a/@title")[0].extract()
                detail_url = li.xpath("./a/@href")[0].extract()
                # bug: 不能在这里提交name,所以，只能在请求传参后解析拉，
                # item['name'] = name
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})

