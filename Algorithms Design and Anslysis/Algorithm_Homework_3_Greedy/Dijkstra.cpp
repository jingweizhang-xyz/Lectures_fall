#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <queue>
#include <algorithm>
#include <ctime>
#include <climits>
#include <chrono>
#include <boost/timer.hpp>
#include <boost/heap/d_ary_heap.hpp>
#include <boost/heap/binomial_heap.hpp>
#include <boost/heap/fibonacci_heap.hpp>

using namespace std;
using namespace boost::heap;

const string file_name("graph.txt");
const int INF = INT_MAX;

struct Edge{
    int s; // start
    int t; // tail
    int w; // weight
    Edge(){}
    Edge(int ss,int tt,int ww):s(ss),t(tt),w(ww){}
};

vector< vector<Edge> > get_graph(){
    vector< vector<Edge> > graph;
    ifstream s_file;
    s_file.open(file_name);
    string str;
    int s,t,w;
    while(getline(s_file,str)){
        if(str.size() <=0 || str[0] == '#'){
            continue;
        } else {
            stringstream ss(str);
            ss>>s>>t>>w;
            while(graph.size() < s + 1 || graph.size() < t + 1){
                graph.push_back(vector<Edge>());
            }
            graph[s].push_back(Edge(s,t,w));
            graph[t].push_back(Edge(t,s,w));
        }
    }
    s_file.close();
    return graph;
}

struct Vertex{
    int v;
    int w;
    Vertex(){}
    Vertex(int vv,int ww):v(vv),w(ww){}
    bool operator<(Vertex const &a) const{
        return w>a.w;
    }
    bool operator>(Vertex const &a) const{
        return w<a.w;
    }
};

template<class Heap>
int Dijkstra_shortest_path(const vector< vector<Edge> > &graph,
                           int s, int t, Heap &heap,
                           bool store_pre, vector< vector<int> > &pre){
    int ans = 0;
    // initial part
    int n = graph.size();
    typedef typename Heap::handle_type handle_t;
    vector<handle_t> handles;
    handles.resize(n);
    vector<bool> vis;
    vis.resize(n);
    vector<int> dis; // distance from s
    dis.resize(n);
    heap.clear();

    // initial previous vertics
    if(store_pre){
        pre.clear();
        pre.resize(n);
        for(int i = 0;i < n;i++){
            pre[i] = vector<int>();
        }
    }

    // initial vertics weight
    // 0 for s and INF for others
    for(int i = 0;i<n;i++){
        const handle_t &h = heap.push(Vertex(i,i==s?0:INF));
        handles[i] = h;
        vis[i] = false;
        dis[i] = i==s?0:INF;
    }

    while(!heap.empty() && !vis[t]){
        const Vertex &v_top = heap.top();
        int u = v_top.v;
        vis[u] = true;
        heap.pop();
        // update all vertex v adjcent to u (u -> v)
        for(const Edge &e: graph[u]){
            int v = e.t;
            if(vis[v] == true){
                continue;
            }

            if(dis[v] - e.w > dis[u]){ // to prevent overflow
                // relax v
                handle_t &handle_v = handles[v];
                int new_dis = dis[u] + e.w;
                dis[v] = new_dis;
                heap.increase(handle_v, Vertex(v, new_dis));
                if(store_pre){
                    pre[v].clear();
                    pre[v].push_back(u);
                }
            } else if(store_pre && dis[v] - e.w == dis[u]) {
                // add pre
                pre[v].push_back(u);
            }

        }
    }
    ans = dis[t];
    return ans;
}

int Dijkstra_shortest_path_pq(const vector< vector<Edge> > &graph,
                           int s, int t){
    int ans = 0;
    // initial part
    int n = graph.size();
    vector<bool> vis;
    vis.resize(n);
    vector<int> dis; // distance from s
    dis.resize(n);
    std::priority_queue<Vertex> heap;

    // initial vertics weight
    // 0 for s and INF for others
    for(int i = 0;i<n;i++){
        heap.push(Vertex(i,i==s?0:INF));
        vis[i] = false;
        dis[i] = i==s?0:INF;
    }
    const Vertex &top = heap.top();

    while(!heap.empty() && !vis[t]){
        const Vertex &v_top = heap.top();
        int u = v_top.v;
        vis[u] = true;
        heap.pop();
        if(dis[u] < v_top.w){
            continue;
        }
        // update all vertex v adjcent to u (u -> v)
        for(const Edge &e: graph[u]){
            int v = e.t;
            if(vis[v] == true){
                continue;
            }
            if(dis[v] - e.w > dis[u]){ // to prevent overflow
                int new_dis = dis[u] + e.w;
                dis[v] = new_dis;
                heap.push(Vertex(v, new_dis));

            }
        }
    }
    ans = dis[t];
    return ans;
}

