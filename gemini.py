import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("map out the experience of a programmer who learned how to write print('Hello world') today")
# print(response.text)
# print(type(response))
print(response.text)

# print(model.count_tokens("Explain how AI works"))
# chat = model.start_chat()
# response = chat.send_message("hello")
# print(response.text)

# genai.GenerativeModel()
