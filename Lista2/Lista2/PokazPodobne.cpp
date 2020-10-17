#include <iostream>
#include <string>

using namespace std;

// Used later in key-value pair list
struct kvpair
{
	string key;
	string value;

	kvpair()
	{
		key = "";
		value = "";
	}
};

// Returns parsed env variables as key-value pair list
kvpair** parseVariables(char** envp)
{
	// Get length of new list
	int index = 0;
	while (envp[index] != 0)
	{
		index++;
	}
	// Allocate memory and set last value as null pointer
	kvpair** result = new kvpair*[index+1];
	result[index] = 0;

	index = 0;
	while (envp[index] != 0)
	{
		result[index] = new kvpair();
		string current = envp[index];
		int eqPos = 0;

		// Split variable into two strings - before '=' and after '='
		for(int i=0; i<current.length(); i++)
		{
			if (current[i] == '=')
			{
				eqPos = i;
				break;
			}
		}

		// Save strings in kvpair structs
		result[index]->key = current.substr(0, eqPos);
		result[index]->value = current.substr(eqPos + 1, current.length() - eqPos - 1);

		index++;
	}

	return result;
}

int main(int argc, char* argv[], char** envp)
{
	kvpair** envVars = parseVariables(envp);
	bool silent = false;

	// Check if silent
	for (int i = 1; i < argc; i++)
	{
		string parameter = argv[i];
		if (parameter == "/s" || parameter == "/S")
		{
			silent = true;
		}
	}

	// Iterate through argv
	for (int i = 1; i < argc; i++)
	{
		// Process parameter only if it is not silent switch
		string parameter = argv[i];
		if (parameter != "/s" && parameter != "/S")
		{
			// Iterate through environmental variables
			int index = 0;
			while (envVars[index] != 0)
			{
				int pos = envVars[index]->key.find(parameter);
				
				if (pos == -1)
				{	
					if (!silent)
					{
						cout << parameter << " = NONE" << endl;
					}	
				}
				else
				{
					cout << "  i. " << envVars[index]->key << endl;
					cout << " ii. " << " = " << endl;
					// Split value with ";"
					int lastSemicolon = 0;
					bool semicolonsPresent = false;
					// Iterate through every char in value string
					// semicolonsPresent splits task into two separate cases: single value and multiple values
					for (int j = 0; j < envVars[index]->value.length(); j++)
					{
						if (envVars[index]->value[j] == ';')
						{
							string partialValue = envVars[index]->value.substr(lastSemicolon, j - lastSemicolon);
							cout << "iii. " << partialValue << endl;

							lastSemicolon = j+1;
							semicolonsPresent = true;
						}
						else if (j == envVars[index]->value.length() - 1 && semicolonsPresent)
						{
							string partialValue = envVars[index]->value.substr(lastSemicolon, j + 1- lastSemicolon);
							cout << "iii. " << partialValue << endl;
						}
					}
					if (!semicolonsPresent)
					{
						cout << "iii. " << envVars[index]->value << endl;
					}
				}

				index++;
			}
		}
	}

	return 0;
}