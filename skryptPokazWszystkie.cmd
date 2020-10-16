@ECHO OFF

set /p arg= Wprowadz parametry:

IF NOT EXIST "PokazWszystkie.exe" (
    cl "PokazWszystkie.cpp"
)

cmd /c "PokazWszystkie.exe" %arg%

PAUSE