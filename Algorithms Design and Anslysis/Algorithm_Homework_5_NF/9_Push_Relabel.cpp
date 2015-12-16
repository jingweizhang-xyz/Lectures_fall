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

inline void init_graph(int num_nodes){
    graph.clear();
    graph.assign(num_nodes,vector<Edge>());
}

inline void add_edge(int from, int to, int cap){
    graph[from].push_back(Edge(to, cap, 0,graph[to].size()));
    graph[to].push_back(Edge(from, 0, 0,graph[from].size() - 1));
}

inline int matrix_index(int n, int r, int c){
    return (r-1) * n + c;
}

bool get_graph(istream& in, int& cap){
    string str;
    int m,n;// m rows and n columns
    bool is_end = true;
    while(getline(in, str)){
        if(str[0] != '#'){
            stringstream ss(str);
            ss>>m>>n;
            is_end = false;
            break;
        }
    }
    cout<<"m:"<<m<<", n:"<<n<<"\t total:"<<m * n + m + n + 2<<endl;
    //cout<<"debug: get m,n end."<<endl;
    if(!is_end){
        // m * n matrix nodes
        // + m row sum nodes + n cloumn sum nodes
        // + s + t
        init_graph(m * n + m + n + 2);
        cap = 0;
        // index range of matrix [1, m*n]
        // index range of row sum [m*n + 1, m*n +m]
        // index range of col sum [m*n + m + 1, m*n + m + n]
        // s: 0,  t: m*n + m + n + 1
        getline(in,str);
        stringstream ssm(str);
        vector<int> r(m + 1);// row
        for(int i = 1;i <= m;i++){
            ssm>>r[i];
            cap += r[i];
        }
        getline(in,str);
        stringstream ssn(str);
        vector<int> c(n + 1);// column
        for(int i = 1;i <= n;i++){
            ssm>>c[i];
            cap += c[i];
        }
        //cout<<"debug: get counted number of row and column"<<endl;
        int s = 0, t = m * n + m + n + 1;
        // s -> matrix nodes
        for(int i = 1; i <= m * n;i++){
            add_edge(s, i, 1);
        }
        //cout<<"debug: s -> m nodes end."<<endl;
        // matrix nodes -> row nodes -> t
        for(int i = 1; i <= m; i++){
            int to = m * n + i;
            for(int j = 1; j<= n; j++){
                //cout<<"\t m: "<<m<<", i:"<<i<<", j:"<<j<<endl;
                int from = matrix_index(n, i, j);
                //cout<<"\t m->r: add_edge: "<<from<<", "<<to<<"\t total: "<<graph.size()<<endl;
                add_edge(from, to, 1);
            }
            //cout<<"\tadd_edge: "<<to<<", "<<t<<endl;
            add_edge(to, t, r[i]);
            //cout<<"\t\tadd_edge ends."<<endl;
        }
        //cout<<"debug: m nodes -> row nodes -> t end."<<endl;
        // matrix nodes -> column nodes -> t
        for(int j = 1; j<= n; j++){
            int to = m * n + m +j;
            for(int i = 1; i <= m; i++){
                int from = matrix_index(n, i, j);
                add_edge(from, to, 1);
            }
            add_edge(to, t, c[j]);
        }
    }
    //cout<<"debug: get_graph ends."<<endl;
    return !is_end;
}

void show_graph(){
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
            if(excess[i] > 0){
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
                //if(e.flow >= 0)
            }
        }
        if(excess[v] > 0){
            // Relabel v
            h[v]++;
        }
    }

    return flow;
}

int main()
{
    // Input part
    ifstream s_file;
    s_file.open(file_name);
    // string str;
    int cap;
    while(get_graph(s_file, cap)){
        // cin>>str;
        int flow = max_flow(0,graph.size()-1);
        cout<< ((flow == cap)?"true":"false") <<endl;
    }
    s_file.close();
    return 0;
}
