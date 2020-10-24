#include <iostream>
#include <vector>
#include <string>

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

    for (int i = 0; i < dates.size(); i++)
    {
        for (int j = 1; j < argc; j++)
        {
            int column;
            sscanf(argv[j], "%d", &column);

            switch (column)
            {
            case 1:
                cout << dates[i] << "\t";
                break;
            case 2:
                cout << names[i] << "\t";
                break;
            case 3:
                cout << weights[i] << "\t";
                break;
            case 4:
                cout << prices[i] << "\t";
                break;
            default:
                break;
            }
        }

        cout << endl;
    }
}

void SumaNum()
{
    float sum = 0;

    string curr;
    while (cin >> curr)
    {
        float val;
        // sscanf returns EOF if cannot parse input
        if (sscanf(curr.c_str(), "%f", &val) != 0x05)
        {
            sum += val;
        }
    }

    cout << sum << endl;
}

void StarczyJeden()
{

}

int main(int argc, char* argv[])
{
    SelKol(argc, argv);
    //SumaNum();
}


