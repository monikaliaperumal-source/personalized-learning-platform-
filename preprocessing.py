import pandas as pd

# ==============================
# 1. LOAD DATASETS
# ==============================

performance_data = pd.read_csv(
    "dataset/interactions_real_rich_scaled_processed.csv"
)

resource_data = pd.read_csv(
    "dataset/optimized_learning_resource_recommendations_200.csv"
)

# ==============================
# 2. CHECK MISSING VALUES
# ==============================

print("===== MISSING VALUES: DATASET 1 =====")
print(performance_data.isnull().sum())

print("\n===== MISSING VALUES: DATASET 2 =====")
print(resource_data.isnull().sum())

# ==============================
# 3. CHECK DUPLICATE ROWS
# ==============================

print("\n===== DUPLICATES =====")

print("Dataset 1 duplicates:",
      performance_data.duplicated().sum())

print("Dataset 2 duplicates:",
      resource_data.duplicated().sum())

# ==============================
# 4. DATA TYPES
# ==============================

print("\n===== DATA TYPES: DATASET 1 =====")
print(performance_data.dtypes)

print("\n===== DATA TYPES: DATASET 2 =====")
print(resource_data.dtypes)

# ==============================
# 5. SELECT USEFUL COLUMNS
# ==============================

resource_features = resource_data[
    [
        "user_id",
        "engagement_score",
        "completion_status",
        "assessment_score",
        "feedback_score",
        "age",
        "education_level",
        "learning_style",
        "preferred_topics",
        "topic",
        "difficulty",
        "content_type"
    ]
]

performance_features = performance_data[
    [
        "user_id_new",
        "skill_id_new",
        "user_mean_correct",
        "user_interaction_count",
        "skill_mean_correct",
        "target_correct_rate"
    ]
]

print("\n===== SELECTED RESOURCE FEATURES =====")
print(resource_features.head())

print("\nShape:", resource_features.shape)

print("\n===== SELECTED PERFORMANCE FEATURES =====")
print(performance_features.head())

print("\nShape:", performance_features.shape)

# ==============================
# 6. ONE-HOT ENCODING
# ==============================

categorical_columns = [
    "completion_status",
    "education_level",
    "learning_style",
    "preferred_topics",
    "topic",
    "difficulty",
    "content_type"
]

encoded_features = pd.get_dummies(
    resource_features,
    columns=categorical_columns
)

print("\n===== ENCODED DATA =====")
print(encoded_features.head())

print("\nEncoded shape:", encoded_features.shape)

print("\nEncoded columns:")
print(encoded_features.columns.tolist())

# ==============================
# 7. PREPARE FEATURES FOR KNN
# ==============================

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Remove user ID because it is only an identifier
X = encoded_features.drop(columns=["user_id"])

# Convert True/False values into 0/1
X = X.astype(float)

print("\n===== ML FEATURES =====")
print("Number of rows:", X.shape[0])
print("Number of features:", X.shape[1])

# ==============================
# 8. SCALE FEATURES
# ==============================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\n===== SCALED FEATURES =====")
print("Shape:", X_scaled.shape)

# ==============================
# 9. CREATE KNN MODEL
# ==============================

knn_model = NearestNeighbors(
    n_neighbors=5,
    metric="cosine"
)

knn_model.fit(X_scaled)

print("\n===== KNN MODEL =====")
print("KNN model trained successfully!")

# ==============================
# 10. RECOMMENDATION FUNCTION
# ==============================

def recommend_resources(
    age,
    education_level,
    learning_style,
    preferred_topics,
    assessment_score,
    feedback_score,
    engagement_score,
    completion_status,
    topic,
    difficulty,
    content_type,
    number_of_recommendations=5
):

    # Create a student profile
    student_profile = pd.DataFrame([{
        "engagement_score": engagement_score,
        "assessment_score": assessment_score,
        "feedback_score": feedback_score,
        "age": age,
        "completion_status": completion_status,
        "education_level": education_level,
        "learning_style": learning_style,
        "preferred_topics": preferred_topics,
        "topic": topic,
        "difficulty": difficulty,
        "content_type": content_type
    }])

    # One-hot encode the student profile
    student_profile = pd.get_dummies(
        student_profile,
        columns=[
            "completion_status",
            "education_level",
            "learning_style",
            "preferred_topics",
            "topic",
            "difficulty",
            "content_type"
        ]
    )

    # Make sure student profile has exactly the same columns as X
    student_profile = student_profile.reindex(
        columns=X.columns,
        fill_value=0
    )

    # Scale the student profile
    student_scaled = scaler.transform(student_profile)

    # Find nearest resources
    distances, indices = knn_model.kneighbors(
        student_scaled,
        n_neighbors=number_of_recommendations
    )

    # Get recommended resources
    recommendations = resource_data.iloc[indices[0]].copy()

    # Add similarity score
    recommendations["similarity_score"] = 1 - distances[0]

    return recommendations

