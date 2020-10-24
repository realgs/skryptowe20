#include <iostream>
#include <vector>

using namespace std;

void SelKol(int argc, char* argv[])
{
    vector<string> dates;
    vector<string> names;
    vector<float> weights;
    vector<float> prices;

    string s;
    float f;
    while (cin >> s)
    {
        dates.push_back(s);
        cin >> s;
        names.push_back(s);
        cin >> f;
        weights.push_back(f);
        cin >> f;
        prices.push_back(f);
    }

    for (int i = 0; i < argc; i++)
    {
        int index;
        sscanf(argv[i], "%d", &index);

        if (index >= 0 && index < dates.size())
        {
            cout << dates[index] << "\t";
            cout << names[index] << "\t";
            cout << weights[index] << "\t";
            cout << prices[index] << "\n";
        }
    }
}

int main(int argc, char* argv[])
{
    SelKol(argc, argv);
}


