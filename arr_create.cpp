#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
 
 using namespace std;
 
 vector<string> split (string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    vector<string> res;

    while ((pos_end = s.find (delimiter, pos_start)) != string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}
 
 
int main()
{
    std::string line;
    std::string token; 
    std::string delimiter_0 = "\n";
    std::string delimiter_1 = ";"; 
    std::ifstream in("/media/sadko/1b32d2c7-3fcf-4c94-ad20-4fb130a7a7d4/PLAYGROUND/intermediate-option/out/file_arr_temp_v1.txt"); // окрываем файл для чтения
    if (in.is_open())
    {
        while (getline(in, line))
        {
        
            vector<string> v = split (line, delimiter_0);
            v = split (v[0], delimiter_1);
//            cout << v.data() << endl;    
            cout << v[0] << endl; // ID user
            cout << v[1].size() << endl; // array  
              
        }
    }
    in.close();     // закрываем файл
     
    std::cout << "Конец программы" << std::endl;
    return 0;
}


