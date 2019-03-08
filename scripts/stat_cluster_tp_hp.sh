#!/bin/bash



echo "Cluster TP and HP" > /root/scripts/nodes-free_tp_hp.html
echo "" >> /root/scripts/nodes-free_tp_hp.html
/usr/bin/python2.7 /root/scripts/nodes-free_tp_hp.py &>> /root/scripts/nodes-free_tp_hp.html
cp /root/scripts/nodes-free_tp_hp.html /var/www/html/
