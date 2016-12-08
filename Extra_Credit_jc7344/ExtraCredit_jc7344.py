
# coding: utf-8

# # Extra credit asisgnment jc7344
# 
# ## LinkNYC, poverty and internet access disparity. 
# 
# ### Research question:
# 
# **Are New Yorkers living in poverty, significantly more likely to be isolated from LinkNYC kiosk network, in comparison to New Yorkers living in low poverty?**
# 
# For this analysis, I formed the following hypotheses:
# 
# *Null Hypothesis:*
# The mean distance to LinkNYC kiosks for New Yorkers living in poverty is the same or less than the mean distance to LinkNYC kiosks for New Yorkers in low poverty, significance level = 0.05.
# 
# *Alternative Hypothesis:*
# The mean distance to LinkNYC kiosks for New Yorkers living in poverty is larger than the mean distance to LinkNYC kiosks for New Yorkers in low poverty, significance level = 0.05
# 

# In[27]:

get_ipython().magic('matplotlib inline')
from __future__  import print_function, division
import numpy as np
from math import *
import pandas as pd
from pandas import DataFrame
from pandas.tools.plotting import scatter_matrix
from geopandas import GeoDataFrame
#import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gp
import zipfile
import glob
import os


# In[28]:

os.getenv('PUIDATA')


# ## Downloading Census tract spatial data (cut to shoreline) from bytes of the big apple. 

# In[29]:

os.system("curl -O http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyct2000_16d.zip")
os.system("mv nyct2000_16d.zip" + os.getenv("PUIDATA"))


# In[30]:

os.system("unzip " + os.getenv('PUIDATA') + '/' + "nyct2000_16d")


# In[31]:

os.path.isfile(os.getenv("PUIDATA") + "/nyct2000_16d/nyct2000_16d/nyct2000.shp")


# In[32]:

tracts = gp.read_file(os.getenv("PUIDATA")+ "/" + '/nyct2000_16d/nyct2000_16d/nyct2000.shp')


# In[33]:

ctnyc_path="/home/cusp/jc7344/PUIdata/nyct2000_16d/nyct2000_16d/nyct2000.shp"
#/home/cusp/jc7344/PUIdata/nyct2000_16d/nyct2000_16d/nyct2000.shp
ct_shape = GeoDataFrame.from_file(ctnyc_path)


# ## Mapping Census tracts 

# In[34]:

f, ax = plt.subplots(figsize=(10,10))
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ct_shape.plot(column='BoroCode',alpha=1,linewidth=0.5,ax=ax)
plt.title("New York City by census tracts")
grey_patch = mpatches.Patch(color='grey', label='Staten Island')
green_patch = mpatches.Patch(color='green', label='Bronx')
red_patch = mpatches.Patch(color='red', label='Manhattan')
orange_patch = mpatches.Patch(color='orange', label='Brooklyn')
brown_patch = mpatches.Patch(color='brown', label='Queens')

plt.legend(handles=[red_patch, orange_patch, green_patch, brown_patch, grey_patch], loc = 'best')


# The map above displays The City of New York. Each of the five boroughs were assigned a different color to clearly identify the census tract boundaries.

# ## Downloading LinkNYC location Map from NYC Open data

# In[35]:

### Here I am using code provided by Professor Bianco.

def get_LinkNYC_csv(filename):
    '''
    Function that get the data file from the NYC Open Data websites and saves it in the PUIdata directory.
    If the file is already there, the function prints a message saying that. 
    '''
    
    print('Getting the data from NYC Open Data website')
    
    ### First check if the csv file is not already at the directory
    if os.path.isfile(os.getenv("PUIDATA") + "/" + filename):
        print ("File was already at the PUIdata directory.")
         
    else :
        # Download the File; move it to the PUIdata directory.
        print ("Downloading")
        
        # Downloading the File
        os.system("curl -O https://data.cityofnewyork.us/resource/" + filename)
        print ("File downloaded.")
        
        # Moving it to the PUIdata directory
        os.system("mv " + filename + " " + os.getenv("PUIDATA"))
        
                  
    ### One final check:
    if not os.path.isfile(os.getenv("PUIDATA") + "/" + filename):
        print ("WARNING!!! something is wrong: the file is not there!")

    else:
        print ("File in place, you can continue.")


# In[36]:

