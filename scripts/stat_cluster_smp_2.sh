#!/bin/bash



echo "Cluster SMP" > /root/scripts/user-free_smp.txt
echo "" >> /root/scripts/user-free_smp.txt
/usr/bin/python2.7 /root/scripts/user-free_smp.py &>> /root/scripts/user-free_smp.txt
cp /root/scripts/user-free_smp.txt /var/www/html/
