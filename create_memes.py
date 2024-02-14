import requests


def get_meme_templates():
    """
    Retrieves a list of available meme templates from the Imgflip API.

    Returns:
        list: A list of meme templates if successful.
        str: Error message if unsuccessful.
    """
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
    """
    Creates a meme using the specified template ID and text captions.

    Args:
        template_id (str): The ID of the meme template.
        text_top (str): The text caption for the top of the meme.
        text_bottom (str): The text caption for the bottom of the meme.

    Returns:
        str: URL of the generated meme if successful.
        str: Error message if unsuccessful.
    """
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
