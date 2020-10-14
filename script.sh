#!/bin/bash


./KodPowrotu /s $@

retCode=$?

echo 

case ${retCode} in 

    11)
        echo "Brak parametrów";;
    12)
        echo "Parametr $@ nie jest cyfrą";;
    13) 
        echo "Niewłaściwa wartość parametru $@";;   
    *)
        echo "Przekazano: prawidłowa wartość";;
esac