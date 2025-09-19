import datetime
import random
import re

# Facts and data
facts = [
    "The tallest building in the world is the Burj Khalifa.",
    "Octopuses have three hearts.",
    "The Indian national bird is the peacock."
]
jokes = [
    "Why do programmers hate nature? It has too many bugs.",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why was the math book sad? Because it had too many problems."
]

# User data for context
user_profile = {
    "name": None,
    "favorite_city": None,
    "favorite_food": None,
    "favorite_color": None,
    "last_mood": None
}

def detect_intent(user_input):
    greetings = {"hello", "hi", "hey", "namaste"}
    farewells = {"bye", "goodbye", "see you", "farewell"}
    thanks = {"thanks", "thank you"}
    jokes_kw = {"joke", "funny"}
    facts_kw = {"fact", "tell me something"}
    time_kw = {"time", "clock"}
    date_kw = {"date", "day", "month", "year"}
    weather_kw = {"weather", "temperature"}
    mood_kw = {"sad", "happy", "great", "down", "good", "bad"}
    
    words = set(re.findall(r'\w+', user_input.lower()))
    
    # Map intent to set intersection
    if greetings & words:
        return "greeting"
    if farewells & words:
        return "farewell"
    if thanks & words:
        return "thanks"
    if jokes_kw & words:
        return "joke"
    if facts_kw & words:
        return "fact"
    if time_kw & words:
        return "time"
    if date_kw & words:
        return "date"
    if weather_kw & words or "ghaziabad" in user_input.lower():
        return "weather"
    if mood_kw & words:
        return "mood"
    if "favorite" in user_input.lower():
        return "favorite"
    if "menu" in user_input.lower() or "options" in user_input.lower():
        return "show_menu"
    return "default"

def advanced_chatbot_response(user_input):
    intent = detect_intent(user_input)
    
    if user_profile["name"] is None:
        user_profile["name"] = input("Bot: May I know your name? ")
        return f"Nice to meet you, {user_profile['name']}! How can I assist you today?"
    
    if intent == "greeting":
        return random.choice([
            f"Hello {user_profile['name']}! What can I do for you?",
            f"Hi {user_profile['name']}! Need help?",
        ])
    if intent == "farewell":
        return f"Take care, {user_profile['name']}! See you again soon."
    if intent == "thanks":
        return random.choice([
            "You're most welcome!",
            "Anytime!",
            f"Glad to help, {user_profile['name']}!"
        ])
    if intent == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    if intent == "date":
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {today}."
    if intent == "weather":
        # Example: Static weather for Ghaziabad
        return "Right now in Ghaziabad, it's 34°C and partly cloudy."
    if intent == "joke":
        return random.choice(jokes)
    if intent == "fact":
        return random.choice(facts)
    if intent == "mood":
        if "sad" in user_input:
            user_profile["last_mood"] = "sad"
            return "I'm sorry to hear that. Want to hear a joke to cheer you up?"
        if "happy" in user_input or "great" in user_input:
            user_profile["last_mood"] = "happy"
            return "That's wonderful! Let me know if you need anything."
        return "Thanks for sharing how you feel!"
    if intent == "favorite":
        if "city" in user_input:
            if user_profile["favorite_city"] is None:
                city = input("Bot: What's your favorite city? ")
                user_profile["favorite_city"] = city
                return f"{city} is a great city! I'll remember that."
            return f"You mentioned your favorite city is {user_profile['favorite_city']}."
        if "food" in user_input:
            if user_profile["favorite_food"] is None:
                food = input("Bot: What's your favorite food? ")
                user_profile["favorite_food"] = food
                return f"Yum! {food} sounds tasty."
            return f"You told me your favorite food is {user_profile['favorite_food']}."
        if "color" in user_input:
            if user_profile["favorite_color"] is None:
                color = input("Bot: What's your favorite color? ")
                user_profile["favorite_color"] = color
                return f"Nice! {color} is a lovely color."
            return f"You said your favorite color is {user_profile['favorite_color']}."
    if intent == "show_menu":
        return (
            "Menu:\n"
            "1. Ask for a joke (type: joke)\n"
            "2. Ask for a fact (type: fact)\n"
            "3. Ask the weather in Ghaziabad\n"
            "4. Ask for today's time or date\n"
        )
    return "I'm still learning. Try asking for a joke, a fact, or about the weather!"

# --- MAIN CHAT LOOP ---
print("Bot: Hello! (Type 'bye' to exit, or type 'menu' to see options.)")
while True:
    user_input = input(f"{user_profile['name'] or 'You'}: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        print(f"Bot: Goodbye, {user_profile['name'] or ''}!")
        break
    print("Bot:", advanced_chatbot_response(user_input))
# --- END OF CHAT LOOP ---
