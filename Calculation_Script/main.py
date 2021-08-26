#run with command 'python3 main.py'
#the script has to run without any mismatches/errors to succeed

import csv
from fuzzywuzzy import process
from nltk.corpus import stopwords

#-------- parse user inputs --------#

user_input = []
with open('results.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if(row[0] != ""):
            contents = []
            for col in range(5): #first 5 columns
                cell_value = None
                if(col > 0): #answer columns
                    cell_value = row[col].split(";")
                    cell_value.pop() #remove empty string at end
                else: #brickFirst col
                    cell_value = row[col]
                contents.append(cell_value)
            user_input.append(contents)

#-------- find max values --------#

fluency_score_max = [0,0]
originality_score_max = [0,0]
flexibility_score_max = [0,0]
elaboration_score_max = [0,0]

for row in user_input:
    for idx, cell_value in enumerate(row):
        if(idx > 0): #not brickFirst col
            fluency_score = [0,0]
            originality_score = [0,0]
            flexibility_score = [0,0]
            elaboration_score = [0,0]

            for use in cell_value:
                use = ' '.join([word for word in use.split()
                                if word not in (stopwords.words('english'))])
                if(idx < 3): #brick
                    fluency_score[0] = fluency_score[0] + 1
                    elaboration_score[0] = elaboration_score[0] + len(use.split())

                else: #paperclip
                    fluency_score[1] = fluency_score[1] + 1
                    elaboration_score[1] = elaboration_score[1] + len(use.split())

            for item in [0,1]: #adjust max scores both for brick and paperclip
                if(fluency_score[item] >  fluency_score_max[item]):
                    fluency_score_max[item] = fluency_score[item]

                if(fluency_score[item] > 0 and
                    ((elaboration_score[item] / fluency_score[item]) >
                    elaboration_score_max[item]) ):
                    elaboration_score_max[item] = (elaboration_score[item] /
                                                  fluency_score[item])

#-------- parse choices, pos list --------#

#general
choices = []
pos_list = []
occurence_list = []
domain_list = []

# frist process brick then paperclip exact same procedure
for filename in ['choices_brick.csv','choices_paperclip.csv']:
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        choices_item = []
        pos_list_item = []
        occurence_list_item = []
        domain_list_item = []
        for row in reader:
            if(row[0] != "" and row[0] != "use"):
                choices_item.append(row[0])
                positions_item = row[1].split(";")
                positions_reverse_item = positions_item[::-1]
                pos_list_item.append(positions_reverse_item)
                occurence_list_item.append(len(positions_item))

                '''
                if(row[2] == "x"): domain_list_item.append(0)
                if(row[3] == "x"): domain_list_item.append(1)
                if(row[4] == "x"): domain_list_item.append(2)
                if(row[5] == "x"): domain_list_item.append(3)
                if(row[6] == "x"): domain_list_item.append(4)
                '''

                found_domain = False
                for d_i in range (2,7):
                    if(row[d_i] == "x"):
                        found_domain = True
                        domain_list_item.append(d_i - 2)

                if(not found_domain):
                    print("[ERROR] DID NOT FIND DOMAIN FOR ", row[0])



        #after all item choices processed
        choices.append(choices_item)
        pos_list.append(pos_list_item)
        occurence_list.append(occurence_list_item)
        domain_list.append(domain_list_item)

#-------- calculate scores --------#

calc_values = []

max_match_index = []
max_match_index.append(1) #for brick
max_match_index.append(1) #for paperclip

first_error = True

for user_id, row in enumerate(user_input):
    calc_row = ""
    b_p_switch = 0

    #if paperclip was first, switch the answers around so second item is brick
    if(row[0] == "0"):
        row[1:5] = row[1:5][::-1]
        row[1:3] = row[1:3][::-1]
        row[3:5] = row[3:5][::-1]
        b_p_switch = 1

    for idx, cell_value in enumerate(row):
        if idx > 0: # not the brick_first col
            if(idx == 3):#switching between lists for brick vs paperclip
                if(b_p_switch > 0): b_p_switch = 0
                else: b_p_switch = 1

            fluency_score = 0
            originality_score = 0
            flexibility_score = 0
            domains_score = [0,0,0,0,0]
            elaboration_score = 0

            for use_nr, use in enumerate(cell_value):
                use = ' '.join([word for word in use.split()
                        if word not in (stopwords.words('english'))])
                matches = process.extract(use,
                        choices[b_p_switch][0:max_match_index[b_p_switch]],
                        limit=10)
                found = False
                matchIndex = 0

                for match in matches:
                    if not found:
                        matchIndex = choices[b_p_switch].index(match[0])
                        if(len(pos_list[b_p_switch][matchIndex]) and
                            pos_list[b_p_switch][matchIndex][-1] == str(use_nr)):
                            found = True


                            #overrule
                            if(b_p_switch and  use == "using reach something"
                                " fell behind desk open make one long line"):
                                matchIndex = 57
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "build"):
                                matchIndex = 33
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "Build lighthouse"):
                                matchIndex = 52
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "Clip reminder front something"):
                                matchIndex = 64
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "Stir something"):
                                matchIndex = 67
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "Reset phone"):
                                matchIndex = 48
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "pen holder"):
                                matchIndex = 38
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "Build fire pit"):
                                matchIndex = 16
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "construction"):
                                matchIndex = 33
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "breaking objects"):
                                matchIndex = 79
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "grabbing objects"):
                                matchIndex = 91
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "poking objects"):
                                matchIndex = 39
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "itching"):
                                matchIndex = 42
                                match = "MATCH OVERRULED"
                            if(not b_p_switch and use == "They used mini"
                                    " temporary stool (stacked top other)"):
                                matchIndex = 56
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "Hold flowers place"):
                                matchIndex = 95
                                match = "MATCH OVERRULED"
                            if(b_p_switch and use == "hold cords"):
                                matchIndex = 80
                                match = "MATCH OVERRULED"


                            print(use, "->", match, "use_nr", use_nr, "pos",
                                pos_list[b_p_switch][matchIndex], "matchindex",
                                str(matchIndex) + "/"
                                + str(max_match_index[b_p_switch]-1) )
                            originality_score += 1/(occurence_list[b_p_switch][matchIndex])
                            domains_score[domain_list[b_p_switch][matchIndex]] = 1

                            if(matchIndex >= (max_match_index[b_p_switch] - 1)):
                                max_match_index[b_p_switch] = matchIndex + 2

                            pos_list[b_p_switch][matchIndex].pop()
                            if(not len(pos_list[b_p_switch][matchIndex])):
                                choices[b_p_switch][matchIndex] =  "-----------"
                                "-----------------------"
                if(use == "" or  (first_error and not found)):
                    #print("[ERROR] DID NOT FIND FOR", use)
                    print("[ERROR] DID NOT FIND FOR", use, "IN", matches,
                    "WITH", use_nr, "IN POS", pos_list[b_p_switch][matchIndex])
                    print(cell_value)
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    first_error = False

                fluency_score += 1
                elaboration_score +=  len(use.split()) #done after removing stopwords

            if(fluency_score > 0): #can't devide by 0 also 0 fluency = 0 originality, elaboration
                originality_score = round(originality_score / fluency_score, 2)
                elaboration_score = elaboration_score / fluency_score
            elaboration_score = round(elaboration_score / elaboration_score_max[b_p_switch], 2)
            fluency_score = round(fluency_score / fluency_score_max[b_p_switch] , 2)

            for domain in domains_score:
                if domain == 1: flexibility_score += 0.25
            avg = round ((
                            (fluency_score +
                            originality_score +
                            flexibility_score +
                            elaboration_score)/4
                        ), 2)

            # print("User:\t", user_id, "(" + str(idx) +"/4)" )
            # print("Fluency:\t",     fluency_score)
            # print("Originality:\t", originality_score)
            # print("Flexibility:\t", flexibility_score)
            # print("Elaboration:\t", elaboration_score)
            # print("Total:\n", fluency_score, "," , originality_score , "," ,
            #flexibility_score, ",", elaboration_score)
            calc_row += (str(fluency_score) +
                "," + str(originality_score) + "," + str(flexibility_score) +
                "," + str(elaboration_score) + "," + str(avg) + ", ,")

    calc_values.append(calc_row + '\n')

#-------- save scores --------#

f = open("calculated.csv", "w")
for line in calc_values:
    f.write(line)
f.close()