get_LinkNYC_csv('tgrn-h24f.csv')


# In[37]:

link = pd.read_csv(os.getenv("PUIDATA")+ "/" + 'tgrn-h24f.csv')


# In[38]:

link.head()


# In[39]:

cd = link['Community Board'].values
cd


# In[43]:

len(cd)


# In[44]:

link.isnull().sum()


# In[45]:

kioskid = link['CB Link ID'].values
kioskid


# In[46]:

kioskid2 = []
for elem in kioskid:
    kioskid2.append(int(elem[6:]))


# In[47]:

print(type(kioskid2[0]))


# In[48]:

link['CB Link ID'] = kioskid2
kioskid2


# In[49]:

link_hist = link['Community Board'].hist(bins = 30)
plt.axis([101, 415, 0, 500])
link_hist.set_title("Histogram 1: LinkNYC distribution by Community board")
link_hist.set_xlabel("Community Board number")
link_hist.set_ylabel("LinkNYC installed")
#plt.text(1910, -30000, 'Age distribution of Citi Bike users excluding those who were born before 1910.', fontsize = 12)


# The figure above displays 454 LinkNYC kiosks installed within the boundaries of 21 community board throughout New York City. As it was possible to see when exploring the data, there were 12 community boards with numbers from 101 to 112 correspond to Manhattan (410 installed kiosks); 5 community board with numbers from 204 to 208 were in the Bronx (with 23 installed kiosks); Brooklyn, on the other hand, was represented by community board 303 (with two LinkNYC kiosks installed in Bedford Stuyvesant), and 3 community boards with numbers from 406 to 412 in Queens. 
# 

# ## Downloading Internet Use and and Demographic data from the class website
# 
# The dataset contains household internet access information by community board. For the purpose of my project, internet access will depend exclusively on the presence Households: With A Internet Subscription. My objective here is to identify a correlation between internet subscriptions and median household income. This will allow me to share more details of the existing connectivity conditions.

# In[50]:

get_ipython().system('curl -O "http://cosmo.nyu.edu/~fb55/PUI2016/data/ACS_Computer_Use_and_Internet_2014_1Year_Estimate.csv"')


# In[51]:

os.system("mv ACS_Computer_Use_and_Internet_2014_1Year_Estimate.csv" + os.getenv("PUIDATA"))


# In[52]:

internet = pd.read_csv(os.getenv("PUIDATA")+ "/" + 'ACS_Computer_Use_and_Internet_2014_1Year_Estimate.csv')


# In[53]:

internet.head()


# In[54]:

print(len(internet))


# In[55]:

internet.isnull().sum()


# In[56]:

internet.columns


# In[76]:

