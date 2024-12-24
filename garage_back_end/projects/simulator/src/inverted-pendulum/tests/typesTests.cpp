#include <types.h>
#include <iostream>
void print_vector(const Vf &v, std::string str)
{
    std::cout << str << std::endl;
    std::cout << v << std::endl;
}

void construct_vector(Vf &v)
{
    for (int i = 0; i < 10; i++)
    {
        v.push_back(i);
    }
    print_vector(v, "initial");
}

void test_addition_i(const Vf &v)
{
    Vf res = v + 10;
    print_vector(res, "adding 10");
}

void test_addition_f(const Vf &v)
{
    Vf res = v + 10.0;
    print_vector(res, "adding 10.0");
}

void test_addition_v(const Vf &v1, const Vf &v2)
{
    Vf res = v1 + v2;
    print_vector(res, "adding v");
}

void test_multiplication_i(const Vf &v)
{
    Vf res = v * 10;
    print_vector(res, "multiply 10");
}

void test_multiplication_f(const Vf &v)
{
    Vf res = v * 10.0;
    print_vector(res, "multiply 10.0");
}

void test_subtraction_i(const Vf &v)
{
    Vf res = v - 10;
    print_vector(res, "subtracting 10");
}

void test_subtraction_f(const Vf &v)
{
    Vf res = v - 10.0;
    print_vector(res, "subtracting 10.0");
}

void test_subtraction_v(const Vf &v1, const Vf &v2)
{
    Vf res = v1 - v2;
    print_vector(res, "subtracting v");
}

void test_division_f(const Vf &v)
{
    Vf res = v / 10.0;
    print_vector(res, "dividing by 10.0");
}

int main()
{
    std::cout << "Tests starts" << std::endl;
    Vf v;
    construct_vector(v);
    test_addition_i(v);
    test_addition_f(v);
    test_addition_v(v, v);
    test_multiplication_i(v);
    test_multiplication_f(v);
    test_subtraction_i(v);
    test_subtraction_f(v);
    test_subtraction_v(v, v);
    test_division_f(v);
}