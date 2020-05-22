import pickle
import pyasn
import plotly.graph_objects as go
import sys

if len(sys.argv)!=2:
    print("Provide an argument:")
    print("For a specific outgoing flow: provide country code")
    print("For all flows: type ALL")
    exit()

country = sys.argv[1]

menog = ["AE","BH","EG","IQ","IR","JO","KW","LB","OM","PS","QA","SA","SY","TR","YE","Dubai","Floor 7"]

labels = ["NL", "US", "GB", "DE", "FR", "EU", "IT", "IN", "RO", "AM","AZ",
          "RU","HK","BG", "IL", "CH", "AT", "KR", "CY","GR","AE_src",
          "BH_src","EG_src","IQ_src","IR_src","JO_src","KW_src","LB_src",
          "OM_src","PS_src","QA_src","SA_src","SY_src","TR_src","YE_src",
          "AE_dest","BH_dest","EG_dest","IQ_dest","IR_dest","JO_dest",
          "KW_dest","LB_dest","OM_dest","PS_dest","QA_dest","SA_dest",
          "SY_dest","TR_dest","YE_dest"]

colors = ["red","blue","orange","green","yellow","purple","crimson","lime",
        "maroon","black","sienna","cyan","olive","dimgray","dodgerblue",
       "navy","deeppink","magenta","orangered","darkcyan",
        "crimson","blue","orange","green","yellow","purple","navy","lime",
        "maroon","deeppink","sienna","cyan","olive","red","dodgerblue",
        "crimson","blue","orange","green","yellow","purple","navy","lime",
        "maroon","deeppink","sienna","cyan","olive","red","dodgerblue"]

def unique(l):
    u = []
    for x in l:
        if x not in u:
            u.append(x)
    if(l[0]==l[len(l)-1]):
        u.append(l[0])
    return u

diction={}
asnames = 'asnames.json'
asndb = 'IPASN.DAT'
db_with_names = pyasn.pyasn(asndb,asnames)
with open('measurements_pickle.txt', 'rb') as filehandle:
    # read the data as binary data stream
    diction = pickle.load(filehandle)

## converting the ip addresses to countries    
ip_to_country = []
for couple, traceroutes in diction.items():
    listOfLists = []
    for traceroute in traceroutes:
        liste=[]
        liste.append(couple[1])
        for ip in traceroute:
            asn, prefix = db_with_names.lookup(ip)
            rec = db_with_names.get_as_name(asn)
            if rec is not None:
                owner_country = rec.split(",")
                liste.append(owner_country[1][1:])
        liste.append(couple[2])
        listOfLists.append(liste)
    ip_to_country.append(listOfLists)

## filtering menog countries except for source and destination
traceroutes = []
for traceroute in ip_to_country:
    t = []
    for trace in traceroute:
        i = 1
        l = []
        l.append(trace[0]+"_src")
        while(i<len(trace)-1):
            if(trace[i] not in menog):
                if(trace[i] == "Russia"):
                    l.append("RU")
                elif(trace[i] == "15123 Maroussi"):
                    l.append("GR")
                else:
                    l.append(trace[i])
            i+=1
        l.append(trace[len(trace)-1]+"_dest")
        p = unique(l)
        if(p not in t):
            t.append(p)
    traceroutes.append(t)

## adapting the results to the diagram input
couples = {}
for trace in traceroutes:
    for traceroute in trace:
        long = len(traceroute)
        if(country=="ALL"):
            t = True
        else:
            t = traceroute[0]==country+"_src"
        if(t):
            i = 1
            while(i<long):
                couple = (labels.index(traceroute[i-1]),labels.index(traceroute[i]))
                d = (traceroute[i-1],traceroute[i])
                if(couple in couples.keys()):
                    couples[couple]+=1
                else:
                    couples[couple]=1
                i+=1

s = []
t = []
v = []

for couple,val in couples.items():
    s.append(couple[0])
    t.append(couple[1])
    v.append(val)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = labels,
      color = colors
    ),
    link = dict(
      source = s,  
      target = t,
      value = v ))])

fig.update_layout(title_text="Menog Sankey Diagram", font_size=10)
fig.show()
