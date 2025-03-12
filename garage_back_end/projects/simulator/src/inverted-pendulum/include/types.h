#pragma once

#include <vector>
#include <ostream>
#include <iostream>
class InvalidSizes : public std::exception
{
public:
    const char *what() const noexcept override
    { // what is char *
        return "Vectors have different sizes";
    }
};

template <typename T>
class Vector
{
public:
    Vector(const std::vector<T> &vector) : internal_vector_(vector){};
    Vector(){};
    std::vector<T> get_internal_vector() const { return internal_vector_; };
    void set_internal_vector(std::vector<T> internal_vector) { internal_vector_ = internal_vector; };
    int size() const { return internal_vector_.size(); };
    void push_back(const T el) { internal_vector_.push_back(el); }
    void reserve(const int &i){internal_vector_.reserve(i);};
    T at(const int &pos) { return internal_vector_.at(pos); };
    T &operator[](const int &i) { return internal_vector_[i] ;};

private:
    std::vector<T> internal_vector_;
};

template <typename T>
Vector<T> operator*(const Vector<T> &v, const float &f)
{
    Vector<T> res;
    for (auto &el : v.get_internal_vector())
    {
        res.push_back(el * f);
    }
    return res;
}

template <typename T>
Vector<T> operator*(const float &f, const Vector<T> &v)
{
    return v * f;
}

template <typename T>
Vector<T> operator+(const Vector<T> &v, const float &f)
{
    Vector<T> res;
    for (auto &el : v.get_internal_vector())
    {
        res.push_back(el + f);
    }
    return res;
}

template <typename T>
Vector<T> operator+(const float &f, const Vector<T> &v)
{
    return v + f;
}

template <typename T>
Vector<T> operator+(const Vector<T> &v1, const Vector<T> &v2)
{
    if (v1.size() != v2.size())
    {
        throw InvalidSizes();
    }

    Vector<T> res;
    std::vector<T> _v1 = v1.get_internal_vector();
    std::vector<T> _v2 = v2.get_internal_vector();
    auto it_1 = _v1.begin();
    auto it_2 = _v2.begin();
    while (it_1 != _v1.end())
    {
        res.push_back(*it_1 + *it_2);
        it_1 = std::next(it_1);
        it_2 = std::next(it_2);
    }

    return res;
}

template <typename T>
Vector<T> operator-(const float &f, const Vector<T> &v)
{
    return f + (-1) * v;
}

template <typename T>
Vector<T> operator-(const Vector<T> &v, const float &f)
{
    return v + (-1) * f;
}

template <typename T>
Vector<T> operator-(const Vector<T> &v1, const Vector<T> &v2)
{
    return v1 + (-1) * v2;
}

template <typename T>
Vector<T> operator/(const Vector<T> &v, const float &f)
{
    return v * (1 / f);
}

template <typename T>
std::ostream &operator<<(std::ostream &os, const Vector<T> &v)
{
    const std::vector<T> &v_std = v.get_internal_vector();
    os << "[";
    for (auto &el : v_std)
    {
        os << el;
        if (&el != &v_std.back())
        {
            os << ", ";
        }
    }
    os << "]";
    return os;
}

typedef Vector<float> Vf;
typedef std::lock_guard<std::mutex> guard;