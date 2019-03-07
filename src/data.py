import math
import numpy as np
import pandas as pd

from src.helper import convert_transaction

# Set numerical columns for visualization
columns = {
    'active_product': 'Active Products',
    'product_sold': 'Products Sold',
    'total_tx': 'Number of Transactions',
    'num_store': 'Number of Physical Stores',
    'rate_service': 'Rate of Service',
    'rate_speed': 'Rate of Speed',
    'rate_accuracy': 'Rate of Accuracy',
    'reputation_score': 'Reputation Score',
    'rate_cancel': 'Cancellation Rate',
}

# Main data
df = pd.read_csv('tokopedia.csv', header=0, sep=';', index_col=0, low_memory=False)
df['total_tx'] = df['total_tx'].apply(lambda x: convert_transaction(x)).astype(float)

# Summary data
summary = df[list(columns.keys())].describe().transpose().reset_index(level=0)
summary['index'] = [columns[key] for key in summary['index']]

# Area summary data
area_summary = df.groupby('city')[['active_product', 'product_sold', 'total_tx', 'num_store']].sum(
).sort_values('num_store', ascending=False)
area_summary.reset_index(level='city', inplace=True)

# Text analysis data
word_counts = pd.read_csv('word_counts.csv', index_col=0).sort_values(
    'frequencies', ascending=False)

# Map data
mapblox_token = 'pk.eyJ1IjoiaW1wZXJhdGl2YTI4IiwiYSI6ImNqc2ZvcDJzaDFqZTg0Nm9heWFtMXd2NW0ifQ.4z5BuZSALFx7vM8alGvXzw'