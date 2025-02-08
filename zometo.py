class RateOrderObserver:
    def update(self, order):
        pass

class Solution:
 
    def __init__(self):
        # self.helper = helper
        self.ordersManager = OrdersManager()
        self.mostRatedRestaurants = MostRatedRestaurants()
        self.mostRatedRestaurantsByFood = MostRatedRestaurantsByFood()
        self.ordersManager.addObserver(self.mostRatedRestaurants)
        self.ordersManager.addObserver(self.mostRatedRestaurantsByFood)
        # self.helper.println("restaurant rating module initialized")

    def order_food(self, orderId, restaurantId, foodItemId):
        self.ordersManager.orderFood(orderId, restaurantId, foodItemId)

    def rate_order(self, orderId, rating):
        self.ordersManager.rateOrder(orderId, rating)

    def get_top_restaurants_by_food(self, foodItemId) -> list[str]:
        return self.mostRatedRestaurantsByFood.getRestaurants(foodItemId, 20)

    def get_top_rated_restaurants(self) -> list[str]:
        return self.mostRatedRestaurants.getRestaurants(20)

class OrdersManager:
    def __init__(self):
        self.map = {}
        self.observers = []

    def orderFood(self, orderId, restaurantId, foodItemId):
        order = Order(orderId, restaurantId, foodItemId, 0)
        self.map[orderId] = order

    def rateOrder(self, orderId, rating):
        order = self.map[orderId]
        order.setRating(rating)
        self.notifyAll(order)

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyAll(self, order):
        for observer in self.observers:
            observer.update(order)

class MostRatedRestaurants(RateOrderObserver):
    def __init__(self):
        self.ratings = {}

    def update(self, order):
        restaurantId = order.getRestaurantId()
        if restaurantId not in self.ratings:
            self.ratings[restaurantId] = Rating(0, 0)
        self.ratings[restaurantId].add(order.getRating())

    def getRestaurants(self, n) -> list[str]:
        sorted_restaurants = sorted(self.ratings.keys(),
                                    key=lambda x: (-self.ratings[x].getAverageRating(), x))
        return sorted_restaurants[:n]


class MostRatedRestaurantsByFood(RateOrderObserver):
    def __init__(self):
        self.ratings = {}

    def update(self, order):
        foodItemId = order.getFoodItemId()
        restaurantId = order.getRestaurantId()
        
        if foodItemId not in self.ratings:
            self.ratings[foodItemId] = {}  # Create an empty dictionary for that food item
        
        if restaurantId not in self.ratings[foodItemId]:
            self.ratings[foodItemId][restaurantId] = Rating(0, 0)
        
        self.ratings[foodItemId][restaurantId].add(order.getRating())

    def getRestaurants(self, foodItemId, n) -> list[str]:
        if foodItemId not in self.ratings:
            return []
        
        restaurants_map = self.ratings[foodItemId]
        sorted_restaurants = sorted(restaurants_map.keys(),
                                    key=lambda x: (-restaurants_map[x].getAverageRating(), x))
        return sorted_restaurants[:n]


class Rating:
    def __init__(self, sum, count):
        self.sum = sum
        self.count = count

    def __str__(self):
        return f"sum {self.sum}, count {self.count}, avg {self.getAverageRating()}"

    def getAverageRating(self):
        if self.count <= 0:
            return 0
        rating = self.sum / self.count
        rating = round(rating, 1)#int((rating + 0.05) * 10) / 10.0
        return rating

    def add(self, num):
        self.sum += num
        self.count += 1

class Order:
    def __init__(self, orderId, restaurantId, foodItemId, rating):
        self.orderId = orderId
        self.restaurantId = restaurantId
        self.foodItemId = foodItemId
        self.rating = rating

    def setRating(self, rating):
        self.rating = rating

    def getRestaurantId(self):
        return self.restaurantId

    def getFoodItemId(self):
        return self.foodItemId

    def getRating(self):
        return self.rating
        
if __name__ == "__main__":
    solution = Solution()
    # solution.init()  # Initialize with None as the helper (not used)
    
    # Create orders and rate them
    solution.order_food(orderId=1, restaurantId=101, foodItemId=501)
    solution.order_food(orderId=2, restaurantId=102, foodItemId=501)
    solution.order_food(orderId=3, restaurantId=103, foodItemId=502)
    solution.order_food(orderId=4, restaurantId=104, foodItemId=502)
    
    solution.rate_order(orderId=1, rating=4)
    solution.rate_order(orderId=2, rating=5)
    solution.rate_order(orderId=3, rating=3)
    solution.rate_order(orderId=4, rating=5)
    
    # Get top-rated restaurants
    top_restaurants = solution.get_top_rated_restaurants()
    print("Top-rated restaurants:", top_restaurants)
    
    # Get top restaurants by food item
    top_restaurants_by_food_501 = solution.get_top_restaurants_by_food(foodItemId=501)
    top_restaurants_by_food_502 = solution.get_top_restaurants_by_food(foodItemId=502)
    print("Top restaurants for food item 501:", top_restaurants_by_food_501)
    print("Top restaurants for food item 502:", top_restaurants_by_food_502)
        
        









