#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <algorithm>
#include <ctime>
#include <chrono>
using namespace std;
class big_int{
public:
    vector<char> n;
    // Constructor
    big_int(){}
    // digits range from n[left,right)
    big_int(big_int &a,int left, int right){
        for(int i = left;i < right;i++){
            n.push_back(a[i]);
        }
    }

    // Common operations
    const int size() const{
        return n.size();
    }
    void clear(){
        n.clear();
    }
    void init0(){
        n.clear();
        n.push_back(0);
    }
    char &operator[](const int i){
        return n[i];
    }
    // Plus equal
    big_int &operator+=(const big_int &b){
        int l = min(this->size(),b.size());
        int carry = 0;
        vector<char> &ans = this->n;
        for(int i = 0;i < l;i++){
            ans[i] = ans[i] + b.n[i] + carry;
            if(ans[i] >= 10){
                ans[i] -= 10;
                carry = 1;
            } else {
                carry = 0;
            }

        }
        // If a is longer than b
        for(;l<ans.size();l++){
            ans[l] = ans[l] + carry;
            if(ans[l] >= 10){
                ans[l] -= 10;
                carry = 1;
            } else {
                carry = 0;
            }
        }
        // If b is longer than a
        for(;l<b.size();l++){
            ans.push_back(b.n[l] + carry);
            if(ans[l] >= 10){
                ans[l] -= 10;
                carry = 1;
            } else {
                carry = 0;
            }
        }
        if(carry > 0){
            ans.push_back(carry);
        }
        return *this;
    }

    // Plus operation
    big_int &operator+(const big_int &b){
        big_int &ret = *new big_int(*this);
        ret += b;
        return ret;
    }

    // this must be larger than b
    big_int &operator-=(const big_int &b){
        int carry = 0;
        big_int &a = *this;
        int l = min(a.size(),b.size());
        for(int i = 0;i<l;i++){
            a[i] = a[i] - b.n[i] + carry;
            if(a[i] < 0){
                a[i] += 10;
                carry = -1;
            } else {
                carry = 0;
            }
        }
        for(int i = l;carry<0 && i<a.size();i++){
            a[i] += carry;
            if(a[i] < 0){
                a[i] += 10;
                carry = -1;
            } else {
                carry = 0;
            }
        }
        return a;
    }

    big_int &operator<<(int b){
        big_int &a = *this;
        for(int i = 0;i < b;i++){
            a.n.push_back(0);
        }
        for(int i = a.n.size()-1;i >= b;i--){
            a[i] = a[i-b];
        }
        for(int i = 0;i < b;i++){
            a[i] = 0;
        }
        return a;
    }
    big_int &naive_mul(big_int &b);
    big_int &operator*(big_int &b);

    big_int &operator*(int b){
        big_int &a = *new big_int(*this);
        int carry = 0;
        for(int i = 0;i< a.size();i++){
            a[i] = a[i] * b + carry;
            carry = a[i] / 10;
            a[i] %= 10;
        }
        if(carry > 0){
            a.n.push_back(carry);
        }
        return a;
    }
};
// Stream out operation
ostream &operator<<(ostream &os, big_int &a){
    bool leading_zero = true;
    for(auto rit = a.n.crbegin();rit != a.n.crend(); rit++){
        if(leading_zero && *rit != 0){
            leading_zero = false;
        }
        if(!leading_zero || (rit+1) == a.n.crend() ){
            os<< (char)(*rit + '0');
        }
    }
    return os;
}
// Stream in operation
istream &operator>>(istream &in, big_int &a){
    //first clear n
    a.n.clear();
    string buf;
    in>>buf;
    if(in){
        for(auto rit = buf.crbegin(); rit != buf.crend(); rit++){
            a.n.push_back(*rit - '0');
        }
    } else {
        // Do nothing
    }
    return in;
}
big_int& big_int::naive_mul(big_int &b){
    big_int &res = *new big_int();
    big_int &a = *this;
    res.init0();
    for(int i = 0;i < b.size();i++){
        big_int &t = a * (int)b[i];
        res += (t<<i);
        delete &t;
    }
    return res;
}
big_int& big_int::operator*(big_int &b){
    big_int &a = *this;
    if(a.size() <= 1){
        // when a contains only one digit
        return (b * (int)a[0]);
    } else if(b.size() <= 1){
        // when b contains only one digit
        return (a * (int)b[0]);
    } else {
        int n = min(a.size(),b.size());
        n /= 2;
        big_int &x_l = *new big_int(a,0,n);
        big_int &x_h = *new big_int(a,n,a.size());
        big_int &y_l = *new big_int(b,0,n);
        big_int &y_h = *new big_int(b,n,b.size());

        big_int &x_h_y_h = x_h * y_h;
        big_int &x_l_y_l = x_l * y_l;

        big_int &sum = (x_h + x_l) * (y_h + y_l);
        sum -= (x_h_y_h + x_l_y_l);
        big_int &ans = (x_h_y_h<<(n*2)) + (sum<<n) + x_l_y_l;
        big_int &ret = *new big_int(ans);
        delete &x_l;delete &x_h;delete &y_l;delete &y_h;
        return ret;
    }
}

// below for testing
inline int gen_digit(){
    return rand()%10;
}
inline int gen_not0_digit(){
    return rand()%9+1;
}
big_int& gen_big_int(int len){
    big_int &ret = *new big_int();
    if(len>1){
        ret.n.push_back(gen_not0_digit());
        for(int i = 1;i<len;i++){
            ret.n.push_back(gen_digit());
        }
    } else if(len == 1){
        ret.n.push_back(gen_digit());
    }
    return ret;
}


int main()
{
    freopen("result.out","w",stdout);
    srand(time(NULL));
    int i;
    for(i = 10;i<=40960;i=i<<1){
        big_int a = gen_big_int(i);
        big_int b = gen_big_int(i);
        cout<<i<<endl;
        // Compare multiplication execution time
        auto start = chrono::high_resolution_clock::now();
        big_int &ans1 = a.naive_mul(b);
        //cout<<ans1<<endl;
        auto diff = chrono::duration_cast<chrono::milliseconds>
            (chrono::high_resolution_clock::now()-start);
        cout<<"grade method:"<<diff.count()<<"ms"<<endl;
        delete &ans1;

        start = chrono::high_resolution_clock::now();
        big_int &ans2 = a*b;
        //cout<<ans2<<endl;
        diff = chrono::duration_cast<chrono::milliseconds>
            (chrono::high_resolution_clock::now()-start);
        cout<<"Karatsuba's method:"<<diff.count()<<"ms"<<endl;
        delete &ans2;
        cout<<endl;
    }
    return 0;
}
