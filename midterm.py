import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
# from vega_datasets import data
from altair.datasets import data


# set title
st.set_page_config(page_title="MSU TPP Placements", layout="wide")
st.title("2025-2026 Teacher Preparation Program Placements")

# read in files
by_building = pd.read_csv("buildings.csv")
demographics = pd.read_csv("demographics_cleaned.csv")

# intro
st.write("Each year, the MSU Teacher Preparation Program places nearly one thousand students in clinical placements to prepare them to be teachers of records. The amount of placements and the range of experiences that students encounter lead to a large amount of data of interest primarily to the placements coordinators and staff/faculty in TPP. It is also of interest to applicable parties such as our district partners, our accreditor, and the Michigan Department of Education. The placement data was compiled from multiple different sources including internal placement documents, school data from mischooldata.com, and addresses from the NCES database. This data can reveal the populations and characteristics of the K-12 student population that MSU Teacher Candidates encounter as well as reveal patterns and resources for the team that places these students. Interactions with this data and resulting visualizations should reveal valuable insight for the Teacher Prep program and tell the story of the 2025-2026 school year for the teacher candidates.\n\n")
st.write(" \n")

# data
st.write("*The Data*")
st.write("The following visualizations combine three data sources:")
st.write("- student placements compiled from MSU TPP internal documents.")
st.write("- student enrollment counts from mischooldata.com.")
st.write("- school building addresses from NCES.")
st.write(" \n")


### visual number one ######################################################################################################################



st.write("_Placement School Demographics_")
st.write("The following visualization answers the following questions: What are the demographics of the schools that TPP teacher candidates are placed at? How to TPP school partners compare to overall Michigan demographics?\n\n")
st.write("Note: ELEM = Elementary, ESL = English as a Second Language, SEC = Secondary, and SPED = Special Education")
# filter results based on choices
teams = ['ELEM', 'ESL', 'SEC', 'SPED']
team_filter1 = st.multiselect("Team", teams, default = teams)
filtered = by_building[np.where(by_building.TeamStr.str.contains('|'.join(team_filter1)),True,False)]


# change column names so it is prettier on the legend
filtered.rename(columns={'AMERICAN_INDIAN_ENROLLMENT':'American Indian',
                    'AFRICAN_AMERICAN_ENROLLMENT':'African American',
                    'HISPANIC_ENROLLMENT':'Hispanic',
                    'WHITE_ENROLLMENT':'White',
                    'HAWAIIAN_ENROLLMENT':'Hawaiian',
                    'ASIAN_ENROLLMENT':'Asian',
                    'TWO_OR_MORE_RACES_ENROLLMENT':'Two or More Races'}, inplace=True)
#list of columns to pull
race = ['American Indian', 'African American', 'Asian', 'Hawaiian', 'Hispanic', 'White', 'Two or More Races']

# custom colors
colors = ["#008208", "#7BBD00", "#49CFA5", "#578800", "#42FF4F", "#0B9A6D", "#CCFA7D"]

# create the histograms
tpp_hist = alt.Chart(filtered, title=alt.Title("School Building Demographics", subtitle='Demographic distributions for buildings hosting MSU TPP Teacher Candidates')).transform_fold(
    race,
    as_=['Enrollment', 'Measurement']
).mark_bar(
    opacity=0.5,
    binSpacing=0
).encode(
    alt.X('Measurement:Q', title="Percentage Enrollment").bin(maxbins=20).axis(format='%'),
    alt.Y('count()', title='Percentage of Schools').stack("normalize"),
    alt.Color('Enrollment:N').scale(domain=race, range=colors)
)

demo = demographics[demographics["BuildingName"] != "All Buildings"]
demo.rename(columns={'AMERICAN_INDIAN_ENROLLMENT':'American Indian',
                    'AFRICAN_AMERICAN_ENROLLMENT':'African American',
                    'HISPANIC_ENROLLMENT':'Hispanic',
                    'WHITE_ENROLLMENT':'White',
                    'HAWAIIAN_ENROLLMENT':'Hawaiian',
                    'ASIAN_ENROLLMENT':'Asian',
                    'TWO_OR_MORE_RACES_ENROLLMENT':'Two or More Races'}, inplace=True)
mi_hist = alt.Chart(demo, title=alt.Title("All Michigan Building Demographics", subtitle=['Demographic distribution for all school buildings in Michigan'])).transform_fold(
    race,
    as_=['Enrollment', 'Measurement']
).mark_bar(
    opacity=0.5,
    binSpacing=0
).encode(
    alt.X('Measurement:Q', title="Percentage Enrollment").bin(maxbins=20).axis(format='%'),
    alt.Y('count()', title='Percentage of Schools').stack("normalize"),
    alt.Color('Enrollment:N').scale(domain=race, range=colors)
)

