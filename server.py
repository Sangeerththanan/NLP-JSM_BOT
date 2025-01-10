import socket
import re

# Initialize socket
s = socket.socket()
host = socket.gethostname()
print("Server will start on host: ", host)

port = 8080
s.bind((host, port))

print("\nServer done binding to host and port successfully!\n")
print("\nServer is waiting for numbers\n")

s.listen(1)

conn, addr = s.accept()
print(addr, " has connected to the server and is now online...\n")

# Food Data
food_data = {
    "pizza": {
        "price": 10.99,
        "description": "Delicious cheesy pizza with your choice of toppings.",
        "availability": True
    },
    "burger": {
        "price": 8.99,
        "description": "Juicy burger with lettuce, tomato, and onion.",
        "availability": True
    },
    "pasta": {
        "price": 12.99,
        "description": "Creamy pasta with your choice of sauce.",
        "availability": True
    },
    "salad": {
        "price": 7.99,
        "description": "Fresh and healthy salad with a variety of vegetables.",
        "availability": True
    },
    "soup": {
        "price": 5.99,
        "description": "Warm and comforting soup to start your meal.",
        "availability": True
    },
    "bread": {
        "price": 3.50,
        "description": "Soft and fresh bread, perfect as a side or snack.",
        "availability": True
    },
    "cake": {
        "price": 15.99,
        "description": "Delicious chocolate or vanilla cake for any occasion.",
        "availability": False
    }
}

# Initialize a variable to store the last queried specific food
last_queried_food = None

def textPreprocessing(question):
    global last_queried_food  # Use the global context variable

    # Convert to lowercase and remove punctuation
    cleaned_text = re.sub(r'[^\w\s]', '', question.lower())
    words = cleaned_text.split()

    # Handle greeting phrases
    greetings = ["hi", "hello", "gm", "good morning", "gn", "good night","good afternoon","ga","good evening","gd eve"]
    if any(word in words for word in greetings):
        return "Hello! How can I assist you today?"

    # Check for general inquiries about the menu or available foods
    if any(word in words for word in ["food", "foods", "menu", "items", "have","meals"]):
        available_foods = [item for item, details in food_data.items() if details["availability"]]
        last_queried_food = None  # Reset context
        return f"We have the following available: {', '.join(available_foods)}."

    # Check for general price inquiry
    if "price" in words or "prices" in words:
        if last_queried_food:  # If a specific food was queried earlier
            food_item = food_data.get(last_queried_food)
            if food_item:
                return f"The price of {last_queried_food} is ${food_item['price']:.2f}."
        else:  # General price inquiry
            prices = [f"{item.capitalize()}: ${details['price']:.2f}" 
                      for item, details in food_data.items()]
            return "Here are the prices of all items:\n" + "\n".join(prices)

    # Check for specific food items
    for word in words:
        if word in food_data:
            last_queried_food = word  # Update context to the specific food
            food_item = food_data[word]
            if "price" in words:
                return f"The price of {word} is ${food_item['price']:.2f}."
            elif any(phrase in question for phrase in ["can i", "is it possible", "can we", "take now", "buy now", "eat now", "cn i", "i can take"]):
                if food_item["availability"]:
                    return f"Yes, {word} is available now! You can enjoy it."
                else:
                    return f"Sorry, {word} is currently not available."
            else:
                return f"{word.capitalize()} - Price: ${food_item['price']:.2f}. Description: {food_item['description']}"

    # Check for generic availability queries
    if any(phrase in question for phrase in ["can i", "is it available", "can we", "take now", "buy now", "eat now", "cn i", "i can take"]):
        if last_queried_food:
            food_item = food_data.get(last_queried_food)
            if food_item:
                if food_item["availability"]:
                    return f"Yes, {last_queried_food} is available now! You can enjoy it."
                else:
                    return f"Sorry, {last_queried_food} is currently not available."
        else:
            return "Please specify the food item you'd like to check availability for."

    # Default response
    return "I'm sorry, I couldn't understand your question. Please ask about the menu, specific food items, or their prices and availability."


# Chat Loop
while True:
    try:
        question = conn.recv(1024).decode()
        if not question:
            break
        print("Client:", question)
        print("")

        answer = textPreprocessing(question)
        conn.send(answer.encode())
        print("Server:", answer)
        print("")
    except Exception as e:
        print("Error:", e)
        break

conn.close()
