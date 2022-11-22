#DEPENDENCIAS
#pip install Scrapy

# from scrapy.spiders import CrawlSpider, Rule

# class SuperSpider(CrawlSpider):
#     name = 'follower'
#     allowed_domains = ['en.wikipedia.org']
#     start_urls = ['https://en.wikipedia.org/wiki/Web_scraping']
#     base_url = 'https://en.wikipedia.org'
 
#     custom_settings = {
#         'DEPTH_LIMIT': 1
#     }
 
#     def parse(self, response):
#         for next_page in response.xpath('.//div/p/a'):
#             yield response.follow(next_page, self.parse)
 
#         for quote in response.xpath('.//h1/text()'):
#             yield {'quote': quote.extract() }
            
# obj = SuperSpider(CrawlSpider)
# res = obj.parse("https://en.wikipedia.org")




# import scrapy

# class LinkCheckerSpider(scrapy.Spider):
#     name = 'link_checker'
#     allowed_domains = ['https://restituciontierras.ramajudicial.gov.co']
#     start_urls = ['https://restituciontierras.ramajudicial.gov.co/RestitucionTierras/Views/Old/sentencias.aspx']

#     def parse(self, response):
#         """ Main function that parses downloaded pages """
#         # Print what the spider is doing
#         print(response.url)
#         # Get all the <a> tags
#         a_selectors = response.xpath("//a")
#         # Loop on each tag
#         for selector in a_selectors:
#             # Extract the link text
#             text = selector.xpath("text()").extract_first()
#             # Extract the link href
#             link = selector.xpath("@href").extract_first()
#             # Create a new Request object
#             request = response.follow(link, callback=self.parse)
#             # Return it thanks to a generator
#             yield request


import scrapy
import gspread

frases_lista = []
# gc = gspread.service_account(filename='/home/nicolas/Proyectos/python/sheets/scraping-link-d8434e0ec14a.json')

# Abrir por titulo
# sh = gc.open("Frases")

# Seleccionar primera hoja
# worksheet = sh.get_worksheet(0)

class ParascrapearSpider(scrapy.Spider):
    name = 'parascrapear'
    allowed_domains = ['parascrapear.com']
    start_urls = ['http://parascrapear.com/']

    def parse(self, response):
        print('Parseando ' + response.url)       
        
        next_urls = response.css('a::attr(href)').getall()
        for next_url in next_urls:
            if next_url is not None:
                yield scrapy.Request(response.urljoin(next_url))
        
        frases = response.css('q::text').getall()
        for frase in frases:
            if frase is not frases_lista:
                frases_lista.append(frase)
                print( frase )
                # row_index = len(worksheet.col_values(1)) + 1
                # worksheet.update('A'+str(row_index), frase)