# Import python packages
import streamlit as st
cnx=st.connection("snowflake")
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched
#session = get_active_session()
session = cnx.session()
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)



name_on_order = st.text_input("Name on Smothie")
st.write("The name on your Smothie will be", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
            ingredients_string+=fruit_chosen+' '
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
            st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert=st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
