# coding:utf-8
import igraph as ig
import plotly.plotly
from plotly.graph_objs import *


def visualize(origin_data):
    data = {}
    data['nodes'] = []
    data['links'] = []

    # tmp用于保存所有的变量
    tmp = set()
    for k,v in origin_data.items():
      for vv in v:
        if vv not in origin_data:
          tmp.add(vv)

    # 然后总共有42个变量,54个函数
    #print(len(origin_data.keys()), len(tmp))
    for key in origin_data.keys():
        node = {'name': key, 'group': 1}
        data['nodes'].append(node)
    for var in tmp:
        node = {'name': var, 'group': 2}
        data['nodes'].append(node)

    for k,v in origin_data.items():
      for vv in v:
        source=data['nodes'].index({'name':k,'group':1})
        if vv in tmp:
          #source=data['nodes'].index({'name':k,'group':1})
          target=data['nodes'].index({'name':vv,'group':2}) 
        else:
          target=data['nodes'].index({'name':vv,'group':1}) 
        data['links'].append({'source':source,'target':target})


    # print(data['nodes'])
    N = len(data['nodes'])

    L = len(data['links'])
    Edges = [(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

    # print(data['links'][0])
    G = ig.Graph(Edges, directed=False)

    labels = []
    group = []
    for node in data['nodes']:
        labels.append(node['name'])
        group.append(node['group'])

    layt = G.layout('kk', dim=3)

    Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
    Yn = [layt[k][1] for k in range(N)]  # y-coordinates
    Zn = [layt[k][2] for k in range(N)]  # z-coordinates
    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    trace1 = Scatter3d(x=Xe,
                       y=Ye,
                       z=Ze,
                       mode='lines',
                       line=Line(color='rgb(125,125,125)', width=1),
                       hoverinfo='none'
                       )
    trace2 = Scatter3d(x=Xn,
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
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
    layout = Layout(
        #title="MSTR Hackathon2017",
        width=1100,
        height=800,
        showlegend=False,
        scene=Scene(
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            zaxis=ZAxis(axis),
        ),
        margin=Margin(
            t=50
        ),
        hovermode='closest',
        annotations=Annotations([
            Annotation(
                showarrow=False,
                text="@MSTR Hackathon2017 ;-)",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                    size=14
                )
            )
        ]), )
    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)

    plotly.offline.plot(fig)



