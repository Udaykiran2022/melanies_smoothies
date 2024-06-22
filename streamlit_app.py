import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Initialize Streamlit app
st.title("Customize Your Smoothie :balloon:")
st.write(
    """Choose your fruits for your customized smoothie."""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Establish Snowflake connection
connection_parameters = {
    "account": "<your_account>",
    "user": "<your_user>",
    "password": "<your_password>",
    "role": "<your_role>",
    "warehouse": "<your_warehouse>",
    "database": "<your_database>",
    "schema": "<your_schema>"
}
session = Session.builder.configs(connection_parameters).create()

# Retrieve fruit options from the Snowflake table
fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_options = [row['FRUIT_NAME'] for row in fruit_options_df.collect()]

# User selects ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options, max_selections=5)

if ingredients_list and name_on_order:
    # Create a string of chosen ingredients
    ingredients_string = ', '.join(ingredients_list)

    # Button to submit the order
    if st.button('Submit Order'):
        try:
            # Insert the order into the database using Python's f-string formatting for values
            session.sql(
                f"""
                INSERT INTO smoothies.public.orders (name_on_order, ingredients)
                VALUES ('{name_on_order}', '{ingredients_string}')
                """
            ).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.write('Something went wrong:', e)
else:
    st.write("Please enter your name and select ingredients.")
