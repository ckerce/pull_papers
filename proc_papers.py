# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:38:18 2023

@author: ckerc
"""

import numpy as np
from matplotlib import pyplot as plt
import json

###########################################################
#
#  Load the data files
#
###########################################################

jsonfile = 'web_scrape_data/cleaned_human_centered_V3.json'
embdfile = 'web_scrape_data/dat_human_centered_embd_v3.npy'

with open(jsonfile,'r') as f:
    for line in f:
        tline = line
        
dat = json.loads(tline)
dat_embeddings = np.load(embdfile)

###########################################################
#
# Helper functions 
#
###########################################################

def search_db( sentence_to_match, score=0.7, dat=dat, edb=dat_embeddings):
   query_embedding = embd_model.encode( sentence_to_match )
   search_result = edb @ np.array(query_embedding)
   plt.hist(search_result,100)
   for idx in np.nonzero( search_result > score )[0]:
       print(dat[idx]['title'], ' :: ' ,  re.sub("\n", " ", html2text.html2text(dat[idx]['abstract'])), '\n\n')

def search_db_top_k( sentence_to_match, top_k=10, dat=dat, edb=dat_embeddings):
   query_embedding = embd_model.encode( sentence_to_match )
   search_result = edb @ np.array(query_embedding)
   idxs = np.argsort(search_result)
   N = len(idxs)
   for idx in idxs[-top_k:]:
       print(dat[idx]['title'], ' :: ' , "score = ", search_result[idx], ' :: ', re.sub("\n", " ", html2text.html2text(dat[idx]['abstract'])), '\n\n')

###########################################################
#
#  Build the similarity matrix M 
#
###########################################################

N = len(dat_embeddings)
M = np.zeros((N,N))

for idx in range(0,N):
    for iidx in range(0,N):
        M[idx, iidx] = np.dot( dat_embeddings[idx], dat_embeddings[iidx])

def visualize(M,eta=0.9, plotsON='True'):
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

  if plotsON:
     plt.figure()
     plt.imshow(QQ)
  
  return QQ  
    

###########################################################
#
#  Do some spectral analysis 
#
###########################################################

a = {'M':[], 't': [], 'sscore': []}
etaStart = 0.5
deta = 0.01

plt.ion()
for idx in range(0, 40):
   t = etaStart + idx*deta
   Mtmp = visualize(M, t , plotsON=False)
   a['M'].append( Mtmp )
   a['t'].append( t    )
   a['sscore'].append( np.sum(np.sum(Mtmp)))

plt.figure()
plt.semilogy(np.array(a['t']), np.array(a['sscore'])/N)
plt.xlabel('Score Threshold')
plt.ylabel('Average Node Degree')
plt.grid('on')

###########################################################
#
#  Run some searches 
#
###########################################################

#M = a['M'][28]
M = a['M'][25]
N = len(M[:,0])

free_for_cluster = np.repeat(True, N)  

clusters = []
for idx in range(0,N):
   if free_for_cluster[idx]:
      tmp = np.nonzero( M[idx,:] )
      for tmpidx in tmp:
         free_for_cluster[tmpidx] = False
      clusters.append( tmp[0] )

cluster_len = [ len(x) for x in clusters]
sorted_clusters = [clusters[idx] for idx in np.argsort( cluster_len)]
plt.plot(np.sort(cluster_len))

def print_clusters( tmp, myIDX ):
   N_clusters = len(tmp)
   cur_cluster = tmp[N_clusters-myIDX-1]
   for idx in cur_cluster:
      print( dat[idx]['title'] + '\n>>   ' + dat[idx]['abstract'] ) 




###########################################################
#
#  Take a look at some cluster properties 
#
###########################################################

for idx in range(35,10,-1):
   M = a['M'][idx]
   N = len(M[:,0])
  
   free_for_cluster = np.repeat(True, N)
  
   clusters = []
   for idx in range(0,N):
     if free_for_cluster[idx]:
        tmp = np.nonzero( M[idx,:] )
        for tmpidx in tmp:
           free_for_cluster[tmpidx] = False
        clusters.append( tmp[0] )
  
   cluster_len = [ len(x) for x in clusters]
   sorted_clusters = [clusters[idx] for idx in np.argsort( cluster_len)]
   plt.semilogy(np.sort(cluster_len))
   plt.grid('on')



