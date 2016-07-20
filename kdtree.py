# -*-mport random
import numpy as np

class Treenode(object):
    def __init__(self, current_node = None, split = None, left = None, right = None):
        self.current_node = None 
        self.split = split 
        self.left = left 
        self.right = right 

def findSplitPoint(datapoints, split):
    local_split = split % (datapoints.shape[0])
    datapoints = datapoints[datapoints[:,local_split].argsort()]
    return datapoints

def buildKdtree(datapoints, split):
    if datapoints.size == 0:
        return
    datapoints = findSplitPoint(datapoints, split)
    numpoints = datapoints.shape[0]
    
    middle = numpoints/2
    left_datapoints = datapoints[:middle,:]
    right_datapoints = datapoints[middle+1:,:]
    current_node = Treenode()
    current_node.split = split
    current_node.current_node = datapoints[middle,:]
    current_node.left = buildKdtree(left_datapoints, split+1)
    current_node.right = buildKdtree(right_datapoints, split+1)
    return current_node

def printKdtree(treenode):
    print treenode.current_node, treenode.split
    if treenode.left:
        printKdtree(treenode.left)
    if treenode.right:
        printKdtree(treenode.right)

def distance(node1, node2):
    return np.linalg.norm(node1-node2)
    
def findNearestNeighbor(root, x):
    p = root
    dim = p.current_node.shape[0]
    search_path = list()
    dist = np.finfo(np.float64()).max
    nearest_neighbor = None
    while p.current_node.size <> 0:
        if (not p.left) and (not p.right):
            current_dist = distance(p.current_node, x)
            if current_dist < dist:
                dist = current_dist
                nearest_neighbor = p.current_node
            break
        search_path.append(p)
        local_split = p.split % dim 
        if x[local_split] < p.current_node[local_split]:
            p = p.left
        else:
            p = p.right
    search_path = np.array(search_path)
    while search_path.size > 0:
        #for item in search_path:
        #    print 'yes', item.current_node,
        #distance between the point x to the separate plane
        current_node = search_path[-1]
        search_path = search_path[:-1]
        local_split = current_node.split % len(x)
        dist_point_plane = x[local_split] - current_node.current_node[local_split]
        if dist_point_plane < dist:
            current_distance =  distance(current_node.current_node, x) 
            if current_distance < dist:
                dist = current_distance
                nearest_neighbor = current_node.current_node
            if (not current_node.left) and (not current_node.right):
                continue
        #    print 'abc', x[local_split], current_node.current_node
        #    print x[local_split] <= current_node.current_node[local_split], local_split
            if x[local_split] <= current_node.current_node[local_split]:
                np.append(search_path, [current_node.right])
            else:
                search_path = np.append(search_path, [current_node.left])
    return dist, nearest_neighbor

if __name__ == "__main__":
    datapoints = list() 
    datapoints = [(2,3), (5,4), (9,6), (4,7),(8,1),(7,2)] 
    ndim = 2
    #for i in range(10):
    #    data = list()
    #    for j in range(ndim):
    #        data.append(random.randint(1, 10))
    #    datapoints.append(data)

    print datapoints
    datapoints = np.array(datapoints)
    for data in datapoints:
        print data

    root = buildKdtree(datapoints, 0)
    printKdtree(root)
    res = findNearestNeighbor(root, (2, 4.5))
    print res
