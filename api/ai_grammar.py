import re

class CorrectionRule:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def apply(self, text):
        raise NotImplementedError("Each rule must implement apply()")

class ArticleAgreementRule(CorrectionRule):
    def __init__(self):
        super().__init__("Article Agreement", "Fixes 'a' vs 'an' based on following word's sound (phonetic exceptions handled).")
        # List of words starting with vowels but sounding like consonants
        self.consonant_phonetic = ["university", "union", "unique", "unit", "user", "european", "one"]
        # List of words starting with consonants but sounding like vowels
        self.vowel_phonetic = ["hour", "honor", "honest", "herb"]

    def apply(self, text):
        new_text = text
        changes = []
        
        # Match 'a' followed by a vowel
        matches = re.finditer(r'\b(a)\s+([aeiouAEIOU][\w]+)', new_text)
        for m in reversed(list(matches)):
            original_a = m.group(1)
            word = m.group(2).lower()
            if word not in self.consonant_phonetic:
                replacement = "an" if original_a == "a" else "An"
                start, end = m.span(1)
                new_text = new_text[:start] + replacement + new_text[end:]
                changes.append({"original": original_a, "replacement": replacement, "rule": self.name})

        # Match 'an' followed by a consonant
        matches = re.finditer(r'\b(an)\s+([^aeiouAEIOU\s][\w]*)', new_text)
        for m in reversed(list(matches)):
            original_an = m.group(1)
            word = m.group(2).lower()
            if any(word.startswith(vp) for vp in self.vowel_phonetic):
                continue # Keep 'an' for 'hour', etc.
            
            replacement = "a" if original_an == "an" else "A"
            start, end = m.span(1)
            new_text = new_text[:start] + replacement + new_text[end:]
            changes.append({"original": original_an, "replacement": replacement, "rule": self.name})
            
        return new_text, changes

class CapitalizationRule(CorrectionRule):
    def __init__(self):
        super().__init__("Capitalization", "Ensures 'I' is capitalized and sentences start with an uppercase letter.")

    def apply(self, text):
        if not text: return text, []
        changes = []
        
        # Capitalize lone 'i'
        new_text = re.sub(r'\bi\b', 'I', text)
        if new_text != text:
             # Find how many were changed
             changes.append({"original": "i", "replacement": "I", "rule": self.name})

        # Capitalize first letter of string
        final_text = ""
        if len(new_text) > 0 and new_text[0].islower():
            final_text = new_text[0].upper() + new_text[1:]
            changes.append({"original": new_text[0], "replacement": new_text[0].upper(), "rule": self.name})
        else:
            final_text = new_text
            
        return final_text, changes

class SpellingRule(CorrectionRule):
    def __init__(self):
        super().__init__("Spelling", "Fixes common high-frequency typos.")
        self.dictionary = {
            "recieve": "receive",
            "definately": "definitely",
            "separate": "separate",
            "occurr": "occur",
            "begging": "beginning",
            "accommodate": "accommodate",
            "tomorrow": "tomorrow",
            "calender": "calendar",
            "suprise": "surprise",
            "relevent": "relevant",
            "revert back": "revert" # Double redundancy
        }

    def apply(self, text):
        new_text = text
        changes = []
        for typo, correction in self.dictionary.items():
            pattern = re.compile(rf'\b{typo}\b', re.IGNORECASE)
            if pattern.search(new_text):
                # Preserve case if it's start of sentence (simplified)
                new_text = pattern.sub(correction, new_text)
                changes.append({"original": typo, "replacement": correction, "rule": self.name})
        return new_text, changes

class SVARule(CorrectionRule):
    def __init__(self):
        super().__init__("SVA (Simple)", "Subject-Verb Agreement for singular subjects like he/she/it.")
        self.singular_pronouns = ["he", "she", "it", "this", "that"]
        self.verb_fixes = {
            "go": "goes",
            "have": "has",
            "do": "does",
            "want": "wants",
            "need": "needs"
        }

    def apply(self, text):
        new_text = text
        changes = []
        for pronoun in self.singular_pronouns:
            for verb, fixed in self.verb_fixes.items():
                pattern = re.compile(rf'\b({pronoun})\s+({verb})\b', re.IGNORECASE)
                if pattern.search(new_text):
                    new_text = pattern.sub(rf'\1 {fixed}', new_text)
                    changes.append({"original": f"{pronoun} {verb}", "replacement": f"{pronoun} {fixed}", "rule": self.name})
        return new_text, changes

class CustomGrammarAI:
    def __init__(self):
        self.rules = [
            ArticleAgreementRule(),
            CapitalizationRule(),
            SpellingRule(),
            SVARule()
        ]

    def suggest_correction(self, text):
        if not text:
            return ""
            
        current_text = text
        all_changes = []
        
        for rule in self.rules:
            current_text, changes = rule.apply(current_text)
            all_changes.extend(changes)
            
        # Also clean up double spaces as a final pass
        clean_text = re.sub(r' +', ' ', current_text)
        if clean_text != current_text:
            all_changes.append({"original": "double space", "replacement": "single space", "rule": "Formatting"})
            current_text = clean_text

        return current_text, all_changes

# Global instance for easy import
grammar_ai = CustomGrammarAI()
