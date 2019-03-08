#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import subprocess
import re

host = "bionmr"
#athost = ["ssh", host]
athost = []

def get_queues_info():
    pbsnodes = subprocess.check_output( athost + ["/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @bcm-head -Q -f"], shell=True)
    lines = pbsnodes.replace("\n\t","").split("\n")
    i = 0
    nodes = {}
    while (i < len(lines)):
        if (len(lines[i]) > 0 and not lines[i].startswith(" ")):
            nodename = lines[i].replace("Queue: ","")
#            print "`%s`"%nodename, lines[i]
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


queues = get_queues_info()

def get_nodes_info():
    pbsnodes = subprocess.check_output(athost + ["/mnt/rhel-6/huawei/torque/6.0.0/bin/pbsnodes -s bcm-head -a"], shell=True)
    lines = pbsnodes.replace("\n\t","").split("\n")
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
    pbsnodes = subprocess.check_output( athost + [ "/mnt/rhel-6/huawei/torque/6.0.0/bin/qstat @bcm-head -f"], shell=True)
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
            nodename = lines[i].replace("Job Id:","")
            nodes[nodename] = {"id": nodename[:nodename.find('.')] }
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
        nodes[n]['jobs_info'] = []

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
                nodes[x]['jobs_info'].append(j)

    for node in nodes.values():
        node['gpu'] = {}
        node['gpu_common'] = {}
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

    return nodes


def subs_or_call(obj, arg):
    try:
        if hasattr(arg, '__call__'):
            return arg(obj)
        else:
            return obj[arg]
    except:
        return "n/a"

def duration_human(duration):
    h,m,s = map(int,duration.split(":"))
    result = ""
    d = h // 24
    h -= d*24
    return "%2dd %02d:%02d"%(d,h,m)

def get_default_time(job):
    q = queues[job['queue']]
    if 'resources_default.walltime' in q:
        return q['resources_default.walltime']
    else:
        return q['resources_max.walltime']

def get_walltime_limit(job):
    if 'Resource_List.walltime' in job:
        return job['Resource_List.walltime']
    else:
        return get_default_time(job)

def get_walltime(job):
    if 'resources_used.walltime' in job:
        used_time = job['resources_used.walltime']
    else:
        used_time = "00:00:00"

    return "%s / %s" % ( duration_human(used_time)
                         , duration_human(get_walltime_limit(job)))

def duration_to_number(duration):
    h, m, s = map(int, duration.split(":"))
    return ((h*60)+m)*60+s

def get_rest_walltime_number(job):
    if 'resources_used.walltime' in job:
        used_time = job['resources_used.walltime']
    else:
        used_time = "00:00:00"
    return duration_to_number(get_walltime_limit(job)) - duration_to_number(used_time)

def number_to_duration(seconds):
    s = seconds % 60
    m = ( seconds // 60) % 60
    h = seconds // 3600
    return "%02d:%02d:%02d"%(h,m,s)

def print_node_table(**kwargs):
    nodes = get_nodes_info_with_load()
    from tabulate import tabulate

    headers = ["node", "user", "job name", 'job id', "queue", "left walltime" ]
    spacer = "-"*10
    table = []
    for node_name in sorted(nodes.keys()):
        node = nodes[node_name]
        node_jobs = node['jobs_info']

        for job in reversed(sorted(node_jobs, key = lambda xxxx: get_rest_walltime_number(xxxx))):
            table.append([
                node_name,
                job['Job_Owner'][:job['Job_Owner'].find('@')],
                job['Job_Name'],
                job['id'],
                job['queue'],
                duration_human(number_to_duration(get_rest_walltime_number(job)))
            ])

        if table[-1:] != [[spacer]*len(headers)]:
            table.append([spacer]*len(headers))

    print tabulate(
        table,
        headers=headers,
        tablefmt="orgtbl",
        stralign="center",
        numalign="center"
    )

    # print nodes


print_node_table()
