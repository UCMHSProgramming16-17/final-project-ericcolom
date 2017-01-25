#import modules/requests
import requests
import bokeh
import pandas as pd
import csv
import numpy as np
import json

api1="https://maps.googleapis.com/maps/api/geocode/json"
csvfile=open('data.csv','w')
csvwriter=csv.writer(csvfile, delimiter=',')

#the while loop allows the user to enter the desired amount of inputs
number=0

city = []
temp = []

while number<3:
    #put together url
    address=input("address:")
    if address=='quit':
        break
    # url=api1+urllib.parse.urlencode({"address":address})
    # print(url)
    #get data from api
    json_data=requests.get(api1, params={'address':address}).json()

    json_status=json_data["status"]
    print("API Status:"+json_status)
    #access sub-dictoionary of results to get easy to read, formatted address
    if json_status == 'OK':
        for each in json_data ["results"][0] ["address_components"]:
            print(each["long_name"])
            
        simple_address=json_data["results"][0]["formatted_address"]
        print(simple_address)
        number+=1
        lat=str(json_data["results"][0]["geometry"]["bounds"]["northeast"]["lat"])
        print(lat)
        lng=str(json_data["results"][0]["geometry"]["bounds"]["northeast"]["lng"])
        print(lng)
    #Use the latitude and longitude from the previous api for the coordinates of Dark sky to get the temperature.
    #create url for dark sky api
    endpoint='https://api.darksky.net/forecast/'
    key='804c033fb6e3278059f4195775533fae'
    payload={'units':'us'}
    url2=endpoint+key+'/'+lat+','+lng
    json_data2=requests.get(url2,params=payload)
    data=json_data2.json()
    temperature=data['currently']['temperature']
    print(temperature)
    city.append(address)
    temp.append(temperature)
    #import bokeh and create x and y axises
from bokeh.charts import Bar, output_file, show
from bokeh.charts import Bar, output_file, save
print('cities', city)
df = pd.DataFrame({'city':city, 'temperature':temp})
print(df)
output_file("Temp of cities")
bar1=Bar(df,"city",values="temperature",title="Temperature of various locations")
save(bar1)

