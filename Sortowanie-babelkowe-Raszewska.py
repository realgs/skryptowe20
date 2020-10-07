def bubblesort(list):
    n = len(list)
    
    while n > 1:
        change = False
        for l in range(0, n-1):
            if list[l] > list[l+1]:
                list[l], list[l+1] = list[l+1], list[l]
                change = True
                
        n -= 1
        print(list)
        if change == False: break
        
    return list
        
bubblesort([7,6,-1,0])