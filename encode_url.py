from urllib.parse import quote

# النص الذي ترغب في ترميزه
text_to_encode = "some string to encode"

# استخدام دالة quote لترميز النص
encoded_text = quote(text_to_encode)

print(encoded_text)
