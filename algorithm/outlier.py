from scipy import stats
'''
fields is a list of tuples. Each tuple represents a field (id, feature). Feature would be things like eta, water depth
Return a list if lists of length 2. The second element in the sublist is a percentile, indicating where the field lies compared to other fields given a specific feature.
The first element of the sublist is field id
'''
def find_outlier(fields):
    fields_features = []
    results = []

    for field in fields:
        fields_features.append(field[1])
        results.append([field[0], None])
    fields_percentiles = stats.rankdata(fields_features, 'min')/len(fields_features)

    for index, field in enumerate(fields):
        results[index][1] = fields_percentiles[index]
    
    return results