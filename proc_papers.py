# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:38:18 2023

@author: ckerc
"""

import numpy as np
from matplotlib import pyplot as plt
import json


with open('cleaned_adversarialML_V3.json','r') as f:
    for line in f:
        tline = line
        
dat = json.loads(tline)

dat_embeddings = np.load('dat_embd_v3.npy')

N = len(dat_embeddings)
M = np.zeros((N,N))

for idx in range(0,N):
    for iidx in range(0,N):
        M[idx, iidx] = np.dot( dat_embeddings[idx], dat_embeddings[iidx])

def visualize(M,eta=0.9):
  Q = M.copy()
  N = len(M[:,0])
  
  for idx in range(0,N):
     tmp = Q[:,idx]
     stmp = np.sort(tmp)
     Q[ tmp < eta*stmp[N-1], idx] = 0
    
  for idx in range(0,N):
     tmp = Q[idx,:]
     stmp = np.sort(tmp)
     Q[idx,tmp < eta*stmp[N-1]] = 0
    

  QQ = Q.copy()
  QQ[ QQ > 0] = 1
  for idx in range(0,50):
     QQ = QQ@QQ
     QQ[ QQ > 0 ] = 1
  plt.figure()
  plt.imshow(QQ)
  
  return QQ  
    

a83 = visualize(M,0.83)
a84 = visualize(M,0.84)
a85 = visualize(M,0.85)
a86 = visualize(M,0.86)
a87 = visualize(M,0.87)
a88 = visualize(M,0.88)


plt.figure()
plt.imshow( np.abs( a83-a84) )
plt.figure()
plt.imshow( np.abs( a84-a85) )
plt.figure()
plt.imshow( np.abs( a85-a86) )
plt.figure()
plt.imshow( np.abs( a86-a87) )
plt.figure()
plt.imshow( np.abs( a87-a88) )


'''  This does not help
def visualize_weak(M,eta=0.9):
  Q = M.copy()
  Q = Q*Q*Q*Q
  N = len(M[:,0])
  
  for idx in range(0,N):
     tmp = Q[:,idx]
     stmp = np.sort(tmp)
     Q[ tmp < eta*stmp[N-1], idx] = 0
    
  for idx in range(0,N):
     tmp = Q[idx,:]
     stmp = np.sort(tmp)
     Q[idx,tmp < eta*stmp[N-1]] = 0
    

  QQ = Q.copy()
  QQ[ QQ > 0] = 1
  for idx in range(0,50):
     QQ = QQ@QQ
     QQ[ QQ > 0 ] = 1
  plt.figure()
  plt.imshow(QQ)
  
  return QQ 
'''