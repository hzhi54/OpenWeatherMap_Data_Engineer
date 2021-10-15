import requests
import json
import time
import pymongo
import pandas as pd


usa = pd.read_csv('usa.csv')
ZIP = ["36104","99801","85001","72201","95814","80202","06103"
    ,"19901","32301","30303","96813","83702","62701","46225","50309"
    ,"66603","40601","70802","04330","21401","02201","48933","55102"
    ,"39205","65101","59623","68502","89701","03301","08608","87501"
    ,"12207","27601","58501","43215","73102","97301","17101","02903"
    ,"29217","57501","37219","78701","84111","05602","23219","98507"
    ,"25301","53703","82001"]
STATE = usa.head(50)['State'].values

LAT = ["32.377716","58.301598","33.448143","34.746613","38.576668","39.739227",
        "41.764046","39.157307","21.307442","30.438118","33.749027","43.617775",
        "39.798363","39.768623","41.591087","39.048191","38.186722","30.457069",
        "44.307167","38.978764","42.358162","42.733635","44.955097","32.303848",
        "38.579201","46.585709","40.808075","39.163914","43.206898","40.220596",
        "35.68224","35.78043","46.82085","42.652843","39.961346","35.492207",
        "44.938461","40.264378","41.830914","34.000343","44.367031","36.16581",
        "30.27467","40.777477","44.262436","37.538857","47.035805","38.336246",
        "43.074684","41.140259"]
LON = ["-86.300568","-134.420212","-112.096962","-92.288986","-121.493629","-104.984856",
        "-72.682198","-75.519722","-157.857376","-84.281296","-84.388229","-116.199722",
        "-89.654961","-86.162643","-93.603729","-95.677956","-84.875374","-91.187393",
        "-69.781693","-76.490936","-71.063698","-84.555328","-93.102211","-90.182106",
        "-92.172935","-112.018417","-96.699654","-119.766121","-71.537994","-74.769913",
        "-105.939728","-78.639099","-100.783318","-73.757874","-82.999069","-97.503342",
        "-123.030403","-76.883598","-71.414963","-81.033211","-100.346405","-86.784241",
        "-97.740349","-111.888237","-72.580536","-77.43364","-122.905014","-81.612328",
        "-89.384445","-104.820236"]

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?zip="
API_KEY = "4bef6b99cccc82e075c4404ee09824f5"

class CurrentWeather:
    
    def getData(self):
        data = []
        for zipcode in ZIP:
            URL = BASE_URL + zipcode + "&units=imperial&appid=" + API_KEY
            response = requests.get(URL)
            data.append(response.json())
            
        
        return data
    
    def toDataBase(self):
        data = self.getData()
        client = pymongo.MongoClient()
        client.list_database_names()
        database = client['test']
        collection = database['current']
        collection.drop()
        collection = database['current']
        for jsn in data:
            collection.insert_one(jsn)
            
    def toDataFrame(self):
        client = pymongo.MongoClient()
        database = client['test']
        collection = database['current']
        cursor = collection.find({},{'_id':0,'main':1,'wind':1,'name':1,'coord':1})
        entity = list(cursor)
        weather_dict = {'Name':[],'Temperature':[],'Temp_Min':[],'Temp_Max':[],'Humidity':[],'Wind':[],'Zip':[],'Latitude':[],'Longitude':[]}
        for i,ent in enumerate(entity):
            weather_dict['Name'].append(ent['name'])
            weather_dict['Temperature'].append(ent['main']['temp'])
            weather_dict['Temp_Min'].append(ent['main']['temp_min'])
            weather_dict['Temp_Max'].append(ent['main']['temp_max'])
            weather_dict['Humidity'].append(ent['main']['humidity'])
            weather_dict['Wind'].append(ent['wind']['speed'])
            weather_dict['Zip'].append(ZIP[i])
            weather_dict['Latitude'].append(ent['coord']['lat'])
            weather_dict['Longitude'].append(ent['coord']['lon'])
            
        df = pd.DataFrame(weather_dict)
        df['State'] = STATE
        # df.to_csv('cutrent.csv',index=False)
        return df
        