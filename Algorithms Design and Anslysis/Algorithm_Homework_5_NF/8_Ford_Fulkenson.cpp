#include<iostream>
#include<cstdio>
#include<fstream>
#include<sstream>
#include<cstdlib>
#include<climits>
#include<vector>
#include<algorithm>

using namespace std;
const string file_name("problem1.data");
struct Edge{
    int to;
    int cap;
    int rev;
    Edge(int tt,int cc, int rr):to(tt),cap(cc),rev(rr){}
};
vector<vector<Edge>> graph;
vector<bool> vis;

inline void init_graph(int num_nodes){
    graph.clear();
    graph.assign(num_nodes,vector<Edge>());
    vis.resize(num_nodes);
}


inline void add_edge(int from, int to, int cap){
    graph[from].push_back(Edge(to, cap, graph[to].size()));
    graph[to].push_back(Edge(from, 0, graph[from].size() - 1));
}

bool get_graph(istream& in){
    string str;
    int m,n;
    bool is_end = true;
    while(getline(in, str)){
        if(str[0] != '#'){
            stringstream ss(str);
            ss>>m>>n;
            is_end = false;
            break;
        }
    }
    if(!is_end){
        init_graph(m+n+2);// m girls + n boys + s + t
        int c;
        int from,to;
        // index range of girls: [1, m+1)
        // index range of boys:[m+1, m+n]
        // s: 0,  t: m+n+1
        for(int i = 1;i <= m;i++){
            getline(in,str);
            stringstream ss(str);
            ss>>c;
            from = i;
            for(int j = 0;j<c;j++){
                ss>>to;
                to += m;
                add_edge(from, to, 1);
            }
        }
        int s = 0, t = m + n + 1;
        for(int i = 1;i <= m + n;i++){
            if(i <= m){
                add_edge(s, i, 1);
            } else {
                add_edge(i, t, 1);
            }
        }
    }
    return !is_end;
}

int dfs(int s, int t, int min_flow){
    if(s == t){
        return min_flow;
    }
    vis[s] = true;
    for(Edge& e:graph[s]){
        if(!vis[e.to] && e.cap > 0){
            min_flow = min(min_flow, e.cap);
            int f = dfs(e.to, t, min_flow);
            if(f > 0){
                // Reduce cap on e and increase cap on rev
                e.cap -= f;
                graph[e.to][e.rev].cap += f;
                return f;
            }
        }
    }
    return 0;
}

int max_flow(int s, int t){
    int flow = 0;
    int f = 0;
    while(true){
        for(int i = 0;i<vis.size();i++){
            vis[i] = 0;
        }
        f = dfs(s,t,INT_MAX);
        flow += f;
        if(f == 0) {
            break;
        }
    }
    return flow;
}

int main()
{
    // Input part
    ifstream s_file;
    s_file.open(file_name);
    while(get_graph(s_file)){
        int flow = max_flow(0,graph.size()-1);
        cout<<flow<<endl;
    }
    s_file.close();
    return 0;
}
