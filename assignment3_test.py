import requests
import json


URL = "http://127.0.0.1:8000"


##test 1 
##Execute three POST /dishes requests using the dishes, “orange”, “spaghetti”, and “apple pie”. 
##The test is successful* if (i) all 3 requests return unique IDs (none of the IDs are the same),
##and (ii) the return status code from each POST request is 201.
def test_post_3_dishes():
    headers = {"content-type":"application/json"}

    payload_1 = json.dumps({"name": "orange"})
    payload_2 = json.dumps({"name": "spaghetti"})
    payload_3 = json.dumps({"name": "apple pie"})

    response_1 = requests.request("POST", URL+"/dishes", headers=headers, data=payload_1)
    response_2 = requests.request("POST", URL+"/dishes", headers=headers, data=payload_2)
    response_3 = requests.request("POST", URL+"/dishes", headers=headers, data=payload_3)

    check_1 = ((response_1.json() != response_2.json()) and (response_1.json() != response_3.json()) and (response_2.json() != response_3.json()))
    check_2 = (response_1.status_code == response_2.status_code == response_3.status_code == 201)

    assert (check_1 and check_2) == True


##test 2
##Execute a GET dishes/<orange-ID> request, using the ID of the orange dish. 
##The test is successful if (i) the sodium field of the return JSON object is between .9 and 1.1 
##and (ii) the return status code from the request is 200.

def test_get_dishes_on_id():
    pass

##test3
##Execute a GET /dishes request. The test is successful if (i) the returned JSON object has 3 embedded JSON objects (dishes), 
##and (ii) the return status code from the GET request is 200.

def test_get_dishes():
    payload =json.dumps({})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", URL+"/dishes" ,headers=headers, data=payload)
    num_keys = len(response.json().keys())
    assert ((num_keys == 3) and (response.status_code == 200))


##test 4
##Execute a POST /dishes request supplying the dish name “blah”. The test is successful if 
##(i) the return value is -3, and (ii) the return code is 404 or 400 or 422.

def test_post_bad_dish():
    headers = {"content-type":"application/json"}
    payload = json.dumps({"name": "blah"})
    response = requests.request("POST", URL+"/dishes", headers=headers, data=payload)

    assert (response.text.rstrip('\n') == "-3") and (response.status_code == 404 or response.status_code == 400 or response.status_code == 422) 


##test 5
##Perform a POST dishes request with the dish name “orange”. 
##The test is successful if (i) the return value is -2 (same dish name as existing dish), and
##(ii) the return status code is 400 or 404 or 422

def test_post_orange():
    headers = {"content-type":"application/json"}
    payload = json.dumps({"name": "orange"})
    response = requests.request("POST", URL+"/dishes", headers=headers, data=payload)

    assert (response.text.rstrip('\n') == "-2" and (response.status_code == 404 or response.status_code == 400 or response.status_code == 422))


##test 6
##Perform a POST /meals request specifying that the meal name is “delicious”,
##and that it contains an “orange” for the appetizer, “spaghetti” for the main, and “apple pie” for the dessert 
##(note you will need to use their dish IDs). The test is
##successful if (i) the returned ID > 0 and (ii) the return status code is 201.

def test_post_meal():
    headers = {"content-type":"application/json"}
    payload = json.dumps({"name": "delicious", "appetizer": 1, "main": 2, "dessert": 3})
    response = requests.request("POST", URL+"/meals", headers=headers, data=payload)

    assert ((int(response.text) > 0) and (response.status_code == 201))
    

##test 7
##Perform a GET /meals request. The test is successful if (i) the returned JSON object has 1 meal, 
##(ii) the calories of that meal is between 400 and 500, and (iii)
##the return status code from the GET request is 200.

def test_get_meals():
    headers = {"content-type":"application/json"}
    payload = json.dumps({})
    response = requests.request("GET", URL+"/meals", headers=headers, data=payload)

    num_keys = len(response.json().keys())
    assert ((num_keys == 1) and ( 400 < response.json()["1"]["cal"] < 500) and (response.status_code == 200))

##test 8
##Perform a POST /meals request as in test 6 with the same meal name (and courses can be the same or different). 
##The test is successful if (i) the code is -2
##(same meal name as existing meal) and, and (ii) the return status code from the
##request is 400 or 422.

def test_post_same_meal():
    headers = {"content-type":"application/json"}
    payload = json.dumps({"name": "delicious", "appetizer": 1, "main": 2, "dessert": 3})
    response = requests.request("POST", URL+"/meals", headers=headers, data=payload)

    assert ((int(response.text) == -2) and (response.status_code == 400 or response.status_code == 422))

    