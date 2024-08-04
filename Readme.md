# Rotating Proxies & Proxy APIs

## What Are Proxies & Why Do We Need Them?

As we saw in [Part 8](https://scrapeops.io/python-scrapy-playbook/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-8-fake-headers-user-agents/), most websites are trying to limit or completely block scrapers from accessing their websites data.

Part of the solution to this is to use optimized fake user-agents and browser headers to make your scraper appear more like a real browser. However, this won't work when scraping at scale as your IP address will be static. This is where **web scraping proxies** come in.

Web scraping proxies are IP addresses that you route your requests through instead of using your own or servers IP address.

We need them when web scraping as they allow us to spread our requests over thousands of proxies so that you can easily scrape a website at scale, without the target website blocking us.

If you doing a very small scraping project or scraping a website without sophisticated anti-bot countermeasures then you mightn't need them. However, when you start scraping big websites or at larger volumes then proxies quickly become a must as they allow you to:

- Bypass anti-bot countermeasures
- Get country-specific data from websites
- Hide your identity from the websites you are scraping

There are many different types of proxies (datacenter proxies, residential proxies, mobile proxies, ISP proxies, SOAX proxies), however, for the purposes of this guide we will focus on how to integrate them into our Scrapy spiders.

## The 3 Most Popular Proxy Integration Methods

When it comes to proxies there are 3 main integration methods that are most commonly used:

1. Proxy Lists
2. Rotating/Backconnect Proxies
3. Proxy APIs

All 3 have their pros and cons, and can have an impact on whether you have dedicated proxies or proxies in a shared pool. However, which type you use is really down to your own personal preferences and project requirements (budget, performance, ease of use, etc).

The cheapest proxies are ones where you can buy **lists of individual proxy IPs** and route your requests through them. However, these are often the most unreliable and hardest to integrate as you have build a lot of logic to manage the IPs, remove dead IPs and source new IPs once your existing ones get blocked.

The easiest proxies to use are **smart proxies** that either allow you to send your requests to a single proxy endpoint or to an HTTP API.

These smart proxy providers take care of all the **proxy selection**, **rotation**, **ban detection**, etc. within their proxy, and allow you to easily enable extra functionality like JS rendering, country-level geotargeting, residential proxies, etc. by simply adding some flags to your request.

Examples of smart proxy providers are: [ScrapeOps](https://scrapeops.io/), [ScraperAPI](https://www.scraperapi.com/?fp_ref=scrapeops), [Scrapingbee](https://www.scrapingbee.com/?fpr=scrapeops)


## How To Integrate & Rotate Proxy Lists

The most fundamental way of using proxies, is to insert a list of proxy IPs into your spider and configure it to select a random proxy every time it makes a request.

```python
'proxy1.com:8000',
'proxy2.com:8031',
'proxy3.com:8032',

```

When you sign up to some proxy providers, they will give you a list of proxy IP addresses that you will then need to use in your spider. Most free proxy lists online use this approach and some large providers still offer this method for datacenter IPs or if you want dedicated proxies.

Here are a list of sources to get **free proxy lists**:

- [FreeProxyLists](https://www.freeproxylists.net/)
- [Geonode Free Proxy Lists](https://geonode.com/free-proxy-list)
- [ProxyNova](https://www.proxynova.com/proxy-server-list/)

Free Proxy Lists

Free proxy lists are notoriously unreliable and seldom work for protected websites as anti-bot companies can scrape the free proxy lists and automatically ban any IP address that appears on one of these lists.

If you want to scrape protected websites, then you will likely need to purchase proxy IPs from a proxy provider. Here is a tool that allows you to [compare the proxy plans of different proxies who sell lists of proxies](https://scrapeops.io/proxy-providers/comparison/best-proxy-ips) to users.

To integrate a list of proxies with your spider, we can build our own proxy management layer or we can simply install an existing Scrapy middleware that will manage our proxy list for us.

There are several free Scrapy middlewares out there that you can choose from (like [scrapy-proxies](https://github.com/aivarsk/scrapy-proxies)), however, for this guide we're going to use the [scrapy-rotating-proxies](https://github.com/TeamHG-Memex/scrapy-rotating-proxies) middleware as it was developed by some of Scrapy's lead maintainers and has some really cool functionality.

[scrapy-rotating-proxies](https://github.com/TeamHG-Memex/scrapy-rotating-proxies) is very easy to setup and very customizable. To get started simply install the middleware:

```bash
pip install scrapy-rotating-proxies

```

Then we just need to update our `settings.py` to load in our proxies and enable the **scrapy-rotating-proxies** middleware:

```python
## settings.py
## Insert Your List of Proxies Here
ROTATING_PROXY_LIST = [
'proxy1.com:8000',
'proxy2.com:8031',
'proxy3.com:8032',
]
## Enable The Proxy Middleware In Your Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
# ...
'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
# ...
}

```

And that's it. After this, all requests your spider makes will be proxied using one of the proxies from the `ROTATING_PROXY_LIST`.

Alternatively, you could give the **scrapy-rotating-proxies** middleware a path to a file that contains the proxy list and your spider will use the proxies from this list when making requests.

```python
## settings.py
ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt'

```

The very cool thing about the **scrapy-rotating-proxies** middleware is that it will actively monitor the health of each individual proxy and remove any dead proxies from the proxy rotation.

You can also define your own ban detection policies, so you can tell the **scrapy-rotating-proxies** middleware what constitutes a dead proxy so it can remove it from the rotation. For more on this functionality then check out the [docs](https://github.com/TeamHG-Memex/scrapy-rotating-proxies).

## How To Use Rotating/Backconnect Proxies

Once upon a time, all proxy providers gave you lists of proxy IPs when you purchased a plan with them.

However, today it is far more common for them to provide you with a single proxy endpoint that you send your requests to and they handle the selection and rotation of the proxies on their end. Making it much easier for you to integrate a proxy solution into your spider.

For these examples, we're going to show you how to integrate [SmartProxy's Residential Proxies](https://smartproxy.pxf.io/q4DVKN) into our `bookscraper` as they offer good proxies and have pay-as-you-go plans. Making SmartProxy ideal for both small and large web scraping projects.

Other examples of rotating single endpoint proxy providers are [BrightData](https://brightdata.grsm.io/1pl6t3r3cfbp) and [Oxylabs](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=379).

To use Smartproxy as your proxy provider you just need to send all your requests to their proxy endpoint (different endpoints based on types of proxies used & features enabled):

```bash
"http://username:password@gate.smartproxy.com:7000"

```

In the above example, we would be using SmartProxy's standard rotating residential endpoint, that will route your requests to a different random IP address with every request. You can obtain the `username` and `password` from the Smartproxy dashboard.

You can simply set the country of the IP addresses by changing the proxy port string (using random **US proxies** in this case):

```bash
"http://username:password@us.smartproxy.com:7000"

```

Or use sticky sessions by adding a `sessionduration` and a different port number to the proxy string:

```bash
"http://username-sessionduration-10:password@gate.smartproxy.com:10000"
"http://username-sessionduration-10:password@gate.smartproxy.com:10001"
"http://username-sessionduration-10:password@gate.smartproxy.com:10002"

```

For more information on using a single endpoint proxy solution like Smartproxy, then [check out their documentation](https://help.smartproxy.com/docs/residential-authentication-methods).

You have a couple of options on how you integrate one of these single rotating proxy endpoints into your spider.

Single Endpoint Proxy

When using a single proxy endpoint, you shouldn't use a rotating proxy middleware like the **scrapy-rotating-proxies** middleware as it could interfere with the correct functioning of the proxy.

### 1. Via Request Parameters

Simply include the proxy connection details in the meta field of every request within your spider.

```python
## your_spider.py
def start_requests(self):
	for url in self.start_urls:
	return Request(url=url, callback=self.parse,
	                   meta={"proxy": "http://username:password@gate.smartproxy.com:70"})

```

Scrapy's [HttpProxyMiddleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpproxy), which is enabled by default, will then route the request through the proxy you defined.

### 2. Create Custom Middleware

A cleaner and more modular approach is to create a custom middleware which you then enable in your `settings.py` file. This will ensure all spiders will use the proxy.

Here is an example custom middleware that you can add to your `middlewares.py` file:

```python
## middlewares.py
import base64
class MyProxyMiddleware(object):
	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings)
	def __init__(self, settings):
	        self.user = settings.get('PROXY_USER')
	        self.password = settings.get('PROXY_PASSWORD')
	        self.endpoint = settings.get('PROXY_ENDPOINT')
	        self.port = settings.get('PROXY_PORT')
	def process_request(self, request, spider):
	        user_credentials = '{user}:{passw}'.format(user=self.user, passw=self.passwod)
		        basic_authentication = 'Basic ' + base64.b64encode(user_credentials
					        .encode()).decode()
	        host = 'http://{endpoint}:{port}'.format(endpoint=self.endpoint, 
														        port=self.port)
	        request.meta['proxy'] = host
	        request.headers['Proxy-Authorization'] = basic_authentication

```

Then you just need to enable it in your `settings.py` file, and fill in your proxy connection details:

```python
## settings.py
PROXY_USER = 'username'
PROXY_PASSWORD = 'password'
PROXY_ENDPOINT = 'gate.smartproxy.com'
PROXY_PORT = '7000'
DOWNLOADER_MIDDLEWARES = {
'bookscraper.middlewares.MyProxyMiddleware': 350,
'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
}

```

**Note:** For this middleware to work correctly, you will need to put it before the default [Scrapy HttpProxyMiddleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpproxy) by assign it a lower number.

## How To Use Proxy APIs

Over the last few years, a number of smart proxy solutions have been launched that take care of all the proxy/user-agent selection, rotation, ban detection, and are easily customizable.

Typically, these smart proxy solutions allow you to make requests via their HTTP endpoint. Some even have dedicated SDKs and traditional proxy endpoints.

Instead, of adding a proxy to your request, you send the URL you want to scrape to them via their API and then they return the HTML response to you. Only charging you if the request has been successful.

The advantages of Smart Proxy APIs is that they:

- Manage optimizing the browser headers and user-agents for you.
- Enable you to use headless browsers & other advanced features by adding query parameters.
- Automatically optimize proxy selection for your target domains.

For this example, we're going to use the [ScrapeOps Proxy Aggregator](https://scrapeops.io/proxy-aggregator/).

### 1. Integrating Into Spider

To send the pages we want to scrape to **ScrapeOps** we simply just need to forward the URLs we want to scrape to their API endpoint.

```bash
"https://proxy.scrapeops.io/v1/?api_key=YOUR_API_KEY&url=http://example.com/"

```

We can do this by creating a simple function:

```python
## booksspider.py
API_KEY = 'YOUR_API_KEY'
def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

```

And use this function in our Scrapy request:

```python
yield scrapy.Request(url=get_proxy_url(url), callback=self.parse)

```

This is how your final code should look.

```python
import scrapy
from urllib.parse import urlencode
API_KEY = 'YOUR_API_KEY'
def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']
    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a').attrib['href']
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
        yield scrapy.Request(get_proxy_url(book_url), callback=self.parse_book_page)
        ## Next Page
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        yield scrapy.Request(get_proxy_url(next_page_url), callback=self.parse)
    def parse_book_page(self, response):
        book = response.css("div.product_main")[0]
        table_rows = response.css("table tr")
        yield {
            'url': response.url,
            'title': book.css("h1 ::text").get(),
            'upc': table_rows[0].css("td ::text").get(),
            'product_type': table_rows[1].css("td ::text").get(),
            'price_excl_tax': table_rows[2].css("td ::text").get(),
            'price_incl_tax': table_rows[3].css("td ::text").get(),
            'tax': table_rows[4].css("td ::text").get(),
            'availability': table_rows[5].css("td ::text").get(),
            'num_reviews': table_rows[6].css("td ::text").get(),
            'stars': book.css("p.star-rating").attrib['class'],
            'category': book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': book.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': book.css('p.price_color ::text').get(),
        }

```

### 2. Using Proxy Middleware

The better approach to integrating proxy APIs into Scrapy spiders is by using a proxy middleware as there can be issues following URLs unless you customize the code to account for the Proxy URL.

Here you can either create your own middleware or some providers have built proxy middlewares for you to use.

With ScrapeOps they have a prebuilt proxy middleware that you can use.

You can quickly install it into your project using the following command:

```bash
pip install scrapeops-scrapy-proxy-sdk

```

And then enable it in your project in the `settings.py` file.

```python
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_PROXY_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

```

The other approach is to create a custom **Downloader Middleware** and activate it for the entire project, each spider individually or on each request. Here is an example middleware you can use:

```python
## middlewares.py

from urllib.parse import urlencode
from scrapy import Request

class ScrapeOpsProxyMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = 'https://proxy.scrapeops.io/v1/?'
        self.scrapeops_proxy_active = settings.get('SCRAPEOPS_PROXY_ENABLED', False)
        self._clean_proxy_settings(settings.get('SCRAPEOPS_PROXY_SETTINGS'))

    @staticmethod
    def _replace_response_url(response):
        real_url = response.headers.get(
            'Sops-Final-Url', def_val=response.url)
        return response.replace(
            url=real_url.decode(response.headers.encoding))
    
    def _clean_proxy_settings(self, proxy_settings):
        if proxy_settings is not None:
            for key, value in proxy_settings.items():
                clean_key = key.replace('sops_', '')
                self.scrapeops_proxy_settings[clean_key] = value
    
    def _get_scrapeops_url(self, request):
        payload = {'api_key': self.scrapeops_api_key, 'url': request.url}
        
        ## Global Request Settings
        if self.scrapeops_proxy_settings is not None:
            for key, value in self.scrapeops_proxy_settings.items():
                payload[key] = value

        ## Request Level Settings 
        for key, value in request.meta.items():
            if 'sops_' in key:
                clean_key = key.replace('sops_', '')
                payload[clean_key] = value

        proxy_url = self.scrapeops_endpoint + urlencode(payload)
        return proxy_url

    def _scrapeops_proxy_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_proxy_active == False:
            return False
        return True
    
    def process_request(self, request, spider):
        if self._scrapeops_proxy_enabled is False or self.scrapeops_endpoint in request.url:
            return None
        
        scrapeops_url = self._get_scrapeops_url(request)
        new_request = request.replace(
            cls=Request, url=scrapeops_url, meta=request.meta)
        return new_request

    def process_response(self, request, response, spider):
        new_response = self._replace_response_url(response)
        return new_response


```

And then enable it in your project in the `settings.py` file.

```python
## settings.py
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_PROXY_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'YOUR_PROJECT_NAME.middlewares.ScrapeOpsProxyMiddleware': 725,
}

```

Now when you run your spiders, the requests will be automatically sent through the [ScrapeOps Proxy API Aggregator](https://scrapeops.io/proxy-aggregator/).

Replace `YOUR_PROJECT_NAME`

Remember to swap the `YOUR_PROJECT_NAME` for the name of your project (`BOT_NAME` in your `settings.py` file).

Most proxy APIs allow you to use advanced functionality like JS rendering or country-level geotargeting by adding extra query parameters to your API query.

You can apply the proxy setting to every spider that runs in your project by adding a `SCRAPEOPS_PROXY_SETTINGS` dictionary to your `settings.py` file with the extra features you want to enable.

```python
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {'country': 'us'}
DOWNLOADER_MIDDLEWARES = {
'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

```

## Next Steps

In this part, we looked at why you need to use proxies to scale your web scraping without getting blocked. We gave examples on how to integrate the 3 most common types of proxies into our Scrapy spiders.

So in [Part 10](https://scrapeops.io/python-scrapy-playbook/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-10-deployment-scrapyd/), we will look at how you can use [Scrapyd](https://scrapyd.readthedocs.io/en/stable/) to deploy and run our spiders in the cloud, and control them using [ScrapeOps](https://scrapeops.io/monitoring-scheduling/) and [ScrapydWeb](https://github.com/my8100/scrapydweb).