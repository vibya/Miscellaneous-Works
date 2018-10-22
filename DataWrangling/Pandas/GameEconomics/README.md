
# Heroes Of Pymoli Data Analysis
- A significant majority of the players are Male(81%).
- Female players, on average, spend as much as Male players on in-game purchases
- A major chunk of players fall between the age group of 15-30 with a significant portion of them between the ages 20-24, implying young adults are more inclined to spend more on in-game purchases
- Since this data is only purchase data and not actual active player data, the above assumptions might be skewed towards the "purchasing" crowd than the non-purchasing crowd who might be enjoying the game without spending on in-game purchases


```python
import pandas as pd
```


```python
purchasefile = "purchase_data.json"
purchase_df = pd.read_json(purchasefile)
```

# Player Count


```python
unique_users = purchase_df["SN"].value_counts()
totalplayers = pd.DataFrame({"Total Players": unique_users.count()},index = [0])
totalplayers
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>




```python
unique_items = purchase_df["Item ID"].value_counts()
```


```python
purchase_analysis_total = pd.DataFrame ({"Number of Unique Items": unique_items.count(),
                                  "Average Price": purchase_df["Price"].mean(),
                                  "Number of Purchases": purchase_df["Item ID"].count(),
                                  "Total Revenue": purchase_df["Price"].sum()
                                  },index = [0])
```


```python
purchase_analysis_total_reorg = purchase_analysis_total[["Number of Unique Items","Average Price","Number of Purchases","Total Revenue"]]
purchase_analysis_total_reorg["Average Price"] = purchase_analysis_total_reorg["Average Price"].map("${:,.2f}".format)
purchase_analysis_total_reorg["Total Revenue"] = purchase_analysis_total_reorg["Total Revenue"].map("${:,.2f}".format)
```

# Purchasing Analysis (Total)


```python
purchase_analysis_total_reorg
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Unique Items</th>
      <th>Average Price</th>
      <th>Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>183</td>
      <td>$2.93</td>
      <td>780</td>
      <td>$2,286.33</td>
    </tr>
  </tbody>
</table>
</div>




```python
female_df = purchase_df.loc[purchase_df["Gender"] == "Female",:]
uniquefemale = female_df["SN"].value_counts()
```


```python
male_df = purchase_df.loc[purchase_df["Gender"] == "Male",:]
uniquemale = male_df["SN"].value_counts()
```


```python
othergender_df = purchase_df.loc[(purchase_df["Gender"] != "Male") & (purchase_df["Gender"] != "Female"),:]
uniqueother = othergender_df["SN"].value_counts()
```


```python
gender_grp = purchase_df.groupby(["Gender"], as_index = False)
genders =(gender_grp.mean())["Gender"]
```


```python
gender_demo = pd.DataFrame({
    "Gender": genders,
    "Total Count": [uniquefemale.count(), uniquemale.count(), uniqueother.count()],
    "Percentage of Players":[round((uniquefemale.count()/unique_users.count())*100,2),round((uniquemale.count()/unique_users.count())*100,2),round((uniqueother.count()/unique_users.count())*100,2)]
    })
```


```python
gender_sorted = gender_demo.sort_values("Total Count", ascending=False)
gender_sorted = gender_sorted.set_index("Gender")
gender_sorted.index.name = None
```

# Gender Demographics


```python
gender_sorted
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.45</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1.40</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
purchase_analysis_gender = pd.DataFrame({"Gender": genders,
                                        "Purchase count":(gender_grp.count())["Item ID"],
                                        "Average Purchase Price":(gender_grp.mean())["Price"],
                                        "Total Purchase Value":(gender_grp.sum())["Price"],
                                        "Normalized Totals":round((gender_grp.sum())["Price"]/gender_demo["Total Count"],2)
                                        })
```


