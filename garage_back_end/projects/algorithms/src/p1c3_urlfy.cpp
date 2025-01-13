/*
 Write a method to replace all spaces in a string with '%20'. You may assume that the string
has sufficient space at the end to hold the additional characters,and that you are given the "true"
length of the string. (Note: If implementing in Java, please use a character array so that you can
perform this operation in place.)

Input:"Mr John Smith    ",13
Output:"Mr%20John%20Smith"
*/

#include "p1c3_urlfy.h"

// O(N)
void replace_spaces(std::string &str){
    std::string::iterator move_to_it = str.end()-1;
    bool is_first = true;
    for (std::string::iterator str_it=str.end()-1; str_it>=str.begin(); str_it--){
        if (!(bool)isspace(*str_it)){
            is_first = false;
        }
        if (!(bool)isspace(*str_it)){
            *move_to_it = *str_it;
            --move_to_it;
        }
        if ((bool)isspace(*str_it) && !is_first){
            *move_to_it = '0';
            --move_to_it;
            *move_to_it = '2';
            --move_to_it;
            *move_to_it = '%';
            --move_to_it; 
        }
    }

}