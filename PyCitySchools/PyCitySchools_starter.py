#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[332]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Calculate the percentage of students who passed math **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[333]:


#Review School Budget Data
school_data.head(2)


# In[334]:


#Review merged data
school_data_complete.head(2)


# In[335]:


#Results Calculations

#Counts
Total_Schools = len(school_data_complete["school_name"].unique())
Total_Students = len(school_data_complete["Student ID"].unique())

#Sum
Total_Budget = school_data["budget"].sum()

#Means (Averages)
Average_Math_Score = school_data_complete["math_score"].mean()
Average_Reading_Score = school_data_complete["reading_score"].mean()

# Create bins in which to place values based upon pass/fail test scores
bins = [0, 69, 100]

# Create labels for these bins
group_labels = ["Failing", "Passing"]

# Forumula to slice the math score data and place it into bins (not applied here)
#pd.cut(school_data_complete["math_score"], bins, labels=group_labels)

# Place the data series into a new column inside of the DataFrame using the slice formula
school_data_complete["Pass_Fail_Math"] = pd.cut(school_data_complete["math_score"], bins, labels=group_labels)

#generate math passing count
school_data_complete_pass_math = (school_data_complete[school_data_complete['Pass_Fail_Math'] == "Passing"]).count()

#isolate math passing count
Math_pass_count = school_data_complete_pass_math['Pass_Fail_Math'].sum()

#Calculate Pct_Passing_Math =  Math_pass_count/Total_Students
Pct_Passing_Math = Math_pass_count/Total_Students*100

# Forumula to slice the reading score data and place it into bins
#pd.cut(school_data_complete["reading_score"], bins, labels=group_labels)

# Place the data series into a new column inside of the DataFrame using the slicer formula
school_data_complete["Pass_Fail_Reading"] = pd.cut(school_data_complete["reading_score"], bins, labels=group_labels)

#generate reading passing count
school_data_complete_pass_reading = (school_data_complete[school_data_complete['Pass_Fail_Reading'] == "Passing"]).count()

#isolate reading passing count
Reading_pass_count = school_data_complete_pass_reading['Pass_Fail_Reading'].sum()

#Calculate Pct_Passing_Reading =  Reading_pass_count/Total_Students
Pct_Passing_Reading = Reading_pass_count/Total_Students*100

#Establish overall pass fail pattern between math and reading
school_data_complete["Pass_Fail_Both"] = school_data_complete["Pass_Fail_Reading"].astype(str)+school_data_complete["Pass_Fail_Math"].astype(str)

#generate overall passing count
school_data_complete_overall_passing = (school_data_complete[school_data_complete['Pass_Fail_Both'] == "PassingPassing"]).count()

#isolate overall passing count
Overall_pass_count = school_data_complete_overall_passing['Pass_Fail_Both'].sum()

#Pct_Overall_Passing =  Overall_pass_count/Total_Students
Pct_Overall_Passing = Overall_pass_count/Total_Students*100


# In[336]:


# Place all of the data found into a summary DataFrame
District_Summary_df = pd.DataFrame({"Total Schools": [Total_Schools],
                              "Total Students": [Total_Students],
                              "Total Budget" : Total_Budget, 
                              "Average Math Score": Average_Math_Score,
                              "Average Reading Score": Average_Reading_Score,
                              "% Passing Math":Pct_Passing_Math,
                              "% Passing Reading":Pct_Passing_Reading,
                              "% Overall Passing":Pct_Overall_Passing})

#format students with comma and budget as currency two decimal places
formatted_dist_sum = District_Summary_df.style.format({'Total Students': '{0:,.0f}','Total Budget': '${0:,.2f}'})

#Display results
formatted_dist_sum


# In[ ]:


#Blank line


# In[5]:


#I left template results to check numbers


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed math **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[337]:


#review School header
school_data_complete.head(2)


# In[338]:


