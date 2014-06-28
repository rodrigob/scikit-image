import numpy as np
from skimage import graph


def max_edge(g, src, dst, n):
    w1 = g[n].get(src, {'weight': -np.inf})['weight']
    w2 = g[n].get(dst, {'weight': -np.inf})['weight']
    return max(w1, w2)


def test_rag_merge():
    g = graph.rag.RAG()

    for i in range(5):
        g.add_node(i, {'labels': [i]})

    g.add_edge(0, 1, {'weight': 10})
    g.add_edge(1, 2, {'weight': 20})
    g.add_edge(2, 3, {'weight': 30})
    g.add_edge(3, 0, {'weight': 40})
    g.add_edge(0, 2, {'weight': 50})
    g.add_edge(3, 4, {'weight': 60})

    gc = g.copy()

    g.merge_nodes(0, 2)
    assert g.edge[1][2]['weight'] == 10
    assert g.edge[2][3]['weight'] == 30

    gc.merge_nodes(0, 2, weight_func=max_edge)
    assert gc.edge[1][2]['weight'] == 20
    assert gc.edge[2][3]['weight'] == 40

    g.merge_nodes(1, 4)
    g.merge_nodes(2, 3)
    g.merge_nodes(3, 4)
    assert sorted(g.node[4]['labels']) == list(range(5))
    assert g.edges() == []


def test_threshold_cut():

    img = np.zeros((100, 100, 3), dtype='uint8')
    img[:50, :50] = 255, 255, 255
    img[:50, 50:] = 254, 254, 254
    img[50:, :50] = 2, 2, 2
    img[50:, 50:] = 1, 1, 1

    labels = np.zeros((100, 100), dtype='uint8')
    labels[:50, :50] = 0
    labels[:50, 50:] = 1
    labels[50:, :50] = 2
    labels[50:, 50:] = 3

    rag = graph.rag_meancolor(img, labels)
    new_labels = graph.threshold_cut(labels, rag, 10)

    # Two labels
    assert new_labels.max() == 1
