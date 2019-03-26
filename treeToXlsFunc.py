from sklearn.tree import _tree
import numpy as np

class treeToXlsFunc():
    def __init__(self,class_names, feature_names, sep=",", table_name="Table1", if_func_name="IF"):
        self.class_names = class_names
        self.feature_names = feature_names
        self.sep = sep
        self.table_name = table_name
        self.if_func_name = if_func_name
    
    def get_col_reference(self, colname):
        return self.table_name + "[@[" + colname + "]]"
    
    def get_class_string(self, class_list):
        return '"' +self.class_names[np.argmax(class_list)]+ '"'  

    def recurse(self,node):
            if self.tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = self.feature_names[node]
                threshold = self.tree_.threshold[node]

                return "".join(["{}(".format(self.if_func_name),
                                "{}<={}{}".format(self.get_col_reference(name), threshold, self.sep) ,  
                                self.recurse(self.tree_.children_left[node]) ,
                                self.sep,
                                self.recurse(self.tree_.children_right[node]),
                                ")"])
            else:
                return(self.get_class_string(self.tree_.value[node])) 
    
    def tree_to_if_function(self, tree):
        self.tree_ = tree.tree_
        self.feature_names = [self.feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
                                                    for i in self.tree_.feature]
        return '=' + self.recurse(0)