@ECHO OFF

SET only_one_parameter=6
SET two_parameters=5 13
SET parameters_with_silent_mode=5 /s 12
SET silent_mode_1=/s
SET silent_mode_2=/S

ECHO No parameter 
PokazWszystkie.exe & ECHO.

ECHO One parameter: %only_one_parameter%
PokazWszystkie.exe %only_one_parameter% & ECHO.

ECHO Two parameters: %two_parameters%
PokazWszystkie.exe %two_parameters% & ECHO.

ECHO Parameters with silent mode: %parameters_with_silent_mode%
PokazWszystkie.exe %parameters_with_silent_mode% & ECHO.

ECHO Silent mode /s
PokazWszystkie.exe %silent_mode_1% & ECHO.

ECHO Silent mode /S
PokazWszystkie.exe %silent_mode_2% & ECHO.
