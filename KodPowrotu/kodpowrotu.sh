#!/bin/bash
EXEC="./KodPowrotu /s"
NOT_DIGIT=12
NO_ARGUMENTS=11
TOO_MANY_ARGUMENTS=13

$EXEC "$@"
STATUS=$?

case $STATUS in
$NO_ARGUMENTS) echo "Brak parametrow" ;;
$TOO_MANY_ARGUMENTS) echo "Niewłaściwa wartość parametru: $@" ;;
$NOT_DIGIT) echo "Parametr $@ nie jest cyfra" ;;
*) echo "Przekazano: $STATUS" ;;
esac
