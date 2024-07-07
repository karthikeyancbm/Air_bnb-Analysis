import pymongo
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as px
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
import time as t
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import tableauserverclient as TSC
import streamlit.components.v1 as components


st.set_page_config(layout="wide")

st.title("  :bar_chart: :violet[AIR BNB] :rainbow[EXPLORATION AND VISUALIZATION]")

def file_read():
    df = pd.read_csv(r"C:\Users\ASUS\Documents\GUVI ZEN CLASSES\MAINT BOOT\AIR BNB PROJECT\Air_bnb.csv",na_filter=False,index_col=0)
    return df


def room_ch():

    data = file_read()
    room_choice = data["room_type"].unique().tolist()
    return room_choice


def country_choice():
    df = file_read()
    country_choice = df.country.unique().tolist()
    return country_choice

def host_nbr_choice():
    df=file_read()
    host_nbr = df.host_neighbourhood.unique().tolist()
    return host_nbr

def country_price(country_choice):

    df = file_read()
    filtered_df = df[df['country'].isin(country_choice)]
    country = filtered_df.groupby(['country']).price.mean().round(2).sort_values().to_frame()
    country = country.reset_index()
    country.rename(columns={"country":"Country","price":"Price"},inplace=True)
    fig_6 = px.bar(country,x="Country",y="Price",color="Price",
                   color_continuous_scale='thermal',
                   title = f'Country vs Price : {country_choice}',height = 500,
                   text="Price")
    fig_6.update_layout(title_font=dict(size=30),title_font_color = "#AD71EF")
    #fig_3.update_traces(text_position = 'outside')
    pie_chart_6 = px.pie(country,values ="Price",names="Country",title = f'Country vs Price : {country_choice}',
                         color_discrete_sequence = px.colors.sequential.RdBu)
    pie_chart_6.update_layout(title_font = dict(size=30),title_font_color="#AD71EF",uniformtext_minsize = 12,uniformtext_mode = "hide",
                                 autosize=False,width=500,height=500)
    pie_chart_6.update_traces(text=country['Country'],textposition ="inside")

    return country,fig_6,pie_chart_6

def country_reviews(country_choice):

    df = file_read()
    filtered_df = df[df['country'].isin(country_choice)]
    country_rev = filtered_df.groupby(['country']).number_of_reviews.mean().round(2).sort_values().to_frame()
    country_rev = country_rev.reset_index()
    country_rev.rename(columns={"country":"Country","number_of_reviews":"No of Reviews"},inplace=True)
    fig_7 = px.bar(country_rev,x="Country",y="No of Reviews",color="No of Reviews",
                    color_continuous_scale='thermal',
                    title = f'Country vs Reviews : {country_choice}',height = 500,
                    text="No of Reviews")
    fig_7.update_layout(title_font=dict(size=30),title_font_color = "#AD71EF")
    #fig_3.update_traces(text_position = 'outside')
    pie_chart_7 = px.pie(country_rev,values ="No of Reviews",names="Country",title = f'Country vs Reviews : {country_choice}',
                            color_discrete_sequence = px.colors.sequential.RdBu)
    pie_chart_7.update_layout(title_font = dict(size=30),title_font_color="#AD71EF",uniformtext_minsize = 12,uniformtext_mode = "hide",
                                    autosize=False,width=500,height=500)
    pie_chart_7.update_traces(text=country_rev['Country'],textposition ="inside")

    return country_rev,fig_7,pie_chart_7


def room_price(room_choice):

    df = file_read()
    filtered_df = df[df['room_type'].isin(room_choice)]
    reviews = filtered_df.groupby(['room_type','price']).number_of_reviews.mean().round(2).sort_values().to_frame()
    reviews = reviews.reset_index()
    reviews.rename(columns={"room_type":"Room_Type","price":"Price",'number_of_reviews':"No_of_reviews"},inplace=True)
    reviews = reviews.sort_values(by=['Price','No_of_reviews'])
    fig = px.bar(reviews, x='Room_Type', y='Price',
                            color='Price', color_continuous_scale='thermal',
                            title=f'Room_type vs Price : {room_choice}', height=500,
                            text = 'Price')
    fig.update_layout(title_font=dict(size=25), title_font_color='#AD71EF')
    fig.update_traces(textposition='outside')
    pie_chart = px.pie(reviews, values='No_of_reviews', names='Price',
                       title=f'Number of Reviews by Price for Room Type: {room_choice}',
                       color_discrete_sequence=px.colors.sequential.Plasma_r)
    pie_chart.update_traces(text=reviews['Room_Type'],textposition='inside')
    pie_chart.update_layout(title_font=dict(size=18), title_font_color='#AD71EF',uniformtext_minsize=12, uniformtext_mode='hide',autosize=False,
    width=500,
    height=500)
    return reviews,fig,pie_chart