# final visual 
visual1 = tpp_hist | mi_hist

st.altair_chart(visual1, use_container_width=False)

# analysis/comments



### visual number two ######################################################################################################################

st.write("\n")
st.write("_Placement School Enrollments_")
st.write("The following visualization answers the following questions: What are the student enrollments of the schools that TPP teacher candidates are placed at? How to TPP school partners compare to overall Michigan demographics?\n\n")


# filter results based on choices
teams2 = ['ELEM', 'ESL', 'SEC', 'SPED']
team_filter2 = st.multiselect("Team(s)", teams2, default = teams2)
filtered = by_building[np.where(by_building.TeamStr.str.contains('|'.join(team_filter2)),True,False)]

# custom colors
colors = ["#008208", "#7BBD00", "#0B9A6D"]

# change column names so it is prettier on the legend
filtered.rename(columns={'ECONOMIC_DISADVANTAGED_ENROLLMENT':'Economically Disadvantaged',
                            'SPECIAL_EDUCATION_ENROLLMENT':'Special Education',
                            'ENGLISH_LANGUAGE_LEARNERS_ENROLLMENT':'English Language Learners'}, inplace=True)

#list of columns to pull
cols_boxplot = ['Economically Disadvantaged', 'Special Education', 'English Language Learners']

tpp_box = alt.Chart(filtered, title=alt.Title("TPP School Building Enrollments", subtitle="2025-2026 Academic Year")).transform_fold(cols_boxplot, as_=["Measurement", "Percentage"]).mark_boxplot(size=50).encode(
    alt.X("Measurement:N", axis=alt.Axis(labels=False)),
    alt.Y("Percentage:Q", title="Percentage Enrollment"),
    color=alt.Color("Measurement:N").scale(domain=cols_boxplot, range=colors)
).properties(width=300)

# clean up demographics data set first
demo = demographics[demographics["BuildingName"] != "All Buildings"]
demo.rename(columns={'ECONOMIC_DISADVANTAGED_ENROLLMENT':'Economically Disadvantaged',
                            'SPECIAL_EDUCATION_ENROLLMENT':'Special Education',
                            'ENGLISH_LANGUAGE_LEARNERS_ENROLLMENT':'English Language Learners'}, inplace=True)

demo = demo[demo["Economically Disadvantaged"]<1]

#list of columns to pull
cols_mi = ['Economically Disadvantaged', 'Special Education', 'English Language Learners']

mi_box = alt.Chart(demo, title=alt.Title("Michigan School Building Enrollments", subtitle="2025-2026 Academic Year")).transform_fold(cols_mi, as_=["Measurement", "Percentage"]).mark_boxplot(size=50).encode(
    alt.X("Measurement:N", axis=alt.Axis(labels=False)),
    alt.Y("Percentage:Q", title="Percentage Enrollment"),
    color=alt.Color("Measurement:N")
).properties(width=300)

# final visual 
visual2 = tpp_box | mi_box

st.altair_chart(visual2, use_container_width=True)

# analysis/comments


### visual number three ######################################################################################################################

st.write("\n")
st.write("_Map of Placements_")
st.write("The following visualization answers the following questions: Where are students placed across Michigan? And at what quantity?\n\n")


min_lat = min(by_building["LAT"])
min_lon = min(by_building["LON"])
max_lat = max(by_building["LAT"])
max_lon = max(by_building["LON"])

strings = ['SPED', "ESL", 'ELEM', 'SEC'] # multi select 
team_filter3 = st.multiselect("Team(s) (map)", strings, default = strings)
map_filter = by_building[np.where(by_building.TeamStr.str.contains('|'.join(team_filter3)),True,False)]


map_filter.replace(["Intern, Pre-Intern", "Pre-Intern, Intern"], value="Both", inplace=True) # only three colors for each status
cols_rename ={'AMERICAN_INDIAN_ENROLLMENT':'American Indian',
                    'AFRICAN_AMERICAN_ENROLLMENT':'African American',
                    'HISPANIC_ENROLLMENT':'Hispanic',
                    'WHITE_ENROLLMENT':'White',
                    'HAWAIIAN_ENROLLMENT':'Hawaiian',
                    'ASIAN_ENROLLMENT':'Asian',
                    'TWO_OR_MORE_RACES_ENROLLMENT':'Two or More Races', 
                    "StatusStr":"Level(s)", 
                    "TeamStr":"Team(s)",
                    }

map_filter.rename(columns=cols_rename, inplace=True) # changing name for 

