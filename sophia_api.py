import requests, os
import openai

#weather api
api_weather = "1a9f612ac578e92b28e1ad44bf0a1c92"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

#open ai
openai.api_key = os.getenv("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")
