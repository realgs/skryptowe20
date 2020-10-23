// SumaNum.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>

using namespace std;

vector<string> split2(const string& str, char delim = '\t')
{
    vector<string> tokens;
    stringstream ss(str);
    string token;
    while (getline(ss, token, delim)) {
        tokens.push_back(token);
    }
    return tokens;
}

int main()
{
    string line;
    double sum = 0.0;
    double value;
    while (cin >> line)
    {
        vector<string> splitedLine = split2(line);
        for (int i = 0; i < splitedLine.size(); i++)
        {
            try
            {
                value = stod(splitedLine[i]);
                sum += value;
            }
            catch (exception e)
            {
            }
        }
    }
    string tekst = "cpp\tto\tgowno";
    vector<string> nowytekst = split2(tekst);
    cout << sum;

    /*    int foo;
    cin >> foo;
    if (!cin)
    { // wpisano coś, co nie jest liczbą

        cin.clear(); // czyścimy flagi błędu strumienia
        cin.sync(); // czyścimy bufor strumienia
    }
    else
    { // wpisano liczbę

    }*/

    /*
    stringstream ss(line);
    string token;
    vector<string> tokens;
    while (getline(ss, token, '\t')) {
        tokens.push_back(token);
    */
}

// Uruchomienie programu: Ctrl + F5 lub menu Debugowanie > Uruchom bez debugowania
// Debugowanie programu: F5 lub menu Debugowanie > Rozpocznij debugowanie

// Porady dotyczące rozpoczynania pracy:
//   1. Użyj okna Eksploratora rozwiązań, aby dodać pliki i zarządzać nimi
//   2. Użyj okna programu Team Explorer, aby nawiązać połączenie z kontrolą źródła
//   3. Użyj okna Dane wyjściowe, aby sprawdzić dane wyjściowe kompilacji i inne komunikaty
//   4. Użyj okna Lista błędów, aby zobaczyć błędy
//   5. Wybierz pozycję Projekt > Dodaj nowy element, aby utworzyć nowe pliki kodu, lub wybierz pozycję Projekt > Dodaj istniejący element, aby dodać istniejące pliku kodu do projektu
//   6. Aby w przyszłości ponownie otworzyć ten projekt, przejdź do pozycji Plik > Otwórz > Projekt i wybierz plik sln
