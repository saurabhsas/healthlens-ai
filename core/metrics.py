def get_kpis(df):
    return {
        'members': len(df),
        'total_cost': df['PAID'].sum(),
        'avg_cost': df['PAID'].mean(),
        'ed_visits': df['ED_VISITS'].sum(),
        'ip_visits': df['IP_VISITS'].sum()
    }