#!/bin/bash



echo "Cluster SMP" > /root/scripts/queue-free_smp.txt
echo "" >> /root/scripts/queue-free_smp.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat -q @pbs-smp >> /root/scripts/queue-free_smp.txt
echo "" >> /root/scripts/queue-free_smp.txt
echo "" >> /root/scripts/queue-free_smp.txt
echo "Tasks in the queue:" >> /root/scripts/queue-free_smp.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @pbs-smp | grep " Q " >> /root/scripts/queue-free_smp.txt
cp /root/scripts/queue-free_smp.txt /var/www/html/
