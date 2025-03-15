from apps.events.models import Category
import pandas as pd

def import_categories(row):
    categories_string = row["Tags categoríes"]
    if pd.isna(categories_string):  #Return none if category is NaN
        return None

    categories_array = categories_string.split(",")
    result = []
    for category_name in categories_array:
        category, created = Category.objects.get_or_create(name=parse_category(category_name))
        result.append(category)
    return result

def parse_category(category_string):
    category = category_string.split("/")[-1]
    formatted_category = category.replace("-", " ").title()
    return formatted_category