```python
purchase_analysis_gender_reorg = purchase_analysis_gender[["Gender","Purchase count","Average Purchase Price","Total Purchase Value","Normalized Totals"]]
purchase_analysis_gender_reorg["Normalized Totals"] = purchase_analysis_gender_reorg["Normalized Totals"].map("${:,.2f}".format)
purchase_analysis_gender_reorg["Total Purchase Value"] = purchase_analysis_gender_reorg["Total Purchase Value"].map("${:,.2f}".format)
purchase_analysis_gender_reorg["Average Purchase Price"] = purchase_analysis_gender_reorg["Average Purchase Price"].map("${:,.2f}".format)
```

# Purchasing Analysis (Gender)


```python
purchase_analysis_gender_reorg.set_index("Gender")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>136</td>
      <td>$2.82</td>
      <td>$382.91</td>
      <td>$3.83</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>633</td>
      <td>$2.95</td>
      <td>$1,867.68</td>
      <td>$4.02</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>11</td>
      <td>$3.25</td>
      <td>$35.74</td>
      <td>$4.47</td>
    </tr>
  </tbody>
</table>
</div>




```python
bins = [5,9,14,19,24,29,34,39,50]

# Create labels for these bins
group_labels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

Agedemo_series = pd.cut(purchase_df["Age"], bins, labels=group_labels)
```


```python
purchase_df["AgeRange"] = Agedemo_series
purchase_df1 = purchase_df.drop_duplicates(['SN'], keep='first')

#grouped using unique players
Agedemo_grp = purchase_df1.groupby("AgeRange",as_index=False)

#grouped using total purchases which include multiple transactions by single player
Agedemo_grp1 = purchase_df.groupby("AgeRange",as_index=False)
```

# Age Demographics


```python
age_demo = pd.DataFrame({" ":(Agedemo_grp.count())["AgeRange"],
                        "Percentage of Players":round(((Agedemo_grp.count())["SN"]/unique_users.count())*100,2),
                        "Total Count":(Agedemo_grp.count())["SN"]})
age_demo.set_index(" ")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>3.32</td>
      <td>19</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>4.01</td>
      <td>23</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>17.45</td>
      <td>100</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>45.20</td>
      <td>259</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>15.18</td>
      <td>87</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>8.20</td>
      <td>47</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>4.71</td>
      <td>27</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>1.92</td>
      <td>11</td>
    </tr>
  </tbody>
</table>
</div>




```python
purchase_analysis_age = pd.DataFrame({" ":(Agedemo_grp.count())["AgeRange"],
                          "Purchase Count":(Agedemo_grp1.count())["SN"],
                          "Average Purchase Price":round((Agedemo_grp1.mean())["Price"],2),
                          "Total Purchase Value":(Agedemo_grp1.sum())["Price"],
                          "Normalized Totals":round(((Agedemo_grp1.sum())["Price"]/(Agedemo_grp.count())["SN"]),2)
                         })
```


```python
purchase_analysis_age_reorg = purchase_analysis_age[[" ","Purchase Count","Average Purchase Price","Total Purchase Value","Normalized Totals"]].set_index(" ")
purchase_analysis_age_reorg["Average Purchase Price"] = purchase_analysis_age_reorg["Average Purchase Price"].map("${:,.2f}".format)
purchase_analysis_age_reorg["Total Purchase Value"] = purchase_analysis_age_reorg["Total Purchase Value"].map("${:,.2f}".format)
purchase_analysis_age_reorg["Normalized Totals"] = purchase_analysis_age_reorg["Normalized Totals"].map("${:,.2f}".format)
```

# Purchasing Analysis (Age)


