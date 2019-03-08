#!/bin/bash



echo "Cluster TP and HP" > /root/scripts/queue-free_tp_hp.txt
echo "" >> /root/scripts/queue-free_tp_hp.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat -q @pbs-tp-new >> /root/scripts/queue-free_tp_hp.txt
echo "" >> /root/scripts/queue-free_tp_hp.txt
echo "" >> /root/scripts/queue-free_tp_hp.txt
echo "Tasks in the queue:" >> /root/scripts/queue-free_tp_hp.txt
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @pbs-tp-new | grep " Q " >> /root/scripts/queue-free_tp_hp.txt
cp /root/scripts/queue-free_tp_hp.txt /var/www/html/
