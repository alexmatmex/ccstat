#!/bin/bash



echo "Cluster Huawei" > /root/scripts/nodes-free_hw.html
echo "" >> /root/scripts/nodes-free_hw.html
/usr/bin/python2.7 /root/scripts/nodes-free_hw.py &>> /root/scripts/nodes-free_hw.html
cp /root/scripts/nodes-free_hw.html /var/www/html/
