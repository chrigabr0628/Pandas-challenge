#PLEASE NOTE: I recieved code source from AskBCS, Xpert Learning Assitant, and tutors.

#!/usr/bin/env python
# coding: utf-8

# PyCity Schools Analysis

# In[1]:


import os
import csv
import pandas as pd
from pathlib import Path


# In[2]:


# Specify the new directory path
new_directory = 'C:\\Users\\chris\\Documents\\Module 4 Challenge'

# Change the current working directory
os.chdir(new_directory)

# Print the new current working directory
print("New Current Working Directory:", os.getcwd())


# In[3]:


school_csv = Path("Resources/schools_complete.csv")
student_csv = Path("Resources/students_complete.csv")


# In[4]:


school_data = pd.read_csv(school_csv)
student_data = pd.read_csv(student_csv)


# In[5]:


school_data_df = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_df.head()


# District Summary

# In[6]:


school_count = len(school_data["school_name"].unique())
school_count


# In[7]:


student_count = school_data_df["student_name"].count()
student_count


# In[8]:


total_budget = school_data["budget"].sum()
total_budget


# In[9]:


average_math_score = school_data_df["math_score"].mean()
average_math_score 


# In[10]:


average_reading_score = school_data_df["reading_score"].mean()
average_reading_score


# In[11]:


