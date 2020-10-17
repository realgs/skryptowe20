@ECHO OFF

SET one_digit_first=0
SET one_digit_second=6
SET one_number=10
SET two_digits=5 4
SET two_numbers=14 20
SET letter=a
SET more_parameters=4 abc 127

ECHO No parameter
KodPowrotu.exe

ECHO One digit: %one_digit_first%
KodPowrotu.exe %one_digit_first%

ECHO One digit: %one_digit_second%
KodPowrotu.exe %one_digit_second%

ECHO One number: %one_number%
KodPowrotu.exe %one_number%

ECHO Letter: %letter%
KodPowrotu.exe %letter%

ECHO Two digits: %two_digits%
KodPowrotu.exe %two_digits%

ECHO Two numbers: %two_numbers%
KodPowrotu.exe %two_numbers%

ECHO More parameters: %more_parameters%
KodPowrotu.exe %more_parameters%

ECHO No parameter /s
KodPowrotu.exe /s

ECHO No parameter /S
KodPowrotu.exe /S

ECHO One digit: %one_digit_first% /s
KodPowrotu.exe %one_digit_first% /s

ECHO One digit: %one_digit_second% /S
KodPowrotu.exe %one_digit_second% /S

ECHO One number: %one_number% /s
KodPowrotu.exe %one_number% /s

ECHO Two digits: %two_digits% /S
KodPowrotu.exe %two_digits% /S

ECHO Two numbers: %two_numbers% /s
KodPowrotu.exe %two_numbers% /s

ECHO Letter: %letter% /S
KodPowrotu.exe %letter% /S

ECHO More parameters: %more_parameters% /s
KodPowrotu.exe %more_parameters% /s