# custom colors
domain = ["Pre-Intern", "Intern", "Both"]
colors = ["#008208", "#7BBD00", "#0B9A6D"]

chart = alt.Chart(map_filter).mark_point().encode(
    x=alt.X('LON:Q', title='Longitude').scale(domain=[min_lon-0.2, max_lon+0.2]),
    y=alt.Y('LAT:Q', title='Latitude').scale(domain=[min_lat-0.2, max_lat+0.2]),
    size=alt.StrokeWidth('Placements:N', legend=None),
    color=alt.Color('Level(s):N').scale(domain=domain, range=colors),
    tooltip=["BuildingName:N", "STREET:N", "CITY:N", "Placements:N", "Team(s)", "Experience:N", 
                 'American Indian:N', 'African American:N', 'Asian:N', 'Hawaiian:N', 'Hispanic:N', 'White:N', 'Two or More Races:N']
).properties(
    width=600, height=350,
    title='Map of Placements'
).interactive()

st.altair_chart(chart, use_container_width=True)

# # filter by selection (team)
# strings = ['SPED', "ESL", 'ELEM', 'SEC'] # multi select 
# team_filter3 = st.multiselect("Team(s) (map)", strings, default = strings)
# map_filter = by_building[np.where(by_building.TeamStr.str.contains('|'.join(team_filter3)),True,False)]

# # rename and replace certain values for readability in the final map
# map_filter.replace(["Intern, Pre-Intern", "Pre-Intern, Intern"], value="Both", inplace=True) # only three colors for each status
# cols_rename ={'AMERICAN_INDIAN_ENROLLMENT':'American Indian',
#                     'AFRICAN_AMERICAN_ENROLLMENT':'African American',
#                     'HISPANIC_ENROLLMENT':'Hispanic',
#                     'WHITE_ENROLLMENT':'White',
#                     'HAWAIIAN_ENROLLMENT':'Hawaiian',
#                     'ASIAN_ENROLLMENT':'Asian',
#                     'TWO_OR_MORE_RACES_ENROLLMENT':'Two or More Races', 
#                     "StatusStr":"Level(s)", 
#                     "TeamStr":"Team(s)",
#                     }

# map_filter.rename(columns=cols_rename, inplace=True) # changing name of columns

# # find minimum and max of the coordinates
# min_lat = min(by_building["LAT"])
# min_lon = min(by_building["LON"])
# max_lat = max(by_building["LAT"])
# max_lon = max(by_building["LON"])

# # create the map background 

# ######
# # credit to: joelostblom from GitHub https://github.com/vega/altair/issues/679#issuecomment-3242491931
# # accessed 10/18/2026
# states = alt.topo_feature(data.us_10m.url, 'states')
# # Create bindings for pan/zoom
# zoom_bind = alt.binding_range(min=2000, max=50000, step=50, name='Zoom ')
# center_lat_bind = alt.binding_range(min=min_lat-1, max=max_lat+1, step=0.1, name='Center Lat ')
# center_lon_bind = alt.binding_range(min=min_lon-1, max=max_lon+1, step=0.1, name='Center Lon ')
# zoom_param = alt.param(value=3500, bind=zoom_bind)
# center_lat_param = alt.param(value=43, bind=center_lat_bind)
# center_lon_param = alt.param(value=-85, bind=center_lon_bind)
# # Base chart with dynamic projection

# base = alt.Chart(states).mark_geoshape(
#     fill='lightgray', stroke='white'
# ).project(
#     type='mercator',
#     scale=zoom_param,
#     center=alt.expr(f'[{center_lon_param.name}, {center_lat_param.name}]')
# ).add_params(zoom_param, center_lat_param, center_lon_param)
# #####



# # create the map of placements
# points = alt.Chart(map_filter, title=alt.Title("Map of Placements", subtitle="2025-2026 Academic Year")).mark_circle().encode(
#     longitude=alt.Longitude('LON', type='quantitative'),
#     latitude=alt.Latitude('LAT', type='quantitative'),
#     size=alt.StrokeWidth('Placements:N', legend=None),
#     color=alt.Color('Level(s):N'),
#     tooltip=["BuildingName:N", "STREET:N", "CITY:N", "Placements:N", "Team(s)", "Experience:N", 
#              'American Indian:N', 'African American:N', 'Asian:N', 'Hawaiian:N', 'Hispanic:N', 'White:N', 'Two or More Races:N']
# ).project(
#     type='mercator',
#     scale=zoom_param,
#     center=alt.expr(f'[{center_lon_param.name}, {center_lat_param.name}]')
# )

# visual3 = base + points

# st.altair_chart(visual3, use_container_width=True)
# st.write(visual3)
