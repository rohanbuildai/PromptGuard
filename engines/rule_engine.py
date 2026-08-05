"""
Rule-based prompt injection detection engine.

Detects known malicious prompt injection patterns using
weighted keyword matching.

"""


from config import patterns
from config.constants import EDUCATIONAL_PATTERNS


def is_educational_prompt(prompt):

    prompt = prompt.lower()

    for pattern in EDUCATIONAL_PATTERNS:
        if pattern in prompt:
            return True

    return False

def detect_prompt_injection(prompt) :
    prompt = prompt.lower()
    educational = is_educational_prompt(prompt)

    matched_patterns = []
    total_score = 0

    for pattern, weight in patterns.SUSPICIOUS_PATTERNS.items() :
        if pattern in prompt :
            matched_patterns.append(pattern)
            total_score += weight

    if educational:
        total_score *= 0.4


    safe = True
    risk = "safe"
    score = 0

    if total_score == 0 :
        safe = True
        risk = "SAFE"
        score = total_score

    elif 1<= total_score <30 :
        safe = False
        risk = "LOW"
        score = total_score


    elif 30<= total_score <70 :
        safe = False
        risk = "MEDIUM"
        score = total_score

    elif total_score >= 70 :
        safe = False
        risk = "HIGH"
        score = total_score

    return {
        "safe" : safe,
        "risk" : risk,
        "score" : score,
        "detection_count" : len(matched_patterns),
        "matched_patterns" : matched_patterns,
        "is_educational" : educational
    }