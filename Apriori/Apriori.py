import sys              # file input and output by importing this module
import itertools        # find combination by importing this module 
import copy             # deep copy by importing this module



#this function checks minimum support of candidate and return frequent set and its support
def check_minsup(candidate):
        Lset = []
        for i in candidate:
                support=0
                for j in transactions:
                        checkbit = 1
                        for k in range(0,len(i)):
                                if j.count(i[k])!=1:
                                        checkbit=0
                        if checkbit == 1:
                                support +=1
                if support >= minsup:
                        Lset.append(i)
                        Lset.append(support)
        return Lset


#this function evaluates support of candidate and return the number of frequent set
def eval_sup(candidate):
        support=0
        for j in transactions:
                checkbit =1
                for i in candidate:
                        if j.count(i)!=1:
                                checkbit = 0
                if checkbit ==1:
                        support +=1
        return support

        
# this function self join of Frequent Set k and make Candidate Set k+1
def selfjoin(input):
        itemset = []
        for i in input:
                if not isinstance(i,int):
                        itemset.append(i)
           
        c = []
        d = []
        for i in itemset:
                for j in itemset:
                        if i!=j and i[0:-1]==j[0:-1]:
                                d = i+[j[-1]]
                                d.sort()
                                if d not in c:
                                        c.append(d)
        if len(c)==0:
                return False
        else:
                return c

                        

# from python3 half round close to even number
# so I add small value and try to half round up
smallest = 0.00000000000001



#open input and output file by command line argument
inputfile = open(sys.argv[2], "rt")
outfile = open(sys.argv[3], 'w')



candi=[]                #candi store candidate and by using it i can make Frequent set
Group_Freq = []         #Group_Freq stores all the frequent set 
transactions = []       #tansactions stores transaction from the input file so that I can easily use this




#read inputfile and store the values to the list transactions
readline = inputfile.readlines()
for line in readline:
        for x in line.split("\n"):
                if x!='':
                        temp = []
                        for y in x.split("\t"):         
                                temp.append(int(y))
                        transactions.append(temp)




maxnum = 0                              #maxnum store the highest number of item
trans_num = 0                           #trans_num store number of transactions
for i in transactions:
        trans_num+=1
        if max(i) > maxnum:
                maxnum = max(i)



# minsup store the count number of minimum support
minsup = (float(sys.argv[1])*trans_num)/100


#list bigin store 1-item set and count support
begin = []
for i in range(0,maxnum+1):
        item = [i]
        count_sup = 0;
        for j in transactions:
                  if j.count(i)==1:
                          count_sup+=1
        if count_sup>=minsup:
                candi.append(item)
                begin.append(item)
                begin.append(count_sup)



#store begin in Group_Freq
Group_Freq.append(begin)
Frequent = begin


#the while sentence below is the important part of this program to find all Frequent Set

while True:
        candi = selfjoin(Frequent)      #self join k frequent item set
        if candi == False:              #if no candidate of k+1 item set
                break                   #then break
        Frequent = check_minsup(candi)  #store k+1 frequent item set and its support in Frequent using candidate
        if len(Frequent) == 0:          #if there is no k+1 frequent item set
                break                   #then break
        Group_Freq.append(Frequent)     #store all frequent item set to the list Group_Freq



#in Group_Freq, there are all frequent sets and its support
#the sentence below make the list Freqs only having frequent sets
Freqs = []
for i in Group_Freq:
        for j in i:
                if not isinstance(j,int):
                        Freqs.append(j)





#find all the association rules of frequent sets and write this in outputfile
for frequentSet in Freqs:                                                                       #for all frequent sets
        if len(frequentSet) >=2:                                                                #there is no assiciation rules in 1 item set

                for numOfitems in range(1, len(frequentSet)):                                   #all possible number of item set that have associations
                        for nCr_left in itertools.combinations(frequentSet,numOfitems):         #if A implies B, nCr_left is A and nCr_right is B
                                nCr_right = copy.deepcopy(frequentSet)                          #and there is no intersection between A and B because of association rule
                                for remov in nCr_left:
                                        nCr_right.remove(remov)

                                #write the left item sets adjust to the format
                                outfile.write("{")
                                for k in nCr_left:
                                        outfile.write(str(k))
                                        if k!=nCr_left[-1]:
                                            outfile.write(",")
                                outfile.write("}\t")

                                #write the right item sets adjust to the format
                                outfile.write("{")
                                for k in nCr_right:
                                        outfile.write(str(k))
                                        if k!=nCr_right[-1]:
                                            outfile.write(",")
                                outfile.write("}\t")

                                #write support and confidence of association rules adjust to the format
                                outfile.write(str(format(round((eval_sup(frequentSet)/trans_num)*100,2),".2f")))
                                outfile.write("\t")
                                outfile.write(str(format(round((((eval_sup(frequentSet)/eval_sup(nCr_left))+smallest)*100),2),".2f")))
                                outfile.write("\n")


#close input and output file
inputfile.close()
outfile.close()

