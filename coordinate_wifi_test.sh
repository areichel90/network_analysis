#!/bin/bash

python network_test_linux.py

testfile="/media/usb/network_test/wifi_test.csv"
while true; do
    if [ -e "$testfile" ]
    then
        echo -e "\nUSB drive found... Copying results to drive"
        sudo cp -f wifi_test.csv /media/usb0/network_test/
    fi

    count=1
    until [ $count -gt 10 ]
    do
        echo -e "\twaiting..."
        sleep 60
        ((count=count+1))
    done
done 