# ==============================
# 11. TEST RECOMMENDATION
# ==============================

recommendations = recommend_resources(
    age=20,
    education_level="Bachelor",
    learning_style="Visual",
    preferred_topics="AI",
    assessment_score=75,
    feedback_score=4.2,
    engagement_score=0.70,
    completion_status="In Progress",
    topic="AI",
    difficulty="Intermediate",
    content_type="Video",
    number_of_recommendations=5
)

print("\n===== RECOMMENDED LEARNING RESOURCES =====")

print(
    recommendations[
        [
            "course_id",
            "title",
            "topic",
            "difficulty",
            "content_type",
            "similarity_score"
        ]
    ].to_string(index=False)
)

# ==============================
# 12. FINAL LEARNING PATH LOGIC
# ==============================

def get_learning_path(
    age,
    education_level,
    learning_style,
    preferred_topics,
    assessment_score,
    feedback_score,
    engagement_score,
    completion_status,
    topic,
    difficulty,
    content_type,
    number_of_recommendations=5
):

    # Get many similar resources from KNN
    recommendations = recommend_resources(
        age=age,
        education_level=education_level,
        learning_style=learning_style,
        preferred_topics=preferred_topics,
        assessment_score=assessment_score,
        feedback_score=feedback_score,
        engagement_score=engagement_score,
        completion_status=completion_status,
        topic=topic,
        difficulty=difficulty,
        content_type=content_type,
        number_of_recommendations=50
    )

    # Keep only resources matching the preferred topic
    recommendations = recommendations[
        recommendations["topic"] == preferred_topics
    ]

    # Remove duplicate courses
    recommendations = recommendations.drop_duplicates(
        subset=["course_id"]
    )

    # Sort by KNN similarity
    recommendations = recommendations.sort_values(
        by="similarity_score",
        ascending=False
    )

    # Return requested number of resources
    return recommendations.head(number_of_recommendations)
# ==============================
# 13. TEST LEARNING PATH
# ==============================

learning_path = get_learning_path(
    age=20,
    education_level="Bachelor",
    learning_style="Visual",
    preferred_topics="AI",
    assessment_score=75,
    feedback_score=4.2,
    engagement_score=0.70,
    completion_status="In Progress",
    topic="AI",
    difficulty="Intermediate",
    content_type="Video",
    number_of_recommendations=5
)

print("\n===== PERSONALIZED LEARNING PATH =====")

print(
    learning_path[
        [
            "course_id",
            "title",
            "topic",
            "difficulty",
            "content_type",
            "similarity_score"
        ]
    ].to_string(index=False)
)

# ==============================
# 14. PERFORMANCE ANALYSIS
# ==============================

average_performance = performance_data["user_mean_correct"].mean()

print("\n===== PERFORMANCE ANALYSIS =====")
print("Average user performance:",
      round(average_performance, 3))

print("\nPerformance statistics:")
print(
    performance_data["user_mean_correct"].describe()
)

# ==============================
# 15. PERFORMANCE LEVEL
# ==============================

def get_performance_level(score):

    if score < 0.60:
        return "Beginner"

    elif score < 0.80:
        return "Intermediate"

    else:
        return "Advanced"
