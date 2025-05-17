# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session
import pandas as pd
import requests

# Write directly to the app
st.title("🥛Customize Your Smoothie!🥛")
st.write("Choose the fruits you want in your custom Smoothie!")

# ✅ Fixed connection to include type
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# ✅ Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)

# ✅ Convert to Pandas for Streamlit compatibility
pd_df = my_dataframe.to_pandas()

# ✅ Extract fruit names into a list for multiselect
fruit_list = pd_df['FRUIT_NAME'].tolist()

# Smoothie name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name in your Smoothie will be: ", name_on_order)

# Multiselect using fruit names
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', fruit_list, max_selections=5
)

# Insert into orders table
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# ✅ New section: Fetch and show nutrition info
if ingredients_list:
    for fruit_chosen in ingredients_list:
        # Check if SEARCH_ON value exists
        search_row = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON']
        if search_row.empty:
            st.warning(f"No SEARCH_ON value found for {fruit_chosen}. Skipping.")
            continue

        search_on = search_row.iloc[0]

        # Display header
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # Fetch from API
        response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")

        if response.status_code == 200:
            try:
                json_data = response.json()
                df = pd.json_normalize(json_data)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error parsing API data for {fruit_chosen}: {e}")
        else:
            st.warning(f"Failed to fetch data for {fruit_chosen} (status code {response.status_code})")


# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# from snowflake.snowpark.context import get_active_session

# # Write directly to the app
# st.title("🥛Customize Your Smoothie!🥛")
# st.write("Choose the fruits you want in your custom Smoothie!")

# # ✅ Fixed connection to include type
# cnx = st.connection("snowflake", type="snowflake")
# session = cnx.session()

# # Load fruit options from Snowflake
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# #st.dataframe(data=my_dataframe, use_container_width =True)
# #st.stop()

# pd_df=my_dataframe.to_pandas()
# #st.dataframe(pd_df)
# #st.stop()

# # Smoothie name input
# name_on_order = st.text_input("Name on Smoothie:")
# st.write("The name in your Smoothie will be: ", name_on_order)

# # Multiselect ingredients
# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients: ',  my_dataframe, max_selections=5
    
# )

# # Submit order if ingredients are selected
# if ingredients_list:
#     ingredients_string = ''
#     for element in ingredients_list:
#         ingredients_string += element + ' '

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#                 values ('""" + ingredients_string + """','""" + name_on_order + """'
#                 )"""

#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")

# #new section
# import requests

# if ingredients_list:
#         ingredients_string=''

#         for fruit_chosen in ingredients_list:
#                 ingredients_string += fruit_chosen +  ' '
        
#                 search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#                 # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

#                 st.subheader(fruit_chosen+' '+'Nutrition Information')
#                 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
#                 fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width =True)
            
#         #st.write(ingredients_string)
