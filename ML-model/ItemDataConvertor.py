import pandas as pd
from DataTypes import Item
from consts import USD_TO_LKR
from gemini import generate_llm_tags_bulk

def csv_to_list(csv_file_path):
    """
    Converts a CSV file containing product data into a list of Item objects.
    
    Args:
        csv_file_path (str): Path to the CSV file
        
    Returns:
        list: List of Item objects containing product information
    """
    df = pd.read_csv(csv_file_path)
    df = df.fillna('')  # Replace NaN values with empty strings
    items_list = []
    tags = generate_llm_tags_bulk(df)  # Generate tags using LLM for all products
    for _, row in df.iterrows():
        if 'in' in row['availability'].lower():  # Only process items that are in stock
            item = Item(
                name=row['product_name'],
                price=generate_price(row), 
                description=row['description'],
                link=row['product_url'],
                rate=float(row['product_rating']) if row['product_rating'] != '' else 0,
                tags=tags[row["product_name"]],
                image_link=row['image'],
            )
            # Only add items that have at least one of: name, price, or link
            if item.name != '' or item.price !='' or item.link != '':
                items_list.append(item)
    return items_list

def generateTags(df):
    """
    Generates a list of tags for a product based on various attributes.
    
    Args:
        df (pandas.Series): Row of product data
        
    Returns:
        list: Unique list of tags for the product
    """
    tags = []
    tags.append(df['brand'].lower())
    # Extract color tags
    for t in df['color'].replace('[', '').replace(']', '').replace('\'', '').replace('\"', '').split(','):
        tags.append(t.lower())
    # Add shipping and warranty tags if applicable    
    if 'true' in str(df['shipping']).lower():
        tags.append('shipping')
    if 'true' in str(df['warranty']).lower():
        tags.append('warranty')   
    # Add tags from product name
    for t in df['product_name'].lower().split():
        tags.append(t)
    # Add tags from description    
    for t in df['description'].lower().replace(':','').split():
        tags.append(t)
    # Remove duplicates
    tags = set(tags)
    tags = list(tags)
    return tags

def generate_price(df):
    """
    Calculates the final price including delivery cost and currency conversion if needed.
    
    Args:
        df (pandas.Series): Row of product data
        
    Returns:
        float: Final price in LKR
    """
    delivery_cost = 0
    if df['delivery_cost'] != '':
        delivery_cost = float(df['delivery_cost'])

    if '$' in df['currency']:  # Convert USD to LKR
        if delivery_cost>0:
            return (float(df['price'].replace(',', '')) + delivery_cost) * USD_TO_LKR
        else:
            return float(df['price'].replace(',', '')) * USD_TO_LKR
    else:  # Price already in LKR
        if delivery_cost>0:
            return (float(df['price'].replace(',', '')) + delivery_cost)
        else:
            return float(df['price'].replace(',', ''))

def replace_special_chars(s):
    """
    Removes all special characters from a string.
    
    Args:
        s (str): Input string
        
    Returns:
        str: String with all special characters removed
    """
    return s.replace('[', '').replace(']', '').replace('\'', '').replace('\"', '').replace(':', '').replace(',', '').replace('(', '').replace(')', '').replace('*', '').replace('?', '').replace('!', '').replace(';', '').replace('.', '').replace('\\', '').replace('/', '').replace('|', '').replace('{', '').replace('}', '').replace('^', '').replace('~', '').replace('`', '').replace('=', '').replace('+', '').replace('-', '').replace('_', '').replace('"', '').replace('\'', '').replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('\v', '').replace('\f', '').replace('\b', '' )

def print_items(items):
    """
    Prints a formatted list of items with their details.
    
    Args:
        items (list): List of Item objects to print
    """
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

# Example usage:
# l = csv_to_list('product.csv')
# print_items(l)