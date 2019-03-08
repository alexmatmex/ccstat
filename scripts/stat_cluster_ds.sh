#!/bin/bash



echo "Cluster DS (Demonstration Stand)" > /root/scripts/nodes-free_ds.html
echo "" >> /root/scripts/nodes-free_ds.html
/usr/bin/python2.7 /root/scripts/nodes-free_ds.py &>> /root/scripts/nodes-free_ds.html
cp /root/scripts/nodes-free_ds.html /var/www/html/
