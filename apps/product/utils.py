import os
import json
from pathlib import Path

import google.generativeai as genai

from django.conf import settings

from apps.department.models import Department


def extract_data_from_tag(image_path):
    print("debug_is_on")
    genai.configure(api_key="AIzaSyAHs5fgDlrSyGLyw1eUPvXSrEWacqnR94s")

    # Set up the model
    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-vision-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # Validate that an image is present
    PATH = os.path.join(settings.MEDIA_ROOT, "tag_images", image_path)

    if not (img := Path(PATH)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {"mime_type": "image/png", "data": Path(PATH).read_bytes()},
    ]

    departments = Department.objects.values("id", "department_name")

    prompt_parts = [
        image_parts[0],
        (
            "Extract the information from this cloth tag. "
            "Map the extracted data to our Product model field, those are - department, brand, color, article_number, size, mrp. "
            "The value of department can be - 2P SUIT, 5P SUIT, ANARKALI KURTA, BLAZER R NECK, BLAZER V NECK, BOTTOM, COTI, DARK INDO, FOOTWERE, INDO BOX, INDO WESTERN, JEANS, JODHPURI, KURTA COTI, KURTA PAJAMA, KURTA SHRUG H, ONLINE, PATHANI, SAFA STALL SET, SHERWANI, SHIRT, STALL, TIE, TROUSER, T-SHIRT, WAIST COAT SUIT or WOOLEN. "
            "The value of brand will be the manufacturer(MFG), Concept by, or the band name on the tag. "
            "The value of color will be the color of cloth mentioned on tag. "
            "The value of article_number will be the unqine code mentioned on tag. It's name can be mentioned as - sytle, d.no, or article. "
            "The value of mrp will be the price of product mentioned on tag. "
            "The value of size will be the size of product mentioned on tag. "
            "Name of the fields will not be same exactly and you may not find all the fields but map the fields which you feel are best suited. "
            "The output you should give should only be the json, mapping the extracted data with the model Product fields. "
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

    if value := json_data.get("department", None):
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        departments_json = json.dumps(list(departments))
        value = value.lower()
        prompt = f"Perform text matching. I am providing you a json of list of department_name and there id - {departments_json}. Match the provided list and check if '{value}' is present in department_name, it will not be same exactly, but its meaning should be similar. The output you should give should only be the matching json."
        prompt_parts = [prompt]
        response = model.generate_content(prompt_parts)
        print(response.text)
        try:
            djson_data = json.loads(response.text)
        except:
            djson_data = {"id": 1}

        try:
            json_data.pop("department")
            json_data["department_id"] = djson_data.get("id")
        except:
            json_data["department_id"] = 1
    else:
        try:
            json_data.pop("department")
            json_data["department_id"] = 1
        except:
            json_data["department_id"] = 1

    return json_data
