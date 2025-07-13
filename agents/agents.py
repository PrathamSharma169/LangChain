import os
import webbrowser
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

if not GROQ_API_KEY:
    print("API key not found! Make sure it's in the .env file.")

class SmartAIAgent:
    def __init__(self):
        self.model = "llama3-8b-8192"  
        self.intents = {
            "open website": self.open_website,
            "get weather": self.get_weather,
            "ask question": self.ask_groq
        }

    def call_groq_api(self, messages):
        """Uses the Groq client to generate responses."""
        chat_completion = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return chat_completion.choices[0].message.content.strip()

    def detect_intent(self, user_input):
        """Uses Groq API to classify intent."""
        prompt = f"Classify the user's request into one of these categories: 'open website', 'get weather', 'ask question'. User's input: {user_input}"
        messages = [
            {"role": "system", "content": "You are an intent detection AI."},
            {"role": "user", "content": prompt}
        ]
        return self.call_groq_api(messages).lower()

    def open_website(self, user_input):
        """Opens a website based on user request."""
        words = user_input.lower().split()
    
        # Extract the URL from the user input
        if "open" in words:
            index = words.index("open") + 1
            if index < len(words):
                url = words[index]
                if not url.startswith("http"):
                    url = f"https://{url}"
                print(f"Opening {url}...")
                webbrowser.open(url)
                return f"Opened {url} in your browser."
    
        return "I couldn't find a website to open."

    def get_weather(self, user_input):
        """Fetches weather using an API (Replace API_KEY with a real one)."""
        city = user_input.split("weather in")[-1].strip()
        api_key = "your_weather_api_key"  # Need to Replace with an actual key
        url = f"https://api.weatherstack.com/current? access_key = {api_key}& query = {city}"
        response = requests.get(url).json()
        if "current" in response:
            temp = response["current"]["temp_c"]
            return f"The current temperature in {city} is {temp}°C."
        return "Sorry, couldn't fetch weather."

    def ask_groq(self, user_input):
        """Handles general queries using Groq API."""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
        return self.call_groq_api(messages)

    def chat(self):
        """Main interaction loop."""
        print("AI Agent: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "bye":
                print("AI Agent: Goodbye!")
                break
            
            intent = self.detect_intent(user_input)
            action = self.intents.get(intent, self.ask_groq)
            response = action(user_input)
            print("AI Agent:", response)

agent = SmartAIAgent()
agent.chat()
