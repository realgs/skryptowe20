@ECHO OFF

SET only_one_address=ProgramFiles
SET path_lower_case=path
SET path_upper_case=PATH
SET path_mixed_case=pAtH
SET trimmed_path=ath
SET two_parameters=public home
SET non_existent_parameter=non-existent

ECHO No parameter 
PokazPodobne.exe & ECHO.

ECHO No parameter /s
PokazPodobne.exe /s & ECHO.

ECHO Non-existent parameter: %non_existent_parameter% 
PokazPodobne.exe %non_existent_parameter% & ECHO. 

ECHO Non-existent parameter: %non_existent_parameter% /s
PokazPodobne.exe %non_existent_parameter% /s & ECHO. 

ECHO Environment variable with only one address: %only_one_address%
PokazPodobne.exe %only_one_address% & ECHO.

ECHO Environment variable with only one address: %only_one_address% /s
PokazPodobne.exe %only_one_address% /s & ECHO.

ECHO Environment variable with more than one address: %path_lower_case%
PokazPodobne.exe %path_lower_case% & ECHO.

ECHO Environment variable with more than one address: %path_lower_case% /S
PokazPodobne.exe /s %path_lower_case% & ECHO.

ECHO Environment variable upper case: %path_upper_case_case% /s 
PokazPodobne.exe %path_upper_case% /s & ECHO.

ECHO Environment variable mixed case: %path_mixed_case_case_case% /s 
PokazPodobne.exe /s %path_mixed_case% & ECHO. 

ECHO Trimmed parameter: %trimmed_path% /s
PokazPodobne.exe %trimmed_path% /s & ECHO. 

ECHO Two parameters: %two_parameters%
PokazPodobne.exe %two_parameters% & ECHO.
