import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/forittik/test_analysis_100_updated/refs/heads/main/final_mereged_data.csv')

# Get the column names
columns = df.columns

# Select the student
student_id = st.selectbox('Select Student ID', [col for col in columns if col.startswith('S')])

# Get the subject start and end indices
physics_start, physics_end = 0, 20
chemistry_start, chemistry_end = 30, 50
math_start, math_end = 60, 80
optional_physics_start, optional_physics_end = 20, 30
optional_chemistry_start, optional_chemistry_end = 50, 60
optional_math_start, optional_math_end = 80, 90

# Calculate the marks for Physics
physics_marks = 0
for i in range(physics_start, physics_end):
    if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
        physics_marks += 4
    elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
        physics_marks -= 1

optional_physics_attempted = 0
for i in range(optional_physics_start, optional_physics_end):
    if df.loc[i, student_id] != 0:
        optional_physics_attempted += 1

if optional_physics_attempted > 5:
    for i in range(optional_physics_start, optional_physics_start + 5):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            physics_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key']:
            physics_marks -= 1
else:
    for i in range(optional_physics_start, optional_physics_end):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            physics_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
            physics_marks -= 1

# Calculate the marks for Chemistry
chemistry_marks = 0
for i in range(chemistry_start, chemistry_end):
    if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
        chemistry_marks += 4
    elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
        chemistry_marks -= 1

optional_chemistry_attempted = 0
for i in range(optional_chemistry_start, optional_chemistry_end):
    if df.loc[i, student_id] != 0:
        optional_chemistry_attempted += 1

if optional_chemistry_attempted > 5:
    for i in range(optional_chemistry_start, optional_chemistry_start + 5):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            chemistry_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key']:
            chemistry_marks -= 1
else:
    for i in range(optional_chemistry_start, optional_chemistry_end):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            chemistry_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
            chemistry_marks -= 1

# Calculate the marks for Mathematics
math_marks = 0
for i in range(math_start, math_end):
    if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
        math_marks += 4
    elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
        math_marks -= 1

optional_math_attempted = 0
for i in range(optional_math_start, optional_math_end):
    if df.loc[i, student_id] != 0:
        optional_math_attempted += 1

if optional_math_attempted > 5:
    for i in range(optional_math_start, optional_math_start + 5):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            math_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key']:
            math_marks -= 1
else:
    for i in range(optional_math_start, optional_math_end):
        if df.loc[i, student_id] == df.loc[i, 'correct_answer_key']:
            math_marks += 4
        elif df.loc[i, student_id] != df.loc[i, 'correct_answer_key'] and df.loc[i, student_id] != 0:
            math_marks -= 1

# Display the results
st.write(f"Physics Marks: {physics_marks}")
st.write(f"Chemistry Marks: {chemistry_marks}")
st.write(f"Mathematics Marks: {math_marks}")
st.write(f"Total Marks: {physics_marks + chemistry_marks + math_marks}")

# Plot the results
fig, ax = plt.subplots()
ax.bar(['Physics', 'Chemistry', 'Mathematics'], [physics_marks, chemistry_marks, math_marks])
ax.set_title(f"{student_id} Marks")
ax.set_xlabel("Subject")
ax.set_ylabel("Marks")
st.pyplot(fig)
