#!/bin/bash
echo "------------STATISCTICS on cluster HUAWEI!------------------" > /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "Total number of cores and free cores on the cluster:" >> /var/www/html/hwstat
/mnt/rhel-6/submit/hcluster/status-hw -p >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "Total number of cores and use cores on the cluster:" >> /var/www/html/hwstat
echo "(name_node: use_cores/total_cores)" >> /var/www/html/hwstat
cat /root/nodes-stat  >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "------------MOAB statistics----------------" >> /var/www/html/hwstat
cat /home/amalevich/showq.dat  >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "------------PBS Torque statistics----------------" >> /var/www/html/hwstat
#echo "Total number of cores and free cores on the cluster:" >> /var/www/html/hwstat
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat -n >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
echo "" >> /var/www/html/hwstat
/mnt/rhel-6/submit/hcluster/nodes-free.sh >> /var/www/html/hwstat
#echo "----------------------------------------------------------" >> /var/www/html/hwstat
#echo "Total number of cores and use cores on the cluster:" >> /var/www/html/hwstat
#echo "name_node: use_cores/total_cores" >> /var/www/html/hwstat
#/root/nodes-free.py >> /var/www/html/hwstat
