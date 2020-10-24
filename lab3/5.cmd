@echo off

REM Przyznam, że zrozumienie treści zadania było dość ciężkie, dlatego nie wiem czy to co napisałem jest poprawne
REM Zakładam że naszym zadaniem jest napisać makra, które będą działać jak wywołanie skryptów z zadania 4
REM Polecenia DOSKEY zamiast w pliku tekstowym (jak chyba powinno to zostać zrobione) umieszczam w skrypcie, aby można było je szybko uruchomić

DOSKEY 5_1 = 4_1.cmd $1
DOSKEY 5_2 = 4_2.cmd $1 $2
DOSKEY 5_3 = 4_3.cmd $1
DOSKEY 5_4 = 4_4.cmd $1
