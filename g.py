import pydot, os
os.environ["PATH"] = "C:\\Program Files\\Graphviz\\bin"
addr = "a"
graph=pydot.Dot('my_graph', graph_type="digraph", rankdir='LR')
graph.add_node(pydot.Node(addr, label=addr+"_"+str(100)))
graph.write_png("AAA.png")