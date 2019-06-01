from math import *
import matplotlib.pyplot as plt
import numpy as np

# gaussian function
def f(mu, sigma2, x):
    coefficient = 1.0 / sqrt(2.0 * pi * sigma2)
    exponential = exp(-0.5 * (x-mu) **2 / sigma2)
    return coefficient * exponential

#update function
def update(mean1,var1,mean2,var2):
    new_mean = (var2*mean1 + var1*mean2) / (var2+var1)
    new_var = 1/(1/var2 + 1/var1)
    return [new_mean, new_var]

#the motion update/predict fuction
def predict(mean1,var1,mean2,var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

def smooth(x,window_len=10,window='hanning'):
    s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat':    #moving average
        w = np.ones(window_len,'d')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')
    return y
