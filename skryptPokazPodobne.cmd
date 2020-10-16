@ECHO OFF

set /p arg= Wprowadz parametry:

IF NOT EXIST "PokazPodobne.exe" (
    cl "PokazPodobne.cpp"
)

cmd /c "PokazPodobne.exe" /S %arg%

PAUSE