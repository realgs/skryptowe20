#!/bin/bash

awk '{n += $1}; END {print n}'

