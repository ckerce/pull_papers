
import json
import numpy as np
from matplotlib import pyplot as plt
import re

from sentence_transformers import SentenceTransformer, util
embd_model = SentenceTransformer('all-mpnet-base-v2')

query_embedding = embd_model.encode('How big is London')
passage_embedding = embd_model.encode(['London has 9,787,426 inhabitants at the 2011 census',
                                  'London is known for its finacial district'])

print("Similarity:", util.dot_score(query_embedding, passage_embedding))


def generate_embeddings(filename, embd_model):
   with open(filename,'r') as f:
       for line in f:
           tline = line
   
   dat = json.loads(tline)
   
   N = len(dat)
   M = np.zeros((len(dat), len(dat)))
   
   dat_embeddings = []
   for idx in range(0,N):
       dat_embeddings.append( embd_model.encode( dat[idx]['abstract']))
   return np.array(dat_embeddings)

#for idx in range(0,Ntmp):
#    for iidx in range(idx+1,Ntmp):
#        abs_2_emb = embd_model.encode( dat[iidx]['abstract'] )
#        M[idx,iidx] = util.dot_score( abs_1_emb, abs_2_emb )
#        M[iidx,idx] = M[idx,iidx]


##############################################################################################
#
#
#
##############################################################################################

edb = np.array( dat_embeddings )

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