def prop_price():
    data = file_read()
    prop_choice = data["property_type"].unique().tolist()
    return prop_choice


def get_property_price(prop_choice):

    df = file_read()
    filtered_df = df[df['property_type'].isin(prop_choice)]
    property = filtered_df.groupby(['property_type']).price.mean().round(2).sort_values().to_frame()
    property = property.reset_index()
    property.rename(columns={"property_type":"Property","price":"Price"},inplace=True)
    fig_1 = px.bar(property, x='Property', y='Price',
                            color='Price', color_continuous_scale='thermal',
                            title=f'Property Type vs Price : {prop_choice}', height=700,
                            text = 'Price')
    fig_1.update_layout(title_font=dict(size=25), title_font_color='#AD71EF')
    fig_1.update_traces(textposition='outside')
    return property,fig_1

def prop_count(prop_choice):

    df =file_read()
    filtered_df = df[df['property_type'].isin(prop_choice)]
    group_df = filtered_df.groupby(['property_type']).size().reset_index(name='count')
    group_df.rename(columns={"property_type":"Property Type","count":"Count"},inplace=True)
    group_df = group_df.sort_values(by='Count',ascending =False)
    fig_8 = px.bar(group_df,x='Property Type',y='Count',color = 'Count',
                    color_continuous_scale = 'thermal',
                    title = f'Property Type vs Count : {prop_choice}',height=700,text='Count')
    fig_8.update_layout(title_font=dict(size=25), title_font_color='#AD71EF')
    fig_8.update_traces(textposition='outside')
    pie_chart_8 = px.pie(group_df,values='Count',names='Property Type',
                         title=f'Property Type and Count: {prop_choice}',
                         color_discrete_sequence = px.colors.sequential.RdBu)
    pie_chart_8.update_layout(title_font=dict(size=28),title_font_color="#AD71EF",uniformtext_minsize=12,
                              uniformtext_mode='hide',autosize=False,width=800,height=800)
    pie_chart_8.update_traces(text=group_df['Property Type'],textposition='inside')

    return group_df,fig_8,pie_chart_8

def property_price():

    df = file_read()
    property = df.groupby(['property_type']).price.mean().round(2).sort_values().to_frame()
    property = property.reset_index()
    property.rename(columns={"property_type":"Property","price":"Price"},inplace=True)
    fig_new = px.bar(property, x='Property', y='Price',color='Price', color_continuous_scale='thermal',
                            title='Property categorisation based on Price', height=500,
                            text = 'Price')
    fig_new.update_layout(title_font=dict(size=28), title_font_color='#AD71EF')
    fig_new.update_traces(textposition='outside')
    pie_chart_1 = px.pie(property,values='Price',names='Property',
                         title="Property categorisation based on Price",color_discrete_sequence = px.colors.sequential.RdBu)
    pie_chart_1.update_traces(text=property['Property'],textposition = 'inside')
    pie_chart_1.update_layout(title_font=dict(size=28),title_font_color="#AD71EF",uniformtext_minsize=12,
                            uniformtext_mode='hide',autosize=False,width=500,height=500)
    prop_list = df.property_type.unique().tolist()
    price_list = df.price.unique().tolist()
    fig = go.Figure(go.Bar(
            x=price_list,
            y=prop_list,
            #text=price_list,textposition="auto",
            marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),orientation='h'))

    return property,fig_new,pie_chart_1,fig


