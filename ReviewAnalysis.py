import pandas as pd
import matplotlib.pyplot as plt
# analysis_1:
# - query rating score & review number per year ( from 2005 to 2017)
def review_rating_by_year(in_file,out_file):
    df = pd.read_csv(in_file, delimiter=",", encoding='utf-8')
    rating_s, number_s, year_s = [], [], []
    for i in range(2005, 2018):
        start = str(i) + "-01-01"
        end = str(i + 1) + "-01-01"
        df_sub = df[(df['Date'] < end) & (df['Date'] >= start)]
        rating_s.append(df_sub.Rating.values.mean())
        number_s.append(df_sub.shape[0])
        year_s.append(i)
    df = pd.DataFrame({'Rating': rating_s, 'Number': number_s, 'Year': year_s})
    df.to_csv(out_file, index=False, sep=',', columns=['Rating', 'Number', 'Year'])
    return 1
#