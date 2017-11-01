# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from urlparse import urlparse, parse_qs


from noticias.items import NoticiasItem


class G1NoticiasSpider(Spider):
    name = 'g1_noticias'
    #allowed_domains = ['g1.globo.com/economia/negocios', 'google.com.br', 'goo.gl']
    #start_urls = ['http://goo.gl/oqrkT7']
    #start_urls = ['file:///home/eduardoe/UEM/GIT/scrapy_simples/data/allintitle_%20petrobras%20site_g1.globo.com_economia_negocios_noticia%20-%20Pesquisa%20Google.html']

    def start_requests(self):
        query = 'allintitle:petrobras site:g1.globo.com/economia'
        date_min = '9/1/2017'
        date_max = '9/30/2017'
        pages = 4
        for i in range(0, pages):
            start = i * 10
            url = 'https://www.google.com.br/search?q={query}&tbs=cdr:1,cd_min:{date_min},cd_max:{date_max}&start={start}'.format(
                query=query, 
                date_min=date_min, 
                date_max=date_max, 
                start=start
            )                    
            yield Request(url)
    
    def format_google_url(self, url):                       
        return parse_qs(urlparse(url).query)['q'][0]

    def parse(self, response):
        news = response.xpath('//*[@class="r"]')
        for new in news:                    
            g1_url = new.xpath('.//a/@href').extract_first()
            if '/url?' in g1_url:
                g1_url = self.format_google_url(g1_url)                    

            if 'blog' not in g1_url:
                yield Request(str(g1_url), callback=self.parse_g1)
        '''
        estou fazendo isso lá em cima
        next_page = response.xpath('//*[@class="pn"]/@href').extract_first()        
        if next_page:
            yield response.follow(next_page, self.parse)
        '''
            
    def parse_g1(self, response):                                        
        titulo = "".join([
                response.xpath('//*[@class="content-head__title"]/text()').extract_first(),
                '\n',
                response.xpath("//*[@class='content-head__subtitle']/text()").extract_first()
        ])
        data_atualizacao = response.xpath('//*[@class="content-publication-data__updated"]/time/text()').extract_first()        
        conteudo = response.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), 'content-text')]/text()").extract()

        if not data_atualizacao:
            data_atualizacao = ''

        l = ItemLoader(item=NoticiasItem(), response=response)
        l.add_value('titulo', titulo)
        l.add_value('data_atualizacao', data_atualizacao)
        l.add_value('conteudo', conteudo)

        yield l.load_item()                                