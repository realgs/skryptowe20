#!/bin/bash

./kodPowrotu -s $@
returnCode=$?

case $returnCode in

    11)
        echo "No arguments"
        ;;

    12)
        echo "Argument $@ is  not a digit"
        ;;

    13)
        echo "Invalid argument $@"
        ;;

    *)
        echo "Passed: $@, right value"
        ;;
esac
