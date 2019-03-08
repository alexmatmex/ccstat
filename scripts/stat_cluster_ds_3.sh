#!/bin/bash



echo "Cluster DS (Demonstration Stand)" > /root/scripts/queue-free_ds.txt
echo "" >> /root/scripts/queue-free_ds.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat -q @pbs-ds >> /root/scripts/queue-free_ds.txt
echo "" >> /root/scripts/queue-free_ds.txt
echo "" >> /root/scripts/queue-free_ds.txt
echo "Tasks in the queue:" >> /root/scripts/queue-free_ds.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @pbs-ds | grep " Q " >> /root/scripts/queue-free_ds.txt
cp /root/scripts/queue-free_ds.txt /var/www/html/