# Using GroupBy in order to separate the student data into fields according to "school" values
school_data_complete_grp = school_data_complete.groupby(['school_name','type'])
school_data_complete_grp.count().head(2)


# In[339]:


# Using GroupBy in order to separate the school data into fields according to "school" values
school_data_grp = school_data.groupby(['school_name','type'])
school_data_grp.count().head(2)


# In[340]:


#Results Calculations

# Total Students per school
Total_Students_per_school= school_data_complete_grp['Student ID'].count()

# Total Budget per school
Total_Budget_per_school= school_data_grp['budget'].sum()

#Average math Scores per school
Average_Math_Score_per_school = school_data_complete_grp["math_score"].mean()

#Average reading Scores
Average_Reading_Score_per_school = school_data_complete_grp["reading_score"].mean()

#Set Pass Math grouping
school_data_math_grp = school_data_complete[school_data_complete['Pass_Fail_Math']=="Passing"].groupby('school_name')

#Passing math per school count = 
Passing_math_per_school_count = school_data_math_grp['Pass_Fail_Math'].count()

#Set Pass Reading grouping
school_data_reading_grp = school_data_complete[school_data_complete['Pass_Fail_Reading']=="Passing"].groupby('school_name')

#Passing reading per school count = 
Passing_reading_per_school_count = school_data_reading_grp['Pass_Fail_Math'].count()

#Set Passing Overall grouping
school_data_overall_grp = school_data_complete[school_data_complete['Pass_Fail_Both']=="PassingPassing"].groupby('school_name')

#Passing overall per school count = 
Passing_Overall_per_school_count = school_data_overall_grp['Pass_Fail_Both'].count()


# In[343]:


# Create a School Overvuew DataFrame
school_summary_df = pd.DataFrame({"Total Students":Total_Students_per_school,
                                  "Total School Budget": Total_Budget_per_school,
                                  "Per Student Budget": Total_Budget_per_school/Total_Students_per_school,
                                  "Average Math Score": Average_Math_Score_per_school,
                                  "Average Reading Score": Average_Reading_Score_per_school,
                                  "% Passing Math": Passing_math_per_school_count/Total_Students_per_school*100,
                                  "% Passing Reading": Passing_reading_per_school_count/Total_Students_per_school*100,
                                  "% Overall Passing": Passing_Overall_per_school_count/Total_Students_per_school*100})

formatted_sch_sum = school_summary_df.style.format({'Total Students': '{0:,.0f}','Total School Budget': '${0:,.2f}', 
                                                    'Per Student Budget': '${0:,.2f}'})

formatted_sch_sum


# In[ ]:


#Blank line


# In[9]:


#I left template results to check numbers


# ## Top Performing Schools (By % Overall Passing)

# * Sort and display the top five performing schools by % overall passing.

# In[345]:


#Redraw the previous unformatted dataframe and sort decending on % overall passing and select the top 5, then reformat
Top_Perform_by_Overall_Percent = school_summary_df.sort_values("% Overall Passing", ascending=False).nlargest(5,'% Overall Passing')

formatted_top_by_ovall_pct = Top_Perform_by_Overall_Percent.style.format({'Total Students': '{0:,.0f}','Total School Budget': '${0:,.2f}', 
                                                    'Per Student Budget': '${0:,.2f}'})

formatted_top_by_ovall_pct


# In[ ]:


#Blank Line


# In[10]:


#I left template results to check numbers


# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[347]:


#Redraw the previous unformatted dataframe and sort ascending on % overall passing and select the bottom 5, then reformat
Bottom_Perform_by_Overall_Percent = school_summary_df.sort_values("% Overall Passing", ascending=True).nsmallest(5,'% Overall Passing')

formatted_bottom_by_ovall_pct = Bottom_Perform_by_Overall_Percent.style.format({'Total Students': '{0:,.0f}','Total School Budget': '${0:,.2f}', 
                                                    'Per Student Budget': '${0:,.2f}'})

