# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My Parents New Healthy Dinner")
st.subtitle("Breakfast Menu")
st.write(
    """
    Omega 3 & Blueberry Oatmeal
    Kale, Spinach & Rocket Smoothie
    Hard-Boiled Free-Range Egg
    """
)

name_on_order = st.text_input('Name on smoothie')
st.write('Chosen name:', name_on_order)

# Display Ingredients
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Menu
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

# Save order to table
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


    # st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        success_statement = 'Your Smoothie is ordered, '+name_on_order+'!'
        st.success(success_statement, icon="✅")