def room_nights():

    df = file_read()
    room_nights  = df.groupby(['room_type']).minimum_nights.mean().round().sort_values().to_frame()
    room_nights = room_nights.reset_index()
    room_nights.rename(columns={"room_type":"Room_Type","minimum_nights":"Average_Min_Nights"},inplace=True)
    fig_2= px.bar(room_nights, x='Room_Type', y='Average_Min_Nights',
                            color='Average_Min_Nights', color_continuous_scale='thermal',
                            title='Room_type vs Average_Min_Nights', height=500,
                            text = 'Average_Min_Nights')
    fig_2.update_layout(title_font=dict(size=28), title_font_color='#AD71EF')
    fig_2.update_traces(textposition='outside')
    pie_chart_2 = px.pie(room_nights, values='Average_Min_Nights', names='Room_Type',
                       title=f'Room_type vs Average_Min_Nights',
                       color_discrete_sequence=px.colors.sequential.RdBu)
    pie_chart_2.update_traces(text = room_nights['Room_Type'],textposition='inside')
    pie_chart_2.update_layout(title_font=dict(size=28), title_font_color='#AD71EF',uniformtext_minsize=12, uniformtext_mode='hide',autosize=False,
    width=500,
    height=500)
    return room_nights,fig_2,pie_chart_2

def total_hosts():

    df = file_read()
    total_host = df.host_name.count().round(2)
    total_reviews = df.host_response_rate.sum().round(2)

    data_2 = {
        'Total_Host': [total_host],
        'Total_Reviews': [total_reviews]

    }

    total_host_review = pd.DataFrame(data_2)
    total_host_review

    plt.bar(total_host_review.columns, total_host_review.iloc[0], color=['blue', 'green'])
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Total Hosts and Total Reviews')
    plt.show()

    return total_host_review


def get_country_price():

    df = file_read()
    country = df.groupby(['country']).price.mean().round(2).sort_values().to_frame()
    country = country.reset_index()
    country.rename(columns={"country":"Country","price":"Price"},inplace=True)
    fig_3 = px.bar(country,x="Country",y="Price",color="Price",
                   color_continuous_scale='thermal',
                   title = "Country categorisation based on Price",height = 500,
                   text="Price")
    fig_3.update_layout(title_font=dict(size=30),title_font_color = "#AD71EF")
    #fig_3.update_traces(text_position = 'outside')
    pie_chart_3 = px.pie(country,values ="Price",names="Country",title = "Country categorisation based on Price",
                         color_discrete_sequence = px.colors.sequential.RdBu)
    pie_chart_3.update_layout(title_font = dict(size=30),title_font_color="#AD71EF",uniformtext_minsize = 12,uniformtext_mode = "hide",
                                 autosize=False,width=500,height=500)
    pie_chart_3.update_traces(text=country['Country'],textposition ="inside")

    return country,fig_3,pie_chart_3

def room_reviews():

    df =file_read()
    room_type_aggregate = df.groupby('room_type').number_of_reviews.max()
    rev = pd.DataFrame(room_type_aggregate)
    rev = rev.reset_index()
    rev.rename(columns={"room_type":"Room Types","number_of_reviews":"No of Reviews"},inplace=True)
    rev = rev.sort_values(by='No of Reviews',ascending =False)
    fig_4 = px.bar(rev,x="Room Types",y="No of Reviews",color="No of Reviews",
                   color_continuous_scale='thermal',title="Most Reviewed Rooms by Hosts",
                   height=500,text='No of Reviews')
    fig_4.update_layout(title_font=dict(size=30),title_font_color="#AD71EF")
    #fig_4.update_traces(text_position='outside')
    pie_chart_4 = px.pie(rev,values="No of Reviews",names="Room Types",title = "Most Reviewed Rooms by Hosts",
                        color_discrete_sequence=px.colors.sequential.RdBu)
    pie_chart_4.update_layout(title_font = dict(size=30),title_font_color="#AD71EF",uniformtext_minsize=15,uniformtext_mode = "hide",
                              autosize=False,width=500,height=500)
    pie_chart_4.update_traces(text = rev['Room Types'],textposition = 'inside')

    return rev,fig_4,pie_chart_4

