"""
Runs in the terminal and calls the OpenAIService directly for chat interactions.
"""

from services.ai.openai_service import OpenAIService


def main():
    print("Welcome to the Summer Smiles chatbot! Type 'exit' to quit.")
    language = input("Select language (en/fr): ").strip().lower()
    if language not in ("en", "fr"):
        print("Invalid language. Defaulting to English.")
        language = "en"
    if language == "en":
        name = "SummerSmiles_English"
        print("Bot: Hello! How can I help you today?")
    else:
        name = "SummerSmiles_French"
        print("Bot: Bonjour! Comment puis-je vous aider aujourd'hui?")
    previous_response_id = None
    openai_service = OpenAIService()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        try:
            response_text, response_id = openai_service.chat(
                user_input, previous_response_id=previous_response_id, name=name
            )
            print("Bot:", response_text)
            previous_response_id = response_id  # Maintain context for threading
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
