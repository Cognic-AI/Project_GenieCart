# Import required libraries
import ML_model.consts as consts
import math
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import ML_model.DataTypes as dt

# Print initialization header
print("<====================>")
print("MODEL INITIALIZATION")
print("<====================>")

class Model:
    def __init__(self, item_array, machine_customer_query):
        """Initialize the model with item array and machine customer query"""
        print("Initializing Model...")
        # Store input parameters
        self.item_array = item_array
        self.machine_customer_query = machine_customer_query
        # Initialize counters for price level tracking
        self.no_of_high = 0
        self.no_of_low = 0
        self.no_of_middle = 0
        # Initialize price ranges and tag vectors
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
        # Calculate scores for all items
        self.assigningScores()
        print("Getting final results...")
        # Sort and return results
        result = self.getFinalResult()
        print("Model execution complete")
        return result

    def assigningScores(self):
        """Assign scores to items based on price, rating and tags"""
        print("\n<====================>")
        print("SCORE ASSIGNMENT")
        print("<====================>")
        print("Starting score assignment for all items...")
        # Process each item in array
        for i in self.item_array:
            print(f"\nProcessing item: {i.name}")
            # Calculate price score using improved algorithm
            price_score = self.addPriceScoreImproved(i.price)
            print(f"Price score: {price_score}")
            print(f"Item score before: {i.score}")
            i.score += price_score
            
            # Calculate rating score
            rate_score = i.rate*consts.RATE_SCORE_FACTOR
            print(f"Rate score: {rate_score}")
            i.score += rate_score
            
            # Calculate tag matching score
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
        # Find minimum and maximum prices in item array
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
        
        # Store price range values
        self.min_p = min_p
        self.max_p = max_p
        self.middle_p = (min_p + max_p)/2
        print(f"Price ranges initialized - Min: {min_p}, Max: {max_p}, Middle: {self.middle_p}")

    def addPriceScore(self,price):
        """Calculate price score based on price level and availability"""
        print(f"\nCalculating price score for price: {price}")
        # Calculate gaps between price points
        upper_gap = self.max_p-price
        middle_gap = abs(self.middle_p-price)
        below_gap = price-self.min_p

        # Find smallest gap to determine price category
        min_gap = min([upper_gap,middle_gap,below_gap])
        print(f"Gaps - Upper: {upper_gap}, Middle: {middle_gap}, Below: {below_gap}")

        # Categorize price level based on smallest gap
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

        # Calculate normalized gap score
        if len(self.item_array)==1:
            mapped_gap = 1
        else:
            mapped_gap = (self.max_p -self.min_p - min_gap)/(self.max_p -self.min_p)

        print(mapped_gap)
        
        # Return final score based on price level match and availability thresholds
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
        
        # Normalize price to 0-1 range
        price_range = self.max_p - self.min_p
        normalized_price = (price - self.min_p) / price_range

        # Define middle price range buffer
        price_range_buffer = price_range * 0.2
        
        # Calculate base score using different functions based on user preference
        if self.machine_customer_query.price_level == consts.HIGH_END_USER:
            # Use sigmoid function for high-end scoring
            base_score = 5 / (1 + math.exp(-10 * (normalized_price - 0.8)))
        elif self.machine_customer_query.price_level == consts.LOW_END_USER:
            # Use sigmoid function for low-end scoring
            base_score = 5 / (1 + math.exp(-10 * (0.2 - normalized_price)))
        else:  # MIDDLE_USER
            # Use Gaussian function for middle range scoring
            sigma = price_range_buffer / 2
            base_score = 5 * math.exp(-((price - self.middle_p) ** 2) / (2 * sigma ** 2))
        
        # Add availability bonus if threshold met
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
        # Return empty dict if no history
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
        
        # Normalize tag weights
        print("Normalizing tag weights...")
        for k in list(tags_vector.keys()):
            tags_vector[k] = tags_vector[k]/total_tags
            print(f"Tag {k}: weight = {tags_vector[k]}")
        
        return tags_vector

    def addTagScore(self, item):
        """Calculate tag matching score for an item"""
        print(f"Calculating tag score for {item.name}")
        sum = 0
        # Process each tag in item
        for t in item.tags:
            print(f"Checking tag: {t}")
            # Add weighted score for history matches
            if t in self.tags.keys():
                history_score = self.tags[t] * consts.TAG_HIT
                sum += history_score
                print(f"Tag {t} matched in history, adding score: {history_score}")
            # Add fixed score for query matches
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
        
        # Initialize user tags with weights
        user_tags = Counter()
        user_tags.update(self.history)
        for tag in self.machine_customer_query.tags:
            user_tags[tag] += 1.5  # Higher weight for explicit query tags
            
        # Define importance weights for retail categories
        tag_importance = {
            
        }
        
        # Convert tags to vectors for similarity calculation
        all_tags = list(set(list(user_tags.keys()) + item.tags))
        user_vector = [user_tags.get(tag, 0) * tag_importance.get(tag, 1.0) for tag in all_tags]
        item_vector = [1.0 * tag_importance.get(tag, 1.0) if tag in item.tags else 0 for tag in all_tags]
        
        # Reshape vectors for sklearn
        user_vector = [user_vector]
        item_vector = [item_vector]
        
        # Calculate similarity score
        similarity = cosine_similarity(user_vector, item_vector)[0][0]
        
        print(f"Final improved tag score for {item.name}: {similarity}")
        return similarity

    def getFinalResult(self):
        """Sort items by score and return sorted array"""
        print("\n<====================>")
        print("FINAL RESULTS")
        print("<====================>")
        print("Sorting items by score...")
        # Sort items by score in descending order
        self.item_array.sort(key=lambda x: x.score, reverse=True)
        print("Top item:")
        print(f"1. {self.item_array[0].name} - Score: {self.item_array[0].score} - Price: {self.item_array[0].price}")
        return self.item_array