passing_math_count = school_data_df[(school_data_df["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[12]:


passing_reading_count = school_data_df[(school_data_df["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[13]:


passing_overall_count = school_data_df[(school_data_df["math_score"] >= 70) & (school_data_df["reading_score"] >= 70)].count()["student_name"]
passing_overall_percentage = passing_overall_count / float(student_count) * 100
passing_overall_percentage


# In[14]:


district_summary = pd.DataFrame({"Total Schools" : [school_count], 
                    "Total Students" : [student_count], 
                    "Total Budget" : [total_budget], 
                    "Average Math Score" : [average_math_score], 
                    "Average Reading Score" : [average_reading_score], 
                    "% Passing Math" : [passing_math_percentage], 
                    "% Passing Reading" : [passing_reading_percentage], 
                    "% Overall Passing" : [passing_overall_percentage]})


district_summary.style.format({"Total Students" : "{:,}",
                       "Total Budget" : "${:,.2f}"})


# School Summary

# In[15]:


#groupby_school = school_data_df.set_index("school_name").groupby(["school_name"])


# In[16]:


groupby_school = school_data_df.groupby(["school_name"])


# In[17]:


school_types = school_data.set_index(["school_name"])["type"]
school_types


# In[18]:


#groupby_school = school_data_df.set_index("school_name").groupby(["school_name"])
#school = groupby_school["type"]
students_per_school = school_data_df["school_name"].value_counts()
students_per_school


# In[19]:


budget_per_school = school_data_df.groupby(["school_name"])["budget"].mean()
budget_per_student = budget_per_school / students_per_school
budget_per_student


# In[20]:


per_school_math = school_data_df.groupby(["school_name"])["math_score"].mean()
per_school_math


# In[21]:


per_school_reading = school_data_df.groupby(["school_name"])["reading_score"].mean()
per_school_reading


# In[22]:


students_passing_math = school_data_df[(school_data_df["math_score"] >= 70)].groupby(["school_name"]).size()
school_students_passing_math = students_passing_math / students_per_school * 100
school_students_passing_math 


# In[23]:


students_passing_reading = school_data_df[(school_data_df["reading_score"] >= 70)].groupby(["school_name"]).size()
school_students_passing_reading = students_passing_reading / students_per_school * 100
school_students_passing_reading


# In[24]:


students_passing_math_and_reading = school_data_df[
    (school_data_df["reading_score"] >= 70) & (school_data_df["math_score"] >= 70)]

school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()
school_students_passing_math_and_reading


# In[25]:


per_school_passing_math = school_students_passing_math / students_per_school * 100
per_school_passing_reading = school_students_passing_reading / students_per_school * 100
overall_passing_rate = school_students_passing_math_and_reading / students_per_school * 100
per_school_passing_math


# In[26]:


per_school_summary = pd.DataFrame({"School Type" : school_types,
                    "Total Students" : students_per_school,
                     "Total School Budget" : budget_per_school,
                     "Per Student Budget" : budget_per_student,
                     "Average Math Score" : per_school_math,
                     "Average Reading Score" : per_school_reading,
                     "% Passing Math" : school_students_passing_math,
                     "% Passing Reading" : school_students_passing_reading,
                     "% Overall Passing Rate" : overall_passing_rate})

per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

per_school_summary


# Highest-Performing Schools (by % Overall Passing)

# In[27]:


top_schools = per_school_summary.sort_values("% Overall Passing Rate", ascending = False)
top_schools.head(5)


# Bottom-Performing Schools (by % Overall Passing)

# In[28]:


bottom_schools = per_school_summary.sort_values("% Overall Passing Rate", ascending = True)
bottom_schools.head(5)


#  Math Scores by Grade

# In[29]:


ninth_math = school_data_df.loc[(school_data_df["grade"] == "9th")].groupby(["school_name"])["math_score"].mean()
tenth_math = school_data_df.loc[(school_data_df["grade"] == "10th")].groupby(["school_name"])["math_score"].mean()
eleventh_math = school_data_df.loc[(school_data_df["grade"] == "11th")].groupby(["school_name"])["math_score"].mean()
twelfth_math = school_data_df.loc[(school_data_df["grade"] == "12th")].groupby(["school_name"])["math_score"].mean()


# In[30]:


math_scores_by_grade = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math})

math_scores_by_grade.index.name = None

math_scores_by_grade 


# Reading Scores by Grade

# In[31]:


ninth_reading = school_data_df.loc[(school_data_df["grade"] == "9th")].groupby(["school_name"])["reading_score"].mean()
tenth_reading = school_data_df.loc[(school_data_df["grade"] == "10th")].groupby(["school_name"])["reading_score"].mean()
eleventh_reading = school_data_df.loc[(school_data_df["grade"] == "11th")].groupby(["school_name"])["reading_score"].mean()
twelfth_reading = school_data_df.loc[(school_data_df["grade"] == "12th")].groupby(["school_name"])["reading_score"].mean()


# In[32]:


reading_scores_by_grade = pd.DataFrame({
        "9th": ninth_reading,
        "10th": tenth_reading,
        "11th": eleventh_reading,
        "12th": twelfth_reading})

reading_scores_by_grade.index.name = None

reading_scores_by_grade 


# Scores by School Spending

# In[33]:


spending_bins = [0, 585, 630, 645, 680]
group_names = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[34]:


scoresby_spending = per_school_summary.copy()


# In[35]:


scoresby_spending["Spending Ranges (Per Student)"] = pd.cut(budget_per_student, spending_bins, labels = group_names, right = False)

scoresby_spending.head()


# In[36]:


spending_math_scores = scoresby_spending.groupby(["Spending Ranges (Per Student)"], observed = False)["Average Math Score"].mean()
spending_reading_scores = scoresby_spending.groupby(["Spending Ranges (Per Student)"], observed = False)["Average Reading Score"].mean()
spending_passing_math = scoresby_spending.groupby(["Spending Ranges (Per Student)"], observed = False)["% Passing Math"].mean()
spending_passing_reading = scoresby_spending.groupby(["Spending Ranges (Per Student)"], observed = False)["% Passing Reading"].mean()
overall_passing_spending = scoresby_spending.groupby(["Spending Ranges (Per Student)"], observed = False)["% Overall Passing Rate"].mean()


# In[37]:


spending_summary = pd.DataFrame({"Average Math Score" : spending_math_scores,
                    "Average Reading Score" : spending_reading_scores,
                     "% Passing Math" : spending_passing_math,
                     "% Passing Reading" : spending_passing_reading,
                     "% Overall Passing Rate"  : overall_passing_spending})


spending_summary


# Scores by School Size

# In[38]:


size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[39]:


per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], size_bins, labels = labels, right = False)
per_school_summary


# In[40]:


size_math_scores = per_school_summary.groupby(["School Size"], observed = False)["Average Math Score"].mean()
size_reading_scores = per_school_summary.groupby(["School Size"], observed = False)["Average Reading Score"].mean()
size_passing_math = per_school_summary.groupby(["School Size"], observed = False)["% Passing Math"].mean()
size_passing_reading = per_school_summary.groupby(["School Size"], observed = False)["% Passing Reading"].mean()
size_overall_passing = per_school_summary.groupby(["School Size"], observed = False)["% Overall Passing Rate"].mean()


# In[41]:


size_summary = pd.DataFrame({"Average Math Score" : size_math_scores,
                    "Average Reading Score" : size_reading_scores,
                     "% Passing Math" : size_passing_math,
                     "% Passing Reading" : size_passing_reading,
                     "% Overall Passing Rate"  : size_overall_passing})


size_summary


# Scores by School Type

# In[42]:


average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing Rate"].mean()


# In[43]:


scoresby_type = pd.DataFrame({"Average Math Score" : average_math_score_by_type,
                    "Average Reading Score" : average_reading_score_by_type,
                     "% Passing Math" : average_percent_passing_math_by_type,
                     "% Passing Reading" : average_percent_passing_reading_by_type,
                     "% Overall Passing Rate"  : average_percent_overall_passing_by_type})

scoresby_type = scoresby_type.groupby('School Type').mean()
scoresby_type.head()

