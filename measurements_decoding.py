import os
import json
import pickle

meas = "\menog-internet-study-master\menog-rtt-measure\measurements\data"
old_dir=str(os.getcwd())+"\measurements_pickle.txt"
directory=str(os.getcwd())+meas
os.chdir(directory)
dictio_ips = {}

for root,direc,files in os.walk(directory, topdown = True):
    if len(files) > 0:
        List = []
        for file in files:
            fileDirectory = root + os.path.sep + file
            with open(fileDirectory,'r') as f:
                array = json.load(f)
            for item in array :
                if(item['msm_name'] != "Traceroute"):
                    continue
                parsed_result = item['result']
                subList = []
                for item in parsed_result :
                    if ("result" in item.keys()):
                        tmp = item['result']
                        i = 0
                        while i < len(tmp):
                            if ("from" in tmp[i].keys()):
                                subList.append(tmp[i]['from'])
                                break
                            i+=1
                List.append(subList)
        key=tuple(root.replace(directory,"").split("\\"))
        dictio_ips[key]=List

with open(old_dir, "wb") as fp:
    pickle.dump(dictio_ips, fp)

