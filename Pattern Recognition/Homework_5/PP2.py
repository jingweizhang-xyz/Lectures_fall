#!/usr/bin/python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

data_file_path = './PP2.data'

def get_samples():
    samples = []
    with open(data_file_path, mode="r") as in_file:
        for line in in_file:
            row = line.split()
            xs = [float(a) for a in row]
            samples.append(xs)
    return samples

if __name__ == '__main__':
    samples = get_samples()
    # print(np.array(samples))
    print("hello") 
