import os
import sys

# Ensure the root directory is in the path so grammar_engine can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from grammar_engine.engine import GrammarEngine

class CustomGrammarAI:
    def __init__(self):
        # 100% Simple Rule-Based Engine (NLP Assignment Version)
        print("Initialising Rule-Based Grammar Engine (Assignment Data)...")
        # Base Path to the grammar engine folder
        self.rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'grammar_engine', 'rules_model.json')
        self.engine = GrammarEngine(self.rules_path)

    def suggest_correction(self, text):
        if not text:
            return "", []
        
        # Simple rule-based correction logic using provided CSV data
        corrected_text, changes = self.engine.apply_corrections(text)
        return corrected_text, changes

# Global instance for easy import
grammar_ai = CustomGrammarAI()
