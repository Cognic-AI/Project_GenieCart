import pandas as pd
from DataTypes import Item
from consts import USD_TO_LKR
from gemini import generate_llm_tags_bulk

def csv_to_list(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df = df.fillna('')
    items_list = []
    tags = generate_llm_tags_bulk(df)
    for _, row in df.iterrows():
        if 'in' in row['availability'].lower():
            item = Item(
                name=row['product_name'],
                price=generate_price(row), 
                description=row['description'],
                link=row['product_url'],
                rate=float(row['product_rating']) if row['product_rating'] != '' else 0,
                # tags=generateTags(row),
                tags=tags[row["product_name"]],
                image_link=row['image'],
            )
            if item.name != '' or item.price !='' or item.link != '':
                items_list.append(item)
    return items_list

def generateTags(df):
    tags = []
    tags.append(df['brand'].lower())
    for t in df['color'].replace('[', '').replace(']', '').replace('\'', '').replace('\"', '').split(','):
        tags.append(t.lower())
    if 'true' in str(df['shipping']).lower():
        tags.append('shipping')
    if 'true' in str(df['warranty']).lower():
        tags.append('warranty')   
    for t in df['product_name'].lower().split():
        tags.append(t)
    for t in df['description'].lower().replace(':','').split():
        tags.append(t)
    tags = set(tags)
    tags = list(tags)
    return tags

def generate_price(df):
    delivery_cost = 0
    if df['delivery_cost'] != '':
        delivery_cost = float(df['delivery_cost'])

    if '$' in df['currency']:
        if delivery_cost>0:
            return (float(df['price'].replace(',', '')) + delivery_cost) * USD_TO_LKR
        else:
            return float(df['price'].replace(',', '')) * USD_TO_LKR
    else:
        if delivery_cost>0:
            return (float(df['price'].replace(',', '')) + delivery_cost)
        else:
            return float(df['price'].replace(',', ''))

def replace_special_chars(s):
    return s.replace('[', '').replace(']', '').replace('\'', '').replace('\"', '').replace(':', '').replace(',', '').replace('(', '').replace(')', '').replace('*', '').replace('?', '').replace('!', '').replace(';', '').replace('.', '').replace('\\', '').replace('/', '').replace('|', '').replace('{', '').replace('}', '').replace('^', '').replace('~', '').replace('`', '').replace('=', '').replace('+', '').replace('-', '').replace('_', '').replace('"', '').replace('\'', '').replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('\v', '').replace('\f', '').replace('\b', '' )

def print_items(items):
    print("\n=== Item List ===")
    for item in items:
        print(f"\nItem: {item.name}")
        print(f"Price: LKR {item.price:,.2f}")
        print(f"Description: {item.description}")
        print(f"Rating: {int(item.rate)}")
        print(f"Tags: {', '.join(item.tags)}")
        print(f"Product Link: {item.link}")
        if item.image_link:
            print(f"Image Link: {item.image_link}")
        print("-" * 50)

# l = csv_to_list('product.csv')
# print_items(l)