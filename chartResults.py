import pickle
import pyasn
import matplotlib.pyplot as plt
import numpy as np

menog = ["AE","BH","EG","IQ","IR","JO","KW","LB","OM","PS","QA","SA","SY","TR","YE","Dubai","Floor 7"]

def unique(l):
    u = []
    for x in l:
        if x not in u:
            u.append(x)
    return u

diction={}
asnames = 'asnames.json'
asndb = 'IPASN.DAT'
db_with_names = pyasn.pyasn(asndb,asnames)
with open('measurements_pickle.txt', 'rb') as filehandle:
    # read the data as binary data stream
    diction = pickle.load(filehandle)

## converting the ip addresses to countries   
ip_to_countries = []
for couple, traceroute in diction.items():
    liste = []
    for trace in traceroute:
        for ip in trace:
            asn, prefix = db_with_names.lookup(ip)
            rec = db_with_names.get_as_name(asn)
            if rec is not None:
                owner_country = rec.split(", ")
                liste.append(owner_country[1])
    ip_to_countries.append(liste)

## filtering menog countries
traceroutes = []
for trace in ip_to_countries:
    i = 0
    l = []
    while(i<len(trace)):
        if(trace[i] not in menog):
            if(trace[i] == "Russia"):
                l.append("RU")
            elif(trace[i] == "15123 Maroussi"):
                l.append("GR")
            else:
                l.append(trace[i])
        i+=1
    traceroutes.append(unique(l))

## adapting the results to the chart input
couples = {}
for traceroute in traceroutes:
    i = 0
    while(i<len(traceroute)):
        if(traceroute[i] in couples.keys()):
            couples[traceroute[i]]+=1
        else:
            couples[traceroute[i]]=1
        i+=1
            
countries = list(couples.keys())
height = list(couples.values())

y_pos = np.arange(len(countries))
plt.barh(y_pos, height)
plt.yticks(y_pos, countries)
plt.show()