formatted_bottom_by_ovall_pct


# In[ ]:


#Blank line


# In[11]:


#I left template results to check numbers


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[348]:


#calculate average math scores by grade by school
#Set grade by school
school_grade_9th_grp = school_data_complete[school_data_complete['grade']=="9th"].groupby('school_name')
school_grade_10th_grp = school_data_complete[school_data_complete['grade']=="10th"].groupby('school_name')
school_grade_11th_grp = school_data_complete[school_data_complete['grade']=="11th"].groupby('school_name')
school_grade_12th_grp = school_data_complete[school_data_complete['grade']=="12th"].groupby('school_name')

#Passing math by grade per school mean = 
average_9th_grade_math_score_by_school = school_grade_9th_grp['math_score'].mean()
average_10th_grade_math_score_by_school = school_grade_10th_grp['math_score'].mean()
average_11th_grade_math_score_by_school = school_grade_11th_grp['math_score'].mean()
average_12th_grade_math_score_by_school = school_grade_12th_grp['math_score'].mean()


# In[349]:


#summarize average math scores by grade by school
average_math_grds_by_school_df = pd.DataFrame({"9th":average_9th_grade_math_score_by_school,
                                  "10th":average_10th_grade_math_score_by_school,
                                  "11th":average_11th_grade_math_score_by_school,
                                  "12th":average_12th_grade_math_score_by_school})

average_math_grds_by_school_df.style


# In[ ]:


#Blank line


# In[12]:


#I left template results to check numbers


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[350]:


#calculate average reading scores by grade by school
#reuse Set grade by school from the math exercise

#Passing reading by grade per school mean = 
average_9th_grade_reading_score_by_school = school_grade_9th_grp['reading_score'].mean()
average_10th_grade_reading_score_by_school = school_grade_10th_grp['reading_score'].mean()
average_11th_grade_reading_score_by_school = school_grade_11th_grp['reading_score'].mean()
average_12th_grade_reading_score_by_school = school_grade_12th_grp['reading_score'].mean()


# In[351]:


#summarize average reading scores by grade by school
average_reading_grds_by_school_df = pd.DataFrame({"9th":average_9th_grade_reading_score_by_school,
                                  "10th":average_10th_grade_reading_score_by_school,
                                  "11th":average_11th_grade_reading_score_by_school,
                                  "12th":average_12th_grade_reading_score_by_school})

average_reading_grds_by_school_df.style


# In[ ]:


#Blank line


# In[13]:


#I left template results to check numbers


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[352]:


# Create bins for budget values
bins = [0, 584, 629, 644, 680]

# Create labels for these bins
group_labels = ["<$585", "$585-630","$630-645","$645-680"]

# Forumula to slice the math score data and place it into bins
#pd.cut(school_summary_df["Per Student Budget"], bins, labels=group_labels)

# Place the data series into a new column inside of the DataFrame
school_summary_df["Spending Ranges (Per Student)"] = pd.cut(school_summary_df["Per Student Budget"], bins, labels=group_labels)

#group by bin
school_summary_df_grp = school_summary_df.groupby(['Spending Ranges (Per Student)']) 


# In[353]:


#Calculate fields
#Average math Scores per school
budget_range_avg_mth_Scr = school_summary_df_grp["Average Math Score"].mean()

#Average reading Scores per school
budget_range_avg_read_Scr = school_summary_df_grp["Average Reading Score"].mean()

#Average % passing math per school
budget_range_avg_pct_math_pass = school_summary_df_grp["% Passing Math"].mean()

#Average % passing read per school
budget_range_avg_pct_read_pass = school_summary_df_grp["% Passing Reading"].mean()

#Average % overall passing per school
budget_range_avg_pct_overall_pass = school_summary_df_grp["% Overall Passing"].mean()


# In[354]:


