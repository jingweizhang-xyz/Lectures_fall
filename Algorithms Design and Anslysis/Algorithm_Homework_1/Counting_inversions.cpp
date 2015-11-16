#include <iostream>
#include <fstream>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <chrono>
using namespace std;
typedef long long LL;
const string file_name("Q5.txt");
// Merge sort part
// Merge c[s,m)(a) and c[m,t)(b) to c[s,t)
vector<int> a;
vector<int> b;
LL merge_count(vector<int> &c,int s,int m,int t){
    LL cnt = 0;
    //vector<int> a(m - s);
    a.resize(m-s);
    for(int i = s;i<m;i++){
        a[i-s] = c[i];
    }
    //vector<int> b(t - m);
    b.resize(t-m);
    for(int i = m;i<t;i++){
        b[i-m] = c[i];
    }

    int i = 0,j = 0,k = s;// a[i], b[j], c[k]
    while(i < a.size() && j< b.size()){
        if(a[i] < b[j]){
            c[k++] = a[i++];
        } else {
            c[k++] = b[j++];
            // inversion counting
            cnt += a.size() - i;
        }
    }
    while(i < a.size()){
        c[k++] = a[i++];
    }
    while(j < b.size()){
        c[k++] = b[j++];
    }
    return cnt;
}

LL count_inversions_merge_sort(vector<int> &v,int s,int t){
    LL cnt = 0;
    if(t-s>1){
        int m = (s + t) / 2;
        LL cnt_l = count_inversions_merge_sort(v,s,m);
        LL cnt_r = count_inversions_merge_sort(v,m,t);
        LL cnt_m = merge_count(v,s,m,t);
        cnt = cnt_l + cnt_r + cnt_m;
    } else {
        //contains only one or 0 elements
        cnt = 0;
    }
    return cnt;
}

// returns the index of pivot
vector<int> larger;
int partition_count(vector<int> &v,int s,int t,LL &cnt){
    int pi = rand() % (t - s) + s;
    int p = v[pi];
    //vector<int> larger;
    larger.clear();
    int j = s;// smaller part: v[s,j)
    for(int i = s;i<t;i++){
        if(i == pi) {
            continue;
        }
        if(v[i] < p){
            // pivot inversion
            if(i > pi){
                cnt++;
            }
            // v[i] inversion
            cnt += larger.size();
            v[j++] = v[i];
        } else if(v[i] > p){
            // pivot inversion
            if(i < pi){
                cnt++;
            }
            larger.push_back(v[i]);
        }
    }
    int m = j;
    v[m] = p;
    for(int i = 0;i<larger.size();i++){
        v[m+i+1] = larger[i];
    }
    return m;
}

LL count_inversions_quict_sort(vector<int> &v,int s,int t){
    LL cnt = 0;
    if(t-s>1){
        int m = partition_count(v,s,t,cnt);
        LL cnt_l = count_inversions_quict_sort(v,s,m);
        LL cnt_r = count_inversions_quict_sort(v,m+1,t);
        cnt += (cnt_l + cnt_r);
    }
    return cnt;
}


int main()
{
    vector<int> s;

    // Input part
    ifstream s_file;
    s_file.open(file_name);
    int a;
    while(s_file>>a){
        s.push_back(a);
    }
    s_file.close();

    // Merge Sort part;
    vector<int> m(s);
    auto start = chrono::high_resolution_clock::now();
    cout<<count_inversions_merge_sort(m,0,m.size())<<"\t";
    auto diff = chrono::duration_cast<chrono::milliseconds>
        (chrono::high_resolution_clock::now()-start);
    cout<<diff.count()<<"ms"<<endl;
    // Quick Sort part
    vector<int> q(s);
    start = chrono::high_resolution_clock::now();
    cout<<count_inversions_quict_sort(q,0,q.size())<<"\t";
    diff = chrono::duration_cast<chrono::milliseconds>
        (chrono::high_resolution_clock::now()-start);
    cout<<diff.count()<<"ms"<<endl;
    return 0;
}
