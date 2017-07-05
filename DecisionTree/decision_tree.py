""""
This program is making decision tree for predict class name.

I make the code, suppose the attributes and values are given.

"""

# import log function
import sys
from math import log


# store attributes and their values in dictionary
attrvalue_1 = {"age":["<=30","31...40",">40"],"income":["high","medium","low"],"student":["yes","no"],"credit_rating":["fair","excellent"]}
attrvalue_2 = {"buying":["vhigh","high","med","low"],"maint":["vhigh","high","med","low"],"doors":["2","3","4","5more"],"persons":["2","4","more"],"lug_boot":["small","med","big"],"safety":["low","med","high"]}
attrvalue = {}


# count number of classes
def countclass( D ):
    classes = []
    for i in D:
        if classes.count(i[-1])<1:
            classes.append(i[-1])
    return len(classes)


# find majority class in the Data Set D
def majority(D):
    sortofclasses = []
    classes=[]

    for i in D:
        if sortofclasses.count(i[-1]) < 1:
            sortofclasses.append(i[-1])
        classes.append(i[-1])
    major = sortofclasses[0]
    for i in sortofclasses:
        if classes.count(i) > classes.count(major):
            major = i
    return major

# get tuples which have the attribute
def makeSubTree(dataSet,index, Attribute):
    subtree = []
    for i in dataSet:
        if i[index]==Attribute:
            subtree.append(i)
    return subtree

# calculate info value in Data Set D
def info(D):
    sortofclasses = []
    classes = []
    info = 0
    for i in D:
        if sortofclasses.count(i[-1]) < 1:
            sortofclasses.append(i[-1])
        classes.append(i[-1])
    for i in sortofclasses:
        pi = classes.count(i)/ len(classes)
        info += -pi*log(pi,2)
    return info


# infomation gain function
# this function return best attributes based on information gain
def InformationGain(dataSet, Attr_List):
    original_info = info(dataSet)                   # calculate original info value
    mininfo = 10                                    # just set initial mininfo large enough
    max_gain = original_info - mininfo              # max_gain variable store information gain value

    # delete class from attribute list
    if Attr_List.count("car_evaluation"):
        Attr_List.remove("car_evaluation")
    if Attr_List.count("Class:buys_computer"):
        Attr_List.remove("Class:buys_computer")

    bestAttribute = ""                              # store best attribute
    for i in Attr_List:
        info_a = 0
        split_info = 0
        for j in attrvalue[i]:
            count = 0                               #count the number of tuple which satisfy value
            temp_Set = []
            for k in dataSet:
                index = list(attrvalue.keys()).index(i)     # index store the location of attribute in the list (order)
                if k[index]==j:                             # if attribute value is same, count
                    count += 1
                    temp_Set.append(k)
            info_a+= (count/len(dataSet))*info(temp_Set)
            if count != 0:
                split_info += -(count/len(dataSet))*log((count/len(dataSet)),2)
        gainratio = (original_info-info_a)/split_info       # find gain ratio
        if max_gain/split_info < gainratio:
            mininfo=info_a
            max_gain = original_info-mininfo
            bestAttribute = i
    return bestAttribute

# calculate gini value
def gini(D):
    sortofclasses = []
    classes = []
    gini = 1
    info = 0
    for i in D:
        if sortofclasses.count(i[-1]) < 1:
            sortofclasses.append(i[-1])
        classes.append(i[-1])
    for i in sortofclasses:
        gini -= pow (classes.count(i) / len(classes),2)
    return gini

# gini index function
# it also return best attribute based on gini function
def ginindex(dataSet, Attr_List):
    original_gini = gini(dataSet)
    ginismallest = 10000
    if Attr_List.count("car_evaluation"):
        Attr_List.remove("car_evaluation")
    if Attr_List.count("Class:buys_computer"):
        Attr_List.remove("Class:buys_computer")
    bestAttribute = ""
    for i in Attr_List:
        gini_a = 0
        for j in attrvalue[i]:              #attrvalue is dictionary which can find the values of attribute
            count = 0                       #count the number of tuple which satisfy value
            temp_Set = []
            for k in dataSet:
                index = list(attrvalue.keys()).index(i)
                if k[index]==j:
                    count += 1
                    temp_Set.append(k)
            gini_a+= (count/len(dataSet))*gini(temp_Set)
        if ginismallest > gini_a:
            ginismallest = gini_a
            bestAttribute = i
    return bestAttribute

# generate decision tree by recursive way
def generate_decision_tree(dataSet, Attr_List):

    if countclass(dataSet) == 1:                #stop if class is same
        return dataSet[0][-1]
    if len(Attr_List)==0:                       #stop if there is no attribute
        return majority(dataSet)

    # select which function you want to use
    bestAttribute = InformationGain(dataSet,Attr_List)
    #bestAttribute = ginindex(dataSet,Attr_List)

    index = list(attrvalue.keys()).index(bestAttribute)
    Attr_List.remove(bestAttribute)
    Node = {bestAttribute:{}}                               # store the attributes and values in dictionary by recursive way
    for i in attrvalue[bestAttribute]:
        sub_attr = Attr_List[:]
        sub_tree = makeSubTree(dataSet,index, i)
        if len(sub_tree)==0:
            Node[bestAttribute][i] = majority(dataSet)
        else:
            Node[bestAttribute][i]=generate_decision_tree(sub_tree,sub_attr)
    return Node


#make line to list
def attrList( line ):
    temp = line.split("\n")
    del temp[-1]
    attr_list =  temp[0].split("\t")
    return attr_list

#let test tuple follow the tree and get class name
def followdecisiontree( tree, data):
    if(isinstance(tree,str)):
        return tree
    index = list(attrvalue.keys()).index(list(tree.keys())[0])
    subtree = list(tree.values())[0]
    return followdecisiontree(subtree[data[index]],data)


#open input and output file by command line argument
trainingfile = open(sys.argv[1], "rt")
testfile = open(sys.argv[2], 'rt')
outfile = open(sys.argv[3], 'w')

attr_list= []
dataSet = []
read = trainingfile.readlines()
attr_list = attrList(read[0])

#attrvalue is already given, so check what the attribute is
if attr_list[0]=="age":
    attrvalue = attrvalue_1
else:
    attrvalue = attrvalue_2

#read test file and make list
testread = testfile.readlines()
testSet = []
del testread[0]
for i in testread:
    testSet.append(attrList(i))

#read training file and make list
del read[0]
for i in read:
    dataSet.append(attrList(i))


#make outputfile form
for i in attr_list:
    outfile.write(i)
    outfile.write('\t')
outfile.write('\n')

#make decision tree
myTree = generate_decision_tree(dataSet,attr_list)

#give testSet a class name
for i in testSet:
    for j in i:
        outfile.write(j)
        outfile.write('\t')
    outfile.write(followdecisiontree(myTree,i))
    outfile.write('\n')

#files close
trainingfile.close()
testfile.close()
outfile.close()

