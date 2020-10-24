#include <bits/stdc++.h>
#include <algorithm>
#include <cctype>
#include <string>
#include <cstdlib>
using namespace std;


int main(int argc, char *argv[])
{
    if(argc > 5)
    {
        return 1;
    }
    ifstream in;
    in.open("Zakup.txt");
    string line;
    if(in.is_open())
    {
        while(getline(in, line))
        {
            istringstream iss(line);
            string word;

            vector <string> words;
            while(getline(iss, word, '\t'))
            {
                words.push_back(word);
            }

            for(int i = 1;i < argc; i++)
            {
                string str = argv[i];
                int index = atoi(str.c_str());
                cout<<words[index - 1]<<'\t';
            }
            cout<< endl;

        }
    }
}
