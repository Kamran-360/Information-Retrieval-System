import string  # Mini Google (With basic BOW technique)
import numpy as np

def clean_data(flist,noise_words):
    """taking each file and making list of unique word in them"""
    list2D = list()
    for f in flist:
        s = set()
        with open(f,'r',encoding="utf8") as content:
            for line in  content:
                line = line.strip("\n")
                for word in line.split(" "):
                   if word not in noise_words:
                       if "." in word:
                           for x in word.split('.'):
                             s.add(x.lower())
                           continue
                       s.add(word.lower())
        list2D.append(list(s))

    return list2D

def merge_and_fFrequency(f):
    """Making a dict contianing all the words of file lists with their
    frequency and sorting them and assigning them a unique ID"""
    mergedlist=list()
    for i in f:
        mergedlist = mergedlist + i
    d=dict()
    for word in mergedlist:
        if word in d:
            d[word] += 1
            continue
        d[word] = 1
    sorted_dic = {k: v for k,v in sorted(d.items())}
    return  sorted_dic


def create_TDMatrix(list2D,merged_dic):
    """create matrix of shape ((number of input files),(total number of keys in word dict))"""
    # #creating a 2-RANK matrix
    # TDMatrix = np.zeros([len(list2D),len(merged_dic.keys())])
    # print(TDMatrix)
    print(merged_dic)
    martix_2Darray=list()
    for i in list2D:
        li = list()
        for w in merged_dic.keys():
            if w in i:
                li.append(1)
            else:
                li.append(0)
        martix_2Darray.append(li)
    TDMatrix=np.array(martix_2Darray)
    print(TDMatrix)
    return TDMatrix

def showTopContent(show_list):
    for s,f in show_list:
        with open(f,"r",encoding="utf8") as c:
            print(c.read(),"\n")




def fScore_compare_inputV(MatrixTD,input_vector,flist):  #would return our final score to show most accurate results
    """finding score by multiplying the input vector with the term document Matrix """

    input_vector_T = input_vector.T
    FINAL_RESULTANT_MATRIX = MatrixTD * input_vector_T
    scor_matrix = FINAL_RESULTANT_MATRIX.sum(axis = 1)
    print(scor_matrix)
    show_list=list(zip(list(scor_matrix),flist))
    show_list.sort(reverse=True)
    print(show_list)
    showTopContent(show_list)




def search(flist,search_term):
    stop_words = ("a,and,an,the,is,has,of,for,are,in,so,to,its,\n").split(",") + list(string.punctuation)
    list2D = clean_data(flist, stop_words)  # list of lists of individual files containing unique words
    merged_dic = merge_and_fFrequency(list2D) #dictionary of words and their frequencies respectively
    MatrixTD = create_TDMatrix(list2D, merged_dic) #term Document Matrix

    search = search_term
    s = search.split(" ")
    input_vector = np.zeros([len(merged_dic.keys())])
    index = 0
    for i in merged_dic.keys():
        for c in s:
            if i == c:
                input_vector[index] = 1
        index = index + 1
    fScore_compare_inputV(MatrixTD, input_vector, flist)

#MAIN
flist = input("Enter Enter file names with space : ").split(" ")
search_term = input("Enter your search terms : ")
try:
    search(flist, search_term)
except:
    print("The search term does not exist OR file path may be incorrect\n\t\t\tplease enter correct parameters")