def get_final_learning_path(
    age,
    education_level,
    learning_style,
    preferred_topics,
    assessment_score,
    feedback_score,
    engagement_score,
    completion_status,
    topic,
    difficulty,
    content_type,
    performance_score,
    number_of_recommendations=5
):

    # Determine performance level
    performance_level = get_performance_level(
        performance_score
    )

    print("\nStudent performance:", performance_score)
    print("Performance level:", performance_level)
    print("Preferred topic:", preferred_topics)

    # Get many KNN recommendations
    recommendations = recommend_resources(
        age=age,
        education_level=education_level,
        learning_style=learning_style,
        preferred_topics=preferred_topics,
        assessment_score=assessment_score,
        feedback_score=feedback_score,
        engagement_score=engagement_score,
        completion_status=completion_status,
        topic=topic,
        difficulty=difficulty,
        content_type=content_type,
        number_of_recommendations=200
    )

    # Keep only preferred topic
    recommendations = recommendations[
        recommendations["topic"] == preferred_topics
    ].copy()

    # Remove duplicate courses
    recommendations = recommendations.drop_duplicates(
        subset=["course_id"]
    )

    # Sort by KNN similarity
    recommendations = recommendations.sort_values(
        by="similarity_score",
        ascending=False
    )

    learning_path = []

    # =========================================
    # BEGINNER STUDENT
    # =========================================

    if performance_level == "Beginner":

        difficulty_order = ["Beginner", "Intermediate", "Advanced"]

        for selected_difficulty in difficulty_order:

            resources = recommendations[
                recommendations["difficulty"] == selected_difficulty
            ]

            for _, resource in resources.iterrows():

                learning_path.append(resource)

                if len(learning_path) >= number_of_recommendations:
                    break

            if len(learning_path) >= number_of_recommendations:
                break

    # =========================================
    # INTERMEDIATE STUDENT
    # =========================================

    elif performance_level == "Intermediate":

        # First select Beginner resources
        beginner_resources = recommendations[
            recommendations["difficulty"] == "Beginner"
        ]

        for _, resource in beginner_resources.head(2).iterrows():
            learning_path.append(resource)

        # Then select Advanced resources
        advanced_resources = recommendations[
            recommendations["difficulty"] == "Advanced"
        ]

        for _, resource in advanced_resources.head(
            number_of_recommendations - len(learning_path)
        ).iterrows():

            learning_path.append(resource)

    # =========================================
    # ADVANCED STUDENT
    # =========================================

    else:

        difficulty_order = ["Advanced", "Intermediate", "Beginner"]

        for selected_difficulty in difficulty_order:

            resources = recommendations[
                recommendations["difficulty"] == selected_difficulty
            ]

            for _, resource in resources.iterrows():

                learning_path.append(resource)

                if len(learning_path) >= number_of_recommendations:
                    break

            if len(learning_path) >= number_of_recommendations:
                break

    return pd.DataFrame(learning_path)
final_path = get_final_learning_path(
    age=20,
    education_level="Bachelor",
    learning_style="Visual",
    preferred_topics="AI",
    assessment_score=75,
    feedback_score=4.2,
    engagement_score=0.70,
    completion_status="In Progress",
    topic="AI",
    difficulty="Intermediate",
    content_type="Video",
    performance_score=0.68,
    number_of_recommendations=5
)

print(
    final_path[
        [
            "course_id",
            "title",
            "topic",
            "difficulty",
            "content_type",
            "similarity_score"
        ]
    ].to_string(index=False)
)    # ==============================
# ==============================
# 16. IMPROVED PERFORMANCE-BASED
#     LEARNING PATH
# ==============================
print("\nAI COURSE DIFFICULTY COUNTS:")
print(
    resource_data[
        resource_data["topic"] == "AI"
    ]["difficulty"].value_counts()
)
def get_performance_based_path(
    preferred_topics,
    performance_score,
    number_of_recommendations=5
):

    # Determine performance level
    performance_level = get_performance_level(performance_score)

    # Difficulty priority
    difficulty_priority = {
        "Beginner": ["Beginner", "Intermediate"],
        "Intermediate": ["Intermediate", "Beginner", "Advanced"],
        "Advanced": ["Advanced", "Intermediate", "Beginner"]
    }

    # Filter preferred topic
    topic_resources = resource_data[
        resource_data["topic"] == preferred_topics
    ].copy()

    # Remove duplicate courses
    topic_resources = topic_resources.drop_duplicates(
        subset=["course_id"]
    )

    # Store selected resources
    learning_path = []

    # Select according to difficulty priority
    for difficulty in difficulty_priority[performance_level]:

        resources = topic_resources[
            topic_resources["difficulty"] == difficulty
        ].copy()

        # Add resources
        for _, resource in resources.iterrows():

            learning_path.append(resource)

            if len(learning_path) >= number_of_recommendations:
                break

        if len(learning_path) >= number_of_recommendations:
            break

    return pd.DataFrame(learning_path)
# ==============================
# 17. TEST PERFORMANCE-BASED PATH
# ==============================
student_performance = 0.68
preferred_topic = "AI"

#print("\n===== PERFORMANCE-BASED LEARNING PATH =====")

#performance_path = get_performance_based_path(
 #   preferred_topics=preferred_topic,
  #  performance_score=student_performance,
   # number_of_recommendations=5
#)

#print(
 #   performance_path[
  #      [
   #         "course_id",
    #        "title",
     #       "topic",
      #      "difficulty",
       #     "content_type"
       # ]
    #].to_string(index=False)
#)