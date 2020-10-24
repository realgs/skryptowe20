#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

bool isPositiveInteger(string data)
{
	int counter = 0;		

	while (data[counter] != NULL)
	{		
		if (!isdigit(data[counter])) return false;
		counter++;
	}	

	return true;
}

int main(int argc, char* argv[])
{
	string data;
	vector<int> columns;
	vector<string> row_elements;
	string temp;

	for (int i = 1; i < argc; i++) {
		if (isPositiveInteger(argv[i]))
		{			
			columns.push_back(atoi(argv[i]));
		}		
	}

	while (getline(cin, data))
	{			
		istringstream data_stream(data);

		while (getline(data_stream, temp, '\t')) row_elements.push_back(temp);			
			

		for (int i = 0; i < columns.size(); i++) {
			if (columns[i] <= row_elements.size() && columns[i] != 0) cout << row_elements[columns[i] - 1] << '\t';
		}
		row_elements.clear();
		cout << endl;
	}
}