internet = internet.replace(['NYC-Bronx Community District 8--Riverdale, New York',
       'NYC-Bronx Community District 12--Wakefield, New York',
       'NYC-Bronx Community District 10--Co-op City, New York',
       'NYC-Bronx Community District 11--Pelham Parkway, New York',
       'NYC-Bronx Community District 3 & 6--Belmont, New York',
       'NYC-Bronx Community District 7--Bedford Park, New York',
       'NYC-Bronx Community District 5--Morris Heights, New York',
       'NYC-Bronx Community District 4--Concourse, New York',
       'NYC-Bronx Community District 9--Castle Hill, New York',
       'NYC-Bronx Community District 1 & 2--Hunts Point, New York',
       'NYC-Manhattan Community District 12--Washington Heights, New York',
       'NYC-Manhattan Community District 9--Hamilton Heights, New York',
       'NYC-Manhattan Community District 10--Central Harlem PUMA, New York',
       'NYC-Manhattan Community District 11--East Harlem PUMA, New York',
       'NYC-Manhattan Community District 8--Upper East Side PUMA, New York',
       'NYC-Manhattan Community District 7--Upper West Side & West Side PUMA, New York',
       'NYC-Manhattan Community District 4 & 5--Chelsea, New York',
       'NYC-Manhattan Community District 6--Murray Hill, New York',
       'NYC-Manhattan Community District 3--Chinatown & Lower East Side PUMA, New York',
       'NYC-Manhattan Community District 1 & 2--Battery Park City, New York',
       'NYC-Staten Island Community District 3--Tottenville, New York',
       'NYC-Staten Island Community District 2--New Springville & South Beach PUMA, New York',
       'NYC-Staten Island Community District 1--Port Richmond, New York',
       'NYC-Brooklyn Community District 1--Greenpoint & Williamsburg PUMA, New York',
       'NYC-Brooklyn Community District 4--Bushwick PUMA, New York',
       'NYC-Brooklyn Community District 3--Bedford-Stuyvesant PUMA, New York',
       'NYC-Brooklyn Community District 2--Brooklyn Heights & Fort Greene PUMA, New York',
       'NYC-Brooklyn Community District 6--Park Slope, New York',
       'NYC-Brooklyn Community District 8--Crown Heights North & Prospect Heights PUMA, New York',
       'NYC-Brooklyn Community District 16--Brownsville & Ocean Hill PUMA, New York',
       'NYC-Brooklyn Community District 5--East New York & Starrett City PUMA, New York',
       'NYC-Brooklyn Community District 18--Canarsie & Flatlands PUMA, New York',
       'NYC-Brooklyn Community District 17--East Flatbush, New York',
       'NYC-Brooklyn Community District 9--Crown Heights South, New York',
       'NYC-Brooklyn Community District 7--Sunset Park & Windsor Terrace PUMA, New York',
       'NYC-Brooklyn Community District 10--Bay Ridge & Dyker Heights PUMA, New York',
       'NYC-Brooklyn Community District 12--Borough Park, New York',
       'NYC-Brooklyn Community District 14--Flatbush & Midwood PUMA, New York',
       'NYC-Brooklyn Community District 15--Sheepshead Bay, New York',
       'NYC-Brooklyn Community District 11--Bensonhurst & Bath Beach PUMA, New York',
       'NYC-Brooklyn Community District 13--Brighton Beach & Coney Island PUMA, New York',
       'NYC-Queens Community District 1--Astoria & Long Island City PUMA, New York',
       'NYC-Queens Community District 3--Jackson Heights & North Corona PUMA, New York',
       'NYC-Queens Community District 7--Flushing, New York',
       'NYC-Queens Community District 11--Bayside, New York',
       'NYC-Queens Community District 13--Queens Village, New York',
       'NYC-Queens Community District 8--Briarwood, New York',
       'NYC-Queens Community District 4--Elmhurst & South Corona PUMA, New York',
       'NYC-Queens Community District 6--Forest Hills & Rego Park PUMA, New York',
       'NYC-Queens Community District 2--Sunnyside & Woodside PUMA, New York',
       'NYC-Queens Community District 5--Ridgewood, New York',
       'NYC-Queens Community District 9--Richmond Hill & Woodhaven PUMA, New York',
       'NYC-Queens Community District 12--Jamaica, New York',
       'NYC-Queens Community District 10--Howard Beach & Ozone Park PUMA, New York',
       'NYC-Queens Community District 14--Far Rockaway, New York'], ['BX08', 'BX12', 'BX10', 'BX11', 'BX06', 'BX07', 'BX05', 'BX04', 'BX09', 'BX02',
'MN12', 'MN09', 'MN10', 'MN11', 'MN08', 'MN07', 'MN04', 'MN06', 'MN03', 'MN01',
'SI03', 'SI02', 'SI01', 'BK01', 'BK04', 'BK03', 'BK02', 'BK06', 'BK08', 'BK16', 'BK05', 'BK18',
'BK17', 'BK09', 'BK07', 'BK10', 'BK12', 'BK14', 'BK15', 'BK11', 'BK13', 'QN01', 'QN03', 'QN07',
'QN11', 'QN13', 'QN08', 'QN04', 'QN06', 'QN02', 'QN05', 'QN09', 'QN12', 'QN10', 'QN14'])


# In[77]:

internet = internet.rename(columns={'Qualifying Name': 'Community district'})


# In[78]:

internet.head()


# In[79]:

internet['Community district'].drop_duplicates().as_matrix()
print(len(internet['Community district'].drop_duplicates().as_matrix()))


# In[80]:

house_int = internet.iloc[:,[2,4]]


# In[81]:

house_int.columns


# In[82]:

house_int['Households: With An Internet Subscription'] = house_int.sum(axis=1)


# In[83]:

house_int.head()


# In[84]:

final_demo = pd.read_csv("http://cosmo.nyu.edu/~fb55/PUI2016/data/Final_Demographics.csv")


# In[85]:

final_demo.head()


# In[86]:

