import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file (assuming it's named 'data.csv')
# Sample data has columns: Question_no, correct_answer_key, Chapter_name, S001, S002, ..., S010, ...
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
        # Check if the question exists in the dataset
        if q in data['Question_no'].values:
            correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]

            if student_answer == correct_answer:
                score += CORRECT_MARK
            elif pd.isna(student_answer):  # Unattempted
                score += UNATTEMPTED_MARK
            else:  # Wrong answer
                score += WRONG_MARK

    # Handle optional questions scoring:
    optional_attempts = []
    
    for q in optional_questions:
        # Check if the question exists in the dataset
        if q in data['Question_no'].values:
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]
            if not pd.isna(student_answer):  # Attempted question
                optional_attempts.append((q, student_answer))

    # If more than 5 optional questions were attempted, only consider the first 5
    if len(optional_attempts) > 5:
        optional_attempts = optional_attempts[:5]

    # Calculate score for the selected optional questions
    for q, student_answer in optional_attempts:
        correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
        if student_answer == correct_answer:
            score += CORRECT_MARK
        else:
            score += WRONG_MARK

    return score

# Streamlit UI
st.title("JEE Mock Test Score Calculator")

# Select student ID
student_id = st.selectbox("Select Student ID", options=data.columns[3:])  # Assuming student IDs start from the 4th column

if student_id:
    # Calculate scores for each subject
    physics_score = calculate_subject_score(data, student_id, PHYSICS_REQUIRED, PHYSICS_OPTIONAL)
    chemistry_score = calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
    mathematics_score = calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)

    # Display scores
    st.subheader("Scores")
    st.write(f"Physics Score: {physics_score}")
    st.write(f"Chemistry Score: {chemistry_score}")
    st.write(f"Mathematics Score: {mathematics_score}")
    total_score = physics_score + chemistry_score + mathematics_score
    st.write(f"Total Score: {total_score} / 300")

    # Plot results in a bar chart
    subjects = ['Physics', 'Chemistry', 'Mathematics']
    scores = [physics_score, chemistry_score, mathematics_score]
    plt.figure(figsize=(10, 6))
    plt.bar(subjects, scores, color=['blue', 'green', 'orange'])
    plt.xlabel("Subjects")
    plt.ylabel("Scores")
    plt.title("Subject-wise Scores")
    plt.ylim(0, 100)  # Assuming a max score of 100 per subject
    st.pyplot(plt)

