#!/bin/bash



echo "Cluster TP and HP" > /root/scripts/user-free_tp_hp.txt
echo "" >> /root/scripts/user-free_tp_hp.txt
/usr/bin/python2.7 /root/scripts/user-free_tp_hp.py &>> /root/scripts/user-free_tp_hp.txt
cp /root/scripts/user-free_tp_hp.txt /var/www/html/