def room_price_rev():

    df=file_read()
    review = df.groupby(['room_type','price']).number_of_reviews.sum().round(2).sort_values().to_frame()
    review = review.reset_index()
    review.rename(columns={"room_type":"Room_type","price":"Price",'number_of_reviews':"No_of_reviews"},inplace=True)
    fig_5=px.bar(review,x='Room_type',y='Price',color="Price",
                 color_continuous_scale='thermal',title='Room Reviews Based on Price',
                 height=500,text="No_of_reviews")
    fig_5.update_layout(title_font=dict(size=28),title_font_color="#AD71EF")
    pie_chart_5 = px.pie(review,values="Price",names="Room_type",title= "Room Reviews Based on Price",
                         color_discrete_sequence=px.colors.sequential.RdBu)
    pie_chart_5.update_layout(title_font=dict(size=28),title_font_color="#AD71EF",uniformtext_minsize=15,uniformtext_mode="hide",
                              autosize=False,width=500,height=500)
    pie_chart_5.update_traces(text=review['Room_type'],textposition='inside')

    return review,fig_5,pie_chart_5

def room_availability():

    df=file_read()

    df_sample = df[0:10][['country','property_type','room_type','price','availability_30','availability_60','availability_90',
                        'availability_365']]
    df_sample.rename(columns={"country":"Country","property_type":"Property_Type","price":"Price","room_type":"Room Type","availability_30":"Availability_30","availability_60":"Availability_60","availability_90":"Availability_90","availability_365":"Availability_365"},inplace=True)
    fig = ff.create_table(df_sample,colorscale = 'Cividis')
    return fig

def tree_map():
    df = file_read()
    fig=px.treemap(df,path=['property_type','room_type','host_neighbourhood'],values = "host_response_rate",hover_data = ["host_response_rate"],
                        color="room_type")
    fig.update_layout(width=1200,height=750)
    return fig

def relate():
    df=file_read()
    data2=px.scatter(df,x='host_neighbourhood',y='number_of_reviews',color='number_of_reviews')
    data2['layout'].update(title="Relationship between Host_neighbourhood and Number_of_reviews",
                            titlefont =dict(size=20),xaxis=dict(title="Host_neighbourhood",titlefont=dict(size=19)),
                            yaxis=dict(title = "No of Reviews",titlefont=dict(size=19)),width=1200,height=650)
    return data2

def host_nbr_review(host_nbr):
    df=file_read()
    filtered_df = df[df['host_neighbourhood'].isin(host_nbr)]
    host_nbr_rev = filtered_df.groupby(['host_neighbourhood']).number_of_reviews.mean().round(2).sort_values().to_frame()
    host_nbr_rev = host_nbr_rev.reset_index()
    host_nbr_rev.rename(columns={"host_neighbourhood":"Host Neighbourhood","number_of_reviews":"Number of Reviews"},inplace=True)
    data3=px.scatter(host_nbr_rev,x='Host Neighbourhood',y='Number of Reviews',color='Number of Reviews')
    data3['layout'].update(title="Relationship between Host_neighbourhood and Number_of_reviews",
                            titlefont =dict(size=20),xaxis=dict(title="Host_neighbourhood",titlefont=dict(size=19)),
                            yaxis=dict(title = "No of Reviews",titlefont=dict(size=19)),width=1200,height=650)
    return host_nbr_rev,data3


def get_hmap():

    df=file_read()
    df_corr = df[['price','host_response_rate','minimum_nights','maximum_nights']].corr()
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.heatmap(df_corr,annot=True,cmap='RdYlGn')
    ax.set_title('Correlation between Price, Host Response Rate, and Staying (min_nights, max_nights)')
    return fig

