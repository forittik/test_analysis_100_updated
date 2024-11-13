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
