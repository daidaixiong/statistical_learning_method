import numpy as np

"""
age     hasjob    hashouse    credit    label
young   n           n           general   n
"""

class Decisiontree():
    def __init__(self):
        self.feature_dim = None
        self.child = list()
        self.label = -1

def compute(D, dim):
    label_dict = {}
    
    for data in D:
        if data[-1] not in label_dict:
            label_dict[data[-1]] = 1
        else:
            label_dict[data[-1]] += 1
    HD = 0
    numpoints = len(D)
    # compute H(D)
    for label,count in label_dict.items():
        p = 1.0*count/numpoints
        HD += (p*np.log2(p))
    HD = -1*HD

    # compute H(D|A) on each attribute of a feature
    # H(D|A) = p(A=ai)*H(D|A=ai)
    # H(D|A=ai) = -p(D=c1|A=ai)logp(D=c1|A=ai) + 
    label_dict = {}
    for data in D:
        if data[dim] not in label_dict:
            label_dict[data[dim]] = dict()
            label_dict[data[dim]][data[-1]] = 1
        else:
            if data[-1] not in label_dict[data[dim]]:
#                print label_dict[data[dim]], data[-1], 'yes'
                label_dict[data[dim]][data[-1]] = 1
            else:
                label_dict[data[dim]][data[-1]] += 1
    
    HDA = 0
    for attribute, class_attribute in label_dict.items():
        datapoints_this_attribute = sum(class_attribute.values())
        p_Aai = 1.0*datapoints_this_attribute/numpoints
        HDCkAai = 0
        for label, count in class_attribute.items():
            p_labelAai = 1.0*count/datapoints_this_attribute
            HDCkAai += p_labelAai*np.log2(p_labelAai)
#            print 'count', 'datapoints_this_attribute', count, datapoints_this_attribute, p_labelAai, HDCkAai
        HDCkAai = -1*HDCkAai
        HDA += p_Aai*HDCkAai
        
    print 'for feature %d, entropy gain %s' % (dim, HD-HDA)
    return HD-HDA

def most_frequent_label(D):
    label_dict = dict()
    for data in D:
        if data[-1] not in label_dict:
            label_dict[data[-1]] = 1
        else:
            label_dict[data[-1]] += 1
    max_count = 0
    max_label = 0
    for label, count in label_dict.items():
        if count > max_count:
            max_label = label
            max_count = count
    return max_label

def build_decisiontree(D, dim_list):
    max_gain = 0
    best_dim = -1
    feature_dim = len(D[0])-1
    
    for dim in dim_list:
        current_gain = compute(D, dim)
        if current_gain > max_gain:
            max_gain = current_gain
            best_dim = dim
    print 'dim_list', 'best_dim', 'max_gain', dim_list, best_dim, max_gain
    if max_gain == 0:
        print 'entropy gain is zero, all points belong to the same class'
    else:
        print 'select feature %d, entropy gain %s' % (best_dim, max_gain)
    print

    tree = Decisiontree()
    # all data belong to a class
    if max_gain == 0:
        tree.label = D[0][-1]
        return tree
    
    dim_list.remove(best_dim)
    if not D or len(dim_list) == 0:
        return tree
    tree.feature_dim = best_dim
    tree.label = most_frequent_label(D)
    sub_D_list = dict()
    for data in D:
        if data[best_dim] not in sub_D_list:
            sub_D_list[data[best_dim]] = [data]
        else:
            sub_D_list[data[best_dim]].append(data)
    
    for item in sub_D_list:
    #    print item, 'hello'
    #    print sub_D_list[item]
    #    print len(sub_D_list[item])
    #    print 
        tree.child.append(build_decisiontree(sub_D_list[item], dim_list))
    return tree

def print_decisiontree(decisiontree):
    if not decisiontree.child:
        print 'I am a leaf node', decisiontree.feature_dim, decisiontree.label
    else:
        print 'I am a internal node', decisiontree.feature_dim, decisiontree.label
        for one_child in decisiontree.child:
            print_decisiontree(one_child)

if __name__ == "__main__":
    
    D=[('young', 'not_has_job', 'not_has_house', 'general_credit', 'not_approved'), ('young', 'not_has_job', 'not_has_house', 'good_credit', 'not_approved'), \
        ('young', 'has_job', 'not_has_house', 'good_credit', 'approved'), ('young', 'has_job', 'has_house', 'general_credit', 'approved'), \
        ('young', 'not_has_job', 'not_has_house', 'general_credit', 'not_approved'), ('middle_age', 'not_has_job', 'not_has_house', 'general_credit', 'not_approved'), \
        ('middle_age', 'not_has_job', 'not_has_house', 'good_credit', 'not_approved'), ('middle_age', 'has_job', 'has_house', 'good_credit', 'approved'), \
        ('middle_age', 'not_has_job', 'has_house', 'very_good_credit', 'approved'), ('middle_age', 'not_has_job', 'has_house', 'very_good_credit', 'approved'), \
        ('old', 'not_has_job', 'has_house', 'very_good_credit', 'approved'), ('old', 'not_has_job', 'has_house', 'good_credit', 'approved'), \
        ('old', 'has_job', 'not_has_house', 'good_credit', 'approved'), ('old', 'has_job', 'not_has_house', 'very_good_credit', 'approved'), \
        ('old', 'not_has_job', 'not_has_house', 'general_credit', 'not_approved') \
        ]
    

    for i in range(4):
        tmp_set = set()
        for item in D:
            tmp_set.add(item[i])
        print tmp_set
            
    decisiontree = build_decisiontree(D, range(len(D[0])-1))
    print_decisiontree(decisiontree)

