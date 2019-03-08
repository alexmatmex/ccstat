#!/bin/bash



echo "Cluster Huawei" > /root/scripts/user-free_hw.txt
echo "" >> /root/scripts/user-free_hw.txt
/usr/bin/python2.7 /root/scripts/user-free_hw.py &>> /root/scripts/user-free_hw.txt
cp /root/scripts/user-free_hw.txt /var/www/html/
