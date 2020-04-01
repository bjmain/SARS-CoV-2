
import pandas as pd
import sys
import matplotlib.pyplot as P
from matplotlib.dates import DateFormatter
import input_urls 

US_deaths = pd.read_csv(input_urls.us_death_url)
CA_deaths = US_deaths.loc[US_deaths['Province_State']=="California"]

# pop sizes
cook_pop = 5238216
LA_pop = 10118759
yolo_pop = 218376
mont_pop = 1048244
charles_pop = 401738
cc_pop = 1144863
solano_pop = 443877
denver_pop = 705439
suffolk_pop = 1483571
spain_pop = 46750000

def make_COUNTRY_DF(global_death_DF, country_name, pop_size,NAME,offset):
    country_df = global_death_DF.loc[global_death_DF['Country/Region']==country_name]
    country_df.drop(['Province/State','Lat','Long'],axis='columns',inplace=True)
    country_df = country_df.T.reset_index()
    country_df.columns = ['date',country_name]
    country_df.drop(country_df.index[0],inplace=True)
    country_df = country_df.reset_index(drop=True)
    country_df['date']=pd.to_datetime(country_df['date'])
    country_df['date'] = country_df['date'] + pd.DateOffset(days=offset)
    country_df[country_name] = country_df[country_name].div(pop_size) * 1000000
    country_df = country_df.set_index('date')
    country_df.columns = [NAME]
    return(country_df)

global_deaths = pd.read_csv(input_urls.global_death_url)
CA_deaths.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2','Country_Region', 'Lat', 'Long_', 'Combined_Key'],axis='columns',inplace=True)
CA_deaths = CA_deaths.groupby('Province_State').sum()
CA_deaths = CA_deaths.T


def make_county_DF(US_death_DF, state, county_name, pop_size):
    COUNTY = US_death_DF.loc[(US_death_DF['Province_State']==state) & (US_death_DF['Admin2']==county_name)]
    COUNTY.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2','Country_Region', 'Lat', 'Long_', 'Combined_Key'],axis='columns',inplace=True)
    COUNTY = COUNTY.T.reset_index()
    COUNTY.columns = ['date',county_name]
    COUNTY.drop(COUNTY.index[0],inplace=True)
    COUNTY = COUNTY.reset_index(drop=True)
    COUNTY['date']=pd.to_datetime(COUNTY['date'])
    COUNTY[county_name] = COUNTY[county_name].div(pop_size) * 1000000
    COUNTY = COUNTY.set_index('date')
    return(COUNTY)


CC_deaths = make_county_DF(US_deaths,"California", "Contra Costa",cc_pop)
solano_deaths = make_county_DF(US_deaths,"California", "Solano",solano_pop)
yolo_deaths = make_county_DF(US_deaths,"California","Yolo",yolo_pop)
LA_deaths = make_county_DF(US_deaths,"California", "Los Angeles",LA_pop)
Mont_deaths = make_county_DF(US_deaths,"Maryland", "Montgomery",mont_pop)
SC_deaths = make_county_DF(US_deaths,"South Carolina", "Charleston",charles_pop)
Chi_deaths = make_county_DF(US_deaths,"Illinois", "Cook",cook_pop)
denver_deaths = make_county_DF(US_deaths,"Colorado", "Denver",denver_pop)
suffolk_deaths = make_county_DF(US_deaths,"New York", "Suffolk",suffolk_pop)
espania_deaths = make_COUNTRY_DF(global_deaths, "Spain", spain_pop, "Spain + 8 days",8)
espania_deaths14 = make_COUNTRY_DF(global_deaths, "Spain", spain_pop, "Spain + 14 days",14)

################## make figure ###############
fig = P.figure() # create a figure object
ax = fig.add_subplot(1, 1, 1)  # create an axes object in the figure

line_w = 3
CC_deaths.plot(kind='line',ax=ax,lw=line_w)
denver_deaths.plot(kind='line',ax=ax,lw=line_w)
solano_deaths.plot(kind='line',ax=ax,lw=line_w)
SC_deaths.plot(kind='line',ax=ax,lw=line_w)
Chi_deaths.plot(kind='line',ax=ax,lw=line_w)
Mont_deaths.plot(kind='line',ax=ax,lw=line_w)

yolo_deaths.plot(kind='line',ax=ax,lw=line_w,ls="-.")
LA_deaths.plot(kind='line',ax=ax,lw=line_w)
suffolk_deaths.plot(kind='line',ax=ax,lw=line_w)
espania_deaths.plot(kind='line',ax=ax,lw=1,ls='--',color='k',alpha=0.5)
espania_deaths14.plot(kind='line',ax=ax,lw=1,ls='--',color='r',alpha=0.5)

ax.set_title("COVID-19 trends",fontsize=14)
ax.set_ylabel("Deaths/million people",fontsize=14)

P.xlim('3/05/20','4/10/20')
P.ylim(0,50)

# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)
P.legend(prop={'size': 12})
P.savefig(input_urls.outfile)
#P.show()

##############################################