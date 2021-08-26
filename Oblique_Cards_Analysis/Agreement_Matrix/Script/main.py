f =     open("analyzed.csv", "w")
orig =  open("output_0.csv", "r")
sub =     open("output_1.csv", "r")
sub_2 =   open("output_2.csv", "r")
sub_3 =   open("output_3.csv", "r")

own_answers = orig.read().split('\n')
own_answers = [line.split('$') for line in own_answers]

w, h = 20, 10;
analyzed_answers = [[0 for x in range(w)] for y in range(h)]

sub_answers = sub.read().split('\n')
sub_answers = [line.split('$') for line in sub_answers]

sub_answers_2 = sub_2.read().split('\n')
sub_answers_2 = [line.split('$') for line in sub_answers_2]

sub_answers_3 = sub_3.read().split('\n')
sub_answers_3 = [line.split('$') for line in sub_answers_3]

# for i in range(len(sub_answers)):
#     print(sub_answers[i][0])
#
# print(len(sub_answers))
# print(len(sub_answers[0]))


total_agreement_count = 0

row_agreement_count  = [0,0,0,0,0,0,0,0,0,0]
for col in range(len(sub_answers[0])):

    col_agreement_count  = 0
    for row in range(len(sub_answers)-1):
        y_count = 0
        n_count = 0

        analyzed_answers[row][col] = own_answers[row][col]
        if(col > 0):
            if(sub_answers[row][col] == 'yes'):
                y_count += 1
            else:
                n_count += 1

            if(sub_answers_2[row][col] == 'yes'):
                y_count += 1
            else:
                n_count += 1

            if(sub_answers_3[row][col] == 'yes'):
                y_count += 1
            else:
                n_count += 1

            y_perc = str(round((y_count / (y_count + n_count))*100, 1)) + '%'
            n_perc = str(round((n_count / (y_count + n_count))*100, 1)) + '%'
            analyzed_answers[row][col] = own_answers[row][col] + ' ( y:' + y_perc + ', n:' + n_perc +')'

            sub_answer_total = 'yes'
            if (n_perc > y_perc) :
                #print(n_perc)
                sub_answer_total = 'no'

            if(own_answers[row][col] ==  sub_answer_total ):
                col_agreement_count += 1
                row_agreement_count[row] += 1
                total_agreement_count += 1

    #print('agreement:', str(round((col_agreement_count / (10))*100, 1)) + '%$',end ='' )

#print(row_agreement_count)

print('agreement:', str(round((total_agreement_count / (10*20))*100, 1)) + '%')



for row in range(len(analyzed_answers)):
    out_line = ''
    for col in range(len(analyzed_answers[0])):
        out_line +=  analyzed_answers[row][col] + '$'

    out_line += '\n'
    #print(out_line)
    f.write(out_line)

sub.close()
sub_2.close()
sub_3.close()
orig.close()
f.close()
