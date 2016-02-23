import math

def mean(dat):
    ret = 0.0
    for i in dat:
        ret += i
    return ret/len(dat)

def stdev(dat):
    ret = 0.0
    mu = mean(dat)
    for i in dat:
        ret += (i-mu)*(i-mu)
    return math.sqrt(ret/len(dat))