def room_clean(room_choice):
    df=file_read()
    filtered_df = df[df['room_type'].isin(room_choice)]
    room_bedroom  = filtered_df.groupby(['room_type','bedrooms']).review_scores_cleanliness.mean().round(2).sort_values().to_frame()
    room_bedroom = room_bedroom.reset_index()
    room_bedroom.rename(columns={"room_type":"Room_Type","bedrooms":"Bedrooms","review_scores_cleanliness":"Review_scores_cleanliness"},inplace=True)
    fig_8=px.bar(room_bedroom,x='Room_Type',y='Bedrooms',color="Review_scores_cleanliness",
                    color_continuous_scale='thermal',title='Room Reviews Based on Price',
                    height=650,text="Bedrooms")
    fig_8.update_layout(title_font=dict(size=28),title_font_color="#AD71EF")
    pie_chart_8 = px.pie(room_bedroom,values="Review_scores_cleanliness",names="Room_Type",title= "Room Cleanliness Review Score",
                            color_discrete_sequence=px.colors.sequential.RdBu)
    pie_chart_8.update_layout(title_font=dict(size=28),title_font_color="#AD71EF",uniformtext_minsize=15,uniformtext_mode="hide",
                                autosize=False,width=500,height=500)
    pie_chart_8.update_traces(text=room_bedroom['Room_Type'],textposition='inside')

    return room_bedroom,fig_8,pie_chart_8



def host_review():
    
    df = file_read()
    host_reviews  = df.groupby(['host_neighbourhood','host_name']).number_of_reviews.mean().round(2).sort_values().to_frame()
    host_reviews = host_reviews.reset_index()
    host_reviews.rename(columns={"host_neighbourhood":"Host_neighbourhood","host_name":"Host_Name","number_of_reviews":"Number_of_Reviews"},inplace=True)
    
    host_nbr = df['host_neighbourhood'].unique()
    review_list = df['number_of_reviews'].unique()
    host_name_list =df['host_name'].unique()
    
    fig = make_subplots(rows=1,cols=2,subplot_titles=("Host_neighbourhood and Reviews given by Hosts", "Host_name and Reviews"))   

    fig.add_trace(
        go.Scatter(x=host_nbr,y=review_list,mode='lines+markers'),

        row=1,col=1
    )

    fig.add_trace(
        go.Scatter(x=host_name_list,y=review_list,mode='lines+markers'),

        row=1,col=2)

    fig.update_layout(height=800,width=1000)
    fig.show()

    return host_reviews,fig

os.chdir(r"C:\Users\ASUS\Documents\GUVI ZEN CLASSES\MAINT BOOT\AIR BNB PROJECT")

st.sidebar.image("airbnb.jpg")

with st.sidebar:

    select = option_menu("Main Menu",["HOME","DATA VIEW","DATA ANALYTICS","DATA VISUALS"])

if select == "HOME":

    os.chdir(r"C:\Users\ASUS\Documents\GUVI ZEN CLASSES\MAINT BOOT\AIR BNB PROJECT")

    st.image("image3.jpg")

    st.header(":violet-background[:red[**About Airbnb**]]")
    st.write("")
    st.write('''***Airbnb is an online marketplace that connects people who want to rent out
              their property with people who are looking for accommodations,
              typically for short stays. Airbnb offers hosts a relatively easy way to
              earn some income from their property.Guests often find that Airbnb rentals
              are cheaper and homier than hotels.***''')
    st.write("")
    st.write('''***Airbnb Inc (Airbnb) operates an online platform for hospitality services.
                  The company provides a mobile application (app) that enables users to list,
                  discover, and book unique accommodations across the world.
                  The app allows hosts to list their properties for lease,
                  and enables guests to rent or lease on a short-term basis,
                  which includes vacation rentals, apartment rentals, homestays, castles,
                  tree houses and hotel rooms. The company has presence in China, India, Japan,
                  Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy,
                  Norway, Portugal, Russia, Spain, Sweden, the UK, and others.
                  Airbnb is headquartered in San Francisco, California, the US.***''')
    
    st.header(":violet-background[:red[**Background of Airbnb**]]")
    st.write("")
    st.write('''***Airbnb was born in 2007 when two Hosts welcomed three guests to their
              San Francisco home, and has since grown to over 4 million Hosts who have
                welcomed over 1.5 billion guest arrivals in almost every country across the globe.***''')

elif select == "DATA VIEW":

    f1 = st.file_uploader(":file_folder: Upload a file",type = (["csv","txt","xlsx","xls"]))

    if f1 != None:
       filename = f1.name

       #st.write(filename)     
       df = pd.read_csv(filename,na_filter=False,index_col=0)
    else:

        os.chdir(r"C:\Users\ASUS\Documents\GUVI ZEN CLASSES\MAINT BOOT\AIR BNB PROJECT")
        df=pd.read_csv("Air_bnb.csv",na_filter=False,index_col=0)
        

    button = st.button("Submit",use_container_width=True)

    if button:
        
        with st.spinner("Extracting Data:satellite_antenna:"):
            t.sleep(25)

        if f1 != None:
            
           df


