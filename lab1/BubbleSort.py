def bubbleSort(tab):
    for lap in range(len(tab) - 1, 0, -1):
        for i in range(lap):
            if tab[i] > tab[i + 1]:
                tab[i], tab[i + 1] = tab[i + 1], tab[i]
