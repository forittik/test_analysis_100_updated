import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
            correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]

            if student_answer == correct_answer:
                score += CORRECT_MARK
            elif pd.isna(student_answer):
                score += UNATTEMPTED_MARK
            else:
                score += WRONG_MARK

    # Calculate optional questions score
    optional_attempts = []
    for q in optional_questions:
        if q in data['Question_no'].values:
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]
            if not pd.isna(student_answer):
                optional_attempts.append((q, student_answer))

    for q, student_answer in optional_attempts:
        correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
        score += CORRECT_MARK if student_answer == correct_answer else WRONG_MARK

    return min(score, 100)

# Streamlit UI
st.title("JEE Mock Test Score Analysis")

# Select multiple student IDs
student_ids = st.multiselect("Select Student IDs", options=data.columns[3:])

if student_ids:
    physics_scores = []
    chemistry_scores = []
    mathematics_scores = []
    total_scores = []

    for student_id in student_ids:
        physics_score = calculate_subject_score(data, student_id, PHYSICS_REQUIRED, PHYSICS_OPTIONAL)
        chemistry_score = calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
        mathematics_score = calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)

        physics_scores.append(physics_score)
        chemistry_scores.append(chemistry_score)
        mathematics_scores.append(mathematics_score)
        total_scores.append(physics_score + chemistry_score + mathematics_score)

    all_student_columns = data.columns[3:]
    all_total_scores = [
        calculate_subject_score(data, student_id, PHYSICS_REQUIRED, PHYSICS_OPTIONAL) +
        calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL) +
        calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)
        for student_id in all_student_columns
    ]
    avg_all_students = np.mean(all_total_scores)
    avg_selected_students = np.mean(total_scores)

    # Total Score Distribution - Bar Plot with Average Lines
    st.subheader("Total Score Distribution (Bar Plot)")
    plt.figure(figsize=(10, 6))
    plt.bar(student_ids, total_scores, color='purple', label='Total Scores')
    plt.axhline(avg_all_students, color='red', linestyle='--', linewidth=1.5, label='Average for All Students')
    plt.axhline(avg_selected_students, color='blue', linestyle='--', linewidth=1.5, label='Average for Selected Students')
    plt.text(len(student_ids) - 0.5, avg_all_students + 5, f"{avg_all_students:.2f}", color='red', ha='center', fontweight='bold')
    plt.text(len(student_ids) - 0.5, avg_selected_students + 5, f"{avg_selected_students:.2f}", color='blue', ha='center', fontweight='bold')
    plt.xlabel("Student IDs")
    plt.ylabel("Total Score")
    plt.title("Total Score Comparison Across Students")
    plt.ylim(0, 300)
    plt.legend()
    st.pyplot(plt)

    # Subject-wise Average Comparison Plot
    st.subheader("Subject-wise Average Scores (Selected vs All Students)")
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

    avg_physics_selected = np.mean(physics_scores)
    avg_chemistry_selected = np.mean(chemistry_scores)
    avg_mathematics_selected = np.mean(mathematics_scores)

    subjects = ['Physics', 'Chemistry', 'Mathematics']
    avg_all_students = [avg_physics_all_students, avg_chemistry_all_students, avg_mathematics_all_students]
    avg_selected_students = [avg_physics_selected, avg_chemistry_selected, avg_mathematics_selected]

    x = np.arange(len(subjects))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, avg_all_students, width, label='All Students', color='skyblue')
    bars2 = ax.bar(x + width/2, avg_selected_students, width, label='Selected Students', color='orange')

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

    ax.set_xlabel("Subjects")
    ax.set_ylabel("Average Scores")
    ax.set_title("Average Scores by Subject for All Students vs Selected Students")
    ax.set_xticks(x)
    ax.set_xticklabels(subjects)
    ax.legend()
    st.pyplot(fig)
