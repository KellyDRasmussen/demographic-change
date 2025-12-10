"""
Process Swedish demographic data from SCB into clean format for Streamlit app
"""
import pandas as pd
import numpy as np

def process_demographic_data():
    """
    Process TAB4824_sv.csv to extract working age (18-67) demographics by kommun
    for 2014 and 2024, broken down by the 4 demographic categories.
    """
    # Read with correct encoding
    df = pd.read_csv("TAB4824_sv.csv", encoding="ISO-8859-1")

    # Category mapping for cleaner names
    category_map = {
        "utrikes födda": "born_overseas",
        "inrikes födda med två utrikes födda föräldrar": "both_parents_overseas",
        "inrikes födda med en inrikes och en utrikes född förälder": "one_parent_overseas",
        "inrikes födda med två inrikes födda föräldrar": "both_parents_sweden"
    }

    # Filter for working age (18-67) and years 2014, 2024
    # First, let's see what age format looks like
    print("Unique age values sample:")
    print(df['ålder'].unique()[:20])

    # We need to filter for ages 18-67
    # The data has individual ages like "18 år", "19 år", etc.
    working_ages = [f"{age} år" for age in range(18, 68)]

    df_filtered = df[
        (df['ålder'].isin(working_ages)) &
        (df['år'].isin([2014, 2024])) &
        (df['utländsk/svensk bakgrund'].isin(category_map.keys()))
    ].copy()

    # Map category names
    df_filtered['category'] = df_filtered['utländsk/svensk bakgrund'].map(category_map)

    # Extract kommun name from region (format: "0114 Upplands Väsby")
    df_filtered['kommun'] = df_filtered['region'].str.replace(r'^\d+\s+', '', regex=True)

    # Remove national level ("Riket")
    df_filtered = df_filtered[df_filtered['kommun'] != 'Riket']

    # Group by kommun, category, and year, summing across gender and individual ages
    df_grouped = df_filtered.groupby(
        ['kommun', 'category', 'år'],
        as_index=False
    )['Antal personer'].sum()

    # Pivot to get 2014 and 2024 as columns
    df_pivot = df_grouped.pivot_table(
        index=['kommun', 'category'],
        columns='år',
        values='Antal personer',
        fill_value=0
    ).reset_index()

    df_pivot.columns = ['kommun', 'category', 'count_2014', 'count_2024']

    # Calculate change
    df_pivot['change_absolute'] = df_pivot['count_2024'] - df_pivot['count_2014']
    df_pivot['change_relative'] = (
        (df_pivot['count_2024'] - df_pivot['count_2014']) /
        df_pivot['count_2014'].replace(0, np.nan) * 100
    )

    # Pivot wider to have each category as columns
    df_wide = df_pivot.pivot_table(
        index='kommun',
        columns='category',
        values=['count_2014', 'count_2024', 'change_absolute', 'change_relative']
    ).reset_index()

    # Flatten column names
    df_wide.columns = ['_'.join(col).strip('_') if col[1] else col[0]
                       for col in df_wide.columns.values]

    # Calculate totals
    category_cols_2014 = [col for col in df_wide.columns if col.startswith('count_2014_')]
    category_cols_2024 = [col for col in df_wide.columns if col.startswith('count_2024_')]

    df_wide['total_2014'] = df_wide[category_cols_2014].sum(axis=1)
    df_wide['total_2024'] = df_wide[category_cols_2024].sum(axis=1)
    df_wide['total_change_absolute'] = df_wide['total_2024'] - df_wide['total_2014']
    df_wide['total_change_relative'] = (
        df_wide['total_change_absolute'] / df_wide['total_2014'].replace(0, np.nan) * 100
    )

    # Calculate percentages for 2024
    for category in category_map.values():
        col_name = f'count_2024_{category}'
        if col_name in df_wide.columns:
            df_wide[f'pct_2024_{category}'] = (
                df_wide[col_name] / df_wide['total_2024'] * 100
            ).round(2)

    # Calculate percentages for 2014
    for category in category_map.values():
        col_name = f'count_2014_{category}'
        if col_name in df_wide.columns:
            df_wide[f'pct_2014_{category}'] = (
                df_wide[col_name] / df_wide['total_2014'] * 100
            ).round(2)

    # Save processed data
    df_wide.to_csv("processed_demographics.csv", index=False, encoding='utf-8')
    print(f"Processed data for {len(df_wide)} kommuner")
    print(f"\nColumns: {list(df_wide.columns)}")
    print(f"\nSample data:")
    print(df_wide.head())

    return df_wide

if __name__ == "__main__":
    df = process_demographic_data()
