import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Crime Analysis",page_icon=":barchart:",layout='wide')

crime_df=pd.read_csv('P7.csv',usecols=[0,1,2,3,4,5,6,7,8,9],nrows=5128)
#crime_df=crime_df.astype(str)


df_c=crime_df.dropna()
df_c['day'] =pd.to_datetime(df_c['Create_Date_Time'],dayfirst=True)
df_c['day']=pd.to_datetime(df_c['day'],yearfirst=True)
new_df = pd.read_csv("P7.csv")
new_df.dropna(inplace=True)
df_c['Create_Date_Time']=new_df['Create_Date_Time']
df_c['Time']=pd.to_datetime(df_c['Create_Date_Time']).dt.time
df_c['Prop_date']=(df_c['day']).dt.strftime('%d/%m/%Y')
month = pd.to_datetime(df_c['Prop_date'],dayfirst=True).dt.strftime('%m')
df_c['month']=month
st.sidebar.header("Filters")
month=st.sidebar.multiselect("Select the Month:",
                             options=df_c['month'].unique(),
                             default=df_c['month'].unique()
                            )
c = st.sidebar.multiselect("Select the Circle:",
            options=df_c["Circle"].unique(),
            default=df_c["Circle"].unique()
        )
ps = st.sidebar.multiselect(
            "Select the Police_Station:",
            options=df_c["Police_Station"].unique(),
            default=df_c["Police_Station"].unique()
        )

df_c.rename(columns = {"Police_Station":"Police_Station"}, inplace = True)

df_selection = df_c.query(
    "month == @month & Circle == @c & Police_Station == @ps"
)
#Title
st.title(":bar_chart: Crime Analysis Dashboard")

#Data Frame displayed on app
df_selection=df_selection.astype(str)
st.dataframe(df_selection)

#Overview numbers
st.markdown("##")
total_crimes = int(df_selection["Police_Station"].count())
average_crimes = round((df_selection["Police_Station"].count()/91))

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total No. of crimes:")
    st.subheader(f"{total_crimes:,}")
with middle_column:
    st.subheader("Avg No. of crimes / day:")
    st.subheader(f"{average_crimes}")
with right_column:
    st.subheader("Most frequent crime:")
    st.subheader("Dispute")

st.markdown("""---""")


#Crimes in Lucknow
x = df_selection.drop(columns=['District', 'Event', 'Circle', 'Police_Station', 'Caller_Source', 'Event_Sub_Type'])
x2 = df_selection['Event_Type']
df2 = x.sort_values(by=['Event_Type'])
df_ = x.drop(columns=['Latitude', 'Longitude', 'day', 'Time', 'Prop_date', 'month'])
count1 = df_.groupby(['Event_Type']).count()
count1.rename(columns = {'Event_Type':'Event type', 
                       'Create_Date_Time':'No. of crimes'}, 
            inplace = True)
s = px.bar(
    count1,
    title="<b>Crimes in Lucknow</b>",
    color_discrete_sequence=["#0083B8"] * len(count1),
    template="plotly_white",
    width=1000,
    height=650,
)

st.plotly_chart(s)

#Crimes based on Month(bar)
x3=x.drop(columns=['Create_Date_Time','day'])
x4=x3.drop(columns=['Latitude','Longitude','Prop_date','Time'])
count4=x4.groupby(['month']).count()
count4.rename(columns={'month':'Month','Event_Type':'No. of crimes'},inplace=True)
#count4.index=['April','May','June']
g=px.bar(
    count4,
    x=count4.index,
    y='No. of crimes',
    title="<b>Crimes Based on Month</b>",
    color_discrete_sequence=["#0083B8"] * len(count1),
    template="plotly_white",
    width=1000,
    height=650,
)
st.plotly_chart(g)

##Crimes based on Month(pie)
g1=px.pie(
    count4,
    values='No. of crimes',names=count4.index,
    title="<b>Crimes Based on Month</b>",
    #color_discrete_sequence=["#0083B8"] * len(count1),
    template="plotly_white",
    width=1000,
    height=650,
)
st.plotly_chart(g1)

#Top 5 crimes
top_5_crimes = x3['Event_Type'].value_counts().sort_values(ascending=False).head()
temp = x3.groupby('Event_Type').agg({"month": "count"})
temp = temp.sort_values(by=['month'], ascending=False).head()
temp = temp.sort_values(by='month', ascending=True)
temp.rename(columns={'month':'No. of crimes','Event_Type':'Event_Type'},inplace=True)
g2=px.bar(
    temp,
    title="<b>Top 5 crimes</b>",
    y=temp.index,
    x='No. of crimes',
    color_discrete_sequence=["#0083B8"] * len(count1),
    template="plotly_white",
    width=1000,
    height=650,
)

st.plotly_chart(g2)

#Crimes based on days
x3['Week'] = pd.to_datetime(x['day']).dt.day_name()
x7=x3.groupby(['Week']).count()
x7=x7.drop(columns=['Latitude','Longitude','Time','Prop_date','month'])
x7.rename(columns={'Week':'Week','Event_Type':'No. of crimes'},inplace=True)
g3=px.bar(
    x7,
    title="<b>Crimes Based on Days</b>",
    y=x7.index,
    x='No. of crimes',
    color_discrete_sequence=["#0083B8"] * len(count1),
    template="plotly_white",
    width=1000,
    height=650,
)
g3.update_layout(yaxis={'categoryorder':'array','categoryarray':['Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday', 'Sunday']})

st.plotly_chart(g3)

#crimes based on time 
def hour(x):
    x = datetime.strptime(x, "%H:%M:%S")
    return x.strftime("%H")
x3['Hour_Day'] = x3['Time'].apply(hour)
test = x3.sort_values(by=['Hour_Day'])
test1 = test
test1 = test1.groupby(['Hour_Day']).count()
test2 = test1.drop(columns=['Latitude', 'Longitude', 'Prop_date', 'Time', 'month', 'Week'])
test2.rename(columns = {'Hour_Day':'Hour_Day', 
                       'Event_Type':'No. of crimes'}, 
            inplace = True)
g4 = px.bar(
      test2,
    x=test2.index,
    y='No. of crimes',
    title="<b>Crimes Based on Time</b>",
    color_discrete_sequence=["#0083B8"] * len(count1),
    template="plotly_white",
    width=1000,
    height=650,)

st.plotly_chart(g4)

'''CRIME MAP'''

#Folium MAP
from streamlit_folium import folium_static
import folium
my_map = folium.Map(location=[26.850000, 81.000], zoom_start=16, prefer_canvas=True, min_zoom=12, max_zoom=18)
for _, l in x3.iterrows():
    folium.CircleMarker(location=[l['Latitude'], l['Longitude']], popup=[l['Latitude'], l['Longitude']], tooltip=[l['Event_Type']], radius=3, color='red', fill=True, fill_color='red', fill_opacity=1,).add_to(my_map)
my_map
folium_static(my_map)