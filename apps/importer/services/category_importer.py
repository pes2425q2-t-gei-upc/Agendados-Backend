from apps.events.models import Category
import pandas as pd

def import_category(row):
    category_name = row["Tags categoríes"]
    if pd.isna(category_name):  #Return none if category is NaN
        return None

    category, created = Category.objects.get_or_create(name=parse_category(category_name))
    return category

def parse_category(category_string):
    print(category_string)
    category = category_string.split("/")[-1]
    formatted_category = category.replace("-", " ").title()
    return formatted_category