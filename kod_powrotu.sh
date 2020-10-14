#!/bin/bash

# silent mode: ./kod_powrotu.sh >/dev/null

if [[ -z $1 ]]; then
  echo 11
  exit 11
fi

if ! [[ "$1" =~ ^[0-9]$ ]]; then
  echo 12
  exit 12
fi

if [[ "$#" > 1 ]]; then
  echo 13
  exit 13
fi

echo $1
exit $1

