import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def ai_request(data_string):
    """
    Function to get an AI request for a book recommendation
    :param data:
    :return:
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="""Can you recommend a book for me based on my ratings of the following dataset,
        with personal ratings form 0 to 10 as float vlaues, please?:
        "dataset":"""+data_string+"""
        Please answer in the json string format , so I can load the request into python.
        Here an example: 
        {"book":
            {"title": "some title",
             "author": "some author",
              "year": "some year",
              "isbn": "some isbn with only numbers please",
              "birthday": "author's birthday" as python datetime object with format "YYYY-MM-DD",
              "died": "author's deathday" as pythondatetime object \
              withformat "YYYY-MM-DD" or 
              Null if still alive},
        "reasoning": "your reasoning text"} 
        """
    )

    json_string = response.text.replace("```json", "")
    json_string = json_string.replace("```", "")

    data = json.loads(json_string)
    return data
