import google.generativeai as genai

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.", stream=True)
for chunk in response:
    print(chunk.text)
    print("-" * 80)
        
