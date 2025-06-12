import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="App.py", layout="wide")

myconnection = pymysql.connect(
    host='localhost',
    user='root',
    password='Theja@22',
    database='project_nasa')

mycursor=myconnection.cursor()

if 'page' not in st.session_state:
    st.session_state.page = 'filters'


# Sidebar navigation
st.sidebar.markdown("## 🚀 Asteroid Data Explorer")
if st.sidebar.button("🔍 Use Filters"):
    st.session_state.page = 'filters'
if st.sidebar.button("📊 Go to  Query Options"):
    st.session_state.page = 'queries'

st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🚀 AstroScope: NASA NEO Explorer</h2>", unsafe_allow_html=True)
st.markdown("---")                                                                                  

if st.session_state.page == 'filters':

    col1, spacer1,col2,spacer2,col3 = st.columns([1,0.2,1,0.2,1])


    with col1:
        
        au=st.slider("Austronomial Unit", 0.00,0.50,(0.00,0.30))  
        lunar=st.slider("Miss Distance Lunar", 0.299363,194.46,(0.34,23.9)) 
        magnitude = st.slider("Absolute Magnitude", 0.0, 33.0, (10.17, 32.3))
     

    with col2:
        min_diameter=st.slider("Minimum Estimated Diameter(KMPH) ", 0.00,23.00,value=(0.00,12.00))
        max_diameter=st.slider("Maximum Estimated Diameter(KMPH) ", 0.00,50.00,value=(0.00,12.00))
        velocity=st.slider("Relative Velocity KMPH", 1054.26,186136.00,value=(1054.26,186136.00))   
        
    with col3:
        start_date = st.date_input("Start Date", datetime(2025, 1,1))
        end_date = st.date_input("End Date", datetime(2027, 7, 29))
        hazard = st.selectbox("Hazardous?", ["All", "Yes", "No"])
      
   

            


    button=st.button("Filter")
    query="""SELECT
       asteroids.id, asteroids.name, asteroids.absolute_magnitude_h, asteroids.estimated_diameter_min_km, 
      asteroids.estimated_diameter_max_km, asteroids.Hazard,close_approach.close_approach_date,close_approach.relative_velocity_kmph,
      close_approach.miss_distance_km,close_approach.astronomical, close_approach.miss_distance_lunar,close_approach.orbiting_body
      FROM asteroids JOIN close_approach ON asteroids.id=close_approach.neo_reference_id
      WHERE  
     close_approach.astronomical BETWEEN %s AND %s
     AND close_approach.miss_distance_lunar BETWEEN %s AND %s
     AND asteroids.absolute_magnitude_h BETWEEN %s AND %s
     AND asteroids.estimated_diameter_min_km BETWEEN %s AND %s
     AND asteroids.estimated_diameter_max_km BETWEEN %s AND %s
     AND close_approach.relative_velocity_kmph BETWEEN %s AND %s
     AND close_approach.close_approach_date BETWEEN %s AND %s
      """

    if hazard == "Yes":
        query += " AND asteroids.Hazard = 1"
    
    elif hazard == "No":
         query += " AND asteroids.Hazard = 0"

    parameters= [
        au[0],au[1],
        lunar[0],lunar[1],
        magnitude[0],magnitude[1],
        min_diameter[0],min_diameter[1],
        max_diameter[0],max_diameter[1],
        velocity[0],velocity[1],
        start_date,end_date,
       
        ]

    if button:
        mycursor.execute(query,parameters)
        rows=mycursor.fetchall()
        dff=pd.DataFrame(rows, columns=[i[0]for i in mycursor.description])
        st.dataframe(dff)





     
     
   


# # -------------------- SIMULATED DATA + RESULT --------------------
# if filter_btn:
#     # For now, just simulate some data to show layout
#     data = {
#         "name": ["Asteroid A", "Asteroid B"],
#         "velocity_kmph": [45000, 120000],
#         "diameter_km": [3.2, 7.8],
#         "hazardous": ["Yes", "No"],
#         "approach_date": ["2024-08-01", "2024-10-20"]
#     }
#     df = pd.DataFrame(data)
#     st.markdown("### 🪐 Filtered Results")
#     st.dataframe(df)
  

