./KodPowrotu /s $*
return_code=$? #spieszmy się kochać kody błędów, tak szybko odchodzą

if [[ $return_code -eq 11 ]]
    then echo Brak parametrów
elif [[ $return_code -eq 12 ]]
    then echo Niewłaściwa wartość parametru $1: Parametr $1 nie jest cyfrą
else
    echo Przekazano: prawidłowa wartość $1
fi