int Dijkstra_shortest_path_vector(const vector< vector<Edge> > &graph,
                                  int s, int t){
    int ans = 0;
    int n = graph.size();

    vector<int> v;
    vector<bool> vis;
    for(int i = 0;i < n;i++){
        v.push_back(INF);
        vis.push_back(false);
    }
    v[s] = 0;

    int left = n;
    while(left > 0){
        // Pick minium vertex(index) in array v
        int min_value = INF;
        int min_idx = -1;
        for(int i = 0;i<v.size();i++){
            if(!vis[i] && v[i] < min_value){
                min_value = v[i];
                min_idx = i;
            }
        }
        if(min_idx == t){ // t is already in SP
            break;
        }

        // relax all edges incident to this vertex
        int v_min = min_idx;
        vis[v_min] = true;
        left--;
        for(const Edge &e: graph[v_min]){
            if(!vis[t]){
                v[e.t] = min(v[e.t], v[e.s] + e.w);
            }
        }
    }

    ans = v[t];
    return ans;
}

// Problem 2
void counting_DFS(const vector<vector<int>> g,
                  int s,
                  vector<int> &before, vector<int> &after){
    // s -> v
    before[s]++;
    int ans = 0; // store the pathes after node s
    if(g[s].size() == 0) { // reaching the tail node
        ans = 1;
    }
    for(int v: g[s]){
        counting_DFS(g,v,before,after);
        ans += after[v];
    }
    after[s] = ans;
}

vector<int> counting_SP_on_nodes(const vector<vector<int>> &pre,
                                 int t){
    int n = pre.size();
    vector<int> ans(n, 0);
    vector<int> before(n, 0);
    vector<int> after(n, 0);

    counting_DFS(pre,t,before,after);

    for(int i = 0;i < n;i++){
        ans[i] = before[i] * after[i];
    }
    return ans;
}

int main()
{
    // Input, graph is a adjcency list
    const vector< vector<Edge> > &graph = get_graph();
    int V = graph.size();

    // Randomly choose starting vertex and ending vertex
    int s,t;
    srand(time(NULL));
    s = rand() % V;
    t = rand() % V;
    cout<<"starting from "<<s<<" to "<<t<<", all "<<V<<" vertics"<<endl;

    // Dijkstra's shortest path:
    vector< vector<int> > pre; // record the previous vertics
    // 1） linked list
    boost::timer timer_1;
    vector<double> time;
    time.push_back(timer_1.elapsed());
    int ans = Dijkstra_shortest_path_vector(graph,s,t);
    time.push_back(timer_1.elapsed());
    cout<<"array like: "<<ans<<"\t"
        <<time[time.size()-1] - time[time.size()-2]<<"seconds"<<endl;

    // 2) binary heap
    time.push_back(timer_1.elapsed());
    int ans_b_heap = Dijkstra_shortest_path_pq(graph,s,t);
    time.push_back(timer_1.elapsed());
    cout<<"binary heap: "<<ans<<"\t"
        <<time[time.size()-1] - time[time.size()-2]<<"seconds"<<endl;


    // 3) binomial heap
    binomial_heap<Vertex> bin_heap;
    time.push_back(timer_1.elapsed());
    int ans_bin_heap = Dijkstra_shortest_path(graph,s,t,bin_heap, false, pre);
    time.push_back(timer_1.elapsed());
    cout<<"binomial heap: "<<ans_bin_heap<<"\t"
        <<time[time.size()-1] - time[time.size()-2]<<"seconds"<<endl;

    // 4) fibonacci_heap
    fibonacci_heap<Vertex> fib_heap;
    time.push_back(timer_1.elapsed());
    int ans_fib_heap = Dijkstra_shortest_path(graph,s,t,fib_heap, false, pre);
    time.push_back(timer_1.elapsed());
    cout<<"fibonacci heap: "<<ans_fib_heap<<"\t"
        <<time[time.size()-1] - time[time.size()-2]<<"seconds"<<endl;

    // problem 2 counting pathes
    Dijkstra_shortest_path(graph,s,t,fib_heap, true, pre);
    vector<int> num = counting_SP_on_nodes(pre,t);
    for(int i = 0;i<num.size();i++){
        if(num[i] > 0 && i != s && i != t){
            cout<<"\tnode "<<i<<": "<<num[i]
                <<" path"<<(num[i]>1?"es":"")<<endl;
        }
    }
    return 0;
}
