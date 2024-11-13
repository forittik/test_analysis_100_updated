import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def calculate_subject_score(data, student_id, required_questions, optional_questions):
    score = 0

    # Calculate required questions score
    for q in required_questions:
        if q in data['Question_no'].values:
            # Get correct answer for the question
            correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
            # Get the student's answer for the question
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]

            # Debugging: Print the student's answer and correct answer
            st.write(f"Required Question {q}: Student Answer: {student_answer}, Correct Answer: {correct_answer}")

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

        # Debugging: Print the student's answer and correct answer for optional questions
        st.write(f"Optional Question {q}: Student Answer: {student_answer}, Correct Answer: {correct_answer}")

        if student_answer == correct_answer:
            score += CORRECT_MARK  # Correct answer
        else:
            score += WRONG_MARK  # Incorrect answer

    return score
