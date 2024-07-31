# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            # get the value of the field
            if field_name != 'description':
                value = adapter.get(field_name)
                if value is not None and isinstance(value, str):
                    adapter[field_name] = value.strip()

        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ["category", "product_type"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value is not None and isinstance(value, str):
                adapter[lowercase_key] = value.lower()

        ## Price --> convert to float
        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None and isinstance(value, str):
                value = value.replace("£", "")
                adapter[price_key] = float(value)

        ## Availability --> extract number of books in stock
        availability_string = adapter.get("availability")
        if availability_string is not None and isinstance(availability_string, str):
            split_string_array = availability_string.split("(")
            
            if len(split_string_array) < 2:
                adapter["availability"] = 0
            else:
                availability_array = split_string_array[1].split(" ")
                adapter["availability"] = int(availability_array[0])

        ## Reviews --> convert string to number
        num_reviews_string = adapter.get("num_reviews")
        if num_reviews_string is not None:
            adapter["num_reviews"] = int(num_reviews_string)

        ## Stars --> convert text to number
        stars_string = adapter.get("stars")
        if stars_string is not None and isinstance(stars_string, str):
            split_stars_array = stars_string.split(" ")
            if len(split_stars_array) > 1:
                stars_text_value = split_stars_array[1].lower()
                stars_mapping = {
                    "zero": 0,
                    "one": 1,
                    "two": 2,
                    "three": 3,
                    "four": 4,
                    "five": 5,
                }
                adapter["stars"] = stars_mapping.get(stars_text_value, 0)

        return item
