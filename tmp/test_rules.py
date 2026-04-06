import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghive_backend.settings')
django.setup()

from api.ai_grammar import grammar_ai

# Test sentences for Linguistic Rules
test_cases = [
    "i have a apple and a orange.",
    "please revert back as soon as possible .",
    "the   blog   has  double   spaces .",
    "an hour ago , i wrote a university blog ."
]

print("--- AI Grammar Linguistic Rules Test ---")
for text in test_cases:
    corrected = grammar_ai.suggest_correction(text)
    print(f"Original:  '{text}'")
    print(f"Corrected: '{corrected}'")
    print("-" * 30)
