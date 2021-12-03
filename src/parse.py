import pandas as pd
import xml.etree.ElementTree as Tree
import os


def parse(path):
    # Getting xml tree
    tree = Tree.parse(path)
    # Get the root of tree
    root = tree.getroot()
    
    parent = 'TermntdRcrd'

    pattern = 'FinInstrmGnlAttrbts'

    tag = 'Issr'

    children = ['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy']
    cols = [pattern + '.' + k for k in children]
    cols.append(tag)
    
    rows = list()
    for i in root.iter():
        if parent in i.tag:
            entry = [None for x in range(len(children) + 1)]
            for child in i:
                if pattern in child.tag:
                    for c in child:                        
                        for k in range(len(children)):
                            
                            if children[k] in c.tag:
                                entry[k] = c.text
                if tag in child.tag:                    
                    entry[5] = child.text
            rows.append(entry)

    df = pd.DataFrame(data=rows, columns=cols)
    df.to_csv('../ans.csv', index=False)    

if __name__ == '__main__':
    
    path = os.path.join(os.pardir, "DLTINS_20210117_01of01.xml")
    
    parse(path)
