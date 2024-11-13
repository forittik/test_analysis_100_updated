import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Only consider the first 5 attempted questions from optional
    optional_attempts = optional_attempts[:5]

    for q, student_answer in optional_attempts:
        correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
        if student_answer == correct_answer:
            score += CORRECT_MARK  # Correct answer
        else:
            score += WRONG_MARK  # Incorrect answer

    return score

# Streamlit UI
st.title("JEE Mock Test Score Calculator")

# Select multiple students
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

    # Create a score distribution plot
    st.subheader("Score Distribution of Selected Students")
    plt.figure(figsize=(10, 6))
    plt.bar(student_ids, total_scores, color='purple')
    plt.xlabel("Student IDs")
    plt.ylabel("Total Score")
    plt.title("Total Score Comparison Across Students")
    plt.ylim(0, 300)  # Max total score of 300
    st.pyplot(plt)

    # Create a subject-wise comparison plot
    st.subheader("Subject-wise Performance Comparison")
    subjects = ['Physics', 'Chemistry', 'Mathematics']
    subject_scores = [physics_scores, chemistry_scores, mathematics_scores]

    plt.figure(figsize=(10, 6))
    width = 0.25  # Width of bars
    x = range(len(student_ids))

    for i, subject_score in enumerate(subject_scores):
        plt.bar([p + width * i for p in x], subject_score, width=width, label=subjects[i])

    plt.xlabel("Student IDs")
    plt.ylabel("Scores")
    plt.title("Subject-wise Comparison")
    plt.xticks([p + width for p in x], student_ids)  # Adjust the labels
    plt.legend()
    st.pyplot(plt)

    # Create a box plot for subject-wise scores comparison
    st.subheader("Subject-wise Score Distribution (Box Plot)")
    subject_scores_data = [physics_scores, chemistry_scores, mathematics_scores]
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=subject_scores_data, orient='v', notch=True, palette="Set2")
    plt.xticks([0, 1, 2], subjects)
    plt.title("Box Plot of Subject-wise Scores")
    plt.ylabel("Scores")
    st.pyplot(plt)
