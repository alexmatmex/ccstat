#!/bin/bash



echo "Cluster SMP" > /root/scripts/nodes-free_smp.html
echo "" >> /root/scripts/nodes-free_smp.html
/usr/bin/python2.7 /root/scripts/nodes-free_smp.py &>> /root/scripts/nodes-free_smp.html
cp /root/scripts/nodes-free_smp.html /var/www/html/
