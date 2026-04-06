import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghive_backend.settings')
django.setup()

from api.ai_grammar import grammar_ai

# Test sentences for Capitalization
test_cases = [
    "i am writing a blog. it is very good.",
    "hello world! how are you? i am fine.",
    "  this starts with space. it should capitalize."
]

print("--- AI Grammar Capitalization Test ---")
for text in test_cases:
    corrected = grammar_ai.suggest_correction(text)
    print(f"Original:  '{text}'")
    print(f"Corrected: '{corrected}'")
    print("-" * 30)
