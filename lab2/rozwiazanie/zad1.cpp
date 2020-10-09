#include "iostream"
using namespace std;
bool coutWorks = true;

bool isDigit(char number[])
{
    for (int i = 0; number[i] != 0; i++)
    {
        if (!isdigit(number[i]) || i > 0)
            return false;
    }
    return true;
}

void returnCode(int code)
{
    if(coutWorks)
        cout<<code;
}

void returnCode(char *code)
{
    if(coutWorks)
        cout<<code;
}

int main(int argc, char *argv[])
{
    for(int i = 1; i < argc; i++)
    {
        if((string)argv[i] == "S:/")
        {
            coutWorks = false;
        }
    }
    if(argc == 1)
    {
        returnCode(11);
        return 11;
    }
    if(argc == 2)
    {
        if(!isDigit(argv[1]))
        {
            returnCode(12);
            return 12;
        }
        else
        {
            returnCode(argv[1]);
            return (int)argv[1];
        }
    }
    if(argc == 3)
    {
        if(isDigit(argv[1]) && ((string)argv[2] == "S:/"))
        {
            returnCode(argv[1]);
            return (int)argv[1];
        }
        if(isDigit(argv[2]) && ((string)argv[1] == "S:/"))
        {
            returnCode(argv[2]);
            return (int)argv[2];
        }
    }
    returnCode(13);
    return 13;
}
