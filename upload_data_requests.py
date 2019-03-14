# Using requests.
# The url only for WSN.

import requests
import string

url = "https://140.124.184.213/~/in-cse/cnt-686670342"
def send(mote,packet_tcflow,temperature,humidity,gasValue,gasAlarm):
    payload = '{"m2m:cin": { "cnf": "json", "con": " { \\\"Mote\\\":\\\"'+mote+'\\\", \\\"Priority\\\":\\\"'+str(packet_tcflow)+'\\\",\\\"EnvTemp\\\":\\\"'+str(temperature*0.01)+'\\\",\\\"EnvHumi\\\":\\\"'+str(humidity*0.01)+'\\\",\\\"EnvCO\\\":\\\"'+str(gasValue)+'\\\",\\\"Alarm\\\":\\\"'+str(gasAlarm)+'\\\"  } " } }'
    #payload = "{\"m2m:cin\":\n\t{\n\t\"cnf\": \"json\",\n\t\"con\": \"{Mote:A6F6, EnvTemp:3531, EnvHumi:6085, EnvCO:40, Alarm:0}\"\n\t}\n}"
    headers = {
      'X-M2M-Origin': "admin:admin",
      'Content-Type': "application/json;ty=4"
    }
    try:
        requests.post(url, data=payload, headers=headers, verify=False)
        print mote+" successful upload data to om2m server."
    except:
        print "The data can not pass to OM2M server, Please check the internet."
        pass
