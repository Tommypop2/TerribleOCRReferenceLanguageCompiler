
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
auto bubbleSort(){std::vector<int> x = {3,2,1};while(true) {auto swaps = 0;for(auto i = 1; i<len(x); i++){if(x[i-1] > x[i]) {auto temp = x[i-1]; x[i-1] = x[i]; x[i] = temp;swaps = swaps + 1;}}if(swaps == 0) {break;}}return(x);}
int main()
{
    std::srand(time(0));
    while(true) {if(1 == 1) {std::cout << "Sup Top G" << '\n';auto result = bubbleSort();for(auto n = 0; n<len(result); n++){std::cout << result[n] << '\n';}}break;}
}
