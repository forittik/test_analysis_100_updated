import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/forittik/test_analysis_100_updated/refs/heads/main/final_mereged_data.csv')

# Select the student
student_id = st.selectbox('Select Student ID', df.columns[4:])

# Calculate the marks for Physics
physics_marks = 0
for i in range(0, 20):
    if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
        physics_marks += 4
    elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
        physics_marks -= 1

optional_physics_attempted = 0
for i in range(20, 30):
    if df.loc[i, student_id] != 0:
        optional_physics_attempted += 1

if optional_physics_attempted > 5:
    for i in range(20, 25):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            physics_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key']:
            physics_marks -= 1
else:
    for i in range(20, 30):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            physics_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
            physics_marks -= 1

# Calculate the marks for Chemistry
chemistry_marks = 0
for i in range(30, 50):
    if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
        chemistry_marks += 4
    elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
        chemistry_marks -= 1

optional_chemistry_attempted = 0
for i in range(50, 60):
    if df.loc[i, student_id] != 0:
        optional_chemistry_attempted += 1

if optional_chemistry_attempted > 5:
    for i in range(50, 55):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            chemistry_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key']:
            chemistry_marks -= 1
else:
    for i in range(50, 60):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            chemistry_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
            chemistry_marks -= 1

# Calculate the marks for Mathematics
maths_marks = 0
for i in range(60, 80):
    if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
        maths_marks += 4
    elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
        maths_marks -= 1

optional_maths_attempted = 0
for i in range(80, 90):
    if df.loc[i, student_id] != 0:
        optional_maths_attempted += 1

if optional_maths_attempted > 5:
    for i in range(80, 85):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            maths_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key']:
            maths_marks -= 1
else:
    for i in range(80, 90):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            maths_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
            maths_marks -= 1

total_marks = physics_marks + chemistry_marks + maths_marks

# Display the results
st.write(f"Physics Marks: {physics_marks}")
st.write(f"Chemistry Marks: {chemistry_marks}")
st.write(f"Mathematics Marks: {maths_marks}")
st.write(f"Total Marks: {total_marks}")

# Plot the results
fig, ax = plt.subplots()
ax.bar(['Physics', 'Chemistry', 'Mathematics'], [physics_marks, chemistry_marks, maths_marks])
ax.set_title(f"{student_id} Marks")
ax.set_xlabel("Subject")
ax.set_ylabel("Marks")
st.pyplot(fig)
