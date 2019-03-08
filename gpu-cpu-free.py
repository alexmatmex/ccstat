#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import subprocess
import re

host = "bionmr-storage"
#color_red = '\033[0;31m'
#color_none = '\033[0m'
#color_blue = '\033[0;34m'
#color_yellow = '\033[0;33m'
#color_green = '\033[0;32m'

def get_nodes_info():
    pbsnodes = subprocess.check_output(["pbsnodes", "-a"])
    lines = pbsnodes.split("\n")
    i = 0
    nodes = {}
    while (i < len(lines)):
        if (len(lines[i]) > 0 and not lines[i].startswith(" ")):
            nodename = lines[i].strip()
            nodes[nodename] = {}
            i += 1
            while (i < len(lines)):
                s = lines[i].strip().split(" = ")
                i += 1
                if (len(s) == 2):
                    nodes[nodename][s[0]] = s[1]
                else:
                    break
        else:
            i += 1
    return nodes


def running_jobs_info():
    pbsnodes = subprocess.check_output(["qstat", "-f"])
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
            i += 1
            while (i < len(lines)):
                s = lines[i].strip().split(" = ")
                i += 1
                if (len(s) == 2):
                    nodes[nodename][s[0]] = s[1]
                else:
                    break
        else:
            i += 1
    return nodes


def ranges_to_int(r):
    s = r.split(",")
    count = 0
    for x in s:
        t = x.split("-")
        if (len(t) == 1):
            count += 1
        else:
            a, b = t
            count += int(b) - int(a) + 1
    return count


def get_nodes_load(s):
    loads = {}
    for x in s.split("+"):
        n, r = x.split("/")
        loads[n] = ranges_to_int(r)

    return loads

def get_gpu_info():
    pass


def get_nodes_info_with_load():
    nodes = get_nodes_info()

    jobs = running_jobs_info()

    for n in nodes:
        nodes[n]['cpu_load'] = 0
        if 'gpus' not in nodes[n]:
            nodes[n]['gpus']='0'
        if 'gpu_status' in nodes[n]:
            nodes[n]['gpu_load'] = int(nodes[n]['gpus']) - nodes[n]['gpu_status'].count("Unallocated")
        else:
            nodes[n]['gpu_load'] = int(nodes[n]['gpus'])

    for idx in jobs:
        j = jobs[idx]
        if (j['job_state'] == "R"):
            loads = get_nodes_load(j['exec_host'])
            for x in loads:
                nodes[x]['cpu_load'] += loads[x]

    for node in nodes.values():
        node['gpu'] = {}
        node['gpu_common'] = {}
        node['status_dict'] = {}
        if 'gpu_status' in node:
            for gpu_info in node['gpu_status'].split(","):
                gpu_id = re.search(r'^gpu\[(\d+)\]=', gpu_info)
                if gpu_id:
                    gpuid = int(gpu_id.group(1))
                    node['gpu'][gpuid] = {}
                    options = re.sub(r'^gpu\[(\d+)\]=', "", gpu_info)
                    for option in options.split(";"):
                        m = re.match("^(\w+)=(.*)$", option)
                        if m:
                            node['gpu'][gpuid][m.group(1)] = m.group(2)
                        else:
                            print "Unknown gpu option format:", option

                else:
                    m = re.match("^(\w+)=(.*)$", gpu_info)
                    if m:
                        node['gpu_common'][m.group(1)] = m.group(2)
                    else:
                        print "Unknown gpu option format:", gpu_info
        if 'status' in node:
            for info in node['status'].split(","):
                m = re.match("^(\w+)=(.*)$", info)
                if m:
                    node['status_dict'][m.group(1)] = m.group(2)
                else:
                    pass;
                    #print "Unknown option format:", info

    return nodes


def subs_or_call(obj, arg):
    try:
        if hasattr(arg, '__call__'):
            return arg(obj)
        else:
            return obj[arg]
    except:
        return "n/a"

def print_node_table(**kwargs):
    nodes = get_nodes_info_with_load()
    from tabulate import tabulate


    return nodes


def subs_or_call(obj, arg):
    try:
        if hasattr(arg, '__call__'):
            return arg(obj)
        else:
            return obj[arg]
    except:
        return "n/a"

def print_node_table(**kwargs):
    nodes = get_nodes_info_with_load()
    from tabulate import tabulate


    print tabulate(
        [
            [ nname ] + [ subs_or_call(nodes[nname],kwargs[h]) for h in sorted(kwargs.keys())] for nname in sorted(nodes.keys())
        ],
        headers=["node"]+sorted(kwargs.keys()),
        tablefmt="orgtbl",
        stralign="center",
        numalign="center"
    )

def colorized_ratio(left, right):
        ratio = "%2d / %2d"%(left,right)
        if left==right:
                return ratio
        elif left > 0.5*right:
                return ratio
        else:
                return ratio

print_node_table(
    cpu_usage =  lambda n: colorized_ratio(int(n['cpu_load']),int(n['np'])),
    gpu_usage =  lambda n: colorized_ratio(int(n['gpu_load']),int(n['gpus'])),
    node_feature =  "properties",
    gpu_temp =   lambda n: ", ".join(n['gpu'][g]['gpu_temperature'].rstrip(" C") for g in sorted(n['gpu'].keys())),
    gpu_memory =   lambda n: ", ".join(n['gpu'][g]['gpu_memory_utilization'] for g in sorted(n['gpu'].keys())),
    gpu_fan =   lambda n: ", ".join("%3s"%subs_or_call(n['gpu'][g],'gpu_fan_speed') for g in sorted(n['gpu'].keys())),
    node_state = "state",
    ram_usage = lambda n: colorized_ratio((int(n["status_dict"]['totmem'].replace('kb',''))-int(n["status_dict"]['availmem'].replace('kb','')))/1024,int(n["status_dict"]['totmem'].replace('kb',''))/1024)
)
