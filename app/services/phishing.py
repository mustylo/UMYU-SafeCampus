"""Local, explainable phishing heuristics. This module never fetches URLs."""
import ipaddress
import re
from urllib.parse import unquote, urlparse

MAX_ANALYSIS_LENGTH = 10000


def analyze(message="", url=""):
    message, url = (message or "").strip(), (url or "").strip()
    if not message and not url:
        raise ValueError("Provide a suspicious message or URL.")
    if len(message) + len(url) > MAX_ANALYSIS_LENGTH:
        raise ValueError("Submission is too long; limit it to 10,000 characters.")
    indicators, score = [], 0
    lower = message.lower()
    rules = [(r"\b(urgent|immediately|act now|final warning|suspended|expire)\b", "Urgency or account-pressure language", 2),
             (r"\b(password|passcode|login credentials|otp|one[- ]time password|verification code)\b", "Request for credentials or an OTP", 3),
             (r"\b(pay|payment|transfer|bank|wallet|fee)\b", "Payment-related request", 2),
             (r"\b(prize|winner|scholarship|job offer|gift)\b", "Unexpected reward or opportunity claim", 1),
             (r"\b(click here|click the link|verify your account)\b", "Prompt to follow a link or verify an account", 2)]
    for pattern, label, points in rules:
        if re.search(pattern, lower): indicators.append(label); score += points
    candidate_urls = re.findall(r"https?://[^\s<>'\"]+", message, flags=re.I)
    if url: candidate_urls.append(url)
    for raw in candidate_urls:
        parsed = urlparse(raw if "://" in raw else f"https://{raw}")
        host = (parsed.hostname or "").lower()
        if not host:
            indicators.append("Malformed URL structure"); score += 2; continue
        try:
            ipaddress.ip_address(host)
            indicators.append("URL uses an IP address instead of a recognizable domain"); score += 3
        except ValueError:
            pass
        if host.count(".") >= 3: indicators.append("URL has an unusually deep subdomain structure"); score += 1
        if "xn--" in host or any(ord(c) > 127 for c in host): indicators.append("Internationalized domain needs careful manual verification"); score += 2
        if "@" in parsed.netloc or "%" in raw or unquote(raw) != raw: indicators.append("URL contains encoding or deceptive addressing syntax"); score += 2
        if re.search(r"(umyu|google|microsoft|bank)[-_]?(verify|secure|login|support)", host): indicators.append("Domain resembles a brand combined with a login/verification term"); score += 2
    if not indicators: risk = "Low"
    elif score >= 8: risk = "Critical"
    elif score >= 5: risk = "High"
    else: risk = "Medium"
    recommendations = ["Do not click suspicious links or open unexpected attachments.", "Never share a password or OTP.", "Verify the sender using an official, independently found contact channel."]
    return {"risk": risk, "score": score, "indicators": indicators or ["No high-confidence heuristic indicators were found."], "recommendations": recommendations, "disclaimer": "This local heuristic assessment is not proof that a message is malicious or safe. Submitted URLs were not opened or fetched."}
