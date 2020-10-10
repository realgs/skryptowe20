#include "iostream"
#include <cstdlib>
using namespace std;


int main(int argc, char *argv[], char **envp)
{
    for (char **env = envp; *env != 0; env++)
    {
    char *thisEnv = *env;
    cout<<thisEnv<<endl;
    }
    for(int i = 1; i < argc; i++)
    {
        cout<<argv[i]<<endl;
    }
}
