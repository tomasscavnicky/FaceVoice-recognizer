# -*- coding: utf-8 -*-
"""
Example of use Hopfield Recurrent network
=========================================

Task: Recognition of letters 

"""

import numpy as np
import neurolab as nl
from neurolab.tool import simhop

# N E R O
target =  [[1,0,0,0,1,
           1,1,0,0,1,
           1,0,1,0,1,
           1,0,0,1,1,
           1,0,0,0,1],
          [1,1,1,1,1,
           1,0,0,0,0,
           1,1,1,1,1,
           1,0,0,0,0,
           1,1,1,1,1],
          [1,1,1,1,0,
           1,0,0,0,1,
           1,1,1,1,0,
           1,0,0,1,0,
           1,0,0,0,1],
          [0,1,1,1,0,
           1,0,0,0,1,
           1,0,0,0,1,
           1,0,0,0,1,
           0,1,1,1,0]]

chars = ['N', 'E', 'R', 'O']
target = np.asfarray(target)
target[target == 0] = -1

# Create and train network
net = nl.net.newhop(target)

output, ows = simhop(net, target)
print "Test on train samples:"
for i in range(len(target)): 
    print chars[i], (output[i] == target[i]).all(), 'Sim. steps',len(ows[i])

print "\nTest on defaced N:"
test =np.asfarray([0,0,0,0,0,
                   1,1,0,0,1,
                   1,1,0,0,1,
                   1,0,1,1,1,
                   0,0,0,1,1])
test[test==0] = -1
out, ows = simhop(net, [test])
print (out[0] == target[0]).all(), 'Sim. steps',len(ows[0])