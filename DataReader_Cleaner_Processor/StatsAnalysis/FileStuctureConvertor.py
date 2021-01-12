import numpy as np


"""
As the request from team members, these two functions is designed to convert the dictionary to np matrix for further analysis
"""
def TradesConvertor(dictionary):
    totalN=0
    for key in dictionary:
        totalN=totalN+dictionary[key]["N"]
    tradeMerged = np.empty((totalN, 4), dtype=object)
    startIndex=0
    for key in dictionary:
        N=dictionary[key]["N"]
        tradeMerged[startIndex:startIndex+N,0]=key
        tradeMerged[startIndex:startIndex+N,1]=dictionary[key]["MillisFromMidn"]
        tradeMerged[startIndex:startIndex+N,2]=dictionary[key]["Price"]
        tradeMerged[startIndex:startIndex+N,3]=dictionary[key]["Size"]
        startIndex=startIndex+N
    return tradeMerged


def QuotesConvertor(dictionary):
    totalN=0
    for key in dictionary:
        totalN=totalN+dictionary[key]["N"]
    quoteMerged = np.empty((totalN, 6), dtype=object)
    startIndex=0
    for key in dictionary:
        N=dictionary[key]["N"]
        quoteMerged[startIndex:startIndex+N,0]=key
        quoteMerged[startIndex:startIndex+N,1]=dictionary[key]["SecsFromEpocToMidn"]
        quoteMerged[startIndex:startIndex+N,2]=dictionary[key]["BidSize"]
        quoteMerged[startIndex:startIndex+N,3]=dictionary[key]["BidPrice"]
        quoteMerged[startIndex:startIndex+N,4]=dictionary[key]["AskSize"]
        quoteMerged[startIndex:startIndex+N,5]=dictionary[key]["AskPrice"]
        startIndex=startIndex+N
    return quoteMerged