final_demo.columns


# In[87]:

cd_id = final_demo['cd_id'].drop_duplicates().as_matrix()


# In[88]:

cd_id


# In[89]:

final_demo = final_demo.replace(['MN11111'], ['MN11'])


# In[90]:

print(len(cd_id))


# In[91]:

final_demo = final_demo.iloc[:,[1, 139]]
final_demo = final_demo.rename(columns={'Median household income (In 2014 Inflation Adjusted Dollars)': 'Median Household Income', 'cd_id': 'Community district'})
final_demo.head()


# In[92]:

access = pd.merge(final_demo, house_int, on='Community district')


# In[93]:

access.head()


# In[94]:

ax = access.plot(x='Community district', y='Households: With An Internet Subscription', kind='bar', figsize=(15, 8), legend=False, fontsize=14, color='DarkOrange')
ax.set_title('Figure 1: Distribution of households with an internet connection by Community District')
ax.set_ylabel('Number of Households', fontsize=14)
ax.set_xlabel('Zip Code', fontsize=14)

ax1 = access.plot(x='Community district', y='Median Household Income', kind='bar', figsize=(15, 8), legend=False, fontsize=14, color='DarkGreen')
ax1.set_title('Figure 2: Distribution household median income by Community District')
ax1.set_ylabel('US Dollars', fontsize=14)
ax1.set_xlabel('Zip Code', fontsize=14)


# The figures above display both the number of households with an internet subscription and their median income. There seems to be a relationship between higher (median) income and the household’s capacity to connect to the internet. Additionally, a relationship between the amount of internet subscriptions and the number of installed linkNYC kiosks (‘Links”) is not evident on the community district level. Manhattan is the borough with the most amount of internet subscriptions per household (specifically, the community districts 08, 07, 01). Ironically, these community districts have 120 LinkNYC kiosks which represents 26% of the total installed “links” in the city. 
# 
# Conversely, digitally isolated (in terms of LinkNYC presence) boroughs like the Bronx and Brooklyn display the least number of households with internet connections. Although the apparent positive relationship between median income and internet access, can be seen on both sides of the spectrum, it is possible to say that the disposition of LinkNYC kiosks seems to be more connected to the presence of households with higher income than to the situation of lower income and unconnected segments of the population. 
# 
# 

# ## Processing of poverty data and mapping on ArcGIS 
# 
# In order to answer my research question I have to merge tabular and spatial data. For my project, I am using poverty by census tract data provided by Census bureau for the year 2014 and census tract clipped to shoreline shapefile downloaded from the agency’s cartographic boundary archives. 
# 
# 

# In[95]:

os.getenv('PUIDATA')


# In[96]:

poverty = pd.read_csv(os.getenv("PUIDATA")+ "/" + 'ACS_14_5YR_S1701_with_a.csv')


# In[97]:

poverty.head()


# In[98]:

poverty = poverty.rename(columns={'GEO.id2': 'GEOID'})
poverty.head()


# In[99]:

poverty = poverty.rename(columns={'Total; Estimate; Population for whom poverty status is determined': 'Total_Pop'})
poverty.head()


# In[100]:

poverty = poverty.rename(columns={'Below poverty level; Estimate; Population for whom poverty status is determined': 'Total_Pov'})
poverty.head()


# In[101]:

os.getenv('PUIDATA')


# In[102]:

os.path.isfile(os.getenv("PUIDATA") + "/shapez/cb_2015_36_tract_500k.shp")


# In[103]:

shape = gp.read_file(os.getenv("PUIDATA")+ "/" + '/shapez/cb_2015_36_tract_500k.shp')


# In[104]:

shape.columns


# In[105]:

shape.head()


# In[106]:

scatter_matrix (shape, s=300, figsize=(16, 16),)


# In order to merge poverty data by census tract to the shapefile, it is crucial to make sure all of the values can be converted into float

# In[107]:

len(shape)


# In[108]:

def canconvert(mydata):
    try:
        float(mydata)
        return True
    except ValueError:
        return False

indx = (np.vectorize(canconvert)(shape['ALAND']))
print("True entries %d"%sum(indx))
shape['ALAND'][~indx] = float('NaN')

indx2 = (np.vectorize(canconvert)(shape['AWATER']))
print("True entries %d"%sum(indx))
shape['AWATER'][~indx2] = float('NaN')

