from flask import jsonify, request
import json
import requests
import os


def find_energy(name):
    yandex_translate_api_string = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=" + os.environ.get(
        "YANDEX_API_KEY", None) + "&text=" + name + "&lang=en"
    usda_api_search_request_string = "https://api.nal.usda.gov/fdc/v1/search?api_key=" + os.environ.get("USDA_API_KEY",
                                                                                                        None)

    yandex_translate_result = json.loads(requests.get(yandex_translate_api_string).content)["text"][0]
    usda_search_result = str(int(json.loads(
        requests.post(usda_api_search_request_string, None,
                      {"generalSearchInput": yandex_translate_result}).content)[
                                     "foods"][0]["fdcId"]))

    usda_api_food_inf_result = "https://api.nal.usda.gov/fdc/v1/" + usda_search_result + "?api_key=" + os.environ.get(
        "USDA_API_KEY", None)

    usda_result_energy_json = json.loads(requests.get(usda_api_food_inf_result).content)['foodNutrients']
    usda_result_energy = '-1.0'

    for i in range(len(usda_result_energy_json)):
        if usda_result_energy_json[i]["nutrient"]["name"] == 'Energy':
            usda_result_energy = str(usda_result_energy_json[i]["amount"])


    return usda_result_energy
