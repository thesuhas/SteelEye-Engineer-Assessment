import pandas as pd
import xml.etree.ElementTree as Tree
import os


def parse(path: str) -> None:
    '''
    Parameters: Path to XML File

    Writes the data in the following tags to a csv file: 
    FinInstrmGnlAttrbts.Id, 
    FinInstrmGnlAttrbts.FullNm,
    FinInstrmGnlAttrbts.ClssfctnTp,
    FinInstrmGnlAttrbts.CmmdtyDerivind,
    FinInstrmGnlAttrbts.NtnlCcy,
    Issr

    Returns: None
    '''

    # Getting xml tree
    tree = Tree.parse(path)
    # Get the root of tree
    root = tree.getroot()
    # Parent node to look at
    parent = 'TermntdRcrd'
    # Desired Child 1
    pattern = 'FinInstrmGnlAttrbts'
    # Desired Child 2
    tag = 'Issr'
    # Initialising the required arrays
    children = ['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy']
    cols = [pattern + '.' + k for k in children]
    cols.append(tag)
    # Get the rows
    rows = list()
    for i in root.iter():
        # If parent is found
        if parent in i.tag:
            # Initialise array of required elements
            entry = [None for x in range(len(children) + 1)]
            for child in i:
                # If required child has been found
                if pattern in child.tag:
                    # Get the required grand-children
                    for c in child:             
                        for k in range(len(children)):
                            # If grandchildren found, update entry
                            if children[k] in c.tag:
                                entry[k] = c.text
                # If Issr found
                if tag in child.tag:                    
                    entry[5] = child.text
            # Add to list of rows
            rows.append(entry)
    # Create Dataframe
    df = pd.DataFrame(data=rows, columns=cols)
    # Save to csv
    df.to_csv('../ans.csv', index=False)    


if __name__ == '__main__':
    # Get the path of the incput file
    path = os.path.join(os.pardir, "DLTINS_20210117_01of01.xml")
    # Execute function
    parse(path)
