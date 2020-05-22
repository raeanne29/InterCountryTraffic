import pickle
import pyasn
from prettytable import PrettyTable

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

## converting the ip addresses to asn     
ip_to_asn = []
for couple, traceroute in diction.items():
    liste = []
    for trace in traceroute:
        for ip in trace:
            tup = ()
            asn, prefix = db_with_names.lookup(ip)
            rec = db_with_names.get_as_name(asn)
            if rec is not None:
                tup+=(asn,)
                owner_country = rec.split(",")
                tup+=(owner_country[0],)
                tup+=(owner_country[1][1:],)
                liste.append(tup)
    ip_to_asn.append(liste)

## filtering menog countries        
traceroutes = []
for trace in ip_to_asn:
    i = 0
    l = []
    while(i<len(trace)):
        if(trace[i][2] not in menog):
            if(trace[i][0]==6453):
                l.append((trace[i][0],"TATA COMMUNICATIONS"))
            else:
                l.append((trace[i][0],trace[i][1]))
        i+=1
    traceroutes.append(unique(l))

## adapting the results to the table input
couples = {}
for trace in traceroutes:
    i = 0
    while(i<len(trace)):
        if(trace[i] in couples.keys()):
            couples[trace[i]]+=1
        else:
            couples[trace[i]]=1
        i+=1

couplesList = sorted(couples, key=couples.get, reverse=True)

asNumbers = []
for asn in couplesList:
    asNumbers.append(str(asn[0]))

asNames = []
for asn in couplesList:
    asNames.append(str(asn[1]))

percentage = []
for asn in couplesList:
    percentage.append(couples[asn])

perc = []
for i in percentage:
    p = round(i*100/196,2)
    a = str(p) + "%"
    perc.append(a)

rank = []
for x in range(len(perc)):
  rank.append(x + 1)

stats = PrettyTable(['Rank','AS Number','AS Name','Perc'])
i = 0
while(i<len(rank)):
    stats.add_row([rank[i],asNumbers[i],asNames[i],perc[i]])
    i+=1
print(stats)


