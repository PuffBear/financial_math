#include<iostream>
#include<fstream>
#include<vector>
#include<string>

using namespace std;

string token;

vector<string>tokenise(string csvLine, char separator)
{
    vector<string>tokens;
    signed int start, end;
    start = csvLine.find_first_not_of(separator, 0);
    do {
        end = csvLine.find_first_of(separator, 0);
        if(start == csvLine.length() || start == end)
            break;
        if(end>=0)
            token = csvLine.substr(start, end-start);
        else
            token = csvLine.substr(start, csvLine.length()-start);
        tokens.push_back(token);
        start = end + 1;
    }
    while(end>0);

    return tokens;
}

int main()
{
    vector<string>tokens;

    ifstream csvFile("PixarMovies.csv");
    string line;

    if(csvFile.is_open())
    {
        cout<<"File Open"<<endl;
        while(getline(csvFile, line))
        {
            std::cout << " ===== Read Line =====" << std::endl;
			tokens = tokenise(line, ',');
			if(tokens.size() != 16) //Bad Line
			{
				std::cout << "Bad Line" << std::endl;
				continue;
			}


            try{
				double rt = std::stod(tokens[3]);
				double imdb = std::stod(tokens[4]);
				std::cout << rt << " : " << imdb << std::endl;
			}catch(std::exception& e){
				std::cout << "Bad Float! " << tokens[3] << std::endl;
				std::cout << "Bad Float! " << tokens[4] << std::endl;
			}
        }
    }
    else
    {
        cout<<"File is NOT open"<<endl;
    }
}