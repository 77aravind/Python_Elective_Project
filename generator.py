import secrets
import string
import random

class PasswordGenerator:
    """
    Handles secure password generation based on platform-specific policies.
    """
    PLATFORM_POLICIES = {
        "WiFi": {
            "min_length": 8,
            "max_length": 13,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": False,
            "min_strength": 1
        },
        "Banking": {
            "min_length": 16,
            "max_length": 20,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": True,
            "min_strength": 4
        },
        "Social Media": {
            "min_length": 10,
            "max_length": 12,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": True,
            "min_strength": 0
        },
        "Gaming": {
            "min_length": 8,
            "max_length": 10,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": False,
            "min_strength": 0
        },
        "Corporate": {
            "min_length": 12,
            "max_length": 15,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": True,
            "min_strength": 3
        }
    }

    def __init__(self, analyzer=None):
        self.analyzer = analyzer

    def generate(self, platform):
        """
        Generates a password for the given platform policy.
        """
        policy = self.PLATFORM_POLICIES.get(platform)
        if not policy:
            raise ValueError(f"Unknown platform: {platform}")

        while True:
            password = self._create_random_string(policy)
            
            # If we have an analyzer, check if it meets the minimum strength requirement
            if self.analyzer:
                result = self.analyzer.analyze(password)
                if result['score'] >= policy['min_strength']:
                    return password
            else:
                return password

    def _create_random_string(self, policy):
        chars = ""
        if policy['use_lower']:
            chars += string.ascii_lowercase
        if policy['use_upper']:
            chars += string.ascii_uppercase
        if policy['use_digits']:
            chars += string.digits
        if policy['use_special']:
            chars += string.punctuation

        length = random.randint(policy['min_length'], policy['max_length'])
        return "".join(secrets.choice(chars) for _ in range(length))

    @classmethod
    def get_platforms(cls):
        return list(cls.PLATFORM_POLICIES.keys())
