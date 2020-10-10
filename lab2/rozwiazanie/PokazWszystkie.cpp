#include "iostream"
#include <cstdlib>
using namespace std;


int main(int argc, char *argv[])
{
    cout<<getenv("PATH")<<endl;
    for(int i = 1; i < argc; i++)
    {
        cout<<argv[i]<<endl;
    }
}
