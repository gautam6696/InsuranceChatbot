from flask import Flask, request, jsonify, render_template
import requests
import json
import pandas as pd
from geopy.geocoders import Nominatim
import apicode
from flask_cors import CORS

app = Flask("__name__")

CORS(app)
dict1 = dict()

def geoDetails(city):
    loc = Nominatim(user_agent="GetLoc")
    # entering the location name
    getLoc = loc.geocode(city)
    state = getLoc.address.split(",")[-3]
    country = getLoc.address.split(",")[-1]

    api_key = "432e12f9-57c3-42c4-8fa1-ba346837d8a8"
    response_api = requests.get(
        f'http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}')
    data = response_api.text
    parse_json = json.loads(data)
    # print(parse_json)
    weather = parse_json['data']['current']['weather']
    temperature = weather['tp']
    aqius = parse_json['data']['current']['pollution']['aqius']
    #print(temperature)
    if temperature > 35:
        climate = "hot climate so be careful"
    else:
        climate = "better climate"
    if aqius > 100:
        pol = "high pollution levels"
        pol1 = "dangerous so be careful when you step out"
    elif aqius < 100 and aqius > 50:
        pol = "moderate pollution"
        pol1 = "okay but take precautions while heading out"
    else:
        pol = "low pollution"
        pol1 = "an excellent place to breathe safely"

    # file = "C:/Users/Gautam/Desktop/Numbeo.csv"
    # df = pd.read_csv(file)
    # df_values = df.loc[df['City'] == city]
    # print(float(df_values["QI"]))

    
    text1 = " {} has generally {}\n It has {} which is {} ".format(city, climate, pol, pol1)
    text2 = "What is your marital status ?"
    chipslist = ["Single","Divorced","Married"]
    return [text1,text2, chipslist]
    # response = {
    #     'fulfillmentMessages': [
    #         {
    #             "text": {
    #                 "text": [
    #                     " {} has generally {}\n It has {} which is {} ".format(city, climate, pol, pol1)
    #                 ],

    #             }
    #         },
    #         {
    #             "text": {
    #                 "text": [
    #                     "When will be your happy retirement age?"
    #                 ]
    #             }
    #         }
    #     ]
    # }
    
    # # response = {
    # #     'fulfillmentText': " {} has generally {}\n It has {} which is {} ".format(city, climate, pol, pol1)
    # # }
    # # response = {
    # #     "outputContexts": [
    # #         {
    # #             "name": "Locationfollowon"
    # #         }ḥ
    # #     ]
    # # }

    # return response


def bmi(height, weight):
    value = round(weight/((height/100)*(height/100)),2)
    if value >= 30.0:
        status = "Obese"
        remark = "You need to reduce a lot of weight as you have a very high risk of heart diseases"
    elif value < 30.0 and value >= 25.0:
        status = "Overweight"
        remark = "You need to look at your diet, exercise and reduce weight as you have high risk of diseases"
    elif value < 25.0 and value > 18.5:
        status = "Healthy"
        remark = "Keep up the good work. You are healthy and fit"
    elif value < 18.5:
        status = "Underweight"
        remark = "Need to put on some weight as you are thin. Eat a healthy balanced diet"
    text1 = "Your bmi is {} which comes under {} category.{}.".format(value, status, remark)
    text2 = "Have you consumed nicotine or tobacco in last 3 years ?"
    return [text1,text2,["Daily","Often","Occasionally", "I do not consume"]]
    # Such a weird json response payload to type in. I think I am missing something? Better to make a class if time permits.
    # response = {
    #     'fulfillmentMessages': [
    #         {
    #             "text": {
    #                 "text": [
    #                     "Your bmi is {} which comes under {} category.{}.".format(
    #                         value, status, remark)
    #                 ],

    #             }
    #         },
    #         {
    #             "text": {
    #                 "text": [
    #                     "Have you consumed nicotine or tobacco in last 3 years ?"
    #                 ]
    #             }
    #         },
    #         {
    #             'payload': {
    #                 "richContent": [
    #                     [
    #                         {
    #                             "type": "chips",
    #                             "options": [
    #                                 {
    #                                     "text": "Daily"
    #                                 },
    #                                 {
    #                                     "text": "Often"
    #                                 },
    #                                 {
    #                                     "text": "Occasionally"
    #                                 },
    #                                 {
    #                                     "text": "I do not consume"
    #                                 }
    #                             ]

    #                         }
    #                     ]
    #                 ]

    #             }
    #         }
    #     ]
    # }

    # return response

bmiintent = "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom.Hi-no-LI-Sex-Age-Ht-custom.Hi-no-LI-Sex-Age-Ht-Wt-custom"