#summarize scores by school spending
scores_by_school_spending_df = pd.DataFrame({"Average Math Score":budget_range_avg_mth_Scr,
                                             "Average Reading Score":budget_range_avg_read_Scr,
                                             "% Passing Math":budget_range_avg_pct_math_pass,
                                             "% Passing Reading":budget_range_avg_pct_read_pass,
                                             "% OverallPassing":budget_range_avg_pct_overall_pass})

scores_by_school_spending_df


# In[ ]:


#Blank line


# In[18]:


#I left template results to check numbers


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[355]:


# Create bins for school size
bins = [0, 999, 1999,5000]

# Create labels for these bins
group_labels = ["Small (<1000)", "Medium (1000-2000)","Large (2000-5000)"]

# Forumula to slice the math score data and place it into bins
#pd.cut(school_summary_df["Total Students"], bins, labels=group_labels)

# Place the data series into a new column inside of the DataFrame
school_summary_df["School Size"] = pd.cut(school_summary_df["Total Students"], bins, labels=group_labels)

#group by bin
school_summary_df_grp_size = school_summary_df.groupby(['School Size']) 


# In[374]:


#Calculate fields

#School_budget
size_range_budget= school_summary_df_grp_size["Total School Budget"].sum()

# School Count 
size_range_school_count= school_summary_df_grp_size["Total Students"].count()

# Total Students 
size_range_total_students= school_summary_df_grp_size["Total Students"].sum()

#Average math Scores per school
size_range_avg_mth_Scr = school_summary_df_grp_size["Average Math Score"].mean()

#Average reading Scores per school
size_range_avg_read_Scr = school_summary_df_grp_size["Average Reading Score"].mean()

#Average % passing math per school
size_range_avg_pct_math_pass = school_summary_df_grp_size["% Passing Math"].mean()

#Average % passing read per school
size_range_avg_pct_read_pass = school_summary_df_grp_size["% Passing Reading"].mean()

#Average % overall passing per school
size_range_avg_pct_overall_pass = school_summary_df_grp_size["% Overall Passing"].mean()


# In[376]:


#summarize scores by school size
scores_by_school_size_df = pd.DataFrame({"School Count":size_range_school_count,
                                         "Total Students":size_range_total_students,
                                         "Per Student Budget":size_range_budget/size_range_total_students,
                                         "Average Math Score":size_range_avg_mth_Scr,
                                         "Average Reading Score":size_range_avg_read_Scr,
                                         "% Passing Math":size_range_avg_pct_math_pass,
                                         "% Passing Reading":size_range_avg_pct_read_pass,
                                         "% OverallPassing":size_range_avg_pct_overall_pass})

scores_by_school_size_df.style


# In[ ]:


#Blank line


# In[22]:


#I left template results to check numbers


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[358]:


#group by school_type
school_summary_df_grp_type = school_summary_df.groupby(['type'])


#Calculate by type fields

#Average math Scores per school
type_avg_mth_Scr = school_summary_df_grp_type["Average Math Score"].mean()

#Average reading Scores per school
type_avg_read_Scr = school_summary_df_grp_type["Average Reading Score"].mean()

#Average % passing math per school
type_avg_pct_math_pass = school_summary_df_grp_type["% Passing Math"].mean()

#Average % passing read per school
type_avg_pct_read_pass = school_summary_df_grp_type["% Passing Reading"].mean()

#Average % overall passing per school
type_avg_pct_overall_pass = school_summary_df_grp_type["% Overall Passing"].mean()


# In[359]:


#summarize scores by school type
scores_by_school_type_df = pd.DataFrame({"Average Math Score":type_avg_mth_Scr,
                                             "Average Reading Score":type_avg_read_Scr,
                                             "% Passing Math":type_avg_pct_math_pass,
                                             "% Passing Reading":type_avg_pct_read_pass,
                                             "% OverallPassing":type_avg_pct_overall_pass})

scores_by_school_type_df.style


# In[ ]:


#Blank Line


# In[24]:


#I left template results to check numbers


# In[ ]:




