import scrapy
from inmobiscrap.items import Departamento


class LeporeSpider(scrapy.Spider):

    name = 'lepore'

    def start_requests(self):
        yield scrapy.FormRequest(
            url='http://leporepropiedades.com.ar/on-search-ajax',
            callback=self.get_urls,
            method='POST',
            formdata={'tipoper': '2', 'order': 'ASC'}
        )

    def get_urls(self, response):
        for title in response.css('h2.property-row-title'):
            url = title.css('a::attr(href)').extract_first()
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        property_list_selector = response.css('div.property-list dl')

        # [Dirección, Ambientes, Valor, Estado, Ubicación, Superficie Cubierta, Superficie Total]
        # May be incomplete or in an incorrect order
        dt_list = property_list_selector[0].css('dt::text').extract()  # headers
        dd_list = property_list_selector[0].css('dd::text').extract()  # values

        # [printstuff, tel:xxxxxxx, mailto:xxxxxxxxx]
        href_list = property_list_selector[0].css('dd a::attr(href)').extract()

        properties_dict = dict(zip(dt_list, dd_list))

        yield Departamento(
            address=properties_dict.get('Dirección'),
            rooms=properties_dict.get('Ambientes'),
            price=properties_dict.get('Valor'),
            status=properties_dict.get('Estado'),
            location=properties_dict.get('Ubicación'),
            covered_area=properties_dict.get('Superficie Cubierta'),
            total_area=properties_dict.get('Superficie Total'),
            phone=href_list[1][4:],
            email=href_list[2][7:],
            url=response.url
        )
