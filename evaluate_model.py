from preprocessing import get_final_learning_path


def test_case(name, topic, performance):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("Preferred Topic :", topic)
    print("Performance     :", performance)

    if performance < 0.60:
        level = "Beginner"
    elif performance < 0.80:
        level = "Intermediate"
    else:
        level = "Advanced"

    print("Expected Level  :", level)

    result = get_final_learning_path(
        age=20,
        education_level="Bachelor",
        learning_style="Visual",
        preferred_topics=topic,
        assessment_score=75,
        feedback_score=4.2,
        engagement_score=0.70,
        completion_status="In Progress",
        topic=topic,
        difficulty="Intermediate",
        content_type="Video",
        performance_score=performance,
        number_of_recommendations=5
    )

    print("\nRecommended Courses:")

    if result.empty:
        print("No recommendations found.")
        return

    for index, row in result.iterrows():
        print(
            f"{row['course_id']} | "
            f"{row['topic']} | "
            f"{row['difficulty']} | "
            f"{row['content_type']} | "
            f"Similarity: {row['similarity_score']:.3f}"
        )


# -------------------------------------------------
# TEST CASES
# -------------------------------------------------

test_case(
    "TEST CASE 1 - Beginner AI Learner",
    "AI",
    0.45
)

test_case(
    "TEST CASE 2 - Intermediate AI Learner",
    "AI",
    0.68
)

test_case(
    "TEST CASE 3 - Advanced AI Learner",
    "AI",
    0.90
)

test_case(
    "TEST CASE 4 - Intermediate Data Science Learner",
    "Data Science",
    0.68
)