# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("🥛Customize Your Smoothie!🥛")
st.write("Choose the fruits you want in your custom Smoothie!")

# ✅ Fixed connection to include type
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SERCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width =True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

# Smoothie name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name in your Smoothie will be: ", name_on_order)

# Multiselect ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',  my_dataframe, max_selections=5
    
)

# Submit order if ingredients are selected
if ingredients_list:
    ingredients_string = ''
    for element in ingredients_list:
        ingredients_string += element + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """'
                )"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#new section
import requests

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width =True)
