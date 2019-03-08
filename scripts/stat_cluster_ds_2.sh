#!/bin/bash



echo "Cluster DS (Demonstration Stand)" > /root/scripts/user-free_ds.txt
echo "" >> /root/scripts/user-free_ds.txt
/usr/bin/python2.7 /root/scripts/user-free_ds.py &>> /root/scripts/user-free_ds.txt
cp /root/scripts/user-free_ds.txt /var/www/html/
