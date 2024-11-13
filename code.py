import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data from the CSV file
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

    # Calculate average scores for each subject across all students
    all_student_columns = data.columns[3:]  # Assuming student data starts from the 4th column
    avg_physics_all_students = np.mean([
        calculate_subject_score(data, student_id, PHYSICS_REQUIRED, PHYSICS_OPTIONAL)
        for student_id in all_student_columns
    ])
    avg_chemistry_all_students = np.mean([
        calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
        for student_id in all_student_columns
    ])
    avg_mathematics_all_students = np.mean([
        calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)
        for student_id in all_student_columns
    ])

    # Calculate average scores for selected students
    avg_physics_selected = np.mean(physics_scores)
    avg_chemistry_selected = np.mean(chemistry_scores)
    avg_mathematics_selected = np.mean(mathematics_scores)

    # Subject-wise Average Comparison Plot
    st.subheader("Subject-wise Average Scores (Selected vs All Students)")

    subjects = ['Physics', 'Chemistry', 'Mathematics']
    avg_all_students = [avg_physics_all_students, avg_chemistry_all_students, avg_mathematics_all_students]
    avg_selected_students = [avg_physics_selected, avg_chemistry_selected, avg_mathematics_selected]

    x = np.arange(len(subjects))  # label locations
    width = 0.35  # width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, avg_all_students, width, label='All Students', color='skyblue')
    bars2 = ax.bar(x + width/2, avg_selected_students, width, label='Selected Students', color='orange')

    # Adding the average values above each bar
    for bar in bars1:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f'{bar.get_height():.2f}',
            ha='center', color='black', fontweight='bold'
        )

    for bar in bars2:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f'{bar.get_height():.2f}',
            ha='center', color='black', fontweight='bold'
        )

    # Labeling and display
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Average Scores")
    ax.set_title("Average Scores by Subject for All Students vs Selected Students")
    ax.set_xticks(x)
    ax.set_xticklabels(subjects)
    ax.legend()

    st.pyplot(fig)
