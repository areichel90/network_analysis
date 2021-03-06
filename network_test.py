
import pandas as pd
import numpy as np
import netifaces as ni
import datetime, subprocess, socket
import speedtest, sys, os, time

class run_test:
    def __init__(self, os_):
        print(os_)

    def run_test(test_count=5):
        bps_mbps = 1000**2
        print("\n--- Running WiFi Test ---")

        ''' try macOS cli commands first, then try linux cli if necessary '''
        try:
            ip = subprocess.check_output('ipconfig getifaddr en0', shell=True).decode('UTF-8')#.split('\n')[0]
            device_ip = str(ip.split('\n')[0])
        except KeyError:
            # test wifi interface - wlan0
            print('trying wifi')
            device_ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        except:
            # if wifi is not connected or turned off, test ethernet
            print('trying ethernet')
            device_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        print(device_ip)
    
        device_ssid = run_test.get_ssid()['SSID']
        print(f"{device_ssid}:  {device_ip}")

        servers, run_dict=[], {}
        try:
            wifi = speedtest.Speedtest()
            #wifi.get_servers(servers)
            wifi.get_best_server()
            
            for i in range(test_count):
                time_now = datetime.datetime.today()
                run_time = f"{time_now.year}{time_now.month}{time_now.day}_{time_now.hour}:{time_now.minute}:{time_now.second}"

                download = wifi.download()/(bps_mbps)
                upload = wifi.upload()/(bps_mbps)
                test_results = {"down":round(download,2),
                                    "up":round(upload,2),
                                    "device_ssid":device_ssid,
                                    "device_ip":device_ip}
                run_dict[run_time] = test_results

                print (f"{run_time}:\t{test_results}")

        except:
            time_now = datetime.datetime.today()
            run_time = f"{time_now.year}{time_now.month}{time_now.day}_{time_now.hour}:{time_now.minute}:{time_now.second}"
            print(f"Test Failure: {run_time}")

            test_results = {"down":np.nan,
                            "up":np.nan,
                            "device_ssid":"None",
                            "device_ip":"None"}
            run_dict[run_time] = test_results
        return run_dict

    def get_ssid():
        try:
            ssid=subprocess.check_output("airport -I", shell=True)
            ssid = ssid.decode('UTF-8')
            params_dict = {}
            for i in ssid.split("\n"):
                i = i.strip(' ')
                i_parts= i.split(':')
                params_dict[i_parts[0]] = ''.join((i_parts[1:]))
        except:
            ssid = subprocess.check_output('iwgetid', shell=True) 
            ssid = ssid.decode('UTF-8')
            ssid = ssid.split('ESSID:')[1].split('\n')[0]
            params_dict={'SSID':ssid}
        
        return params_dict


    def restuls_to_df(run_dict):
        df = pd.DataFrame.from_dict(run_dict, orient='index')
        return df


def write_to_file(file_path:str, df_out:pd.DataFrame):
    # try to load existing file
    try:
        df = pd.read_csv(file_path, index_col=0)
        to_concat = [df, df_out]
        df_out = pd.concat(to_concat)
    except:    
        print("Something went wrong")

    # TODO: Add check for file size to avoid creating a massive, singular file

    # write file to file_path
    print(f"Writing dataframe to {file_path}")
    df_out.to_csv(file_path)


if __name__ == "__main__":
    test_count = 1*10**3
    sample_rate = 5*60  # tests run per seconds (max)
    os_ = 'mac'

    run_count, last_run = 0, datetime.datetime.now()
    while run_count < test_count:
        last_run = datetime.datetime.now()
        #initialize run_test
        wifi_test = run_test(os_)
        results = run_test.run_test()
        res_df = run_test.restuls_to_df(results)

        print(res_df)

        # write file to csv
        write_to_file("wifi_test.csv", res_df)

        # TODO: Add check for results std dev, re-run test if above a threshold

        run_count += 1
        time_now = datetime.datetime.now()
        time_delta = time_now - last_run
        while time_delta.total_seconds() < sample_rate:
            print(f"waiting... {round(time_delta.total_seconds() - sample_rate,2)} sec.")
            time.sleep(30)
            time_now = datetime.datetime.now()
            time_delta = time_now - last_run
