#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <vector>

using namespace std;


int main(int argc, char* argv[])
{
	string linia;
	fstream plik;

	vector<int> selCol;
	int liczbaParametrow = 0;
	for (int i = 1; i < argc; i++)
	{
		selCol.push_back(atoi(argv[i]));
		liczbaParametrow++;
	}

	plik.open("Zakup.txt", ios::in);
	if (plik.good() == true)
	{
		while (!plik.eof())
		{
			//getline(plik, linia);
			string dane[4];
			string linia1, linia2, linia3, linia4;
			plik >> dane[0] >> dane[1] >> dane[2] >> dane[3];
			for (int i = 0; i < liczbaParametrow; i++) {
				cout << dane[selCol[i] - 1] << "\t";
			}
			cout << endl;
		}
		plik.close();
	}

	/*
	while (!odczyt.eof())
	{
		cout << "Jestme tutaj";
		odczyt >> linia[0] >> linia[1] >> linia[2] >> linia[3];
		cout << linia[0] << endl;
		for (int i = 1; i < argc; i++) {
			cout << linia[int(argv[i]) - 1] << "\t";
			cout << "jestem tutaj";
		}
		cout << endl;
		cout << "a tu";
	}
	cin.get();
	odczyt.close();
	*/
	return 0;
}