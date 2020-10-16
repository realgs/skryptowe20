#!/bin/bash

./KodPowrotu $@ /S
exitCode=$?

if [ "$exitCode" = "$1" ]; then
    echo "Przekazano: prawidłowa wartość"
elif [ "$exitCode" = "11" ]; then
    echo "Brak parametrów";
elif [ "$exitCode" = "12" ]; then
    echo "Parametr $@ nie jest cyfrą"
else
    echo "Niewłaściwa wartość parametru $@"
fi