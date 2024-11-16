import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import fitz
from PIL import Image
import os
import pathlib
import google.generativeai as genai
import time
import random

# Set up the API key for Google Generative AI
GOOGLE_API_KEY = "your_google_api_key"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

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

# Function to convert PDF pages to JPEG
def pdf_page_to_jpeg(pdf_path, output_dir, page_numbers):
    pdf_document = fitz.open(pdf_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in page_numbers:
        if page_num < 0 or page_num >= len(pdf_document):
            continue

        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        jpeg_filename = os.path.join(output_dir, f"page_{page_num + 1}.jpeg")
        image.save(jpeg_filename, "JPEG")
    pdf_document.close()

# Function to process the image
def process_image(image_path):
    img = Image.open(image_path)
    response = model.generate_content(["""From the given image, give me the topics and concepts that the questions depend upon. 
    Also make sure that we constrain the chapter names to JEE syllabus only.
    Also just give me topics and sub-topics without any description of that sub-topic.
    Make sure the output is in sequence; don't jumble up question numbers.""", img])
    return response.text

# Streamlit UI
st.title("JEE Mock Test Score Analysis")

# Upload PDF File
pdf_file = st.file_uploader("Upload a PDF File", type=["pdf"])

# Select multiple student IDs
student_ids = st.multiselect("Select Student IDs", options=data.columns[3:])

if student_ids:
    physics_scores = []
    chemistry_scores = []
    mathematics_scores = []
    total_scores = []

    # Loop through selected students and calculate scores
    for student_id in student_ids:
        physics_score = calculate_subject_score(data, student_id, PHYSICS_REQUIRED, PHYSICS_OPTIONAL)
        chemistry_score = calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
        mathematics_score = calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)

        physics_scores.append(physics_score)
        chemistry_scores.append(chemistry_score)
        mathematics_scores.append(mathematics_score)
        total_scores.append(physics_score + chemistry_score + mathematics_score)

    # Display score format for each selected student
    for i, student_id in enumerate(student_ids):
        st.subheader(f"Scores of {student_id}")
        st.write(f"Physics Score: {physics_scores[i]}")
        st.write(f"Chemistry Score: {chemistry_scores[i]}")
        st.write(f"Mathematics Score: {mathematics_scores[i]}")
        st.write(f"Total Score: {total_scores[i]} / 300")
        st.write("---")

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
        for student_id in data.columns[3:]
    ])
    avg_chemistry_all_students = np.mean([
        calculate_subject_score(data, student_id, CHEMISTRY_REQUIRED, CHEMISTRY_OPTIONAL)
        for student_id in data.columns[3:]
    ])
    avg_mathematics_all_students = np.mean([
        calculate_subject_score(data, student_id, MATHEMATICS_REQUIRED, MATHEMATICS_OPTIONAL)
        for student_id in data.columns[3:]
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

    # Chapter-wise Average Score Analysis
    st.subheader("Chapter-wise Average Score Analysis")
    chapter_scores = {}
    chapter_question_counts = {}

    for student_id in student_ids:
        for q in data['Question_no']:
            chapter = data.loc[data['Question_no'] == q, 'Chapter_name'].values[0]
            correct_answer = data.loc[data['Question_no'] == q, 'correct_answer_key'].values[0]
            student_answer = data.loc[data['Question_no'] == q, student_id].values[0]

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

    chapter_avg_scores = {
        chapter: chapter_scores[chapter] / chapter_question_counts[chapter]
        for chapter in chapter_scores
    }

    chapters = list(chapter_avg_scores.keys())
    avg_scores = list(chapter_avg_scores.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(chapters, avg_scores, color='teal')

    ax.set_xlabel("Average Score")
    ax.set_ylabel("Chapters")
    ax.set_title("Chapter-wise Average Scores")
    st.pyplot(fig)

    # Handling PDF for Image-based Question Analysis
    if pdf_file:
        st.subheader("PDF Image-based Analysis")
        pdf_path = pdf_file
        output_dir = "output_images"
        page_numbers = [0, 1, 2]  # Example: extract the first three pages
        pdf_page_to_jpeg(pdf_path, output_dir, page_numbers)
        
        for page_num in page_numbers:
            image_path = f"{output_dir}/page_{page_num + 1}.jpeg"
            st.image(image_path, caption=f"Page {page_num + 1}", use_column_width=True)

            image_text = process_image(image_path)
            st.text_area(f"Text from Page {page_num + 1}", image_text, height=300)
