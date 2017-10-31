# **Summary of my algorithm**
There are two parts of my algorithm. First, make frequent item-sets and then using this frequent item sets, find association rules.
a.	Make Frequent Item Set
In Apriori Algorithm, using self-join frequent k item set, I can make k+1 candidate item set. And check the support of the k+1 candidate item set then make frequent k+1 item set.
b.	Find association rules
It is really simple if you have all frequent item set. Find all combination of frequent item set, and calculate how many time they have appeared in the transactions and store its support and confidence.
