import pandas as pd

df = pd.read_xml('/Users/marjoleinvantol/Desktop/CDTF/export.xml')
df.to_csv('yasmin.csv', index=False)