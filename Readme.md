## Scrapy Feed Exporters

Scrapy has a easy to use way to save the data to several different formats, [**Feed Exporters**](https://docs.scrapy.org/en/latest/topics/feed-exports.html).

Out of the box Scrapy's **FeedExporter** functionality provides the following formats to save/export the scraped data:

- JSON file format
- CVS file format
- XML file format
- Pythons pickle format

The files which are generated can then be saved to the following places using a Feed Exporter:

- The machine Scrapy is running on (obviously)
- To a remote machine using FTP (file transfer protocall)
- To Amazon S3 Storage
- To Google Cloud Storage
- Standard output


## Saving Data To CSVs

There are two approaches to saving data to CSVs with Scrapy:

- Via command line arguments
- Via FeedExporters in `settings.py` file

### Saving Data To CSVs Via Command Line

The first and simplest way to create a CSV file of the data you have scraped, is to simply define a output path when starting your spider in the command line.

To save to a CSV file add the flag `-o` to the `scrapy crawl` command along with the file path you want to save the file to.

You can set a relative path like below:

```bash
scrapy crawl bookspider -o bookspider_data.csv

```

Or you can also set a absolute path like this:

```bash
scrapy crawl bookspider -o file:///path/to/my/project/bookspider_data.csv

```

You have two options when using this command, use are small `-o` or use a capital `-O`.

| Flag | Description |
| ---  | --- |
| -o   | Appends new data to an existing file. |
| -O   | Overwrites any existing file with the same name with the current data. |

Telling Scrapy to save the data to a CSV via the command line is okay, but can be a little messy. The other option is setting it in your code, which Scrapy makes very easy.


### Saving Data To CSVs Via Feeds

Often the cleanest option is to tell Scrapy to save the data to a CSV via the [FEEDS](https://docs.scrapy.org/en/stable/topics/feed-exports.html#feeds) setting.

We can configure it in our `settings.py` file by passing it a dictionary with the path/name of the file and the file format:

```python
# settings.py
FEEDS = {
'data.csv': {'format': 'csv'}
}

```

You can also configure this in each individual spider by setting a `custom_setting` in your spider.

```python
# bookspider.py
import scrapy
from proxy_waterfall.items import BookItem
class BookSpider(scrapy.Spider):
	name = 'bookspider'
	start_urls = ["http://books.toscrape.com"]
	custom_settings = {
        'FEEDS': { 'data.csv': { 'format': 'csv',}}
    }

def parse(self, response):
    for article in response.css('article.product_pod'):
                book_item = BookItem(
                    url = article.css("h3 > a::attr(href)").get(),
                    title = article.css("h3 > a::attr(title)").extract_first(),
                    price = article.css(".price_color::text").extract_first(),
    )
    yield book_item

```

The default overwriting behaviour of the **FEEDS** functionality is dependant on where the data is going to be stored. However, you can set it to overwite existing data or not by adding a `overwrite` key to the `FEEDS` dictionary with either **True** or **False**.

```python
# settings.py
FEEDS = {
'data.csv': {'format': 'csv', 'overwrite': True}
}

```

When saving locally, by default `overwrite` is set to **False**. The full set of defaults can be found in the [Feeds docs](https://docs.scrapy.org/en/stable/topics/feed-exports.html#feeds).

Setting a static filepath is okay for development or very small projects, however, when in production you will likely don't want all your data being saved into one big file. So to solve this Scrapy allows you create dynamic file paths/names using spider variables.

For example, here tell create a CSV for the data in the data folder, followed by the subfolder with the spiders name, and a file name that includes the spider name and date it was scraped.

```python
# settings.py
FEEDS = {
'data/%(name)s/%(name)s_%(time)s.csv': {
'format': 'csv',
}
}

```

The generated path would look something like this.

```bash
"data/bookspider/bookspider_2022-05-18T07-47-03.csv"

```

There are a lot more customization options when saving CSVs which we cover in our [Saving Data To CSVs Guide](https://scrapeops.io/python-scrapy-playbook/scrapy-save-csv-files/)


## Saving Data To JSON Files

Like saving data to CSV files, there are two approaches to saving data to JSON files with Scrapy:

- Via command line arguments
- Via Feeds in `settings.py` file

### Saving Data To JSON Files Via Command Line

The first and simplest way to create a JSON file of the data you have scraped, is to simply define a output path when starting your spider in the command line.

To save to a JSON file add the flag `-o` to the `scrapy crawl` command along with the file path you want to save the file to.

You can set a relative path like below:

```
scrapy crawl bookspider -o bookspider_data.json

```

To save in JSON lines format, simply change the file format:

```bash
scrapy crawl bookspider -o bookspider_data.jsonl

```

Or you can also set a absolute path like this:

```bash
scrapy crawl bookspider -o file:///path/to/my/project/bookspider_data.jsonl

```

You have two options when using this command, use are small `-o` or use a capital `-O`.

| Flag | Description |
| ---  | --- |
| -o   | Appends new data to an existing file. |
| -O   | Overwrites any existing file with the same name with the current data. |

Saving To JSON vs JSON Lines Files

When saving in JSON format, we have two options: **JSON** and **JSON lines**.

Storing data in JSON format is okay for small amounts of data but it doesn’t scale well for large amounts of data, as incremental (aka. stream-mode) parsing is not well supported (if at all) and can result in the entire dataset being stored into memory creating the potential for a memory leak.

JSON data is held memory in an array and new data is appended to it:

```python
[
    {"name": "Color TV", "price": "1200"},
    {"name": "DVD player", "price": "200"}
]

```

As a result, it is advised to use JSON lines format if you want to save data in JSON.

```python
{"name": "Color TV", "price": "1200"}
{"name": "DVD player", "price": "200"}

```

Using JSON lines allows new data to be incrementally added to a file and can be split into numerous chunks.

### Saving Data To JSON Files Via Feeds

Telling Scrapy to save the data to a JSON via the command line is okay, but can be a little messy. The other option is setting it in your code, which Scrapy makes very easy.

Often the better option is to tell Scrapy to save the data to a JSON via the [FEEDS](https://docs.scrapy.org/en/stable/topics/feed-exports.html#feeds) setting.

We can configure it in our `settings.py` file by passing it a dictionary with the path/name of the file and the file format.

For JSON format:

```python
# settings.py
FEEDS = {
'data.json': {'format': 'json'}
}

```

For JSON lines format:

```python
# settings.py
FEEDS = {
'data.jsonl': {'format': 'jsonlines'}
}

```

You can also configure this in each individual spider by setting a `custom_setting` in your spider.

```python
# bookspider.py
import scrapy
from proxy_waterfall.items import BookItem
class BookSpider(scrapy.Spider):
	name = 'bookspider'
	start_urls = ["http://books.toscrape.com"]
	custom_settings = {
        'FEEDS': { 'data.jsonl': { 'format': 'jsonlines',}}
    }

def parse(self, response):
    for article in response.css('article.product_pod'):
                book_item = BookItem(
                    url = article.css("h3 > a::attr(href)").get(),
                    title = article.css("h3 > a::attr(title)").extract_first(),
                    price = article.css(".price_color::text").extract_first(),
    )
    yield book_item

```

The default overwriting behaviour of the **FEEDS** functionality is dependant on where the data is going to be stored. However, you can set it to overwite existing data or not by adding a `overwrite` key to the `FEEDS` dictionary with either **True** or **False**.

```python
# settings.py
FEEDS = {
    'data.jsonl': {'format': 'jsonlines', 'overwrite': True}
}

```

When saving locally, by default `overwrite` is set to **False**. The full set of defaults can be found in the [Feeds docs](https://docs.scrapy.org/en/stable/topics/feed-exports.html#feeds).


## Saving Data to a MySQL Database

When doing larger scale scraping it is normally better to store the scraped data into a database like MySQL or Postgres over saving to a CSV or JSON file.

Next, we will walk through how to save data to a MySQL database using Item Pipelines.

### Step 1: Get MySQL Database

To get started we first need to setup a MySQL database.

Either you can set one up on your local machine by using [one of the appropriate installer for your operating system](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).

Or you could get a hosted version with cloud provider like [DigitalOcean](https://m.do.co/c/2656441c8345).

Once setup you should have access to the database connection details of your database:

```python
host="localhost",
database="my_database",
user="root",
password="123456"

```

### Step 2: Install MySQL Python Library

To interact with our database we will need a library to handle the interaction. For this will install `mysql` and `mysql-connector-python`.

```bash
pip install mysql mysql-connector-python

```

We will use `mysql` to interact with our MySQL database.

### Step 3: Setup Our Pipeline

The next step is we need to open our `pipelines.py` file and set up our pipeline.

First, we're going to `import mysql` into our `pipelines.py` file, and create an `__init__` method that we will use to create our database and table.

```python
# pipelines.py
import mysql.connector
class SaveToMySQLPipeline:
def __init__(self):
pass
def process_item(self, item, spider):
return item

```

Inside the `__init__` method, we will configure the pipeline to do the following everytime the pipeline gets activated by a spider:

1. Try to connect to our database `books`, but if it doesn't exist create the database.
2. Create a cursor which we will use to execute SQL commands in the database.
3. Create a new table `books` with the columns for each field in our Item if one doesn't already exist in the database.

```python
# pipelines.py
import mysql.connector
class SaveToMySQLPipeline:
def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '******',
            database = 'books'
)
## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)
def process_item(self, item, spider):
return item

```

### Step 4: Save Scraped Items Into Database

Next, we're going to use the `process_item` event inside in our Scrapy pipeline to store the data we scrape into our MySQL database.

The `process_item` will be activated everytime, a item is scraped by our spider so we need to configure the `process_item` method to insert the items data in the database.

We will also the `close_spider` method, which will be called when the Spider is shutting down, to close our connections to the cursor and database to avoid leaving the connection open.

```python
# pipelines.py
import mysql.connector
class SaveToMySQLPipeline:
def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '******',
            database = 'books'
)
## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)
def process_item(self, item, spider):
## Define insert statement
        self.cur.execute(""" insert into books (
            url,
            title,
            upc,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
str(item["description"])
))
## Execute insert of data into database
        self.conn.commit()

def close_spider(self, spider):
## Close cursor & connection to database
        self.cur.close()
        self.conn.close()

```

### Step 5: Activate Our Item Pipeline

Finally, to activate our Item Pipeline we need to include it in our `settings.py` file:

```python
# settings.py
ITEM_PIPELINES = {
'bookscraper.pipelines.SaveToMySQLPipeline': 300,
}

```

Now, when we run our `bookspider` it will save the scraped data into our `books` MySQL database.`

This is a example of a simple MySQL integration, if you would like to learn more about saving data into MySQL databases with Scrapy then [checkout our Scrapy MySQL Guide here](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-mysql/).

## Saving Data to a Postgres Database

Another common database developers like to save their scraped data into is Postgres databases which are ideally suited to large amounts of scraped data.

### Step 1: Get Postgres Database

To get started we first need to setup a Postgres database.

Either you can set one up on your local machine by using [one of the following downloads](https://www.postgresql.org/download/).

Or you could get a hosted version with cloud provider like [DigitalOcean](https://m.do.co/c/2656441c8345).

Once setup you should have access to the database connection details of your database:

```python
host="localhost",
database="my_database",
user="root",
password="123456"

```

### Step 2: Install psycopg2

To interact with our database we will need a library to handle the interaction. For this will install `psycopg2`.

```bash
pip install psycopg2

```

We will use `psycopg2` to interact with our Postgres database.

### Step 3: Setup Our Pipeline

The next step is we need to open our `pipelines.py` file and set up our pipeline.

First, we're going to `import psycopg2` into our `pipelines.py` file, and create an `__init__` method that we will use to create our database and table.

```python
# pipelines.py
import psycopg2
class SaveToPostgresPipeline:
def __init__(self):
pass
def process_item(self, item, spider):
return item

```

Inside the `__init__` method, we will configure the pipeline to do the following everytime the pipeline gets activated by a spider:

1. Try to connect to our database `books`, but if it doesn't exist create the database.
2. Create a cursor which we will use to execute SQL commands in the database.
3. Create a new table `books` with columns for every field in our Item, if one doesn't already exist in the database.

```python
# pipelines.py
import psycopg2
class SaveToPostgresPipeline:
    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = '*******' # your password
        database = 'books'
        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text
        )
        """)
    def process_item(self, item, spider):
    return item

```

### Step 4: Save Scraped Items Into Postgres Database

Next, we're going to use the `process_item` event inside in our Scrapy pipeline to store the data we scrape into our Postgres database.

The `process_item` will be activated everytime, a item is scraped by our spider so we need to configure the `process_item` method to insert the items data in the database.

We will also the `close_spider` method, which will be called when the Spider is shutting down, to close our connections to the cursor and database to avoid leaving the connection open.

```python
# pipelines.py
import psycopg2
class SaveToPostgresPipeline:
def __init__(self):
## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = '******' # your password
        database = 'books'
## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text
        )
        """)
def process_item(self, item, spider):
## Define insert statement
        self.cur.execute(""" insert into books (
            url,
            title,
            upc,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
str(item["description"])
))
## Execute insert of data into database
        self.connection.commit()
return item
def close_spider(self, spider):
## Close cursor & connection to database
        self.cur.close()
        self.connection.close()

```

### 5. Activate Our Item Pipeline

Finally, to activate our Item Pipeline we need to include it in our `settings.py` file:

```python
# settings.py
ITEM_PIPELINES = {
'bookscraper.pipelines.SaveToPostgresPipeline': 300,
}

```

Now, when we run our **books** spider the **SaveToPostgresPipeline** will store all the scraped items in the database.

This is an example of a simple Postgres integration, if you would like to learn more about saving data into Postgres databases with Scrapy then [checkout our Scrapy Postgres Guide here](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-postgres/).