import socket
import re
from difflib import get_close_matches

# Initialize socket
s = socket.socket()
host = socket.gethostname()
print("Server will start on host: ", host)

port = 8080
s.bind((host, port))

print("\nServer done binding to host and port successfully!\n")
print("\nServer is waiting for queries...\n")

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

def textPreprocessing(question):
    # Convert to lowercase and remove punctuation
    cleaned_text = re.sub(r'[^\w\s]', '', question.lower())
    words = cleaned_text.split()

    # Handle greeting phrases
<<<<<<< HEAD
    greetings = ["hi", "hello", "gm", "good morning", "gn", "good night", "good afternoon", "ga"]
=======
    greetings = ["hi", "hello", "gm", "good morning", "gn", "good night","good afternoon","ga","good evening","gd eve"]
>>>>>>> 0e01e175922790c45286f69f53662cf3e83f94e9
    if any(word in words for word in greetings):
        return "Hello! How can I assist you today?"

    # Handle identity-related questions
    if any(phrase in question.lower() for phrase in ["who are you", "what is your name", "who is this"]):
        return "I'm JSM, your friendly server assistant. How can I help you today?"

    # Check for delivery inquiries
    if any(phrase in question.lower() for phrase in ["online delivery", "door delivery", "home delivery"]):
        return (
            "We do not offer door delivery directly. "
            "You can pick up your order at our location. "
            "Alternatively, you may use services like XEAT or Uber Eats for door delivery."
        )

    # Check for specific quantities and calculate total price
    quantity_match = re.search(r"(\d+)\s+(\w+)", question)
    if quantity_match:
        quantity = int(quantity_match.group(1))
        item = quantity_match.group(2)
        if item in food_data and food_data[item]["availability"]:
            total_price = quantity * food_data[item]["price"]
            return f"The total amount for {quantity} {item}(s) is ${total_price:.2f}. You can pick it up at our store."
        return f"Sorry, {item} is not available or not recognized."

    # Check for general inquiries about the menu or available foods
<<<<<<< HEAD
    if any(word in words for word in ["menu", "items", "available", "food"]):
=======
    if any(word in words for word in ["food", "foods", "menu", "items", "have","meals"]):
>>>>>>> 0e01e175922790c45286f69f53662cf3e83f94e9
        available_foods = [item for item, details in food_data.items() if details["availability"]]
        return f"We have the following available: {', '.join(available_foods)}."

    # Check for food item details
    for word in words:
        if word in food_data:
            food_item = food_data[word]
            if "price" in words:
                return f"The price of {word} is ${food_item['price']:.2f}."
            elif any(phrase in question for phrase in ["can i", "is it available", "buy now"]):
                if food_item["availability"]:
                    return f"Yes, {word} is available now! You can enjoy it."
                else:
                    return f"Sorry, {word} is currently not available. Would you like to try something else?"

            return f"{word.capitalize()} - Price: ${food_item['price']:.2f}. Description: {food_item['description']}"

    # Suggest close matches for unrecognized items
    unrecognized_foods = [word for word in words if word not in food_data]
    if unrecognized_foods:
        suggestions = []
        for word in unrecognized_foods:
            close_matches = get_close_matches(word, food_data.keys(), n=3, cutoff=0.5)
            if close_matches:
                suggestions.append(f"Did you mean {', '.join(close_matches)}?")
        if suggestions:
            return "I couldn't find the item in our menu. " + " ".join(suggestions)
        else:
            available_foods = [item for item, details in food_data.items() if details["availability"]]
            return f"I couldn't find the item in our menu. Here's what we have available: {', '.join(available_foods)}."

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
