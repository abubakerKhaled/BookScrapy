# Fake Headers & User Agents | ScrapeOps

## Getting Blocked Whilst Web Scraping

For this course we're scraping [BooksToScrape](https://books.toscrape.com/) a website intended to help you to learn web scraping, so it doesn't block you no matter how obvious it is you are a scraper.

However, what you will quickly find out when you start scraping protected websites like Amazon, Google, Zillow, etc, is that building and running your scrapers is the easy part.

The true difficulty of web scraping is in being able to reliably retrieve HTML responses from the pages you want to scrape.

This is because most websites want to limit or completely stop your ability to scrape data from their websites.

Websites use a number of methods to detect and ban scrapers from extracting their data:

- **IP Address**
- **TLS** or **TCP/IP fingerprint**
- **HTTP headers** (values, order and cases used)
- **Browser fingerprints**
- **Cookies/Sessions**

For more information on the above, then check out our [how to scrape without getting blocked guide here](https://scrapeops.io/web-scraping-playbook/web-scraping-without-getting-blocked/).

However, the most important and easiest to mitigate ways of bypassing a websites anti-bot protection systems is to **fake your headers and user-agents**, and use **rotating proxy pools**.

We will look at how you can integrate and rotate proxies with Scrapy.

However, for this we will focus why and how you should use fake headers and user-agents when scraping.

## What Are User-Agents & Why Do We Need To Manage Them?

User Agents are strings that let the website you are scraping identify the application, operating system (OSX/Windows/Linux), browser (Chrome/Firefox/Internet Explorer), etc. of the user sending a request to their website. They are sent to the server as part of the request headers.

Here is an example User agent sent when you visit a website with a Chrome browser:

```bash
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36

```

When scraping a website, you also need to set user-agents on every request as otherwise the website may block your requests because it knows you aren't a real user.

In the case of Scrapy. When you use Scrapy with the default settings, the user-agent your spider sends is the following by default:

```bash
Scrapy/VERSION (+https://scrapy.org)

```

This user agent will clearly identify your requests as coming from a web scraper, so the website can easily block you from scraping the site.

That is why we need to manage the user-agents Scrapy sends with our requests.

## How To Set A Fake User-Agent In Scrapy

There are a couple of ways to set new user agent for your spiders to use.

### 1. Set New Default User-Agent

The easiest way to change the default Scrapy user-agent is to set a default user-agent in your `settings.py` file.

Simply uncomment the `USER_AGENT` value in the `settings.py` file and add a new user agent:

```python
## settings.py
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

```

### 2. Add A User-Agent To Every Request

Another option is to set a user-agent on every request your spider makes by defining a user-agent in the headers of your request:

```python
## myspider.py
def start_requests(self):
    for url in self.start_urls:
    return Request(url=url, callback=self.parse,
                       headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})

```

Both of these options work, however, you will have the same user-agent for every single request which the target website might pick up on and block you for. That is why we need to have a list of user-agents and select a random one for every request.

## How To Rotate User Agents

Rotating through user-agents is also pretty straightforward, and we need a list of user-agents in our spider and use a random one with every request we make using a similar approach to [option #2 above](https://scrapeops.io/python-scrapy-playbook/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-8-fake-headers-user-agents/#2-add-a-user-agent-to-every-request).

```python
## myspider.py
import random
user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]
def start_requests(self):
    for url in self.start_urls:
    return Request(url=url, callback=self.parse,
                       headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]})

```

This works but it has 2 drawbacks:

1. We need to manage a list of user-agents ourselves.
2. We would need to implement this into every spider, which isn't ideal.

A better approach would be to use a Scrapy middleware to manage our user-agents for us.


## How To Manage Thousands of Fake User Agents

The best approach to managing user-agents in Scrapy is to build or use a custom Scrapy middleware that manages the user agents for you.

You could build a custom middleware yourself if your project has specific requirements like you need to use specific user-agents with specific sites. However, in most cases using a off-the-shelf user-agent middleware is enough.

Developers have realised of user-agent middlewares for Scrapy, however, for this guide we will use [ScrapeOps Fake User-Agent API](https://scrapeops.io/docs/fake-user-agent-headers-api/fake-user-agents/) as it is one of the best available.

### ScrapeOps Fake User-Agent API

The [ScrapeOps Fake User-Agent API](https://scrapeops.io/docs/fake-user-agent-headers-api/fake-user-agents/) is a **free user-agent API**, that returns a list of fake user-agents that you can use in your web scrapers to bypass some simple anti-bot defenses.

To use the **ScrapeOps Fake User-Agents API** you just need to send a request to the API endpoint to retrieve a list of user-agents.

You first need an **API key** which you can get by signing up for a [free account here](https://scrapeops.io/app/register/headers).

```bash
http://headers.scrapeops.io/v1/user-agents?api_key=YOUR_API_KEY

```

Example response from the API:

```python
{
  "result": [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
  ]
}

```

The best way to integrate the **Fake User-Agent API** is to create a Downloader middleware and have a fake user-agent be added to every request. Here is an example middleware you can use:

```python
## middlewares.py
from urllib.parse import urlencode
from random import randint
import requests
class ScrapeOpsFakeUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'http://headers.scrapeops.io/v1/user-agents?')
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()
    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])
    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]
    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

def process_request(self, request, spider):
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent

```

**Note:** This middleware example requires the installation of **Python Requests** via `pip install requests`.

And then enable it in our projects `settings.py` file.

```python
## settings.py
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
'bookscraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
}

```

When activated, the **ScrapeOpsFakeUserAgentMiddleware** will download a list of the most common user-agents from the API and use a random one with every request, so you don't need to create your own list.

To see all the configuration options, then check out the [docs here](https://scrapeops.io/docs/fake-user-agent-headers-api/fake-user-agents/).


## Fake Browser Headers vs Fake User-Agents

Just adding fake user-agents to your requests will help you scrape websites with simple anti-bot protection systems, however, for websites with proper anti-bot protection just setting users-agents isn't enough.

To convince these websites (Amazon, Google, etc.) you aren't a scraper you must be using fake browser headers to mimic mimic the browser fingerprints of real users.

For example, here is an example of the headers a **Chrome browser on a MacOS machine** would send to a website:

```bash
Host: 127.0.0.1:65432
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8

```

These fake browser headers include fake user-agents but also a lot of other headers that a real browser would typically send to the website.

As a result, if your requests don't contain the correct browser headers it is very easy for anti-bot protection systems to determine that the requests are not coming from a real users browser. So they block the requests.

Optimizing fake browser headers is a whole topic in of itself, so if you would like to learn more about it then [check out our guide to fake browser headers](https://scrapeops.io/web-scraping-playbook/web-scraping-guide-header-user-agents/).

## Using Fake Browser Headers With Scrapy

You can add fake browser headers just as you would add fake user-agents as user-agents are just one type of header:

```python
## myspider.py
def start_requests(self):
    fake_browser_header = {
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "\"Linux\"",
"sec-fetch-site": "none",
"sec-fetch-mod": "",
"sec-fetch-user": "?1",
"accept-encoding": "gzip, deflate, br",
"accept-language": "fr-CH,fr;q=0.9,en-US;q=0.8,en;q=0.7"
}
for url in self.start_urls:
return Request(url=url, callback=self.parse, headers=fake_browser_header)

```

### ScrapeOps Fake Browser Header API

The [ScrapeOps Fake Browser Header API](https://scrapeops.io/docs/fake-user-agent-headers-api/fake-browser-headers/) is a **free fake browser header API**, that returns a list of fake browser headers that you can use in your web scrapers to bypass more complex anti-bot defenses.

To use the **ScrapeOps Fake Browser Headers API** you just need to send a request to the API endpoint to retrieve a list of user-agents.

You first need an **API key** which you can get by signing up for a [free account here](https://scrapeops.io/app/register/headers).

```
http://headers.scrapeops.io/v1/browser-headers?api_key=YOUR_API_KEY

```

The best way to integrate the **Fake Browser Headers API** is to create a Downloader middleware and have a fake browser headers be added to every request. Here is an example middleware you can use:

```python
## middlewares.py
from urllib.parse import urlencode
from random import randint
import requests
class ScrapeOpsFakeBrowserHeaderAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers?')
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])


    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]


    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True

    def process_request(self, request, spider):
        random_browser_header = self._get_random_browser_header()
        request.headers = random_browser_header

```

**Note:** This middleware example requires the installation of **Python Requests** via `pip install requests`.

And then enable it in our projects `settings.py` file.

```python
## settings.py
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
DOWNLOADER_MIDDLEWARES = {
    'bookscraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 400,
}

```

When activated, the **ScrapeOpsFakeBrowserHeaderAgentMiddleware** will download a list of the most common browser headers from the API and use a random one with every request, so you don't need to create your own list.

To see all the configuration options, then check out the [docs here](https://scrapeops.io/docs/fake-user-agent-headers-api/fake-browser-headers/).


## Next Steps

In this part, we looked at why you need to manage your scrapers user-agents and headers when scraping websites. Along with how to manage them in Scrapy.

Optimizing your scrapers headers will help you bypass some anti-protection systems when scraping at smaller scales. However, when scraping at scale your requests are highly likely to get detected and blocked by websites as you will be using the same IP address for every request.

So in [Part 9](https://scrapeops.io/python-scrapy-playbook/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-9-rotating-proxies/), we will look at how you can use rotating proxy pools to hide your IP address and scrape at scale without getting blocked.