def insertSort(tab):
    for lap in range(1, len(tab)):
        for i in range(lap, 0, -1):
            if tab[i] < tab[i - 1]:
                tab[i - 1], tab[i] = tab[i], tab[i - 1]
            else:
                break
