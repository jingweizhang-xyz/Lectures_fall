#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <algorithm>

using namespace std;

const int MIN = 0;
const int MAX = 2000;
const int N = 1000;

int rand_between(int a, int b){
    if(a>b) swap(a,b);
    return rand() % (b - a) + a;
}

int main()
{
    srand(time(NULL));
    //freopen(".in","r",stdin);
    freopen("stocks.in","w",stdout);

    for(int i = 0;i < N;i++){
        printf("%d ", rand_between(MIN, MAX));
    }
    printf("\n");

    return 0;
}
