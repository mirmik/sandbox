#!/usr/bin/env python3

import rlview
import numpy as np

part1 = rlview.rlview(open("part1.rlamu", "rb"))
part2 = rlview.rlview(open("part2.rlamu", "rb"))
part3 = rlview.rlview(open("part3.rlamu", "rb"))

data1 = part1.get_array()
data2 = part2.get_array()
data3 = part3.get_array()

#0-6
#1-4
#0-3

print(part1.get_ncoords())
print(part2.get_ncoords())
print(part3.get_ncoords())

arr1 = part1.get_array()[:,0:7,:,:]
arr2 = part2.get_array()[:,1:5,:,:]
arr3 = part3.get_array()[:,0:4,:,:]

arr = np.concatenate((arr1, arr2, arr3), axis=1)

print(arr1.shape)
print(arr2.shape)
print(arr3.shape)
print(arr.shape)

rlview.form_file_with_proto(proto=part1, tgt="complete.rlamu", array=arr)

#print(data1[2][9])
#print(data3[2][5])
