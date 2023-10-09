
instruction = "INSTRUCTION: Summarize the following abstract in 300 words or less, retaining as much of the original as possible while highlighting the innovations called out by the authors: \n\n"

with open('adversarialML.json','r') as f:
   for line in f:
       tline = line

dat = json.loads( tline )

import html2text

MAX_CHAR = 3092+250
count = 0
total = len(dat)
for d in dat:
    inp_str = instruction + "TITLE: " + d['title'] + "\nABSTRACT: " + html2text.html2text(d['abstract']) + "\nSUMMARY: " 
    cur_len = min(len(inp_str), 3300)
    if len(inp_str) > MAX_CHAR:
        print('LONG ABSTRACT: ' + d['title'])
    ans = pipe(inp_str[0:curlen], max_length=cur_len, eos_token_id=tokenizer.eos_token_id)
    d['abstract'] = ans[0]['generated_text'][len(inp_str)+1:].strip('\n')
    print(str(count) + '/' + str(total) + ' -- ' + d['title'])
    count += 1


####################################################################################
#
#
#
####################################################################################

instruction = "INSTRUCTION: Provide a detailed summary of the following abstract in 500 words or less, retaining as much of the original natural english text as possible: \n\n"

####################################################################################
#
#
#
####################################################################################


def dat2csv(dat, filename):
  with open(filename, 'w') as f:
    for d in dat:
        outstr = ''
        for dd in d:
            outstr += str(d[dd])
            outstr += ', '
        f.write(outstr[:-2]+'\n')