elif st.session_state.page == 'queries':
    st.markdown("")


    st.subheader("Choose the Pre-defined Querys")
    query_options = [
        "1. Count how many times each asteroid has approached Earth",
        "2. Average velocity of each asteroid over multiple approaches",
        "3. List top 10 fastest asteroids",
        "4. Find potentially hazardous asteroids that have approached Earth more than 3 times",
        "5. Find the month with the most asteroid approaches",
        "6. Get the asteroid with the fastest ever approach speed",
        "7. Get the asteroid with the fastest ever approach speed",
        "8. An asteroid whose closest approach is getting nearer over time",
        "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
        "10. List names of asteroids that approached Earth with velocity > 50,000 km/h",
        "11. Count how many approaches happened per month",
        "12. Find asteroid with the highest brightness (lowest magnitude value)",
        "13. Get number of hazardous vs non-hazardous asteroids",
        "14. Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
        "15. Find asteroids that came within 0.05 AU(astronomical distance)"
    ]
    select_query = st.selectbox("Choose your Query", query_options)

    if st.button("Run Query"):
        if select_query=='1. Count how many times each asteroid has approached Earth':
            mycursor.execute('select count(*),id from asteroids group by id order by count(*) desc;')
            result=mycursor.fetchall()
            df=pd.DataFrame(result,columns=[i[0]for i in mycursor.description])
            st.dataframe(df)
        elif select_query=="2. Average velocity of each asteroid over multiple approaches":
            mycursor.execute('select avg(relative_velocity_kmph) as Average_velocity, count(*), neo_reference_id from close_approach group by neo_reference_id;')
            result=mycursor.fetchall()
            df1=pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
            st.dataframe(df1)
        elif select_query=="3. List top 10 fastest asteroids":
            mycursor.execute('select relative_velocity_kmph, neo_reference_id from close_approach order by relative_velocity_kmph desc limit 10; ')
            result=mycursor.fetchall()
            df2=pd.DataFrame(result, columns=[i[0] for i in mycursor.description])
            st.dataframe(df2)
        elif select_query=="4. Find potentially hazardous asteroids that have approached Earth more than 3 times":
            mycursor.execute('''select a.id,a.name,a.Hazard,count(a.id)as approached_count from asteroids as a join close_approach as c on 
            a.id=c.neo_reference_id where Hazard=True group by a.id,a.name having count(a.id)>3 order by count(a.id)desc;''')
            resultt=mycursor.fetchall()
            df4=pd.DataFrame(resultt, columns=(i[0]for i in mycursor.description))
            st.dataframe(df4)
        elif select_query=="5. Find the month with the most asteroid approaches":
            mycursor.execute('''select count(month(close_approach_date))as total_approach,month(close_approach_date)as Month 
            from close_approach group by month(close_approach_date) order by total_approach desc limit 1 ;''')
            resultt=mycursor.fetchall()
            df5=pd.DataFrame(resultt, columns=(i[0]for i in mycursor.description))
            st.dataframe(df5)      
        elif select_query=="6. Get the asteroid with the fastest ever approach speed":
            mycursor.execute(''' select  neo_reference_id,  relative_velocity_kmph from close_approach
            order by relative_velocity_kmph desc limit 1;''')
            resultt=mycursor.fetchall()
            df6=pd.DataFrame(resultt, columns=(i[0]for i in mycursor.description))
            st.dataframe(df6)
        elif select_query=="7. Get the asteroid with the fastest ever approach speed":
            mycursor.execute('''select id,name,estimated_diameter_max_km from asteroids order by estimated_diameter_max_km desc;''')
            result=mycursor.fetchall()
            df7=pd.DataFrame(result, columns=(i[0] for i in mycursor.description))
            st.dataframe(df7)        
        elif select_query=="8. An asteroid whose closest approach is getting nearer over time":
            mycursor.execute('''select name,close_approach_date, miss_distance_km from asteroids join close_approach
            on id=neo_reference_id order by miss_distance_km limit 1;''')
            result=mycursor.fetchall()
            df8=pd.DataFrame(result, columns=(i[0] for i in mycursor.description))
            st.dataframe(df8)        
        elif select_query=="9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
            mycursor.execute('''select name, max(close_approach_date),min(miss_distance_km) from asteroids join close_approach on id=neo_reference_id 
            group by name order by min(miss_distance_km),max(close_approach_date) desc;''')
            result=mycursor.fetchall()
            df9=pd.DataFrame(result, columns=(i[0]for i in mycursor.description))
            st.dataframe(df9)        
        elif select_query=="10. List names of asteroids that approached Earth with velocity > 50,000 km/h":
            mycursor.execute('''SELECT name,relative_velocity_kmph FROM asteroids 
            JOIN close_approach  ON id = neo_reference_id
            WHERE relative_velocity_kmph > 50000;''')
            result=mycursor.fetchall()
            df10=pd.DataFrame(result, columns=(i[0] for i in mycursor.description))
            st.dataframe(df10)        
        elif select_query=="11. Count how many approaches happened per month":
            mycursor.execute('''select count(month(close_approach_date))as total_approach,month(close_approach_date)as Month 
            from close_approach group by month(close_approach_date) order by total_approach desc limit 1 ;''')
            resultt=mycursor.fetchall()
            df11=pd.DataFrame(resultt, columns=(i[0]for i in mycursor.description))
            st.dataframe(df11)   
        elif select_query=="12. Find asteroid with the highest brightness (lowest magnitude value)":
            mycursor.execute('select * from asteroids order by absolute_magnitude_h limit 1;')
            result=mycursor.fetchall()
            df12=pd.DataFrame(result, columns=(i[0]for i in mycursor.description))
            st.dataframe(df12)         
        elif select_query=="13. Get number of hazardous vs non-hazardous asteroids":
            mycursor.execute('SELECT hazard AS hazard_status,COUNT(*) FROM asteroids GROUP BY hazard;')
            result=mycursor.fetchall()
            df13=pd.DataFrame(result, columns=(i[0]for i in mycursor.description))
            st.dataframe(df13)       
        elif select_query=="14. Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance":
            mycursor.execute('''select id, close_approach_date, miss_distance_lunar from asteroids join
            close_approach on id=neo_reference_id where miss_distance_lunar <1;''')
            result=mycursor.fetchall()
            df14=pd.DataFrame(result, columns=(i[0]for i in mycursor.description))
            df14.drop_duplicates(inplace=True)
            st.dataframe(df14)         
        elif select_query=="15. Find asteroids that came within 0.05 AU(astronomical distance)":
            mycursor.execute('select neo_reference_id, astronomical from close_approach where astronomical <0.05;')
            result=mycursor.fetchall()
            df15=pd.DataFrame(result, columns=(i[0]for i in mycursor.description))
            st.dataframe(df15)   
        