indx3 = (np.vectorize(canconvert)(shape['GEOID']))
print("True entries %d"%sum(indx))
shape['GEOID'][~indx3] = float('NaN')


# In[109]:

try:
    shape['ALAND'].astype(float)
except ValueError:
    print("conversion failed")


# In[110]:

shape['GEOID'] =             pd.to_numeric(shape['GEOID'], 
                          errors='coerce').astype(float)


# In[111]:

shape['GEOID']


# In[112]:

proxim = pd.merge(poverty, shape, on='GEOID')


# In[113]:

proxim


# ## Mapping on ArcGIS
# 
# After processing and merging both tabular and spatial data, I used ArcGIS to map the current locations of installed LinkNYC kiosks.  Additionally, I created a 1/2mile buffer (which I defined as “walking distance”) around kiosks and analyze the percentage of the population in poverty living in a walking distance from the nearest kiosk. Lastly, I generated centroids on the current location of LinkNYC kiosk to identify the average distance (in US feet) to residential units located in low and high poverty census tracts.
# 
# 1) Currently installed LinkNYC kiosks.
# 
# 2) 1/2 mile buffer around installed LinkNYC kiosks (percentage of population below poverty living in walking distance from their nearest LinkNYC kiosk.
# 
# 3) Spatial analysis (average distance)
# 

# In[114]:

from IPython.core.display import Image, display
display(Image(os.getenv("PUIDATA") + '/pui map.png'), width=900, unconfined=True)


# The map above illustrates the currently installed LinkNYC kiosk throughout New York City. Out of the originally planned installation scheme (replacing 7,000 phone booths with ‘Links”), the public/private partnership has placed a total of 456 kiosks. The self-funded project has presence in four boroughs and Manhattan hosts 90% of the installed links. 
# 
# After mapping the information, a preliminary analysis suggested that out of the total population below poverty, only 27% New Yorkers live within walking distance of a LinkNYC kiosk. 
# 
# <table>
#   <thead>
#     <tr>
#         <th>Total population below poverty</th>
#       <th>Percentage</th>
#     <tr>
#       <td>1,696,394</td>
#       <td>100%</td>
#     </tr>
#       <th>Population below poverty living within 1/2 mile to a LinkNYC kiosk</th>
#       <th>Percentage</th>
#   </thead>
#   <tbody>
#     <tr>
#       <td>460,683</td>
#       <td>27%</td>
#     </tr>
#   </tbody>
# </table>
# 
# In terms of the total population of New York City, it could be said that only 6% of residents live within walking distance from a LinkNYC  kiosk.
# 
# 
# <table>
#   <thead>
#     <tr>
#         <th>Total population of NYC</th>
#       <th>Percentage</th>
#     <tr>
#       <td>8,219,906</td>
#       <td>100%</td>
#     </tr>
#       <th>Population below poverty living within 1/2 mile to a LinkNYC kiosk</th>
#       <th>Percentage</th>
#   </thead>
#   <tbody>
#     <tr>
#       <td>460,683</td>
#       <td>6%</td>
#     </tr>
#   </tbody>
# </table>
# 
# 

# ## Spatial Analysis-Average (linear) distance
# 
# For this portion of the project, the average linear distance between households and LinkNYC kiosks was calculated by identifying residential units for each borough. Having the results of previous analysis in hand, it was possible to establish a relationship between the census tracts with lower median income, high poverty and low connectivity (measured by calculating the number of internet subscriptions) and the hosting boroughs. In order to calculate the average distance within the boundaries of each MapPLUTO, the residential units were seen as centroids and a proximity analysis tool (geoprocessing tools) was utilized to identify the linear distance between selected residential units and LinkNYC kiosks. 
# 
# For the purpose of this project, Manhattan contains most of the community districts whose households have higher median income, whose population by census tract has lower poverty levels and has most the internet subscriptions. Additionally, Manhattan is also the borough with the most installed LinkNYC kiosks and with the largest share of population within a walking distance from them. Conversely, Brooklyn has the least number of installed kiosks, its community districts contain households with lower median income and the least number of internet subscriptions. 
# 
# Lastly, and as a final assumption, it is necessary to state that all distances will be calculated  according to the Euclidean metric (straight line) and measured in miles. 
# 
# Below, the proximity analysis for all the boroughs with LinkNYC presence will be displayed:

