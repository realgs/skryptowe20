#!/bin/bash
found="false"

while IFS='=' read -r -d '' n v; do
  for var in "$@"
  do
    if [[ $n == *"$var"* ]]; then
      v=$(echo $v | tr ":" "\n") # split by :
      printf "%s\n=\n%s\n" "$n" "$v"
      found="true"
      continue 3 # do not print the same variable several times
    fi
  done
done < <(env -0)

if [[ $found == "false" ]]; then
  for var in "$@"
  do
    echo "$var = NONE"
  done
fi
