import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data from the CSV file (assuming it's named 'data.csv')
data = pd.read_csv('https://raw.githubusercontent.com/forittik/test_analysis_100_updated/refs/heads/main/final_mereged_data.csv')

# Set up constants
CORRECT_MARK = 4
WRONG_MARK = -1
UNATTEMPTED_MARK = 0

# Define question ranges for each subject
PHYSICS_REQUIRED = list(range(1, 21))         # Questions 1-20
PHYSICS_OPTIONAL = list(range(21, 31))        # Questions 21-30

CHEMISTRY_REQUIRED = list(range(31, 51))      # Questions 31-50
CHEMISTRY_OPTIONAL = list(range(51, 61))      # Questions 51-60

MATHEMATICS_REQUIRED = list(range(61, 81))    # Questions 61-80
MATHEMATICS_OPTIONAL = list(range(81, 91))    # Questions 81-90

# Function to calculate scores based on rules
def calculate_subject_score(data, student_id, required_questions, optional_questions):
    score = 0

    # Calculate required questions score
    for q in required_questions:
        if q in data['Question_no'].values:
            # Get correct answer for the question
            correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
            # Get the student's answer for the question
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]

            # Compare student's answer with the correct answer
            if student_answer == correct_answer:
                score += CORRECT_MARK  # Correct answer
            elif pd.isna(student_answer):  # Unattempted question
                score += UNATTEMPTED_MARK
            else:  # Wrong answer
                score += WRONG_MARK

    # Handle optional questions scoring:
    optional_attempts = []
    for q in optional_questions:
        if q in data['Question_no'].values:
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]
            if not pd.isna(student_answer):  # Attempted question
                optional_attempts.append((q, student_answer))

    # Compare the student's answers with the correct answers for all attempted optional questions
    for q, student_answer in optional_attempts:
        correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
        
        if student_answer == correct_answer:
            score += CORRECT_MARK  # Correct answer
        else:
            score += WRONG_MARK  # Incorrect answer

    # Ensure the score does not exceed the maximum score of 100 for each subject
    return min(score, 100)

# Streamlit UI
st.title("JEE Mock Test Score Calculator")

# Select multiple student IDs
student_ids = st.multiselect("Select Student IDs", options=data.columns[3:])  # Assuming student IDs start from the 4th column

if student_ids:
    # Initialize score lists for each student
    physics_scores = []
    chemistry_scores = []
    mathematics_scores = []
    total_scores = []

    # Loop through each selected student
    for student_id in student_ids:
        # Calculate scores for each subject
        physics_score = calculate_subject_score(data, student_id, PHYSICS_REQUIRED, PHYSICS_OPTIONAL)
        chemistry_score = calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
        mathematics_score = calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)

        # Append the results to the lists
        physics_scores.append(physics_score)
        chemistry_scores.append(chemistry_score)
        mathematics_scores.append(mathematics_score)
        total_scores.append(physics_score + chemistry_score + mathematics_score)

    # Display scores for each student
    for idx, student_id in enumerate(student_ids):
        st.subheader(f"Scores for {student_id}")
        st.write(f"Physics Score: {physics_scores[idx]}")
        st.write(f"Chemistry Score: {chemistry_scores[idx]}")
        st.write(f"Mathematics Score: {mathematics_scores[idx]}")
        st.write(f"Total Score: {total_scores[idx]} / 300")

    # Total Score Distribution - Bar Plot
    st.subheader("Total Score Distribution (Bar Plot)")
    plt.figure(figsize=(10, 6))
    plt.bar(student_ids, total_scores, color='purple')
    plt.xlabel("Student IDs")
    plt.ylabel("Total Score")
    plt.title("Total Score Comparison Across Students")
    plt.ylim(0, 300)  # Max total score of 300
    st.pyplot(plt)

    # Subject-wise Performance Comparison - Side-by-Side Column Chart
    st.subheader("Subject-wise Performance Comparison (Side-by-Side Column Chart)")

    # Ensure the lists match the length of student_ids
    if len(student_ids) == len(physics_scores) == len(chemistry_scores) == len(mathematics_scores):
        subjects = ['Physics', 'Chemistry', 'Mathematics']
        subject_scores = [physics_scores, chemistry_scores, mathematics_scores]

        # Create a side-by-side bar chart
        width = 0.25  # Width of bars
        x = np.arange(len(student_ids))  # Position of bars on x-axis

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(x - width, physics_scores, width, label='Physics', color='blue')
        ax.bar(x, chemistry_scores, width, label='Chemistry', color='green')
        ax.bar(x + width, mathematics_scores, width, label='Mathematics', color='orange')

        ax.set_xlabel("Student IDs")
        ax.set_ylabel("Scores")
        ax.set_title("Subject-wise Scores (Side-by-Side Comparison)")
        ax.set_xticks(x)
        ax.set_xticklabels(student_ids)
        ax.legend()
        st.pyplot(fig)

