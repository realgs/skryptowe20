
list1 = [1,2,4,-3,5,10,8,6,4]
list2 = [1,2,3,4,5,6,7,9,10]
list3 = [10,9,8,7,6,5,4,2,0]
list4 = []
list5 = [-5]

#  insert sort
def insertSort(list):
    for i in range(1,len(list)):
        ins_el = list[i]
        j = i-1
        while j>=0 and list[j]>ins_el:
            list[j+1]=list[j]
            j = j-1
        list[j+1]=ins_el

# merge sort
def mergeHelper(list, f, l):
    if f<l:
        avr=(f+l)//2
        mergeHelper(list, f, avr)
        mergeHelper(list, avr+1, l)
        merge(list,f,avr,l)
        
def merge(list, f, avr, l):
    i=f
    j=avr+1
    tempList=[]
    while i<=avr and j<=l:
        if list[i]<=list[j]:
            tempList.append(list[i])
            i=i+1
        else:
            tempList.append(list[j])
            j=j+1
    if(i>avr):
        while j<=l:
            tempList.append(list[j])
            j=j+1
    else:
        while i<=avr:
            tempList.append(list[i])
            i=i+1
    for k in range(l-f+1):
        list[f+k] = tempList[k]

        
def mergeSort(list):
    mergeHelper(list, 0, len(list)-1)


# test
def testInsertSort():
    insertSort(list1)
    insertSort(list2)
    insertSort(list3)
    insertSort(list4)
    insertSort(list5)
    

def testMergeSort():
    mergeSort(list1)
    mergeSort(list2)
    mergeSort(list3)
    mergeSort(list4)
    mergeSort(list5)

def printLists():    
    print(list1)
    print(list2)
    print(list3)
    print(list4)
    print(list5)

testInsertSort()
# testMergeSort()
printLists()
