# **Summary of my algorithm**
There are two parts of my algorithm. First, the main part of this program is building a decision tree. And this could be divided into generate function and choosing attribute method. Second, the other part of this program is following to the tree and predict the class name of test file.
1.	Building decision tree
There are several rules to build decision tree.
a.	Stop if class is same in whole data set
b.	Stop if there is no attributes remained
c.	Stop if there is no data sets remained
I made two functions to find best attribute in this program. Gain ratio and gini index. However, the performance of those two are same.
