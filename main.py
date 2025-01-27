import google.generativeai as genai

genai.configure(api_key="AIzaSyCOB2y0BvA7vek7NHko_uMKfjIb1Kg2ets")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)