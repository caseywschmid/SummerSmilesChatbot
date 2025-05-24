#!/usr/bin/env python3
"""
Test client for the FastAPI chatbot
Step-by-step:
1. Establish initial connection via /chat endpoint with no user_input
2. Send chat messages with context preservation
3. Demonstrate API usage patterns
"""

import requests


class ChatbotClient:
    """
    Client for interacting with the Summer Smiles FastAPI chatbot
    Used for testing and demonstrating API usage patterns
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """Initialize client with API base URL"""
        self.base_url = base_url
        self.language = None
        self.previous_response_id = None

    def establish_connection(self, language: str) -> dict:
        """
        Establish initial connection by sending chat request with no user_input
        This will return the welcome message for the selected language
        """
        payload = {
            "language": language
        }

        response = requests.post(f"{self.base_url}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            self.language = language
            print(f"Bot: {data['response_text']}")
            return data
        else:
            print(f"Error establishing connection: {response.text}")
            return None

    def send_message(self, message: str) -> dict:
        """
        Send a chat message to the bot
        Maintains conversation context using previous_response_id
        """
        if not self.language:
            print("Please establish connection first")
            return None

        payload = {
            "user_input": message,
            "language": self.language,
            "previous_response_id": self.previous_response_id,
        }

        response = requests.post(f"{self.base_url}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            self.previous_response_id = data["response_id"]  # Maintain context
            print(f"Bot: {data['response_text']}")
            return data
        else:
            print(f"Error sending message: {response.text}")
            return None


def main():
    """
    Main test function demonstrating the chatbot client usage
    """
    client = ChatbotClient()

    print("Welcome to the Summer Smiles FastAPI Chatbot Test Client!")

    language = input("Select language (en/fr): ").strip().lower()
    if language not in ("en", "fr"):
        print("Invalid language. Defaulting to English.")
        language = "en"

    # Establish initial connection
    print("\nEstablishing connection...")
    client.establish_connection(language)

    # Chat loop
    print("\nType 'exit' to quit the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        client.send_message(user_input)


if __name__ == "__main__":
    main()
