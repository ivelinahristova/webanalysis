import matplotlib.pyplot as plt
import pandas as pd

from app.db import db
from app.models import Article


class Plotter:

    def plot_share_counts(self, from_date, to_date, source, month):
        query = db.session.query(Article).filter(
            Article.shares_count >= 0,
            (Article.date > from_date),
            (Article.date < to_date),
            Article.source == source
        )
        if query.count == 0:
            return
        df = pd.read_sql(query.statement, db.session.bind)
        plt.figure()

        df['date'] = df['date'].apply(lambda x: x.day)
        if df.empty:
            return
        df = df.groupby('date').agg({'shares_count': 'mean'})
        df.reset_index(inplace=True)
        plt.plot(df['date'], df['shares_count'], marker='o',
                 markerfacecolor='skyblue', markersize=12, color='skyblue',
                 linewidth=4)

        plt.savefig(f'app/static/export/{month}_{source}.png')