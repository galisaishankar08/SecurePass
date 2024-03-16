import nltk
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.metrics import edit_distance
import re

# Download NLTK resources
nltk.download('punkt')
nltk.download('words')

class PasswordPolicy:
    def __init__(self):
        self.common_words = set(words.words())
        self.min_length = 8
        self.max_edit_distance = 2

    def is_password_secure(self, password, name, dob, email):
        # Check minimum length
        if len(password) < self.min_length:
            return False, "Password should be at least {} characters long.".format(self.min_length)

        # Check if the password is a common word
        if password.lower() in self.common_words:
            return False, "Avoid using common words as passwords."

        # Check for similarity to common words using edit distance
        for common_word in self.common_words:
            if edit_distance(password.lower(), common_word) <= self.max_edit_distance:
                return False, "Avoid passwords similar to common words."

        # Check for a mix of uppercase and lowercase letters
        if not (any(c.isupper() for c in password) and any(c.islower() for c in password)):
            return False, "Include both uppercase and lowercase letters in the password."

        # Check for the presence of numbers
        if not any(c.isdigit() for c in password):
            return False, "Include numbers in the password."

        # Check for the presence of special characters
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Include special characters in the password."

        # Tokenize name and email to get their components
        name_tokens = set(word_tokenize(name.lower()))
        email_local_part = email.split('@')[0]
        email_tokens = set(word_tokenize(email_local_part.lower()))
        
        # Prepare DOB variations
        dob_variations = set([
            dob.replace('-', ''),  # YYYYMMDD
            dob.replace('-', '')[2:],  # YYMMDD
            dob.replace('-', '/'),  # YYYY/MM/DD
            dob.replace('-', '/')[2:],  # YY/MM/DD
        ])
        
        # Combine all tokens and DOB variations to check against password
        all_checks = name_tokens.union(email_tokens).union(dob_variations)
        
        # Check if any part of the name, DOB, or email is in the password
        for check in all_checks:
            if check in password.lower():
                return False, "Password should not be a part of the personal info in password"  # Found a part of the personal info in password

        # If all checks pass, consider the password secure
        return True, "Password is secure."

# Example usage
if __name__ == "__main__":
    password_policy = PasswordPolicy()

    # Example
    password = "JohnDoe@1990"
    name = "John Doe"
    dob = "1990-01-01"  # Format: YYYY-MM-DD
    email = "john.doe@example.com"

    is_secure, message = password_policy.is_password_secure(password, name, dob, email)
    print(f"Password: {password}, Secure: {is_secure}, Message: {message}")