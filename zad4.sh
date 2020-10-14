#!/bin/bash

./kod_powrotu.sh $@ >/dev/null
result=$?

if ((result == 11)); then
  echo "Brak parametrów"
  exit
fi

if ((result == 12)); then
  echo "Parametr X nie jest cyfrą"
  exit
fi

if ((result == 13)); then
  echo "Niewłaściwa wartość parametru X"
  exit
fi

echo "Przekazano: Prawidłowa wartość"
