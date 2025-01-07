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
st.text(smoothiefroot_response.json())
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

#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df=st.experimental_data_editor(my_dataframe)
    
    submitted = st.button('Submit')
    if submitted:
        st.success('Someone clicked the button', icon = '👍')
        og_dataset = session.table("smoothies.public.orders")    
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write("Something went wrong")
else:
    st.success('There are no pending orders right now')
