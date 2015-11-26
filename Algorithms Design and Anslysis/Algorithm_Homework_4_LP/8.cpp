#include <iostream>
#include <cstdio>
#include <vector>
#include <cstdlib>
#include <algorithm>

using namespace std;

const int EPS = 1E-5;

struct Edge{
    int t;
    int w;
    bool reversed;
    Edge(){}
    Edge(int tt,int ww,bool rr):t(tt),w(ww),reversed(rr){}
};

vector< vector<Edge> > g; // graph, adjcency list
vector<int> x;// vertics
int sum; // the objective function value

void get_input(){
    int s,t,w;
    g.clear();

    while(cin>>s>>t>>w){
        while(s >= g.size() || t >= g.size()){
            g.push_back(vector<Edge>());
        }
        g[s].push_back(Edge(t, w, false));
        g[t].push_back(Edge(s, -w, true));
    }

}

void BFS(){
    x.resize(g.size());
    x[1] = 0;

    vector<int> q;// queue
    int tail = 0;// points to the tail of queue
    q.push_back(1);

    vector<bool> vis(x.size(), false);
    while(tail < q.size()){
        int u = q[tail++];
        vis[u] = true;
        for(Edge &e: g[u]){
            int v = e.t;
            if(!vis[v]){
                x[v] = x[u] - e.w;
                q.push_back(v);
            }
        }
    }

}

void solve(){
    BFS();
    // optimization
    vector<int> weights;
    bool is_conv = false;
    //int cnt = 0;
    while(!is_conv){
        //cout<<"\t"<<++cnt<<endl;
        is_conv = true;
        for(int u = 1;u < g.size();u++){
            weights.clear();
            for(Edge &e: g[u]){
                weights.push_back(x[e.t] + e.w);
            }
            //cout<<"\t"<<weights.size()<<endl;
            nth_element(weights.begin(),
                        weights.begin() + weights.size() / 2,
                        weights.end());
            int new_x = weights[weights.size() / 2];
            if(abs(new_x - x[u]) > EPS){
                is_conv = false;
                x[u] = new_x;
            }
        }
    }
    // make x[0] be 0
    for(int i = x.size()-1;i >= 1;i--){
        x[i] -= x[1];
    }
    //for(int w: x){cout<<w<<endl;}
    // compute the objective function value
    sum = 0;
    for(int u = 1;u < g.size(); u++){
        for(Edge &e:g[u]){
            if(!e.reversed){
                int v = e.t;
                sum += abs(x[u] - x[v] - e.w);
            }
        }
    }
}

int main()
{
    freopen("8_CInput.in","r",stdin);
    get_input();
    solve();
    cout<<sum<<endl;
    return 0;
}
