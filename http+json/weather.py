import http.client
import json
conn = http.client.HTTPSConnection("api.apis.guru")

# headers = {
#     'X-RapidAPI-Key': "SIGN-UP-FOR-KEY",
#     'X-RapidAPI-Host': "imdb8.p.rapidapi.com"
# }
def json_check():
    conn.request("GET", "/v2/metrics.json")

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))

    json_load=json.loads(data.decode())
    for i,j in json_load["datasets"][0]["data"].items():
        print(i)

    input_recieved=input("select one provider from above: ")

    if input_recieved in json_load["datasets"][0]["data"]:
        print(json_load["datasets"][0]["data"][input_recieved])
    # else:
    #     print((json_load["datasets"][0]["data"][input_recieved]))

json_check()