GSM_7_BASIC = (
    '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?'
    '¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`abcdefghijklmnopqrstuvwxyzäöñüà'
)

def is_gsm7(text):
    for char in text:
        if char not in GSM_7_BASIC:
            return False
    return True

def split_sms_wordsafe(text):
    if is_gsm7(text):
        single_limit = 160
        multi_limit = 153
    else:
        single_limit = 70
        multi_limit = 67

    if len(text) <= single_limit:
        return [text]

    words = text.split()
    parts = []
    current_part = ""

    for word in words:
        # If adding this word exceeds the part length
        if len(current_part) + len(word) + (1 if current_part else 0) > multi_limit:
            parts.append(current_part)
            current_part = word
        else:
            current_part += (" " if current_part else "") + word

    if current_part:
        parts.append(current_part)

    return parts

# Example usage
message = "Hello! Це змішане повідомлення з латиницею і кирилицею. Ми хочемо зберегти цілі слова та правильні межі частин SMS."
parts = split_sms_wordsafe(message)

for i, part in enumerate(parts, 1):
    print(f"Part {i}/{len(parts)}: {part}")
