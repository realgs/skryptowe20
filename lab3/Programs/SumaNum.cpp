#include <iostream>
#include <string>

int main(int argc, char** argv, char** envp)
{
    std::string word;
    double sum = 0;
    while (std::cin >> word) 
    {
        double number = 0;
        try 
        {
            number = std::stod(word);
        }
        catch (std::invalid_argument)
        {
            
        }
        sum += number;
    }
    std::cout << sum;
    return 0;
}
