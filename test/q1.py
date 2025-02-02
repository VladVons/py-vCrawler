import re

def extract_domains(text):
    pattern = r"\b[a-z0-9.-]+\.[a-z]{2,}(?:\.[a-z]{2,})?\b"
    return re.findall(pattern, text)

# List of example strings
examples = [
    "Visit oster.com.ua for details.",
    "Check out 1x1.ru now!",
    "Search on google.com.",
    "Invalid domain EXAMPLE.COM should not match.",
    "This is not a link.",
    "My site is example-domain.com."
]

# Extract domains from each example
extracted_domains = [extract_domains(example) for example in examples]

# Print results
for i, domains in enumerate(extracted_domains):
    print(f"Example {i + 1}: {domains}")
