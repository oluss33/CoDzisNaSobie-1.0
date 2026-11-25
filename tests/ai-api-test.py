from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Ile to jest 2/i w liczbach zespolonych?",
)

print(response.text)