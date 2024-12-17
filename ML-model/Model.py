import consts
import math
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import DataTypes as dt

print("<====================>")
print("MODEL INITIALIZATION")
print("<====================>")

class Model:
    def __init__(self, item_array, machine_customer_query):
        """Initialize the model with item array and machine customer query"""
        print("Initializing Model...")
        self.item_array = item_array
        self.machine_customer_query = machine_customer_query
        self.no_of_high = 0
        self.no_of_low = 0
        self.no_of_middle = 0
        print("Initializing prices...")
        self.initializePrices()
        print("Initializing tags vector...")
        self.tags = self.initializeTagsVector()
        print("Model initialization complete")

    def execute(self):
        """Execute the model to get recommendations"""
        print("\n<====================>")
        print("MODEL EXECUTION")
        print("<====================>")
        print("Executing model...")
        print("Assigning scores to items...")
        self.assigningScores()
        print("Getting final results...")
        result = self.getFinalResult()
        print("Model execution complete")
        return result

    def assigningScores(self):
        """Assign scores to items based on price, rating and tags"""
        print("\n<====================>")
        print("SCORE ASSIGNMENT")
        print("<====================>")
        print("Starting score assignment for all items...")
        for i in self.item_array:
            print(f"\nProcessing item: {i.name}")
            # Calculate and add price score based on price level and availability
            price_score = self.addPriceScoreImproved(i.price)  # Using improved version
            print(f"Price score: {price_score}")
            print(f"Item score before: {i.score}")
            i.score += price_score
            
            # Calculate and add rating score using rate score factor
            rate_score = i.rate*consts.RATE_SCORE_FACTOR
            print(f"Rate score: {rate_score}")
            i.score += rate_score
            
            # Calculate and add tag matching score
            tag_score = self.addTagScore(i)
            print(f"Tag score: {tag_score}")
            i.score += tag_score
            print(f"Total score for {i.name}: {i.score}")

    
    def initializePrices(self):
        """Initialize min, max and middle prices from item array"""
        print("\n<====================>")
        print("PRICE INITIALIZATION")
        print("<====================>")
        print("Finding min and max prices...")
        min_p = None
        max_p = None
        for i in self.item_array:
            if min_p==None:
                min_p = i.price
                max_p = i.price
                continue
            if min_p>i.price:
                min_p= i.price
                continue
            if max_p<i.price:
                max_p = i.price
        
        self.min_p = min_p
        self.max_p = max_p
        self.middle_p = (min_p + max_p)/2
        print(f"Price ranges initialized - Min: {min_p}, Max: {max_p}, Middle: {self.middle_p}")

    def addPriceScore(self,price):
        """Calculate price score based on price level and availability"""
        print(f"\nCalculating price score for price: {price}")
        # Calculate gaps to different price points
        upper_gap = self.max_p-price
        middle_gap = abs(self.middle_p-price)
        below_gap = price-self.min_p

        min_gap = min([upper_gap,middle_gap,below_gap])
        print(f"Gaps - Upper: {upper_gap}, Middle: {middle_gap}, Below: {below_gap}")

        # Determine price level category based on smallest gap
        if min_gap == upper_gap:
            price_level_cal = consts.HIGH_END_USER
            self.no_of_high+=1
            print("Categorized as HIGH END")
        elif min_gap == middle_gap:
            price_level_cal = consts.MIDDLE_USER
            self.no_of_middle+=1
            print("Categorized as MIDDLE")
        else:
            price_level_cal = consts.LOW_END_USER
            self.no_of_low+=1
            print("Categorized as LOW END")

        # Calculate mapped gap score
        if len(self.item_array)==1:
            mapped_gap = 1
        else:
            mapped_gap = (self.max_p -self.min_p - min_gap)/(self.max_p -self.min_p)

        print(mapped_gap)
        
        # Return final price score based on price level match and availability
        if self.machine_customer_query.price_level == price_level_cal:
            if self.no_of_high>=consts.EXACT_AVAILABILITY_THRESHOLD:
                return consts.EXACT*mapped_gap + consts.AVAILABLE
            else:
                return consts.EXACT*mapped_gap + consts.NOT_AVAILABLE
        if self.machine_customer_query.price_level == consts.MIDDLE_USER:
            if self.no_of_middle>=consts.NORMAL_AVAILABILITY_THRESHOLD:
                return consts.NORMAL*mapped_gap + consts.AVAILABLE
            else:
                return consts.NORMAL*mapped_gap + consts.NOT_AVAILABLE
        if self.no_of_low>=consts.WORST_AVAILABILITY_THRESHOLD:
            return consts.WORST*mapped_gap + consts.AVAILABLE
        else:
            return consts.WORST*mapped_gap + consts.NOT_AVAILABLE

    def addPriceScoreImproved(self, price):
        """Improved price scoring with smoother transitions and better range handling"""
        print(f"\nCalculating improved price score for price: {price}")
        
        # Define normalized price
        price_range = self.max_p - self.min_p
        normalized_price = (price - self.min_p) / price_range

        # Define scoring ranges for middle user
        price_range_buffer = price_range * 0.2
        lower_mid = self.middle_p - price_range_buffer
        upper_mid = self.middle_p + price_range_buffer
        
        # Calculate score based on user preference
        if self.machine_customer_query.price_level == consts.HIGH_END_USER:
            # Sigmoid function for smoother transitions
            base_score = 5 / (1 + math.exp(-10 * (normalized_price - 0.8)))
        elif self.machine_customer_query.price_level == consts.LOW_END_USER:
            # Sigmoid function for smoother transitions
            base_score = 5 / (1 + math.exp(-10 * (0.2 - normalized_price)))
        else:  # MIDDLE_USER
            # Gaussian function centered on middle price
            sigma = price_range_buffer / 2
            base_score = 5 * math.exp(-((price - self.middle_p) ** 2) / (2 * sigma ** 2))
        
        # Add availability bonus
        availability_bonus = 0
        if self.machine_customer_query.price_level == consts.HIGH_END_USER and self.no_of_high >= consts.EXACT_AVAILABILITY_THRESHOLD:
            availability_bonus = 1
        elif self.machine_customer_query.price_level == consts.MIDDLE_USER and self.no_of_middle >= consts.NORMAL_AVAILABILITY_THRESHOLD:
            availability_bonus = 1
        elif self.machine_customer_query.price_level == consts.LOW_END_USER and self.no_of_low >= consts.WORST_AVAILABILITY_THRESHOLD:
            availability_bonus = 1
        
        total_score = base_score + availability_bonus
        print(f"Improved price score: {total_score}")
        return total_score

    
    
    def initializeTagsVector(self):
        """Initialize tag weights based on customer purchase history"""
        print("\n<====================>")
        print("TAG INITIALIZATION")
        print("<====================>")
        if self.machine_customer_query.history == []:
            print("No history found, returning empty dictionary")
            return dict()
        tags_vector = dict()
        total_tags = 0
        
        # Count frequency of each tag in history
        for h in self.machine_customer_query.history:
            print(f"Processing history item: {h.name}")
            for tag in h.tags:
                total_tags+=1
                if tag in list(tags_vector.keys()):
                    tags_vector[tag] += 1
                else:
                    tags_vector[tag] = 1
        
        # Normalize tag weights by dividing by total tags
        print("Normalizing tag weights...")
        for k in list(tags_vector.keys()):
            tags_vector[k] = tags_vector[k]/total_tags
            print(f"Tag {k}: weight = {tags_vector[k]}")
        
        return tags_vector

    def addTagScore(self, item):
        """Calculate tag matching score for an item"""
        print(f"Calculating tag score for {item.name}")
        sum = 0
        for t in item.tags:
            print(f"Checking tag: {t}")
            # Add score for tags matching history
            if t in self.tags.keys() and self.machine_customer_query.isHistory:
                history_score = self.tags[t] * consts.TAG_HIT
                sum += history_score
                print(f"Tag {t} matched in history, adding score: {history_score}")
            # Add score for tags matching query
            if t in self.machine_customer_query.tags:
                sum+=consts.TAG_HIT
                print(f"Tag {t} matched in query tags, adding score: {consts.TAG_HIT}")
        print(f"Final tag score for {item.name}: {sum}")
        return sum

    def addTagScoreImproved(self, item):
        """
        Calculate an improved tag matching score using cosine similarity
        and weighted tag importance
        """
        print(f"Calculating improved tag score for {item.name}")
        
        # Create user tags dictionary with weights
        user_tags = Counter()
        if self.machine_customer_query.isHistory:
            user_tags.update(self.history)
        for tag in self.machine_customer_query.tags:
            user_tags[tag] += 1.5  # Higher weight for explicit query tags
            
        # Define tag importance based on common retail categories
        tag_importance = {
            
        }
        
        # Convert tags to vectors for cosine similarity
        all_tags = list(set(list(user_tags.keys()) + item.tags))
        user_vector = [user_tags.get(tag, 0) * tag_importance.get(tag, 1.0) for tag in all_tags]
        item_vector = [1.0 * tag_importance.get(tag, 1.0) if tag in item.tags else 0 for tag in all_tags]
        
        # Reshape vectors for sklearn
        user_vector = [user_vector]
        item_vector = [item_vector]
        
        # Calculate cosine similarity
        similarity = cosine_similarity(user_vector, item_vector)[0][0]
        
        print(f"Final improved tag score for {item.name}: {similarity}")
        return similarity

    def getFinalResult(self):
        """Sort items by score and return sorted array"""
        print("\n<====================>")
        print("FINAL RESULTS")
        print("<====================>")
        print("Sorting items by score...")
        self.item_array.sort(key=lambda x: x.score, reverse=True)
        print("Top 3 items:")
        for i in range(len(self.item_array)):
            print(f"{i+1}. {self.item_array[i].name} - Score: {self.item_array[i].score}")
        return self.item_array


