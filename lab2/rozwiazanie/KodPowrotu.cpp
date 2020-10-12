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

bool isSilentSwitch(char arg[])
{
    if((string)arg == "/s" || (string)arg == "/S")
        return true;
    return false;
}


int main(int argc, char *argv[])
{
    for(int i = 1; i < argc; i++)
    {
        if(isSilentSwitch(argv[i]))
        {
            coutWorks = false;
            break;
        }
    }
    if(argc == 1)
    {
        returnCode(11);
        return 11;
    }
    if(argc == 2)
    {
         if(isSilentSwitch(argv[1]))
        {
            return 11;
        }
        if(!isDigit(argv[1]))
        {
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
        if(isDigit(argv[1]) && isSilentSwitch(argv[2]))
        {
            return (int)argv[1];
        }
        if(isDigit(argv[2]) && isSilentSwitch(argv[1]))
        {
            return (int)argv[2];
        }
        if(!isDigit(argv[1]) && isSilentSwitch(argv[2]))
        {
            returnCode(12);
            return 12;
        }
        if(!isDigit(argv[2]) && isSilentSwitch(argv[1]))
        {
            returnCode(12);
            return 12;
        }
    }
    returnCode(13);
    return 13;
}
