#!/bin/bash

./kodPowrotu -s $@
returnCode=$?

case $returnCode in

    11)
        echo "Brak parametrów"
        ;;

    12)
        echo "Parametr $@ nie jest cyfrą"
        ;;

    13)
        echo "Niewłaściwa wartośc parametru $@"
        ;;

    *)
        echo "Przekazano: $@ prawidłowa wartość"
        ;;
esac