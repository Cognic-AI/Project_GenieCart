import DataTypes as dt
import Model

# Create machine customers (3 per real customer, with different item interests)
machine_customers = [
    # For John Smith
    dt.MachineCustomer(1, "phone", 1, tags=["premium", "latest"]),
    dt.MachineCustomer(1, "laptop", 1, tags=["business", "powerful"]),
    dt.MachineCustomer(5, "car", 1, tags=["luxury", "sports"]),
    
    # For Mary Johnson
    dt.MachineCustomer(2, "phone", 2, tags=["mid-range", "value"]),
    dt.MachineCustomer(1, "laptop", 1, tags=["portable","mac"],isHistory=True),
    dt.MachineCustomer(7, "car", 2, tags=["family", "efficient"]),
    
    # For Bob Wilson
    dt.MachineCustomer(3, "phone", 3, tags=["budget", "basic"]),
    dt.MachineCustomer(3, "laptop", 3, tags=["entry-level", "student"]),
    dt.MachineCustomer(4, "car", 3, tags=["economy", "compact"]),
    
    # For Alice Brown
    dt.MachineCustomer(5, "phone", 1, tags=["flagship", "camera"]),
    dt.MachineCustomer(6, "laptop", 1, tags=["premium", "creator"]),
    dt.MachineCustomer(6, "car", 1, tags=["premium", "electric"]),
    
    # For James Davis
    dt.MachineCustomer(8, "phone", 2, tags=["balanced", "durable"]),
    dt.MachineCustomer(9, "laptop", 2, tags=["multimedia", "versatile"]),
    dt.MachineCustomer(10, "car", 2, tags=["midsize", "reliable"])
]

# Create dtems lists
phones = [
    dt.Item("iPhone 14 Pro", 999, "Latest Apple flagship", "link1", 4.8, ["premium", "latest", "flagship", "iphone", "pro", "apple"], 0),
    dt.Item("Samsung S23 Ultra", 1199, "Premium Android flagship", "link2", 4.9, ["premium", "latest", "samsung", "ultra", "s23"], 0),
    dt.Item("Google Pixel 7", 599, "Great camera phone", "link3", 4.7, ["mid-range", "camera", "google", "pixel"], 0),
    dt.Item("OnePlus 11", 699, "Fast performance", "link4", 4.6, ["mid-range", "fast", "oneplus"], 0),
    dt.Item("iPhone 13", 699, "Previous gen flagship", "link5", 4.7, ["premium", "iphone", "apple"], 0),
    dt.Item("Samsung A53", 449, "Mid-range Samsung", "link6", 4.5, ["mid-range", "balanced", "samsung", "a53"], 0),
    dt.Item("Motorola G Power", 249, "Budget battery king", "link7", 4.3, ["budget", "battery", "motorola", "power"], 0),
    dt.Item("iPhone SE", 429, "Budget iPhone", "link8", 4.4, ["budget", "compact", "iphone", "se", "apple"], 0),
    dt.Item("Xiaomi 13", 899, "Premium features", "link9", 4.6, ["premium", "value", "xiaomi"], 0),
    dt.Item("Nothing Phone", 749, "Unique design", "link10", 4.5, ["mid-range", "unique", "nothing"], 0),
    dt.Item("Sony Xperia 1", 1299, "Premium multimedia", "link11", 4.7, ["premium", "multimedia", "sony", "xperia"], 0),
    dt.Item("ASUS ROG Phone", 999, "Gaming focused", "link12", 4.8, ["premium", "gaming", "asus", "rog"], 0),
    dt.Item("Samsung Z Fold4", 1799, "Foldable flagship", "link13", 4.7, ["premium", "innovative", "samsung", "fold", "z"], 0),
    dt.Item("Google Pixel 6a", 349, "Mid-range Google", "link14", 4.5, ["budget", "camera", "google", "pixel"], 0),
    dt.Item("Huawei P50", 899, "Premium build", "link15", 4.6, ["premium", "design", "huawei", "p50"], 0),
    dt.Item("Oppo Find X", 949, "Premium features", "link16", 4.7, ["premium", "camera", "oppo", "find", "x"], 0),
    dt.Item("Vivo X90", 799, "Premium mid-range", "link17", 4.6, ["mid-range", "camera", "vivo", "x90"], 0),
    dt.Item("Nokia X30", 499, "Mid-range durabildty", "link18", 4.4, ["mid-range", "durable", "nokia", "x30"], 0),
    dt.Item("Realme GT", 599, "Performance focused", "link19", 4.5, ["mid-range", "fast", "realme", "gt"], 0),
    dt.Item("Poco F4", 399, "Budget flagship", "link20", 4.4, ["budget", "performance", "poco", "f4"], 0)
]

