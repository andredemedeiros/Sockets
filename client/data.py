from time import sleep
import subprocess

def get_cpu_data():
    path = "/proc/stat"
    lines = []
    with open(path, "r") as f:
        for line in f.read().split("\n"):
            if "cpu" in line:
                lines.append(line)

    n = len(lines)-1
    cpus = [[int(i) for i in l.split()[1:]]for l in lines]   
    return cpus

def get_cpu_per():
    data1 = get_cpu_data()
    sleep(1) 
    data2 = get_cpu_data()
    diff = data1.copy()
    for i in range(0,len(data1)):
        for j in range(0, len(data1[1])):
            diff[i][j] = data2[i][j] -  data1[i][j]
    cpu_per = [ (sum(l)-l[3])/sum(l)*100 for l in diff]
    return cpu_per

def get_mem():
    res = subprocess.run(["free"],
                         stdout=subprocess.PIPE) \
                         .stdout.decode("utf-8") \
                         .split("\n")[1].split()[1:4]
    return [int(i) for i in res]

def get_mem_per():
    total, used, free = get_mem()
    return used/total * 100


