import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose your fruit you want in your custom smoothie
    """)

# Input for Name on order
Name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on smoothie will be:", Name_on_order)

# Get active session and query the fruit options from Snowflake
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name")).collect()

# Convert the result to a list of strings (fruit names)
fruit_options = [row['FRUIT_NAME'] for row in my_dataframe]

# Multiselect input for ingredients
ingredients_list = st.multiselect('Choose up to 6 ingredients:', fruit_options)

if ingredients_list:
    # Create a comma-separated string of ingredients
    ingredients_string = ', '.join(ingredients_list)
    
    # SQL Insert statement with both ingredients and name
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_order}')
    """
    
    # Button to submit order
    time_to_insert = st.button('Submit order')
    if time_to_insert:
        # Execute the SQL statement
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
