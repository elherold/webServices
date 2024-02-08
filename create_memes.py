import requests

def get_meme_templates():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            return data["data"]["memes"] 
        else:
            return "Failed to retrieve memes."
    else:
        return "API request failed."


def create_meme(template_id, text_top, text_bottom):
    url = "https://api.imgflip.com/caption_image"
    params = {
        'username': 'elherold',
        'password': 'MemeAPI!',
        'template_id': template_id,
        'text0': text_top,
        'text1': text_bottom,
    }
    print("top text:", text_top)
    print("bottom:", text_bottom)
    print("template_id:", template_id)

    response = requests.post(url, data=params).json()
    if response["success"]:
        return response["data"]["url"]
    else:
        return "Failed to create meme."

"""
# Example usage
meme_url = create_meme('112126428', 'Mensa Fries', 'Me')
print(meme_url)

# Example usage
templates = get_meme_templates()
for template in templates[:5]:  # Print the first 5 templates
    print(template["name"], template["url"])
"""