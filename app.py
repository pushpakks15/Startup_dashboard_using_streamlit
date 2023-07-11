import pandas
import streamlit as st  #importing
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns

df=pd.read_csv('startup.csv')
st.set_page_config(layout='wide',page_title='Startup Analysis')

df2=pd.read_csv('Startups1.csv')





def investor_details(investor):
    df1=df[df['investor'].str.contains(investor)].groupby('startup').sum().sort_values(by='Rs in crores',ascending=False).head(5)
    st.title(investor)
    st.subheader('Recent investment details')
    st.dataframe(df[df['investor'].str.contains(investor)].head(5))
    st.subheader('Top 5 biggest investments')
    df1_reset_index = df1.reset_index()
    # Create a column chart using altair
    chart = alt.Chart(df1_reset_index).mark_bar().encode(
        x='startup',
        y='Rs in crores'
    )

    # Adjust chart properties if necessary
    chart = chart.properties(
        width=alt.Step(40)  # Adjust the width of the columns as needed
    )

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

    #Two cols layout:
    c1,c2=st.columns(2)

    with c1:
        st.subheader('Sectors Invested')
        v_series=df[df['investor'].str.contains(investor)].groupby('vertical')['Rs in crores'].sum()
        fig, ax = plt.subplots()
        ax.pie(v_series, labels=v_series.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures a circular pie chart

        st.pyplot(fig)

    with c2:
        st.subheader('Type of investments')
        v_series1 = df[df['investor'].str.contains(investor)].groupby('invest_type')['Rs in crores'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(v_series1, labels=v_series1.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures a circular pie chart

        st.pyplot(fig1)


    #4th plot
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    series1=df[df['investor'].str.contains(investor)].groupby('year')['Rs in crores'].sum()
    st.subheader('Year wise investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(series1.index,series1.values)
    st.pyplot(fig2)


st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select one',['Overall Analysis','Start-ups','Investors'])


def load_analysis():
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    st.title('Overall Analysis')
    a,b,c,d=st.columns(4)
    with a:
        total=round(df['Rs in crores'].sum()) #Total amt invested
        st.metric('Total Funding' , f'{total} CR')
    with b:
        max_amt=round(df['Rs in crores'].max())
        st.metric('Max amount invested',f'{max_amt} CR')
    with c:
        mean_amt=round(df['Rs in crores'].mean())
        st.metric('Average amount invested',f'{mean_amt} CR')
    with d:
        startups=df['startup'].nunique()
        st.metric('Total startups funded',f'{startups}')

    st.subheader('Month wise investment')


    #2
    col1,col2=st.columns(2)
    with col1:
        st.subheader('1. Month wise amount invested')
        fig3, ax3 = plt.subplots()
        temp_df = df.groupby(['year', 'month'])['Rs in crores'].sum().reset_index()
        temp_df['month_year'] = temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str)
        ax3.plot(temp_df['month_year'], temp_df['Rs in crores'])
        st.pyplot(fig3)
    with col2:
        st.subheader('2. Month wise no of Startups funded')
        fig4, ax4 = plt.subplots()
        temp_df = df.groupby(['year', 'month'])['startup'].count().reset_index()
        temp_df['month_year'] = temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str)
        ax4.plot(temp_df['month_year'], temp_df['startup'])
        st.pyplot(fig4)

    #3
    one,two=st.columns(2)
    with one:
        st.subheader('Type of funding')
        v_series2 = df['invest_type'].value_counts()
        fig5, ax5 = plt.subplots()
        ax5.pie(v_series2, labels=v_series2.index, autopct='%1.1f%%', startangle=90)
        ax5.axis('equal')  # Equal aspect ratio ensures a circular pie chart
        st.pyplot(fig5)
    with two:
        st.subheader('City wise funding')
        v_series3 = df['city'].value_counts()
        fig6, ax6 = plt.subplots()
        ax6.pie(v_series3, labels=v_series3.index, autopct='%1.1f%%', startangle=90)
        ax6.axis('equal')  # Equal aspect ratio ensures a circular pie chart
        st.pyplot(fig6)


    ek,don=st.columns(2)
    with ek:
        st.subheader('Top startups in recent years')
        tdf=df.groupby(['startup', 'year'])['Rs in crores'].sum().sort_values(ascending=False).reset_index().drop_duplicates(
            subset='year').sort_values(by='year', ascending=False)
        st.dataframe(tdf)

    with don:
        st.subheader('Top investors in recent years')
        tdf1 = df.groupby(['investor', 'year'])['Rs in crores'].sum().sort_values(
            ascending=False).reset_index().drop_duplicates(
            subset='year').sort_values(by='year', ascending=False)
        st.dataframe(tdf1)

    st.subheader('Amount invested in different years')
    data=df.groupby(['year'])['Rs in crores'].sum().reset_index()
    fig7, ax7 = plt.subplots()
    sns.heatmap(data, annot=True, cmap='YlGnBu', fmt=".1f", ax=ax7)
    st.pyplot(fig7)


def startup_details(startup):
    st.title(startup)
    st.write(df2[df2['Company'] == startup]['Description'].iloc[0])
    edf = df2[df2['Company'] == startup]['Founders'].tolist()
    st.subheader("I] Founders")
    for i in edf:
        st.write(i)

    st.subheader('II] Location')
    st.write(df2[df2['Company'] == startup]['City'].iloc[0])

    edf1 = df2[df2['Company'] == startup]['Industries'].tolist()
    st.subheader("III] Industries")
    for i in edf1:
        st.write(i)

    st.subheader('IV] Founded on')
    st.write(df2[df2['Company'] == startup]['Starting Year'].iloc[0])

    st.subheader('V] No of investors')
    st.write(df2[df2['Company'] == startup]['No. of Investors'].iloc[0])

    st.subheader(f'VI] Total amount invested in {startup} (in CR)')
    st.write(((df2[df2['Company'] == startup]['Funding Amount in $']*80)/10000000).iloc[0])







if option=='Overall Analysis':
    btn3=st.sidebar.button('Load overall analysis')
    if btn3:
        load_analysis()
elif option=='Start-ups':
    start_up=st.sidebar.selectbox('Select one startup',sorted(df2['Company'].unique().tolist()))
    btn1=st.sidebar.button("Find startup details")
    if btn1:
        startup_details(start_up)

else:
    investor=st.sidebar.selectbox('Select one investor',sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find investor details")
    if btn2:
        investor_details(investor)





