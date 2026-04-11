import os
import json
import re
from difflib import get_close_matches

class GrammarEngine:
    def __init__(self, rules_path='grammar_engine/rules_model.json'):
        # 100% Unified Rule-Based Engine (NLP Assignment Version)
        self.rules = {}
        self.vocabulary = set()
        
        if os.path.exists(rules_path):
            print(f"Loading {rules_path}...")
            with open(rules_path, 'r') as f:
                data = json.load(f)
                self.rules = data.get("rules", {})
                self.vocabulary = set(data.get("vocabulary", []))
            print(f"Loaded {len(self.rules)} Grammar Rules and {len(self.vocabulary)} Vocabulary words.")
        else:
            print("Warning: rules_model.json not found. Run trainer.py first.")

    def apply_corrections(self, text):
        if not text:
            return "", []

        original_text = text
        corrected_text = text
        all_changes = []

        # 1. GRAMMAR RULE MATCHING (Phrase based)
        sorted_symbols = sorted(self.rules.items(), key=lambda x: len(x[0]), reverse=True)
        for ungrammatical, standard in sorted_symbols:
            # Word boundary matching
            pattern = re.compile(r'\b' + re.escape(ungrammatical) + r'\b', re.IGNORECASE)
            if pattern.search(corrected_text):
                all_changes.append({
                    "original": ungrammatical,
                    "replacement": standard,
                    "type": "Grammar Rule"
                })
                corrected_text = pattern.sub(standard, corrected_text)

        # 2. SPELLING CORRECTION (Word based using Assignment Vocabulary)
        words = re.findall(r"[\w']+|[.,!?;]", corrected_text)
        new_words = []
        
        for word in words:
            # Clean word for lookup
            clean_word = word.lower()
            
            # If it's a word and not in vocabulary
            if clean_word.isalpha() and len(clean_word) > 2 and clean_word not in self.vocabulary:
                # Find closest match from assignment data
                matches = get_close_matches(clean_word, self.vocabulary, n=1, cutoff=0.7)
                if matches:
                    replacement = matches[0]
                    # Preserve original casing
                    if word[0].isupper():
                        replacement = replacement.capitalize()
                    
                    all_changes.append({
                        "original": word,
                        "replacement": replacement,
                        "type": "Spelling Correction"
                    })
                    new_words.append(replacement)
                    continue
            
            new_words.append(word)

        # Reconstruct text
        final_text = ""
        for i, w in enumerate(new_words):
            if w in ".,!?;":
                final_text = final_text.rstrip() + w + " "
            else:
                final_text += w + " "
        
        final_text = final_text.strip()
        
        # Sentence Capitalization
        if final_text:
            final_text = final_text[0].upper() + final_text[1:]

        # Clean up double changes (if same word corrected twice)
        unique_changes = []
        seen = set()
        for c in all_changes:
            key = (c['original'].lower(), c['replacement'].lower())
            if key not in seen:
                unique_changes.append(c)
                seen.add(key)

        return final_text, unique_changes

if __name__ == "__main__":
    # Final Test for NLP Assignment Proof
    engine = GrammarEngine()
    test_cases = [
        "Frinday week beofore saturday",
        "i goes to the store",
        "they was playing soccer"
    ]
    
    print("\n--- UNIFIED RULE-BASED TEST (ALL CSV DATA) ---")
    for test in test_cases:
        corrected, changes = engine.apply_corrections(test)
        print(f"Original:  {test}")
        print(f"Corrected: {corrected}")
        for c in changes:
             print(f"  [{c['type']}] {c['original']} -> {c['replacement']}")
        print("-" * 20)
