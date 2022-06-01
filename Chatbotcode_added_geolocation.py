from flask import Flask, request, jsonify, render_template
import requests
import json
import pandas as pd
from weo import download, WEO
import numpy_financial as npf
from geopy.geocoders import Nominatim
import apicode
from flask_cors import CORS
import os
from countryinfo import CountryInfo



app = Flask("__name__")

CORS(app)
dict1 = dict()

#Dictionary Inititialisations to avoid errors
dict1["type"] = ""
dict1["RetrResp"] = ""
dict1["RetrAmt"]= -1
dict1["Investments"]=0
#Changes Made
def sumInsured():
    #Calculating Inflation using WEO
    path, url = download(2022, 1)
    print(dict1["country"])
    df_cpi_country = WEO(path).countries(dict1["country"])["ISO"]
    print(df_cpi_country)
    country_code = list(df_cpi_country)[0]
    df_cpi_inflation = WEO(path).inflation()[country_code]["2021"]
    inflation = df_cpi_inflation*0.01

    #Sum Insured Calculation
    years = dict1["RetrAge"] - dict1["Age"]
    inv_rate = 0.10
    disc_rate = 0.10 - inflation
    avg_expenses = dict1["AvgExpenses"]*12
    pmt = dict1["Income"] - avg_expenses
    other_income = dict1["Investments"] - dict1["Loan"]
    pv = npf.pv(disc_rate,years,-avg_expenses,0,when='end')
    sum_insured = round(pv[0] - other_income, -3)
    currencies = CountryInfo(dict1["country"]).currencies()
    text1 = "Based on your details the right sum assured for you would be {} {} ".format(sum_insured,currencies[0])
    if dict1["Nicotine"] == "I do not consume":
        text2 = "Thank you for the details"
    else:
        text2 = "You might need Critical Insurance Rider"
    return [text1,text2]

def goalPlan(age,retrAge):
    diffAge = retrAge - age
    if diffAge >= 3 :
        plan = "Deferred Plan"
    else :
        plan = "Immediate Plan"
    dict1["AnnuityPlan"] = plan
    text1 = "According to your response it would be preferrable to select {}".format(plan)
    text2 = "Could you please confirm by selecting the preferred choice"
    return [text1,text2,["Deferred Plan","Immediate Plan"]]

def annCalculation():
    #Calculating Inflation using WEO
    path, url = download(2022, 1)
    print(dict1["country"])
    df_cpi_country = WEO(path).countries(dict1["country"])["ISO"]
    print(df_cpi_country)
    country_code = list(df_cpi_country)[0]
    df_cpi_inflation = WEO(path).inflation()[country_code]["2021"]
    inflation = df_cpi_inflation*0.01
    #Annuity Calculation
    n = dict1["RetrAge"] - dict1["Age"]
    roi = 0.09
    expenses = dict1["AvgExpenses"]*0.75
    fv_expenses = (expenses * pow((1 + inflation), n))
    retr_age = dict1["RetrAge"]
    if dict1["Sex"] == "Male":
        life_expectancy = 73
    elif dict1["Sex"] == "Female":
        life_expectancy = 76
    arr = ((1 + roi) / (1 + inflation)) - 1
    arr_monthly = arr / 12
    retr_months = (life_expectancy - retr_age) * 12
    pmt = fv_expenses
    if dict1["RetrAmt"]> 0:
        corpus = npf.pv(arr_monthly, retr_months, -pmt, when='end')
        corpus= corpus[0] - dict1["RetrAmt"]
    else:
        corpus = npf.pv(arr_monthly, retr_months, -pmt, when='end')
        corpus = corpus[0]
    print(corpus)

    if dict1["Investments"]>0:
        corpus-=dict1["Investments"]
    corpus =round (corpus, -3)
    premium = npf.pmt(roi / 12, n * 12, 0, -corpus, when='end')
    premium =round(premium, -2)
    currencies = CountryInfo(dict1["country"]).currencies()
    print(currencies[0])
    text1 = "According to your responses you would need approximately {} {} as retirement corpus".format(corpus,currencies[0])
    text2 = "So if you invest {} {} monthly as part of Annuity Plan you would be able to secure your retirement. ".format(premium,currencies[0])
    if int(dict1["Income"]/12)*0.20 < premium:
        text3 = "\nI would suggest you to check the Guaranteed Lifetime Withdrawal Benefit rider"
        text2 = text2+text3
    return [text1,text2]


