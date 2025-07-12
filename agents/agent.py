import os
import webbrowser
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Replace with 'GROQ_API_KEY' if using Groq
client = OpenAI(api_key=OPENAI_API_KEY)

if not OPENAI_API_KEY:
    print("❌ API key not found! Make sure it's in the .env file.")
class SmartAIAgent:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # Change model as needed
        self.intents = {
            "open website": self.open_website,
            "get weather": self.get_weather,
            "ask question": self.ask_gpt
        }

    def detect_intent(self, user_input):
        """Uses GPT to detect intent."""
        prompt = f"Classify the user's request into one of these categories: 'open website', 'get weather', 'ask question'. User's input: {user_input}"
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are an intent detection AI."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip().lower()

    def open_website(self, user_input):
        """Opens a website based on user request."""
        url = user_input.split("open ")[-1]
        print(f"Opening {url}...")
        webbrowser.open(f"https://{url}")
        return f"Opened {url} in your browser."

    def get_weather(self, user_input):
        """Fetches weather using an API (Replace API_KEY with a real one)."""
        city = user_input.split("weather in")[-1].strip()
        api_key = "your_weather_api_key"  # Replace with an actual key
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url).json()
        if "current" in response:
            temp = response["current"]["temp_c"]
            return f"The current temperature in {city} is {temp}°C."
        return "Sorry, couldn't fetch weather."

    def ask_gpt(self, user_input):
        """Handles general queries using GPT."""
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                      {"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content

    def chat(self):
        """Main interaction loop."""
        print("AI Agent: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "bye":
                print("AI Agent: Goodbye!")
                break
            
            intent = self.detect_intent(user_input)
            action = self.intents.get(intent, self.ask_gpt)
            response = action(user_input)
            print("AI Agent:", response)

# Run the AI Agent
agent = SmartAIAgent()
agent.chat()
