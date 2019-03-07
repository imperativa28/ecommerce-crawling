def convert_transaction(transaction):
    if 'rb' in transaction:
        transaction = float(transaction[:-2].replace(',', '.')) * 1000
    elif 'jt' in transaction:
        transaction = float(transaction[:-2].replace(',', '.')) * 1000000
    return transaction


def remove_outlier(df, column):
    return df[((df[column] - df[column].mean()) / df[column].std()).abs() < 3][column]
