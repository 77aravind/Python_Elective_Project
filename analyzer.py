import zxcvbn
import math

class PasswordAnalyzer:
    """
    Analyzes password strength using zxcvbn and custom entropy logic.
    """
    @staticmethod
    def analyze(password):
        """
        Returns a dictionary containing strength score, crack time, and entropy.
        """
        if not password:
            return {
                "score": 0,
                "crack_time": "Instant",
                "entropy": 0.0,
                "feedback": "Empty password"
            }

        results = zxcvbn.zxcvbn(password)
        
        # Calculate Entropy: log2(Character Pool Size ^ Length)
        entropy = PasswordAnalyzer._calculate_entropy(password)
        
        # Refine score based on entropy and length to avoid "everything is 4"
        score = results['score']
        length = len(password)
        
        # Refined caps for nuanced scoring variety
        if length < 8:
            score = min(score, 1)
        elif length < 10:
            score = min(score, 2)
        elif length < 12:
            score = min(score, 3)  # Keeping a slight cap for 10-11 chars to avoid instant 4/4
            
        return {
            "score": score,  # 0 to 4
            "crack_time": results['crack_times_display']['offline_slow_hashing_1e4_per_second'],
            "entropy": round(entropy, 2),
            "feedback": results['feedback']['warning'] or "Good password"
        }

    @staticmethod
    def _calculate_entropy(password):
        if not password:
            return 0
        
        pool_size = 0
        if any(c.islower() for c in password): pool_size += 26
        if any(c.isupper() for c in password): pool_size += 26
        if any(c.isdigit() for c in password): pool_size += 10
        if any(not c.isalnum() for c in password): pool_size += 32
        
        if pool_size == 0:
            return 0
            
        return len(password) * math.log2(pool_size)
