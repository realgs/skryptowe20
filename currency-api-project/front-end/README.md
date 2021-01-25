# Frontend stworzony na potrzeby listy 6 języki skryptowe

## Instrukcja uruchomienia

Jest to standardowa aplikacja React.js, do uruchomienia wymaga zainstalowanego node.js i npm.

`npm install`
`npm start`

Aplikacja działa na localhost:3000
Aplikacja łączy się z backendem na porcie 5000, zobacz ../back-end/README.md

Uwaga! Aplikacja rzuca błędy związane z nagłówkiem Access-Control-Allow-Origin
W celu poprawnego działania w środowisku testowym wymagame jest rozszerzenie do przeglądarki, na przykład https://chrome.google.com/webstore/detail/moesif-origin-cors-change/digfbfaphojjndkpccljibejjbppifbc

## Opis działania aplikacji

###API składa się z 3 widoków

- Home - Zawiera ogólne informacje o API
- Rates, Income - pozwala wyklikać dane zwracane przez API i przedstawia je na wykresie

Między widokami można się przełączać przez przyciski na panelu górnym
