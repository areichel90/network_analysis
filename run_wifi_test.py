import network_test_linux as wifiTest
from SimpleREST import network_test_post


def post_or_put(payload, route = "http://192.168.1.4:8000/sandbox"):
    device = 'ethernet'

    try:  # try GET of current device, and put (post if try fails)
        endpoint = route+"/"+device
        print(f"Trying PUT: {endpoint}")
        test = network_test_post.put_payload(endpoint=endpoint, payload=payload)
        print(test)
    except:
        pass

    if test == None:
        print("PUT failed. Trying POST")
        response = network_test_post.post_payload(endpoint=route, payload=payload)  
        print(f"REQUEST: {response}")
    




if __name__ == "__main__":

    '''  run wifi test   '''
    wifi_test = wifiTest.run_test("linux")
    test_results = wifiTest.run_test.run_test()
    
    '''  pull results from wifi test  '''
    # test results are indexed in test_results dict by datetime;
    # need to grab the dictionary from test_results by tbe datetime used to set index
    ind = list(test_results)[0]
    test_data = test_results[ind]
    
    print(test_results, "\n")
    print(f'down: {test_data["down"]}\n', 
            f'up: {test_data["up"]}\n', 
            f'device: {test_data["device_ssid"]}\n',
            f'device ip: {test_data["device_ip"]} ')

    '''  post wifi test to server  '''
    route = "http://"+test_data["device_ip"]+":8000/sandbox"#+test_data['device_ip']
    post_or_put(payload=test_results, route=route)