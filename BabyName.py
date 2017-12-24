import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
#from wordcloud import WordCloud
df=pd.read_csv('NationalNames.csv')
print(df.head())

glob_freq = (df.groupby('Name')
             .agg({'Count': 'sum'})  
             .sort_values('Count', ascending=False))

glob_freq[['Count']].head(10).plot(kind='bar')
plt.title('Top Ten Names')
#Names Having Less No. Of Counts
fg=glob_freq.query('Count <= 10').sample(10, random_state=2)
print(fg)
fg[['Count']].head(10).plot(kind='bar')
plt.title('Unique Ten Names')

#Common Names Between Male And Female
tmp = df.groupby(['Gender', 'Name']).agg({'Count': 'sum'}).reset_index()
male = (tmp.query("Gender == 'M'")
        .set_index("Name")
        .rename(columns={'Count': 'Male'}))
female = (tmp.query("Gender == 'F'")
          .set_index("Name")
          .rename(columns={'Count': 'Female'}))
join = male[['Male']].join(female[['Female']], how='inner')
join['Frequency'] = join['Male'] + join['Female']
join['FemalePct'] = join['Female'] / join['Frequency'] * 100.0
join['MalePct'] = join['Male'] / join['Frequency'] * 100.0
print(join[['Frequency', 'FemalePct', 'MalePct']]
 .query('(FemalePct > 10) & (MalePct) > 10')
 .sort_values('Frequency', ascending=False)
 .head(10))


con = sqlite3.connect('database.sqlite')

popular_female_dacade = pd.read_sql_query("""
WITH name_dacade AS (
SELECT 
CASE WHEN year like '188%' THEN '1880-1889'
     WHEN year like '189%' THEN '1890-1899'
     WHEN year like '190%' THEN '1900-1909'
     WHEN year like '191%' THEN '1910-1919'
     WHEN year like '192%' THEN '1920-1929'
     WHEN year like '193%' THEN '1930-1939'
     WHEN year like '194%' THEN '1940-1949'
     WHEN year like '195%' THEN '1950-1959'
     WHEN year like '196%' THEN '1960-1969'
     WHEN year like '197%' THEN '1970-1979'
     WHEN year like '198%' THEN '1980-1989'
     WHEN year like '199%' THEN '1990-1999'
     WHEN year like '200%' THEN '2000-2009'
     WHEN year like '201%' THEN '2010-2019'
END AS dacade,
Name, SUM(Count) AS Total_Count
FROM NationalNames
WHERE Gender = 'F'
GROUP BY dacade, Name)
SELECT dacade, Name, MAX(Total_Count) AS Total_Count
FROM name_dacade
GROUP BY dacade""", con)
popular_female_dacade

print(popular_female_dacade)

popular_male_dacade=pd.read_sql_query("""
WITH name_dacade AS (
SELECT 
CASE WHEN year like '188%' THEN '1880-1889'
     WHEN year like '189%' THEN '1890-1899'
     WHEN year like '190%' THEN '1900-1909'
     WHEN year like '191%' THEN '1910-1919'
     WHEN year like '192%' THEN '1920-1929'
     WHEN year like '193%' THEN '1930-1939'
     WHEN year like '194%' THEN '1940-1949'
     WHEN year like '195%' THEN '1950-1959'
     WHEN year like '196%' THEN '1960-1969'
     WHEN year like '197%' THEN '1970-1979'
     WHEN year like '198%' THEN '1980-1989'
     WHEN year like '199%' THEN '1990-1999'
     WHEN year like '200%' THEN '2000-2009'
     WHEN year like '201%' THEN '2010-2019'
END AS dacade,
Name, SUM(Count) AS Total_Count
FROM NationalNames
WHERE Gender = 'M'
GROUP BY dacade, Name)
SELECT dacade, Name, MAX(Total_Count) AS Total_Count
FROM name_dacade
GROUP BY dacade""", con)
popular_male_dacade
#print(popular_male_dacade)

plt.plot(popular_female_dacade['dacade'],popular_female_dacade['Total_Count'] , label='Average length of female names', color='r')
plt.plot(popular_male_dacade['dacade'],popular_male_dacade['Total_Count'], label='Average length of male names', color='b')
plt.title('Population Change For Male And Female')

Female=df[df['Gender']=='F']
Male=df[df['Gender']=='M']
glob_freq1 = Female.groupby('Name').agg({'Count': 'sum'}).sort_values('Count', ascending=False)
glob_freq1[['Count']].head().plot(kind='bar')
plt.title('Top Ten Female Names')
glob_freq1 = Male.groupby('Name').agg({'Count': 'sum'}).sort_values('Count', ascending=False)
glob_freq1[['Count']].head().plot(kind='bar')
plt.title('Top Ten Male Names')



population = df[['Year', 'Count']].groupby('Year').sum()
population.plot()
plt.title('Population Rate')
#Top 4 Name Count Plot
df.query('Name=="James"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name James')
a =1930
b= 1970
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

df.query('Name=="John"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name John')
a =1942
b= 1970
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

df.query('Name=="Robbert"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name Robbert')
a =1955
b= 1970
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

df.query('Name=="Michael"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name Michael')
a =1950
b= 1978
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

#Top 4 Female Name
df.query('Name=="Mary"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name Mary')
a =1910
b= 1970
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

df.query('Name=="Patricia"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name Patricia')
a =1935
b= 1960
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

df.query('Name=="Jennifer"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name Jennifer')
a =1965
b= 1990
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)

df.query('Name=="Linda"')[['Year', 'Count']].groupby('Year').sum().plot()
plt.title('Count Plot Of Name Linda')
a =1945
b= 1958
plt.axvspan(a, b, color='y', alpha=0.5, lw=0)
   
'''
e= str()
x= [((str(df.Country[i])+' ')*10) if i<10 else ((str(df.Country[i])+' ')*5) if i<30 else ((str(df.Country[i])+' ')*3) if i<50 else (str(df.Country[i])+' ') for i in range(len(df))]
for i in x:
    e+= i
#print(np.array(e))
e= str(e)
def word_count(string):
    my_string = string.lower().split()
    my_dict = {}
    for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1
    return my_dict
dicti= word_count(e)
#print(dicti)
plt.figure(figsize= (10, 10))
word_cloud = WordCloud().generate_from_frequencies(dicti)
plt.imshow(word_cloud)
plt.axis("off")
plt.show()
'''