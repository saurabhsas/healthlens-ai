def run_structured_query(query_json, df):
    groupby_col = query_json['groupby']
    metric_cols = query_json['metrics']
    agg = query_json['aggregation']
    filters = query_json.get('filters', {})

    value_map = {
      'MALE':'M','MALES':'M','M':'M',
      'FEMALE':'F','FEMALES':'F','F':'F'
    }

    filtered = df.copy()
    for col,val in filters.items():
        val = value_map.get(str(val).upper(), str(val).upper())
        filtered = filtered[
            filtered[col].astype(str).str.upper()==val
        ]

    if len(filtered)==0:
        raise Exception('No rows returned after filters')

    g = filtered.groupby(groupby_col)[metric_cols]
    if agg=='sum':
        return g.sum()
    if agg=='mean':
        return g.mean()
    if agg=='count':
        return g.count()
    raise Exception('Unsupported aggregation')