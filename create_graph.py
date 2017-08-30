import plotly
from plotly.graph_objs import *

from bs4 import BeautifulSoup
from urllib.request import urlopen, HTTPError
import igraph as ig
#make globals to hold node, edge, and node count
_node_number = 0
_nodes = {}
_edges = []

#populates node and edge data by scraping the given link
#and scraping each of its children nodes for num_nodes generations
#take care since this can scrape sites exponentially
def populate_node_and_edge_data(link_name, num_nodes):
    global _node_number, _nodes, _edges

    if num_nodes > 0:
        try:
            url = link_name
            content = urlopen(url).read()
            soup = BeautifulSoup(content)

            current_node = _node_number
            for a in soup.find_all('a', href=True):
                #allow one facebook and one twitter per page
                if a['href'][:5] == "https":
                    _node_number += 1
                    print ("[",_node_number,"] ","retrieving site: ", a['href'],"...")
                    #add the parent source number and childnodenumber
                    _edges.append((current_node, _node_number))
                    #num_nodes is the current generation of child(differentiates the color of nodes by generation)
                    _nodes[_node_number] = (link_name, num_nodes)
                    #populate data for all children of this node as well
                    populate_node_and_edge_data(a['href'], (num_nodes-1))
        except HTTPError:
            print("error recieved from HTTP request in populate_node_and_edge_data")
            print ("this is probably due to trying to request a forbidden site")
            print ("")


def create_3d_Network(link_name, num_nodes):
    print("creating...")
    #initialize for first parent node
    global _node_number, _nodes
    _nodes[_node_number] = link_name
    #populate data
    populate_node_and_edge_data(link_name, num_nodes+3)

    #begin construction of the 3d network graph
    G=ig.Graph(_edges, directed=False)

    labels=[]
    group=[]
    number_of_nodes = len(_nodes)

    for i in range(0, number_of_nodes):
         labels.append(_nodes[i][0])
         #group just changes the color
         group.append(_nodes[i][1])

    layt = G.layout('kk', dim=3)

    Xn=[layt[k][0] for k in range(number_of_nodes)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(number_of_nodes)]# y-coordinates
    Zn=[layt[k][2] for k in range(number_of_nodes)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in _edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]

    trace1=Scatter3d(x=Xe,
                     y=Ye,
                     z=Ze,
                     mode='lines',
                     line=Line(color='rgb(125,125,125)', width=1),
                     hoverinfo='none'
                     )
    trace2=Scatter3d(x=Xn,
                     y=Yn,
                     z=Zn,
                     mode='markers',
                     name='actors',
                     marker=Marker(symbol='dot',
                                   size=6,
                                   color=group,
                                   colorscale='Viridis',
                                   line=Line(color='rgb(50,50,50)', width=0.5)
                                   ),
                    text=labels,
                    hoverinfo='text'
                    )
    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )

    layout = Layout(
             title="Link network(3D visualization)",
             width=1000,
             height=1000,
             showlegend=False,
             scene=Scene(
             xaxis=XAxis(axis),
             yaxis=YAxis(axis),
             zaxis=ZAxis(axis),
            ),
        margin=Margin(
            t=100
       ),
       hovermode='closest',
            )
    data=Data([trace1, trace2])
    fig=Figure(data=data, layout=layout)
    #return a div of the graph to be shown in browser
    plotly.offline.plot(fig, output_type='file')

print ("please provide link of 3d network you want to create")
link_name = input()
print("Please provide number of child nodes each node will have")
child_nodes = int(input())
create_3d_Network(link_name, child_nodes)
