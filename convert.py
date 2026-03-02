import pandas as pd

df = pd.read_xml('/Users/marjoleinvantol/Desktop/CDTF_project/export.xml')
df.to_csv('yasmin.csv', index=False)