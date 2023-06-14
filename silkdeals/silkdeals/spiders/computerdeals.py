import scrapy
from scrapy_selenium import SeleniumRequest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_binary_path = "C:\\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.binary_location = chrome_binary_path
driver = webdriver.Chrome(executable_path="C:\\Users\mohan\projects_scraping\silkdeals\chromedriver", options=chrome_options)

def remove_characters(self,value):
    return value.strip('')

class ComputerdealsSpider(scrapy.Spider):
    name = "computerdeals"
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3,
            callback = self.parse

        )

    def parse(self, response):
        products = response.xpath("//ul[@class = 'bp-p-filterGrid_items']/li")
        for product in products:
            yield{
                'name': product.xpath(".//div/a[@class='bp-c-card_title bp-c-link']/text()").get(),
                'link': product.xpath(".//div/a[@class='bp-c-card_title bp-c-link']/@href").get(),
                'store_name':  product.xpath("normalize-space(.//div/span[3])").get(),
                'price': product.xpath("normalize-space(.//div/span[1]/text())").get()


            }

        #the pagination wont work becasue the website updated 
        next_page = response.Xpath("//div[@class = 'bp-c-pagination_wrapper bp-c-pagination_ends']/button[@data-page='next']").get()
        if next_page:
            absolute_url = f"https://slickdeals.net/computer-deals/{next_page}" 
            yield SeleniumRequest(
                url = absolute_url,
                wait_time = 3,
                callback = self.parse

            )
       