import scrapy

class LoopNetSpider(scrapy.Spider):
    name = 'loopnet'
    allowed_domains = ['loopnet.com']
    start_urls = ['https://www.loopnet.com']

    def parse(self, response):
        # Extract data from the response using XPath or CSS selectors
        property_listings = response.css('.property-listing')

        for listing in property_listings:
            title = listing.css('.listing-title::text').get().strip()
            price = listing.css('.listing-price::text').get().strip()
            description = listing.css('.listing-description::text').get().strip()

            # Process and store the extracted data as needed
            yield {
                'title': title,
                'price': price,
                'description': description,
            }
