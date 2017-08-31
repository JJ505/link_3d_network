# link_3d_network
creates a 3d network of a given web address for a specified number of children deep

run in command line using python 3

Usage:
python3 create_graph.py
please provide link of 3d network you want to create
<paste your site link here>
Please provide number of child nodes each node will have
2
creating...

Once its done the graph will open up in your browser

Its best to limit the number of children nodes to a small number.
For example, 5 children nodes will produce a graph with potentially 5^5 or 3125 nodes.

BeautifulSoup(python library) is used to scrape the site links and igraph/plotly is used to create the 3d network.

![Alt text](https://github.com/JJ505/link_3d_network/blob/master/3d_network_image_example.png "example 3d network created using create_graph")