# def test_tag_score(item, machine_customer_query, history=None):
#     """
#     Standalone test function for tag score calculation using cosine similarity
#     and weighted tag importance
#     """
#     print(f"Calculating test tag score for {item.name}")
    
#     # Create user tags dictionary with weights  
#     user_tags = Counter()
#     if machine_customer_query.isHistory and history:
#         user_tags.update(history)
#     for tag in machine_customer_query.tags:
#         user_tags[tag] += 1.5  # Higher weight for explicit query tags
        
#     # Define tag importance based on common retail categories
#     tag_importance = {
#         'premium': 1.3,
#         'budget': 1.3,
#         'quality': 1.2,
#         'performance': 1.2,
#         'value': 1.1,
#         'portable': 1.1
#     }
    
#     # Convert tags to vectors for cosine similarity
#     all_tags = list(set(list(user_tags.keys()) + item.tags))
#     user_vector = [user_tags.get(tag, 0) * tag_importance.get(tag, 1.0) for tag in all_tags]
#     item_vector = [1.0 * tag_importance.get(tag, 1.0) if tag in item.tags else 0 for tag in all_tags]
    
#     # Reshape vectors for sklearn
#     user_vector = [user_vector]
#     item_vector = [item_vector]
    
#     # Calculate cosine similarity
#     similarity = cosine_similarity(user_vector, item_vector)[0][0]
    
#     print(f"Final test tag score for {item.name}: {similarity}")
#     return similarity

# # Create dummy data for testing
# dummy_item = dt.Item("Test Laptop", 1000,description="",link="", tags=["premium", "portable", "white"],rate=4.3)
# dummy_machine_customer = dt.MachineCustomer(1, "laptop", 1, ["portable", "premium"])
# dummy_history = ["premium", "performance", "quality"]

# # Test the tag scoring
# test_tag_score(dummy_item, dummy_machine_customer, dummy_history)