laptops = [
    dt.Item("MacBook Pro 16", 2499, "Premium Apple laptop", "link21", 4.9, ["premium", "powerful", "mac", "pro", "apple"], 0),
    dt.Item("Dell XPS 15", 2299, "Premium Windows laptop", "link22", 4.8, ["premium", "business", "dell", "xps"], 0),
    dt.Item("Lenovo ThinkPad X1", 1999, "Business laptop", "link23", 4.8, ["business", "reliable", "lenovo", "thinkpad", "x1"], 0),
    dt.Item("HP Spectre x360", 1699, "Premium convertible", "link24", 4.7, ["premium", "versatile", "hp", "spectre", "x360"], 0),
    dt.Item("ASUS ROG Zephyrus", 2199, "Gaming laptop", "link25", 4.8, ["premium", "gaming", "asus", "rog", "zephyrus"], 0),
    dt.Item("Acer Swift 5", 1099, "Ultraportable", "link26", 4.6, ["mid-range", "portable", "acer", "swift"], 0),
    dt.Item("Microsoft Surface Laptop", 999, "Clean design", "link27", 4.7, ["mid-range", "design", "microsoft", "surface"], 0),
    dt.Item("Dell Inspiron 15", 799, "General purpose", "link28", 4.5, ["mid-range", "general", "dell", "inspiron"], 0),
    dt.Item("HP Envy 13", 899, "Premium build", "link29", 4.6, ["mid-range", "premium", "hp", "envy"], 0),
    dt.Item("Lenovo Yoga 7i", 899, "Convertible", "link30", 4.6, ["mid-range", "versatile", "lenovo", "yoga"], 0),
    dt.Item("ASUS VivoBook", 649, "Budget friendly", "link31", 4.4, ["budget", "value", "asus", "vivobook"], 0),
    dt.Item("Acer Aspire 5", 599, "Budget performance", "link32", 4.3, ["budget", "performance", "acer", "aspire"], 0),
    dt.Item("HP Pavilion", 699, "Entry level", "link33", 4.4, ["budget", "general", "hp", "pavilion"], 0),
    dt.Item("HP Pavilion2", 799, "Entry level", "link33", 4.3, ["budget", "general", "hp", "pavilion"], 0),
    dt.Item("Lenovo IdeaPad 3", 549, "Student laptop", "link34", 4.3, ["budget", "student", "lenovo", "ideapad"], 0),
    dt.Item("MSI Modern 14", 799, "Slim design", "link35", 4.5, ["mid-range", "portable", "msi", "modern"], 0),
    dt.Item("Razer Blade 15", 1999, "Premium gaming", "link36", 4.8, ["premium", "gaming", "razer", "blade"], 0),
    dt.Item("LG Gram 17", 1599, "Lightweight premium", "link37", 4.7, ["premium", "portable", "lg", "gram"], 0),
    dt.Item("Gigabyte Aero", 1799, "Creator laptop", "link38", 4.7, ["premium", "creator", "gigabyte", "aero"], 0),
    dt.Item("Framework Laptop", 999, "Modular design", "link39", 4.6, ["mid-range", "innovative", "framework"], 0),
    dt.Item("Chromebook Pixel", 649, "Premium Chromebook", "link40", 4.5, ["budget", "portable", "chromebook", "pixel", "google"], 0)
]

cars = [
    dt.Item("Tesla Model S", 89990, "Premium electric sedan", "link41", 4.8, ["premium", "electric", "tesla", "model", "s"], 0),
    dt.Item("BMW 7 Series", 93400, "Luxury sedan", "link42", 4.9, ["luxury", "premium", "bmw", "7series"], 0),
    dt.Item("Mercedes S-Class", 94250, "Ultimate luxury", "link43", 4.9, ["luxury", "premium", "mercedes", "sclass"], 0),
    dt.Item("Porsche 911", 106100, "Sports car", "link44", 4.9, ["luxury", "sports", "porsche", "911"], 0),
    dt.Item("Audi A8", 86500, "Luxury sedan", "link45", 4.8, ["luxury", "premium", "audi", "a8"], 0),
    dt.Item("Toyota Camry", 25945, "Mid-size sedan", "link46", 4.7, ["midsize", "reliable", "toyota", "camry"], 0),
    dt.Item("Honda Accord", 26520, "Family sedan", "link47", 4.7, ["family", "reliable", "honda", "accord"], 0),
    dt.Item("BMW 3 Series", 43300, "Entry luxury", "link48", 4.7, ["premium", "sports", "bmw", "3series"], 0),
    dt.Item("Tesla Model 3", 46990, "Electric sedan", "link49", 4.8, ["premium", "electric", "tesla", "model", "3"], 0),
    dt.Item("Hyundai Sonata", 24950, "Mid-size value", "link50", 4.6, ["midsize", "value", "hyundai", "sonata"], 0),
    dt.Item("Toyota Corolla", 20425, "Compact car", "link51", 4.6, ["economy", "reliable", "toyota", "corolla"], 0),
    dt.Item("Honda Civic", 22550, "Compact car", "link52", 4.7, ["economy", "efficient", "honda", "civic"], 0),
    dt.Item("Mazda 3", 21445, "Compact premium", "link53", 4.6, ["economy", "premium", "mazda", "3"], 0),
    dt.Item("Volkswagen Golf", 23195, "Compact hatch", "link54", 4.5, ["economy", "practical", "volkswagen", "golf"], 0),
    dt.Item("Hyundai Elantra", 20500, "Compact value", "link55", 4.5, ["economy", "value", "hyundai", "elantra"], 0),
    dt.Item("Ford Mustang", 27470, "Sports car", "link56", 4.7, ["sports", "performance", "ford", "mustang"], 0),
    dt.Item("Chevrolet Corvette", 64995, "Premium sports", "link57", 4.8, ["premium", "sports", "chevrolet", "corvette"], 0),
    dt.Item("Lexus ES", 41875, "Entry luxury", "link58", 4.7, ["premium", "comfort", "lexus", "es"], 0),
    dt.Item("Audi A4", 39900, "Entry luxury", "link59", 4.7, ["premium", "balanced", "audi", "a4"], 0),
    dt.Item("Genesis G70", 37775, "Entry luxury", "link60", 4.6, ["premium", "value", "genesis", "g70"], 0)
]

def execute(item_array,machine_customer):
    model  = Model.Model(item_array,machine_customer)
    return model.execute()

result = execute(laptops,machine_customers[4])