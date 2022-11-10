
#include <iostream>
#include <time.h>
#include <string>
#include <vector>
std::string getInput(std::string prompt)
{
    std::cout << prompt;
    std::string data = "";
    std::getline(std::cin, data);
    return data;
}
int len(std::vector<int> lst)
{
    return lst.size();
}
auto sum(int n1, int n2) { return (n1 + n2); }
int main()
{
    std::srand(time(0));
    for (auto i = 0; i < 9; i++)
    {
        for (auto n = 1; n < 10; n++)
        {
            auto z = 2;
        }
    }
}
