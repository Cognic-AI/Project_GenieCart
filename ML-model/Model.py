import consts
import UserFixedDataConvertor as uc

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
            price_score = self.addPriceScore(i.price)
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
        

    def addTagScore(self,item):
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
