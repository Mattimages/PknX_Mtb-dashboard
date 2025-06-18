import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.express as px

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='PknX dashboard',
    page_icon=':microbe:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/Big_data_sup2.csv'
    raw_data_df = pd.read_csv(DATA_FILENAME)

    raw_data_df['Fold-change (log2)'] = raw_data_df['Fold-change (log2)'].fillna(15)
    
    return raw_data_df

PknX_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :microbe: PknX dashboard

Browse expression data from [Frando et al.](https://www-nature-com.vu-nl.idm.oclc.org/articles/s41564-022-01313-7#Sec26). 

'''

# Add some spacing
''
''

min_value = PknX_df['Fold-change (log2)'].min()
max_value = PknX_df['Fold-change (log2)'].max()

from_Ascore, to_Ascore = st.slider(
    'Which Log2fold change are you interested in? ',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

Enzymes = PknX_df['STPK'].unique()

if not len(Enzymes):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which kinases would you like to view?',
    Enzymes,
    ['PknB', 'PknD', 'PknE', 'PknF', 'PknG', 'PknH', 'PknI', 'PknJ', 'PknK', 'PknL'])
""
"" 
""
Experiments = PknX_df['Mutant'].unique()

if not len(Enzymes):
    st.warning("Select at least one country")


selected_experiments = st.multiselect(
    'Which experiments would you like to view? (Overexpression or Loss of Function)', 
    Experiments,
    ["OE", "LOF"])
''
''
''

# Filter the data
PknX_df["rv_sort"] = (
    PknX_df["Rv Number"]
    .str.replace(r"^Rv", "", regex=True)
    .str.replace(r"[a-zA-Z]$", ".1", regex=True)
    .astype(float)
)
PknX_df = PknX_df.sort_values(by="rv_sort", ascending=True)
filtered_PknX_df = PknX_df[
    (PknX_df['STPK'].isin(selected_countries))
    &(PknX_df['Mutant'].isin(selected_experiments))
    & (PknX_df['Fold-change (log2)'] <= to_Ascore)
    & (from_Ascore <= PknX_df['Fold-change (log2)'])
]
# Search bar
search = st.text_input("Search for a protein:")

# Filter DataFrame based on search input (case-insensitive)
if search:
    filtered_PknX_df = filtered_PknX_df[filtered_PknX_df["Rv Number"].str.contains(search, case=False, na=False)]
else:
    None
#st.header('GDP over time', divider='gray')

''



##make it specific for a selected protein

''
fig = px.scatter(
    filtered_PknX_df,
    x='rv_sort',
    y='Fold-change (log2)',
    #size="size",
    hover_name="Phosphosite",
    color="STPK",
    title="Interactive Bubble Plot"
)
''
st.plotly_chart(fig)

#first_year = gdp_df[gdp_df['Year'] == from_year]
#last_year = gdp_df[gdp_df['Year'] == to_year]
#
#st.header(f'GDP in {to_year}', divider='gray')

''

#cols = st.columns(4)

#for i, country in enumerate(selected_countries):
 #   col = cols[i % len(cols)]

 #   with col:
  #      first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
 #       last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
#
 #       if math.isnan(first_gdp):
 #           growth = 'n/a'
 #           delta_color = 'off'
#        else:
  #          growth = f'{last_gdp / first_gdp:,.2f}x'
  #          delta_color = 'normal'
#
 #       st.metric(
 #           label=f'{country} GDP',
 #           value=f'{last_gdp:,.0f}B',
#            delta=growth,
#            delta_color=delta_color
#        )
#
