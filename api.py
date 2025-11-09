import requests
import base64

api_key = "AIzaSyBoRT98AzjxgJMWSgMjtpAfKlBUyjlXsZ8"  # Please set your API key
prompt = input("enter text to generate image:")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": prompt}], "role": "user"}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()  # Raise an error for bad status

data = response.json()

# Find the image data in the response
image_part = None
for part in data["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        image_part = part["inlineData"]
        break

if image_part:
    image_data = base64.b64decode(image_part["data"])
    mime_type = image_part["mimeType"]
    
    # Save the image to a file with appropriate extension
    ext = mime_type.split("/")[-1]
    filename = f"sample.{ext}"
    with open(filename, "wb") as f:
        f.write(image_data)
    print(f"Image saved as {filename}")
else:
    print("No image data found in response.")