elif select == "DATA ANALYTICS": 

    tab1,tab2,tab3 = st.tabs(["Price Analysis","Country Analysis","Review Analysis"])

    with tab1:        

        option = st.radio("Select the Option",["Price vs Room Type","Price Vs Property Type","Property Type vs Count"])

        if option == "Price vs Room Type":  

            col1,col2 = st.columns(2)

            with col1:
            
                select_type = st.multiselect("Select the Type",room_ch(),placeholder="Select the Type...")

                if st.button(":violet[**Get Data**]",use_container_width=True):

                    if select_type: 

                        filtered_data,fig,pie_chart= room_price(select_type)

                        st.dataframe(filtered_data)
                        st.plotly_chart(pie_chart)

                        with col2:
                            st.plotly_chart(fig)

        elif option == "Price Vs Property Type":

            col1,col2 = st.columns(2)

            with col1:
            
                select_type = st.multiselect("Select the Type",prop_price(),placeholder="Select the Type...")

                if st.button(":violet[**Get Data**]",use_container_width=True):
                    if select_type:

                        filtered_data,fig= get_property_price(select_type)

                        st.dataframe(filtered_data)
                                                
                        with col2:
                            st.plotly_chart(fig)

        elif option == "Property Type vs Count":

            col1,col2 = st.columns(2)

            with col1:

                select_type = st.multiselect("Select the Type",prop_price(),placeholder="Select the type...")

                if st.button(":violet[**Get Data**]",use_container_width=True):

                    if select_type:

                        filtered_data,fig_8,pie_chart_8 = prop_count(select_type)

                        st.dataframe(filtered_data)
                        st.plotly_chart(pie_chart_8)

                        with col2:

                            st.plotly_chart(fig_8)


    with tab2:

        option = st.radio("Select the Option",["Country vs Price","Country Vs Reviews"])

        if option == "Country vs Price":  

            col1,col2 = st.columns(2)

            with col1:
            
                select_type = st.multiselect("Select the Type",country_choice(),placeholder="Select the Type...")

                if st.button(":violet[**GET DATA**]",use_container_width=True):

                    if select_type:

                        filtered_data,fig_6,pie_chart_6= country_price(select_type)

                        st.dataframe(filtered_data)
                        st.plotly_chart(pie_chart_6)

                        with col2:
                            st.plotly_chart(fig_6)

        if option == "Country Vs Reviews":  

            col1,col2 = st.columns(2)

            with col1:
            
                select_type = st.multiselect("Select the Type",country_choice(),placeholder="Select the Type...")

                if st.button(":violet[**GET DATA**]",use_container_width=True):

                    if select_type:

                        filtered_data,fig_7,pie_chart_7= country_reviews(select_type)

                        st.dataframe(filtered_data)
                        st.plotly_chart(pie_chart_7)

                        with col2:
                            st.plotly_chart(fig_7)

    with tab3:

        option = st.radio("Select the Option",["Host_Neighbourhood vs Reviews","Rooms vs Cleanliness Reviews Scores"])

        if option == "Host_Neighbourhood vs Reviews":  

            col1,col2 = st.columns(2)

            with col1:
            
                select_type = st.multiselect("Select the Type",host_nbr_choice(),placeholder="Select the Type...")

                if st.button(":violet[**Submit**]",use_container_width=True):

                    if select_type:

                        host_nbr_rev,data3= host_nbr_review(select_type)

                        st.dataframe(host_nbr_rev)
                        

                        with col2:
                            st.plotly_chart(data3)


        if option == "Rooms vs Cleanliness Reviews Scores":  

            col1,col2 = st.columns(2)

            with col1:

                select_type_1 = st.multiselect('Select the Type_1',room_ch(),placeholder="Select the Type_1....")

                if st.button(":violet[**Submit**]",use_container_width=True):
                    
                    if select_type_1:

                        filtered_data,fig_8,pie_chart_8 = room_clean(select_type_1)

                        st.dataframe(filtered_data)
                        st.plotly_chart(pie_chart_8)

                        with col2:
                            st.plotly_chart(fig_8)


