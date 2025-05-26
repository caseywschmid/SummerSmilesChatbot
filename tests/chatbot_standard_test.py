from services.ai.openai_service import OpenAIService
import json
import os
from datetime import datetime
from services.logger import configure_logging

log = configure_logging(__name__, log_level="DEBUG")

# Step-by-step instructions:
# 1. This test sends 10 questions (5 English, 5 French) to the chatbot via OpenAIService.chat.
# 2. It collects the chatbot's responses along with the questions and language.
# 3. It saves the results to a JSON file named chatbot_test_<timestamp>.json in /tests/results.
# 4. The file contains a list of objects with 'question', 'response', and 'language' fields.
# 5. The /tests/results directory is created if it does not exist.
# 6. You can update the questions as needed to evaluate chatbot quality after code changes.
# 7. To run: pytest tests/chatbot_standard_test.py


def test_chatbot_responses():
    """
    Sends 10 questions (5 English, 5 French) to the chatbot, saves the Q&A to a timestamped JSON file for manual review.
    """
    service = OpenAIService()
    english_questions = [
        "I need to drain my spa. Is there anything special I need to do?",  # content/english/pages/spa-closing-draining.json
        "Do you offer in store water analysis?",  # content/english/pages/in-store-water-analysis.json
        "It rained yesterday and now my pool chemistry is off. Is it the rain?",  # content/english/posts/how-does-rain-affect-my-pool-water.json
        "A friend said I should be using Calcium +. Can you tell me about it?", # content/english/products/calcium-plus-pool-care.json
        "How do I know if I have phosphates my pool?", # content/english/posts/phosphates-in-pool-water.json
    ]
    french_questions = [
        "Je dois vider mon spa. Y a-t-il quelque chose de spécial à faire?", # content/french/pages/fermeture-et-drainage-spa.json
        "Offrez-vous une analyse de l'eau en magasin?", # content/french/pages/analyse-deau-en-magasin.json
        "Il a plu hier et maintenant la chimie de ma piscine est déréglée. Est-ce à cause de la pluie?", # content/french/posts/quels-effets-la-pluie-peut-elle-avoir-sur-leau-de-ma-piscine.json
        "Un ami m'a dit que je devrais utiliser Calcium +. Pouvez-vous m'en parler?", # content/french/products/calcium-plus-entretien-de-la-piscine.json
        "Comment savoir si j'ai des phosphates dans ma piscine?", # content/french/posts/les-phosphates-dans-leau-de-piscine.json
    ]
    all_questions = [
        (q, "English", "SummerSmiles_English") for q in english_questions
    ] + [(q, "French", "SummerSmiles_French") for q in french_questions]
    # Each question is sent as a standalone (not a conversation)
    results = []
    for idx, (question, language, name) in enumerate(all_questions, 1):
        try:
            response_text, _ = service.chat(
                question, previous_response_id=None, name=name
            )
            results.append(
                {"question": question, "response": response_text, "language": language}
            )
        except Exception as e:
            log.error(f"Error for question {idx}: {e}")
            results.append(
                {"question": question, "response": f"Error: {e}", "language": language}
            )
    # Ensure the results directory exists
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chatbot_test_{timestamp}.json"
    filepath = os.path.join(results_dir, filename)
    # Save results to JSON file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log.success(f"\nResults saved to {filepath}")
