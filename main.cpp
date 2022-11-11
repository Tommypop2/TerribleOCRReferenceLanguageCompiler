
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
auto yes(int y) { std::cout << y << '\n'; }
int main()
{
    std::srand(time(0));
    std::vector<int> x = {1, 2, 3};
    while (true)
    {
        if (1 == 1)
        {
            std::cout << "Sup Top G" << '\n';
            yes(x[1]);
        }
        break;
    }
}
