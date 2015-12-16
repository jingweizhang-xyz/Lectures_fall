#include<iostream>
#include<cstdio>
#include<fstream>
#include<sstream>
#include<cstdlib>
#include<climits>
#include<vector>
#include<algorithm>

using namespace std;
const string file_name("problem2.data");
struct Edge{
    int to;
    int cap;
    int flow;
    int rev;
    Edge(int tt,int cc, int ff,int rr):
        to(tt),cap(cc),flow(ff),rev(rr){}
};
vector<vector<Edge>> graph;
int m,n;// m rows and n columns
vector<int> r;// row
vector<int> c;// column
inline void init_graph(int num_nodes){
    graph.clear();
    graph.assign(num_nodes,vector<Edge>());
}

inline void add_edge(int from, int to, int cap){
    graph[from].push_back(Edge(to, cap, 0,graph[to].size()));
    graph[to].push_back(Edge(from, 0, 0,graph[from].size() - 1));
}

inline int matrix_index(int r, int c){
    return (r-1) * n + c;
}

bool get_graph(istream& in, int& cap){
    string str;
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
        // m row nodes + n cloumn nodes + s + t
        init_graph(m + n + 2);
        // index range of row [1, m]
        // index range of col [m + 1, m + n]
        // s: 0,  t: m + n + 1
        getline(in,str);
        stringstream ssm(str);
        r.assign(m + 1, 0);
        c.assign(n + 1, 0);
        for(int i = 1;i <= m;i++){
            ssm>>r[i];
        }
        getline(in,str);
        stringstream ssn(str);
        for(int i = 1;i <= n;i++){
            ssn>>c[i];
        }
        int s = 0, t = m + n + 1;
        // s -> row nodes
        for(int i = 1; i <= m;i++){
            add_edge(s, i, r[i]);
        }
        // column nodes -> t
        for(int i = 1; i <= n;i++){
            add_edge(i + m, t, c[i]);
        }
        // row nodes -> column nodes
        for(int i = 1;i <= m;i++){
            for(int j = 1;j <= n;j++){
                add_edge(i, j + m, 1);
            }
        }
    }
    return !is_end;
}

void show_graph(){
    // for debug
    for(int i = 0;i< graph.size();i++){
        cout<<i<<":";
        for(Edge &e: graph[i]){
            cout<<" ["<<e.to<<","<<e.cap<<"]";
        }cout<<endl;
    }
}

int max_flow(int s, int t){
    int flow = 0;
    int N = graph.size();
    vector<int> h(N, 0); // Height of every nodes
    vector<int> excess(N, 0);
    // Initial pre-flow
    h[s] = N;
    for(Edge &e:graph[s]){
        e.flow += e.cap;
        graph[e.to][e.rev].flow -= e.cap;
        excess[e.to] += e.cap;
    }

    while(true){
        bool stop = true;
        int v; // find E(v) > 0
        for(int i = 0;i < N;i++){
            if(excess[i] > 0 && i != s && i != t){
                stop = false;
                v = i;
                break;
            }
        }
        if(stop) break;
        for(Edge &e: graph[v]){
            if(excess[v] <= 0) {
                break;
            }
            int w = e.to;
            if(h[v] > h[w]){
                // Push excess: v->w
                int amt = min(excess[v], e.cap - e.flow);
                e.flow += amt;
                graph[w][e.rev].flow -= amt;
                excess[v] -= amt;
                excess[w] += amt;
            }
        }
        if(excess[v] > 0){
            // Relabel v
            h[v] = 2*N;
            for(Edge& e:graph[v]){
                if(e.cap - e.flow > 0){
                    h[v] = min(h[v], h[e.to]+1);
                }
            }
        }
    }
    for(Edge& e: graph[s]){
        flow += e.flow;
    }
    return flow;
}
vector<vector<int>> get_matrix(){
    vector<vector<int>> matrix(m + 1,vector<int>(n + 1,0));
    for(int i = 1;i<=m;i++){
        for(Edge& e: graph[i]){
            if(e.flow > 0){
                int j = e.to - m;
                matrix[i][j] = 1;
            }
        }
    }
    return matrix;
}

bool check_matrix(){
    vector<vector<int>> matrix = get_matrix();
    bool is_right = true;
    vector<int> check_r(m + 1, 0);
    vector<int> check_c(n + 1, 0);
    for(int i = 1;i <= m;i++){
        for(int j = 1;j <= n;j++){
            if(matrix[i][j] >= 1){
                check_r[i]++;
                check_c[j]++;
            }
        }
    }
    for(int i = 1;i <= m;i++){
        if(check_r[i] != r[i]){
            is_right = false;
            break;
        }
    }
    for(int j = 1;j <= n;j++){
        if(check_c[j] != c[j]){
            is_right = false;
            break;
        }
    }
    return is_right;
}

int main()
{
    // Input part
    ifstream s_file;
    s_file.open(file_name);
    //string str;
    int cap;
    while(get_graph(s_file, cap)){
        //show_graph();
        //cin>>str;
        int flow = max_flow(0,graph.size()-1);
        cout<<"flow: "<<flow<<endl;
        bool is_right = check_matrix();
        cout<<"check result: "<<(is_right?"right":"error")<<"."<<endl;

    }
    s_file.close();
    return 0;
}
