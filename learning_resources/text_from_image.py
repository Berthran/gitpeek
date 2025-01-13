import google.generativeai as genai

import PIL.Image

model = genai.GenerativeModel("gemini-1.5-flash")
organ = PIL.Image.open(media / "organ.jpg")
response = model.generate_content(["Tell me about this instrument", organ])
print(response.text)
