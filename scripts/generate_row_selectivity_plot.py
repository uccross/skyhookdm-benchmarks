import json
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
from decouple import config
from datetime import date

COMMIT_SHA = config('github.sha')
today = date.today().strftime("%Y-%m-%d")

path = "../benchmarks-result/" + today + "/" + COMMIT_SHA + "/"
# path = "./benchmarks-result/" + '2021-07-30' + "/" + COMMIT_SHA + "/"

plot_df = pd.DataFrame({'fileType':[],
        'result':[],
        'selectivity': []})

for i in [1, 10, 25, 50, 75, 90, 99, 100]:
    filename = 'dataset-selectivity-' + str(i) + '-row-parquet.json'
    f = open(path + filename,)
    data = json.load(f)
    df = pd.DataFrame({'fileType':["Parquet"],
        'result':[float(data["stats"]["data"][0])],
        'selectivity': [i]})
    plot_df = plot_df.append(df)

for i in [1, 10, 25, 50, 75, 90, 99, 100]:
    filename = 'dataset-selectivity-' + str(i) + '-row-rados.json'
    f = open(path + filename,)
    data = json.load(f)
    df = pd.DataFrame({'fileType':["Rados"],
        'result':[float(data["stats"]["data"][0])],
        'selectivity': [i]})
    plot_df = plot_df.append(df)

plot_df = plot_df.sort_values(by=['selectivity'])
sns.barplot(data=plot_df, x="selectivity",y = "result", hue="fileType")

print(plot_df)
plt.savefig(path + 'row-result.png')