# In[115]:

display(Image(os.getenv("PUIDATA") + '/PuiMap2.png'), width=900, unconfined=True)
display(Image(os.getenv("PUIDATA") + '/PuiMap3.png'), width=900, unconfined=True)
display(Image(os.getenv("PUIDATA") + '/PuiMap4.png'), width=900, unconfined=True)
display(Image(os.getenv("PUIDATA") + '/PuiMap5.png'), width=900, unconfined=True)


# 
# As result of my calculations, Manhattan is the borough with the shortest average distance between its residential units and LinkNYC kiosks with 0.25 miles (0.25 miles shorter than the walking distance). Brooklyn’ residential units are the most distant to the closest LinkNYC kiosk with 3.7 miles. 
# 
# <table>
#   <thead>
#     <tr>
#         <th>Borough</th>
#       <th>Average distance to LinkNYC kiosk</th>
#     <tr>
#       <td>Manhattan</td>
#       <td>13.26 ft/0.25 miles</td>
#     </tr>
#     <th>Borough</th>
#       <th>Average distance to LinkNYC kiosk in miles</th>
#     <tr>
#       <td>Bronx</td>
#       <td>12,672 ft/2.4 miles</td>
#     </tr>
#       <th>Borough</th>
#       <th>Average distance to LinkNYC kiosk in miles</th>
#     <tr>
#       <td>Brooklyn</td>
#       <td>19,524 ft/3.7 miles</td>
#     </tr>
#       <th>Borough</th>
#       <th>Average distance to LinkNYC kiosk in miles</th>
#   </thead>
#   <tbody>
#     <tr>
#       <td>Queens</td>
#       <td>16,368 ft/3.1 miles</td>
#     </tr> 
#   </tbody>
# </table>

# ## Hypothesis testing:
# 
# As deliverables for my project, I submit a statistical result which was produced after performing a Z-test. Additionally, I include various plots, tables and graphs supporting the result of my analysis and the possible rejection of the Null Hypothesis. Lastly, I will deliver a map displaying both a spatial diagnosis of existing conditions and the future locations of LinkNYC kiosks. My intention is to translate technical language into succinct information in order to facilitate decision-making and promote participatory planning in the City.
# 

# In[116]:

# low_pov corresponds to the average distance between residential units and LinkNYC kiosks within low poverty census tracts.
low_pov = pd.read_csv(os.getenv("PUIDATA")+ "/" + 'Table.csv')


# In[117]:

low_pov.head()


# In[118]:

low_pov.drop(['OBJECTID', 'Borough', 'Block',
       'Lot', 'CD',
       'CT2010', 'CB2010', 'SchoolDist',
       'Council', 'ZipCode'], axis = 1, inplace = True)


# In[119]:

low_pov.head()


# In[120]:

mean_low = low_pov.mean()


# In[121]:

mean_low


# In[122]:

stdlow = low_pov.std()


# In[123]:

low_pov.std()


# In[124]:

# high_pov corresponds to the average distance between residential units and LinkNYC kiosks within high poverty census tracts.
high_pov = pd.read_csv(os.getenv("PUIDATA")+ "/" + 'Table_2.csv')


# In[125]:

high_pov.head()


# In[126]:

high_pov.drop(['OBJECTID', 'Borough', 'Block',
       'Lot', 'CD',
       'CT2010', 'CB2010', 'SchoolDist',
       'Council', 'ZipCode'], axis = 1, inplace = True)


# In[127]:

high_pov.head()


# In[128]:

mean_high = high_pov.mean()


# In[129]:

mean_high


# In[130]:

high_pov.std()


# In[131]:

z_test = ((mean_high) - low_pov.mean())/(high_pov.std()/sqrt(len(high_pov)))


# In[132]:

z_test


# From our Z-test, we obtained a Z-statistic of 919. From the Z-Table, this gave an area  0.9998. Thus, our p-value is (1 - 0.9998), or 0.0002, meaning there is a 0.02% probability that the difference observed between the two groups is due to chance alone. Specifically, this p-value is much smaller than our alpha level of 0.05, meaning we can reject our null hypothesis, and can conclude that the **mean distance to LinkNYC kiosks for New Yorkers living in poverty is larger than the mean distance to LinkNYC kiosks for New Yorkers in low poverty, significance level = 0.05**