def geoDetails(city):
    loc = Nominatim(user_agent="GetLoc")
    # entering the location name
    getLoc = loc.geocode(city)
    if len(getLoc.address.split(",")) == 5:
        state = getLoc.address.split(",")[-3]
        country = getLoc.address.split(",")[-1]
        dict1["country"] = country.strip()
    if len(getLoc.address.split(",")) == 4:
        state = getLoc.address.split(",")[-2]
        country = getLoc.address.split(",")[-1]
        dict1["country"] = country.strip()

    if dict1["country"] == "United States":
        country1 = "USA"
    else:
        country1 = dict1["country"]
    api_key = "432e12f9-57c3-42c4-8fa1-ba346837d8a8"
    response_api = requests.get(
        f'http://api.airvisual.com/v2/city?city={city}&state={state}&country={country1}&key={api_key}')
    data = response_api.text
    parse_json = json.loads(data)
    # print(parse_json)
    weather = parse_json['data']['current']['weather']
    temperature = weather['tp']
    aqius = parse_json['data']['current']['pollution']['aqius']
    #print(temperature)
    if temperature > 35:
        climate = "hot climate so be hydrated & take care when you step out"
    else:
        climate = "good climate conditions"
    if aqius > 100:
        pol = "high pollution levels"
        pol1 = "dangerous so be careful when you step out"
    elif aqius < 100 and aqius > 50:
        pol = "moderate pollution levels"
        pol1 = "okay but take precautions while heading out"
    else:
        pol = "low pollution levels"
        pol1 = "an excellent place to be in"
    #Changes Made
    #Expenses details
    file = "C:/Users/Gautam/Desktop/Numbeo.csv"
    df = pd.read_csv(file)
    df_values = df.loc[df['City'] == city]["Expenses3"]
    dict1["AvgExpenses"] = df_values

    
    text1 = "I see that {} has {}.\n The AQI states {} which is {} ".format(city, climate, pol, pol1)

    if dict1["type"] == "Annuity":
        text2 = 'Did you invest in CDs, Mutual Funds, Equity, etc. ?'
        chipslist = ["yes","no"]
    else:
        text2 = "What is your marital status ?"
        chipslist = ["Single", "Divorced", "Married"]
    return [text1, text2, chipslist]
    #chipslist = ["Single","Divorced","Married"]

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
        if dict1["Nicotine"] == "I do not consume":
            text1 = 'Awesome! you are one in 13 out of 100 who doesnt smoke'
            text2 = 'What is your annual income before tax ?'
            return [text1,text2]
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
    elif act == "Hi.Hi-no.Hi-no-Li-Sex-custom.Hi-no-LI-Sex-Age-custom.Hi-no-LI-Sex-Age-Ht-custom.Hi-no-LI-Sex-Age-Ht-Wt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-custom.Hi-no-LI-Sex-Age-Ht-Wt-Nt-Inr-custom":
        dict1["Income"] = data1.query_result.parameters["number"]
    elif act == "Investments.Investments-yes.Investments-yes-custom":
        dict1["Investments"] = data1.query_result.parameters["number"]
    elif act == "loan":
        dict1["Loan"] = data1.query_result.parameters["number"]
    elif act == "Investments.Investments-yes.Investments-yes-custom.Investments-yes-amt-custom.Investments-yes-amt-goals-custom":
        dict1["RetrAge"] = data1.query_result.parameters["number"]
        sum_insured = sumInsured()
        return sum_insured
    return 0
    


def yesLife(data1):
    act = data1.query_result.action
    if act == "Hi.Hi-yes.Hi-yes-custom":
        dict1["Sex"] = data1.query_result.query_text
    elif act == "Hi.Hi-yes.Hi-yes-custom.Age-custom":
        dict1["Age"] = data1.query_result.parameters["number"]
    elif act == "Hi.Hi-yes.Hi-yes-custom.Age-custom.Ret-custom":
        dict1["RetrAge"] = data1.query_result.parameters["number"]
        planType = goalPlan(dict1["Age"],dict1["RetrAge"])
        return planType
    elif act == "Hi.Hi-yes.Hi-yes-custom.Age-custom.Ret-custom.Typ-custom.Nt-custom":
        dict1["Nicotine"] = data1.query_result.query_text
        if dict1["Nicotine"] == "I do not consume":
            text1 = 'Awesome! you are one in 13 out of 100 who doesnt smoke'
            text2 = 'How much do you earn annually?'
            return [text1,text2]
    elif act == "Hi.Hi-yes.Hi-yes-custom.Age-custom.Ret-custom.Typ-custom.Nt-custom.Rt-custom":
        dict1["Income"] = data1.query_result.parameters["number"]
    elif act == "Hi.Hi-yes.Hi-yes-custom.Age-custom.Ret-custom.Typ-custom.Nt-custom.Rt-custom.Rp-yes":
        dict1["RetrResp"] = "Yes"
    elif act == "LocAnn":
        if dict1["RetrResp"] == "yes":
            dict1["RetrAmt"] = data1.query_result.parameters["number"]
            print(dict1["RetrAmt"])
    elif act == "Loc-Ann.Loc-Ann-custom":
        city = data1.query_result.parameters["geo-city"]
        dict1["Location"] = city
        a = geoDetails(city)
        return a
    elif act == "Loc-Ann.Loc-Ann-custom.Inv-no":
        amt = annCalculation()
        return amt
    elif act == "Loc-Ann.Loc-Ann-custom.Inv-yes.Inv-yes-custom":
        dict1["Investments"] = data1.query_result.parameters["number"]
        amt = annCalculation()
        return amt





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
    resp = apicode.detect_intent_texts("nova-dskj","1234",text)
    
    
    richresponses = resp.query_result.fulfillment_messages
    # print("=" *20)
    #msg.payload["richContent"][0][0]["options"][i]["text"]
    
    #print(len(msg.payload["richContent"][0][0]["options"]))
    #print([len(msg.payload["richContent"][0][0]["options"]) for msg in richresponses if msg.payload])
    # print("=" *20)

    # GOD please help me on how to deserialise a Struct protubuf by google. This is a hacky solution until then :(
    act = resp.query_result.action
    if act == "Hi.Hi-no":
        dict1["type"] = "Life Insurance"
    elif act == "Hi.Hi-yes":
        dict1["type"] = "Annuity"
    else:
        pass

    if dict1["type"] == "Life Insurance":
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

    elif dict1["type"] == "Annuity":
        funcot = yesLife(resp)
        if funcot:
            for i, text in enumerate(funcot):
                message["answer" + str(i)] = funcot[i]
                if i == 1:
                    break

            if len(funcot) > 2:
                for i, text in enumerate(funcot[2]):
                    message["chips" + str(i)] = funcot[2][i]
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
