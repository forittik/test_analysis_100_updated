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

        # Label the bars with their scores
        for i, v in enumerate(physics_scores):
            ax.text(x[i] - width, v + 1, str(v), ha='center', fontweight='bold')
        for i, v in enumerate(chemistry_scores):
            ax.text(x[i], v + 1, str(v), ha='center', fontweight='bold')
        for i, v in enumerate(mathematics_scores):
            ax.text(x[i] + width, v + 1, str(v), ha='center', fontweight='bold')

        ax.set_xlabel("Student IDs")
        ax.set_ylabel("Scores")
        ax.set_title("Subject-wise Scores (Side-by-Side Comparison)")
        ax.set_xticks(x)
        ax.set_xticklabels(student_ids)
        ax.legend()
        st.pyplot(fig)

    # Chapter-wise Average Score Analysis
        # Chapter-wise Average Score Analysis
    # Chapter-wise Average Score Analysis
st.subheader("Chapter-wise Average Score Analysis")

# Create a dictionary to store chapter-wise scores
chapter_scores = {}
chapter_question_counts = {}

# Iterate through the questions in the data and calculate the scores for each chapter
for student_id in student_ids:
    for q in data['Question_no']:
        # Get the chapter name directly from the 'Chapter_name' column
        chapter = data.loc[data['Question_no'] == q, 'Chapter_name'].values[0]
        correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
        student_answer = data.loc[data['Question_no'] == q, student_id].values[0]

        # Update chapter scores and counts
        if chapter not in chapter_scores:
            chapter_scores[chapter] = 0
            chapter_question_counts[chapter] = 0

        if student_answer == correct_answer:
            chapter_scores[chapter] += CORRECT_MARK
        elif pd.isna(student_answer):
            chapter_scores[chapter] += UNATTEMPTED_MARK
        else:
            chapter_scores[chapter] += WRONG_MARK

        chapter_question_counts[chapter] += 1

# Calculate average score per chapter
chapter_avg_scores = {
    chapter: chapter_scores[chapter] / chapter_question_counts[chapter] 
    for chapter in chapter_scores
}

# Plot Chapter-wise Average Scores
chapters = list(chapter_avg_scores.keys())
avg_scores = list(chapter_avg_scores.values())

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(chapters, avg_scores, color='teal')

ax.set_xlabel("Average Score")
ax.set_ylabel("Chapters")
ax.set_title("Chapter-wise Average Scores")

# Display the plot
st.pyplot(fig)

# Chapter-wise Question Distribution for Physics, Chemistry, and Mathematics
st.subheader("Chapter-wise Question Distribution for Physics, Chemistry, and Mathematics")

# Function to calculate the number of questions per chapter for each subject
def chapter_question_distribution(subject_required, subject_optional):
    # Combine required and optional questions for the subject
    subject_questions = subject_required + subject_optional
    chapter_counts = {}

    for q in subject_questions:
        if q in data['Question_no'].values:
            chapter = data.loc[data['Question_no'] == q, 'Chapter_name'].values[0]
            if chapter not in chapter_counts:
                chapter_counts[chapter] = 0
            chapter_counts[chapter] += 1

    return chapter_counts

# Get chapter-wise question distribution for each subject
physics_chapter_distribution = chapter_question_distribution(PHYSICS_REQUIRED, PHYSICS_OPTIONAL)
chemistry_chapter_distribution = chapter_question_distribution(CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
mathematics_chapter_distribution = chapter_question_distribution(MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)

# Plot Chapter-wise Question Distribution for each subject
subjects = ['Physics', 'Chemistry', 'Mathematics']
chapter_distributions = [physics_chapter_distribution, chemistry_chapter_distribution, mathematics_chapter_distribution]

# Set up the plot
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

# Physics Chapter Distribution Plot
axes[0].bar(physics_chapter_distribution.keys(), physics_chapter_distribution.values(), color='blue')
axes[0].set_title("Physics Chapter-wise Question Distribution")
axes[0].set_xlabel("Chapters")
axes[0].set_ylabel("Number of Questions")
axes[0].tick_params(axis='x', rotation=45)

# Chemistry Chapter Distribution Plot
axes[1].bar(chemistry_chapter_distribution.keys(), chemistry_chapter_distribution.values(), color='green')
axes[1].set_title("Chemistry Chapter-wise Question Distribution")
axes[1].set_xlabel("Chapters")
axes[1].tick_params(axis='x', rotation=45)

# Mathematics Chapter Distribution Plot
axes[2].bar(mathematics_chapter_distribution.keys(), mathematics_chapter_distribution.values(), color='orange')
axes[2].set_title("Mathematics Chapter-wise Question Distribution")
axes[2].set_xlabel("Chapters")
axes[2].tick_params(axis='x', rotation=45)

# Display the plot
plt.tight_layout()
st.pyplot(fig)

