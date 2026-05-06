import pandas as pd

def fill_missing_dates(df):
    all_states = df['state'].unique()
    final_df = []

    for state in all_states:
        temp = df[df['state'] == state].copy()

        # Set date as index
        temp = temp.set_index('date')

        # Convert to weekly frequency
        temp = temp.asfreq('W')

        # Fill missing state
        temp['state'] = state

        # Interpolate missing sales
        temp['total'] = temp['total'].interpolate()

        final_df.append(temp)

    return pd.concat(final_df).reset_index()