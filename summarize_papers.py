

with open('adversarialML.json','r') as f:
   for line in f:
       tline = line

dat = json.loads( tline )

import html2text

instruction = "INSTRUCTION: Summarize the following abstract in 300 words or less, retaining as much of the original as possible while highlighting the innovations called out by the authors: \n\n"

MAX_CHAR = 3092+250
count = 0
total = len(dat)
FIX_ABSTRACT='True'
bad_abstracts = []
for d in dat:
    if d['abstract']:
       # The text processing agent's task
       inp_str = instruction + "TITLE: " + d['title'] + "\nABSTRACT: " + html2text.html2text(d['abstract']) + "\nSUMMARY: " 

       # Check for overflow to the model, and give a warning.  LLama2 has a 4092 context window
       cur_len = min(len(inp_str), 3500)
       if len(inp_str) > MAX_CHAR:
           print('LONG ABSTRACT: ' + d['title'])

       # Trim input to context window and execute the task.
       clip_str = inp_str[0:cur_len]

       abstract_pass = 0
       while FIX_ABSTRACT:
           ans = pipe(clip_str, max_length=cur_len, eos_token_id=tokenizer.eos_token_id)

           potential_abstract = ans[0]['generated_text'][len(clip_str)+1:].strip('\n')
           check_instruction = "Examine the following text and assess whether or not it needs to be adjusted for grammer or extraneous characters. Return either a YES or NO answer with absolutely no other information.  Your reply should either be 'ANSWER: YES' or 'ANSWER: NO'."
           inp_check = check_instruction + potential_abstract
           assessment = pipe( inp_check, max_length = len(inp_check)+15, eos_token_id=tokenizer.eos_token_id) 
           yesno = assessment[0]['generated_text'][len(inp_check)+1:]

           # If new abstract looks good, replace the original abstract with the new abstract. Else do nothing.
           if not re.search(r'\bNO\b', yesno):
              d['abstract'] = potential_abstract
              print(str(count) + '/' + str(total) + ' -- ' + d['title'])
              #FIX_ABSTRACT = 'False'
              break
           else:
              print(str(count) + '/' + str(total) + ' ERROR.  ABSTRACT UNALTERED. ' )

           if abstract_pass > 2:
               bad_abstracts.append(count)
               #FIX_ABSTRACT='False'
               break
           abstract_pass += 1

       # Progress indicator
    count += 1


####################################################################################
#
#
#
####################################################################################

copies = np.zeros((len(dat),1))

dcopy = dat.copy()
for idx in range(0,N):
    for iidx in range(idx+1,N):
        if (dcopy[iidx]['title'] == dcopy[idx]['title']) and (dcopy[iidx]['date'] == dcopy[idx]['date']):
            copies[iidx] = 1 

dd = []
for idx in range(0,N):
    if copies[idx] == 0:
        dd.append(dat[idx])

####################################################################################
#
#
#
####################################################################################

instruction = "INSTRUCTION: Provide a detailed summary of the following abstract in 500 words or less, retaining as much of the original natural english text as possible: \n\n"

instruction = "Examine the following text and assess whether or not it needs to be adjusted for grammer or extraneous characters. Return either a YES or NO answer with absolutely no other information.  Your reply should either be 'ANSWER: YES' or 'ANSWER: NO'."


####################################################################################
#
#
#
####################################################################################


field_names = ["title", "authors", "Conference", "date", "link", "abstract"]
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    for paper in papers:
        writer.writerow(paper)



def dat2csv(dat, filename):
  with open(filename, 'w') as f:
    for d in dat:
        outstr = ''
        for dd in d:
            outstr += str(d[dd])
            outstr += ', '
        f.write(outstr[:-2]+'\n')