elif select == "DATA VISUALS":

        options = st.selectbox(":violet[_Insights_]",("Select the Quries to be Analysed:",
            "1.Which Room type is most Occupied?",
            "2.Relationship between Hostneighbourhood and Room type",
            "3.Country categorisation based on Price",
            "4.Property categorisation based on Price",
            "5.Most Reviewed Rooms by Hosts",
            "6.Hierarchical view of Property Type",
            "7.Room availability summary table",
            "8.How the price and Host repsonse rate affects the staying?",
            "9.Relationship between Host_neighbourhood and No of Reviews",
            "10.Room Reviews Based on Price",
            "11.Reviews given by hosts on Host_neighbourhood"
             ),
            index=None,
            placeholder="Select the Query...",
            )


        st.write('You selected:', options)

        if options == "1.Which Room type is most Occupied?":

            col1,col2 = st.columns(2)

            with col1:

                if st.button(":violet[**Get Data**]",use_container_width=True):

                    filtered_data_1,fig_2,pie_chart_2= room_nights()

                    st.dataframe(filtered_data_1)
                    st.plotly_chart(pie_chart_2)

                    with col2:
                        st.plotly_chart(fig_2)

        elif options == "2.Relationship between Hostneighbourhood and Room type":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                    df = file_read()
                    fig=px.sunburst(df,path=['host_neighbourhood','room_type'],values='price')
                    fig.update_layout(title={'text': "Sunburst Chart of Host Neighbourhood and Room Type:",
                                             'font': {'size': 24}},width=800,height=650)                                            
                    st.plotly_chart(fig)
                    

            

        elif options == "3.Country categorisation based on Price":

            col1,col2 = st.columns(2)

            with col1:

                if st.button(":violet[**Get Data**]",use_container_width=True):

                    filter_data,fig_3,pie_chart_3 = get_country_price()

                    st.dataframe(filter_data)
                    st.plotly_chart(pie_chart_3)

                    with col2:

                        st.plotly_chart(fig_3)

        elif options == "4.Property categorisation based on Price":

            col1,col2 =st.columns(2)

            with col1:

                if st.button(":violet[**Get Data**]",use_container_width=True):

                    filtered_data,fig_new,pie_chart_1,fig = property_price()
                    
                    st.dataframe(filtered_data)
                    st.plotly_chart(pie_chart_1)
                    

                    with col2:
                        st.plotly_chart(fig_new)
                        st.plotly_chart(fig)

        elif options == "5.Most Reviewed Rooms by Hosts":

            col1,col2 =st.columns(2)

            with col1:

                if st.button(":violet[**Get Data**]",use_container_width=True):

                    filtered_data,fig_4,pie_chart_4 = room_reviews()

                    st.dataframe(filtered_data)
                    st.plotly_chart(pie_chart_4)

                    with col2:
                        st.plotly_chart(fig_4)

        elif options == "6.Hierarchical view of Property Type":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                st.plotly_chart(tree_map())

        elif options == "7.Room availability summary table":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                filtered_data = room_availability()

                st.plotly_chart(filtered_data)

        elif options == "8.How the price and Host repsonse rate affects the staying?":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                st.pyplot(get_hmap())
        

        elif options == "9.Relationship between Host_neighbourhood and No of Reviews":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                st.plotly_chart(relate())

        elif options == "10.Room Reviews Based on Price":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                col1,col2 =st.columns(2)

                with col1:

                    filtered_data,fig_5,pie_chart_5 = room_price_rev()

                    st.dataframe(filtered_data)
                    st.plotly_chart(pie_chart_5)

                    with col2:

                        st.plotly_chart(fig_5)

        elif options == "11.Reviews given by hosts on Host_neighbourhood":

            if st.button(":violet[**Get Data**]",use_container_width=True):

                filtered_data,fig=host_review()

                st.dataframe(filtered_data)
                st.plotly_chart(fig)



            



                        

                    



            




            
                
                
                

            





            

      
       
    

