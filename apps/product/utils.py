import json

from pathlib import Path
import google.generativeai as genai


def extract_data_from_tag(image_path):
    genai.configure(api_key="AIzaSyAHs5fgDlrSyGLyw1eUPvXSrEWacqnR94s")

    # Set up the model
    generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
    ]

    model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    # Validate that an image is present
    PATH = f"/Users/kushagraagarwal/Documents/dimple_collection/dimple_collection_business_pipeline/apps/media/tag_images/{image_path}"
    if not (img := Path(PATH)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
    {
        "mime_type": "image/png",
        "data": Path(PATH).read_bytes()
    },
    ]

    prompt_parts = [
    image_parts[0],
        (
            "Extract the information from this cloth tag."
            "Map the extracted data to our Product model field, those are - department, brand, color, article_number, size, mrp"
            "The value of department can be - 2P SUIT, 5P SUIT, ANARKALI KURTA, BLAZER R NECK, BLAZER V NECK, BOTTOM, COTI, DARK INDO, FOOTWERE, INDO BOX, INDO WESTERN, JEANS, JODHPURI, KURTA COTI, KURTA PAJAMA, KURTA SHRUG H, ONLINE, PATHANI, SAFA STALL SET, SHERWANI, SHIRT, STALL, TIE, TROUSER, T-SHIRT, WAIST COAT SUIT or WOOLEN"
            "The value of brand will be the manufacturer(MFG), Concept by, or the band name on the tag"
            "The value of color will be the color of cloth mentioned on tag"
            "The value of article_number will be the unqine code mentioned on tag. It's name can be mentioned as - sytle, d.no, or article"
            "The value of mrp will be the price of product mentioned on tag"
            "The value of size will be the size of product mentioned on tag"
            "Name of the fields will not be same exactly and you may not find all the fields but map the fields which you feel are best suited"
            "The output you should give should only be the json, mapping the extracted data with the model Product fields"
        ),
    ]
    response = model.generate_content(prompt_parts)
    print(response.text)
    try:
        json_data = json.loads(response.text)
    except:
        json_content = response.text.strip("`\n")
        json_content = json_content[8:]
        json_data = json.loads(json_content)
    return json_data
