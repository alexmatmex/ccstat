#!/bin/bash



echo "Cluster Huawei" > /root/scripts/queue-free_hw.txt
echo "" >> /root/scripts/queue-free_hw.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat -q @bcm-head >> /root/scripts/queue-free_hw.txt
echo "" >> /root/scripts/queue-free_hw.txt
echo "" >> /root/scripts/queue-free_hw.txt
echo "Tasks in the queue:" >> /root/scripts/queue-free_hw.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @bcm-head | grep " Q " >> /root/scripts/queue-free_hw.txt
cp /root/scripts/queue-free_hw.txt /var/www/html/
