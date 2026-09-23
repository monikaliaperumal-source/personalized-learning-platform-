from flask import Flask, render_template, request

from preprocessing import get_final_learning_path

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    age = int(request.form["age"])
    education_level = request.form["education_level"]
    learning_style = request.form["learning_style"]
    preferred_topics = request.form["preferred_topics"]

    assessment_score = float(request.form["assessment_score"])
    feedback_score = float(request.form["feedback_score"])
    engagement_score = float(request.form["engagement_score"])

    completion_status = request.form["completion_status"]
    performance_score = float(request.form["performance_score"])

    learning_path = get_final_learning_path(
        age=age,
        education_level=education_level,
        learning_style=learning_style,
        preferred_topics=preferred_topics,
        assessment_score=assessment_score,
        feedback_score=feedback_score,
        engagement_score=engagement_score,
        completion_status=completion_status,
        topic=preferred_topics,
        difficulty="Intermediate",
        content_type="Video",
        performance_score=performance_score,
        number_of_recommendations=5
    )

    return render_template(
        "result.html",
        learning_path=learning_path.to_dict("records"),
        performance_score=performance_score,
        preferred_topic=preferred_topics
    )


if __name__ == "__main__":
    app.run(debug=False)