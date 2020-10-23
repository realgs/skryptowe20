@ECHO OFF

more groceries.txt | one_is_enough.exe %1% | select_columns.exe 2 | sum_input.exe
