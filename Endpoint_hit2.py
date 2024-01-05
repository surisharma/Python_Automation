import json
import requests
person_ISS=[]
person_Tiangong=[]
def space_endpoint(url):
    data = requests.get(url)
   # print(data.json())
    dump = data.json()
    for  person in dump["people"]:
        print(person["craft"])
        if (person["craft"] == "ISS"):
          person_ISS.append(person["name"])
        else:
          person_Tiangong.append(person["name"])
    print("Total number of person in ISS" +   str(len(person_ISS)))
    print("Total number of person in Tiangong" +   str(len(person_Tiangong))) 
space_endpoint("http://api.open-notify.org/astros.json")          