```python
purchase_analysis_age_reorg
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>28</td>
      <td>$2.98</td>
      <td>$83.46</td>
      <td>$4.39</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>35</td>
      <td>$2.77</td>
      <td>$96.95</td>
      <td>$4.22</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>133</td>
      <td>$2.91</td>
      <td>$386.42</td>
      <td>$3.86</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>336</td>
      <td>$2.91</td>
      <td>$978.77</td>
      <td>$3.78</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>125</td>
      <td>$2.96</td>
      <td>$370.33</td>
      <td>$4.26</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>64</td>
      <td>$3.08</td>
      <td>$197.25</td>
      <td>$4.20</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>42</td>
      <td>$2.84</td>
      <td>$119.40</td>
      <td>$4.42</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>17</td>
      <td>$3.16</td>
      <td>$53.75</td>
      <td>$4.89</td>
    </tr>
  </tbody>
</table>
</div>




```python
topspenders = purchase_df.groupby("SN")
```


```python
topspendertotal = topspenders.sum()
topspendertotal["Average Purchase Price"] = (topspenders.mean())["Price"]
topspendertotal["Purchase Count"] = (topspenders.count())["Item ID"]
topspendertotal = topspendertotal.rename(columns={"Price": "Total Purchase Value"})
```


```python
topspenders_sorted = topspendertotal.sort_values("Total Purchase Value", ascending = False)[["Purchase Count","Average Purchase Price","Total Purchase Value"]]
topspenders_sorted["Average Purchase Price"] = topspenders_sorted["Average Purchase Price"].map("${:,.2f}".format)
topspenders_sorted["Total Purchase Value"] = topspenders_sorted["Total Purchase Value"].map("${:,.2f}".format)
```

# Top Spenders


```python
topspenders_sorted.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>5</td>
      <td>$3.41</td>
      <td>$17.06</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>4</td>
      <td>$3.39</td>
      <td>$13.56</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>4</td>
      <td>$3.18</td>
      <td>$12.74</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>3</td>
      <td>$4.24</td>
      <td>$12.73</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>3</td>
      <td>$3.86</td>
      <td>$11.58</td>
    </tr>
  </tbody>
</table>
</div>




```python
mostpopular = purchase_df.groupby(["Item ID","Item Name"])
```


```python
purchase_count = mostpopular.count()
purchase_count["Item Price"] = (mostpopular.mean())["Price"]
purchase_count["Total Purchase Value"] = (mostpopular.sum())["Price"]
purchase_count["Item Price"] = purchase_count["Item Price"].map("${:,.2f}".format)
```


```python
purchase_count_popular = purchase_count[["SN","Item Price","Total Purchase Value"]].sort_values("SN",ascending = False).head(5)
purchase_count_popular = purchase_count_popular.rename(columns={"SN": "Purchase Count"})
purchase_count_popular["Total Purchase Value"] = purchase_count_popular["Total Purchase Value"].map("${:,.2f}".format)
```

# Most Popular Items


```python
purchase_count_popular
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <th>Betrayal, Whisper of Grieving Widows</th>
      <td>11</td>
      <td>$2.35</td>
      <td>$25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <th>Arcane Gem</th>
      <td>11</td>
      <td>$2.23</td>
      <td>$24.53</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>9</td>
      <td>$2.07</td>
      <td>$18.63</td>
    </tr>
    <tr>
      <th>175</th>
      <th>Woeful Adamantite Claymore</th>
      <td>9</td>
      <td>$1.24</td>
      <td>$11.16</td>
    </tr>
    <tr>
      <th>13</th>
      <th>Serenity</th>
      <td>9</td>
      <td>$1.49</td>
      <td>$13.41</td>
    </tr>
  </tbody>
</table>
</div>




```python
purchase_count_profit = purchase_count[["SN","Item Price","Total Purchase Value"]].sort_values("Total Purchase Value",ascending = False).head(5)
purchase_count_profit = purchase_count_profit.rename(columns={"SN": "Purchase Count"})
purchase_count_profit["Total Purchase Value"] = purchase_count_profit["Total Purchase Value"].map("${:,.2f}".format)
```

# Most Profitable Items


```python
purchase_count_profit
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>9</td>
      <td>$4.14</td>
      <td>$37.26</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>7</td>
      <td>$4.25</td>
      <td>$29.75</td>
    </tr>
    <tr>
      <th>32</th>
      <th>Orenmir</th>
      <td>6</td>
      <td>$4.95</td>
      <td>$29.70</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>6</td>
      <td>$4.87</td>
      <td>$29.22</td>
    </tr>
    <tr>
      <th>107</th>
      <th>Splitter, Foe Of Subtlety</th>
      <td>8</td>
      <td>$3.61</td>
      <td>$28.88</td>
    </tr>
  </tbody>
</table>
</div>


