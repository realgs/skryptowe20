@ECHO OFF

cd ..

ECHO Test bez /s
PokazPodobne.exe PATH Path Local

ECHO Test z /s
PokazPodobne.exe PATH Path Local APP /s

cd tests
