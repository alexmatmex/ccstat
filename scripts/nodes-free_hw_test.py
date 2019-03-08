#!/usr/bin/env /usr/bin/python2.7
import subprocess
import re


def get_nodes_info():
    pbsnodes = subprocess.check_output(["/mnt/rhel-6/huawei/torque/6.0.0/bin/pbsnodes -s bcm-head -a"], shell=True)
    lines = pbsnodes.split("\n")
    i = 0
    nodes = {}
    while (i < len(lines)):
        if (len(lines[i]) > 0 and not lines[i].startswith(" ")):
            nodename = lines[i].strip()
            nodes[nodename] = {}
            i+=1
            while (i < len(lines)):
                s = lines[i].strip().split(" = ")
                i+=1
                if (len(s)==2):
                    nodes[nodename][s[0]] = s[1]
                else:
                    break
        else:
            i+=1
    return nodes

def running_jobs_info():
    pbsnodes = subprocess.check_output(["/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @bcm-head -f"], shell=True)
    lines0 = pbsnodes.split("\n")
    lines = []
    for l in lines0:
        if (l.startswith("\t")):
            lines[-1] = lines[-1] + l[1:]
        else:
            lines.append(l)

    i = 0
    nodes = {}
    while (i < len(lines)):
        if (len(lines[i]) > 0 and lines[i].startswith("Job Id:")):
            nodename = lines[i].lstrip("Job Id:")
            nodes[nodename] = {}
            i+=1
            while (i < len(lines)):
                s = lines[i].strip().split(" = ")
                i+=1
                if (len(s)==2):
                    nodes[nodename][s[0]] = s[1]
                else:
                    break
        else:
            i+=1
    return nodes


def ranges_to_int(r):
    s = r.split(",")
    count = 0
    for x in s:
        t = x.split("-")
        if (len(t)==1):
            count += 1
        else:
            a,b = t
            count += int(b)-int(a)+1
    return count

def get_nodes_load(s):
    loads = {}
    for x in s.split("+"):
        n,r = x.split("/")
        loads[n] = ranges_to_int(r)

    return loads


nodes = get_nodes_info();

jobs = running_jobs_info()

print(jobs)
# print(nodes)

for n in nodes:
    # print(n)
    nodes[n]['total_load'] = 0

for idx in jobs:
    j = jobs[idx]
    if (j['job_state']=="R"):
        loads = get_nodes_load(j['exec_host'])
        for x in loads:
            print(loads[x])
            nodes[x]['total_load'] += loads[x]

for n in sorted(nodes.keys()):
    print "%10s: %2d / %2d" % ( n , nodes[n]['total_load'], int(nodes[n]['np']))