def noLife(data1):
    act = data1.query_result.action
    if act == "Hi.Hi-no.Hi-no-Li-Sex-custom":
        dict1["Sex"] = data1.query_result.query_text
    elif act == "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom":
        #print("Numbersa re", data1.query_result)
        dict1["Age"] = data1.query_result.parameters["number"]
        #print(dict1)
    elif act == "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom.Hi-no-LI-Sex-Age-Ht-custom":
        dict1["Height"] = data1.query_result.parameters["number"]
        #print(dict1)
    elif act == bmiintent:
        dict1["Weight"] = data1.query_result.parameters["number"]
        bmiresponse = bmi(float(dict1["Height"]), float(dict1["Weight"]))
        #dict1["bmi"] = bmiresponse
        return bmiresponse
    elif act == "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom.Hi-no-LI-Sex-Age-Ht-custom.Hi-no-LI-Sex-Age-Ht-Wt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-custom":
        dict1["Nicotine"] = data1.query_result.query_text
    elif act == "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom.Hi-no-LI-Sex-Age-Ht-custom.Hi-no-LI-Sex-Age-Ht-Wt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-Inr-custom":
        dict1["Income"] = data1.query_result.parameters["number"]
    elif act == "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom.Hi-no-LI-Sex-Age-Ht-custom.Hi-no-LI-Sex-Age-Ht-Wt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-Inr-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-Inr-Oc-custom":
        dict1["Occupation"] = data1.query_result.query_text
    elif act == "location":
        city = data1.query_result.parameters["geo-city"]
        print("City is", city)
        dict1["Location"] = city
        a = geoDetails(city)
        return a
    return 0
    


def yesLife(data1):
    pass
    #print("Yes life", data1)


# @ app.route("/", methods=['POST'])
# def index():
#     data1 = request.get_json()
#     if "initial" in data1['queryResult']['action']:
#         pass
#     elif "Hi.Hi-no" == data1['queryResult']['action']:
#         dict1["Life Insurance"] = "No"
#     elif "Hi.Hi-yes" == data1['queryResult']['action']:
#         dict1["Life Insurance"] = "Yes"
#     elif "Life Insurance" in dict1.keys():
#         if dict1["Life Insurance"] == "No":
#             end, a = noLife(data1)
#             if end == "end":
#                 return jsonify(a)
#         else:
#             yesLife()
#     response = {
#         'fulfillmentText': ""
#     }
#     return jsonify(response)
#<link rel="stylesheet" href="{{ url_for('static',  filename='css/template.css') }}">

@ app.route("/welcome", methods=['POST'])
def welcome():
    message = {}
    richresponses = apicode.welcome_text()
    i = 0
    for messageresp in richresponses:
        #print(i,messageresp.text.text[0])
        message["answer"+str(i)] = messageresp.text.text[0]
        i = i+1
    return jsonify(message)

#query_text and parameters
# https://googleapis.dev/python/dialogflow/latest/dialogflow_v2/types.html?highlight=query#google.cloud.dialogflow_v2.types.QueryResult

@ app.route("/predict", methods=["POST"])
def predict():
    message = {}
    #print("This is the object", request.get_json())
    text = request.get_json().get("message")
    resp = apicode.detect_intent_texts("insurchatbot","1234",text)
    
    
    richresponses = resp.query_result.fulfillment_messages
    # print("=" *20)
    #msg.payload["richContent"][0][0]["options"][i]["text"]
    
    #print(len(msg.payload["richContent"][0][0]["options"]))
    #print([len(msg.payload["richContent"][0][0]["options"]) for msg in richresponses if msg.payload])
    # print("=" *20)

    # GOD please help me on how to deserialise a Struct protubuf by google. This is a hacky solution until then :(



    funcot = noLife(resp)
    if funcot:
        for i,text in enumerate(funcot):
            message["answer"+str(i)] = funcot[i]
            if i==1:
                break

        if len(funcot)>2:
            for i,text in enumerate(funcot[2]):
                message["chips"+str(i)] = funcot[2][i]  
        return jsonify(message)

    i = 0

    # GOD please help me on how to deserialise a Struct protubuf by google. This is a hacky solution until then :(
    for messageresp in richresponses:
        if messageresp.payload:
            # templist = []
            for j in range(len(messageresp.payload["richContent"][0][0]["options"]) ):
                #templist.append(messageresp.payload["richContent"][0][0]["options"][j]["text"])
                message["chips"+str(j)] = messageresp.payload["richContent"][0][0]["options"][j]["text"]

        if messageresp.text:
            message["answer"+str(i)] = messageresp.text.text[0]
            i = i+1
    
    return jsonify(message)

@ app.route("/")
def website():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
