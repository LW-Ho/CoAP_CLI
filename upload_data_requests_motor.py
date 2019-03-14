# Using requests.
# The url only for motor.

import requests
import string

url = "https://140.124.184.213/~/in-cse/cnt-706018400"
def send(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23, data24, data25, data26, data27, data28, data29, data30, data31, data32):
    payload = '{"m2m:cin": { "cnf": "json", "con": "['+str(data1*0.0001)+', '+str(data2*0.0001)+', '+str(data3*0.0001)+', '+str(data4*0.0001)+', '+str(data5*0.0001)+', '+str(data6*0.0001)+', '+str(data7*0.0001)+', '+str(data8*0.0001)+', '+str(data9*0.0001)+', '+str(data10*0.0001)+', '+str(data11*0.0001)+', '+str(data12*0.0001)+', '+str(data13*0.0001)+', '+str(data14*0.0001)+', '+str(data15*0.0001)+', '+str(data16*0.0001)+', '+str(data17*0.0001)+', '+str(data18*0.0001)+', '+str(data19*0.0001)+', '+str(data20*0.0001)+', '+str(data21*0.0001)+', '+str(data22*0.0001)+', '+str(data23*0.0001)+', '+str(data24*0.0001)+', '+str(data25*0.0001)+', '+str(data26*0.0001)+', '+str(data27*0.0001)+', '+str(data28*0.0001)+', '+str(data29*0.0001)+', '+str(data30*0.0001)+', '+str(data31*0.0001)+', '+str(data32*0.0001)+']" } }'

    headers = { 'X-M2M-Origin': "admin:admin", 'Content-Type': "application/json;ty=4", 'Connection': "close" }
    try:
        if data32 == 0:
            print "The data incomplete, wating next get. "
        else:
            requests.packages.urllib3.disable_warnings()
            requests.request("POST", url, data=payload, headers=headers, verify=False)
            print "Successful upload data to om2m server."
    except:
        print "The data can not pass to OM2M server, Please check the internet."
        pass