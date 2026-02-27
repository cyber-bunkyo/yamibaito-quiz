from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --------------------
# スタートページ
# --------------------
@app.route("/")
def index():
    session.clear()  # セッションリセット
    return render_template("index.html")

# --------------------
# スタートボタン
# --------------------
@app.route("/start_quiz", methods=["POST"])
def start_quiz():
    difficulty = request.form.get("difficulty", "easy")  # easy or hard
    session["difficulty"] = difficulty
    return redirect(url_for("quiz"))

# --------------------
# クイズページ
# --------------------
@app.route("/quiz")
def quiz():
    if "quizzes" not in session:
        difficulty = session.get("difficulty", "easy")

        x_df = pd.read_csv("static/data/quiz_x.csv")
        insta_df = pd.read_csv("static/data/quiz_insta.csv")
        line_df = pd.read_csv("static/data/quiz_line.csv")

        quizzes = []
        for df, style in [(x_df, "x"), (insta_df, "insta"), (line_df, "line")]:
            # 難易度でフィルタ
            df_filtered = df[df['difficulty'] == difficulty]
            samples = df_filtered.sample(n=4)
            for _, row in samples.iterrows():
                quiz = row.to_dict()
                quiz["style"] = style
                quizzes.append(quiz)

        random.shuffle(quizzes)
        quizzes = quizzes[:10]

        session["quizzes"] = quizzes
        session["current_index"] = 0
        session["score"] = 0

    current_index = session.get("current_index", 0)
    quizzes = session.get("quizzes", [])

    if current_index >= len(quizzes):
        return redirect(url_for("result"))

    quiz = quizzes[current_index]
    return render_template(f"quiz_{quiz['style']}.html", quiz=quiz, question_number=current_index + 1)

# --------------------
# iframe プレビュー用ルート（安全版）
# --------------------
@app.route("/preview/<style>")
def preview_quiz(style):
    quiz_id = request.args.get("quiz_id")
    if not quiz_id:
        return "quiz_id が指定されていません", 404

    quizzes = session.get("quizzes", [])

    # セッションにない場合は CSV から検索
    if not quizzes:
        df_map = {
            "x": pd.read_csv("static/data/quiz_x.csv"),
            "insta": pd.read_csv("static/data/quiz_insta.csv"),
            "line": pd.read_csv("static/data/quiz_line.csv")
        }
        df = df_map.get(style)
        if df is None:
            return "不正なスタイルです", 404
        quiz_row = df[df['id'] == int(quiz_id)]
        if quiz_row.empty:
            return "クイズが見つかりませんでした", 404
        quiz = quiz_row.iloc[0].to_dict()
        quiz["style"] = style
    else:
        quiz = next(
            (q for q in quizzes if str(q.get("id")) == str(quiz_id) and q.get("style") == style),
            None
        )
        if quiz is None:
            return "クイズが見つかりませんでした", 404

    preview_template = f"quiz_{style}_preview.html"
    return render_template(preview_template, quiz=quiz)

# --------------------
# 解説ページ POST
# --------------------
@app.route("/explanation", methods=["POST"])
def explanation_post():
    user_answer = request.form["answer"]
    current_index = session.get("current_index", 0)
    quizzes = session.get("quizzes", [])

    quiz = quizzes[current_index]
    is_correct = (user_answer == quiz["answer"])

    if is_correct:
        session["score"] += 1

    quiz["user_answer"] = user_answer
    quizzes[current_index] = quiz
    session["quizzes"] = quizzes
    session["last_is_correct"] = is_correct
    session["last_user_answer"] = user_answer

    return redirect(url_for("explanation_get"))

# --------------------
# 解説ページ GET
# --------------------
@app.route("/explanation_get")
def explanation_get():
    current_index = session.get("current_index", 0)
    quizzes = session.get("quizzes", [])
    quiz = quizzes[current_index]

    is_correct = session.get("last_is_correct", False)
    user_answer = session.get("last_user_answer", None)

    return render_template(
        "quiz_kaisetsu.html",
        quiz=quiz,
        is_correct=is_correct,
        user_answer=user_answer,
        question_number=current_index + 1
    )

# --------------------
# 次の問題へ
# --------------------
@app.route("/quiz/next")
def next_quiz():
    session["current_index"] += 1
    return redirect(url_for("quiz"))

# --------------------
# 結果ページ
# --------------------
@app.route("/result")
def result():
    score = session.get("score", 0)
    quizzes = session.get("quizzes", [])

    result_details = []
    for quiz in quizzes:
        result_details.append({
            "id": quiz["id"],
            "style": quiz["style"],
            "content": quiz.get("content", ""),
            "answer": quiz["answer"],
            "user_answer": quiz.get("user_answer", ""),
            "is_correct": quiz.get("user_answer", "") == quiz["answer"],
            "username": quiz.get("username", "")
        })

    if score >= 9:
        message = "バッチリ！闇バイトの見抜き方、完璧だね✨"
        user_type = "鋭いプロフェッショナル"
    elif score >= 6:
        message = "なかなか鋭いね！あとちょっとで完璧！"
        user_type = "慎重派バイト見極め人"
    elif score >= 3:
        message = "もう少し慎重に見極めてみよう💭"
        user_type = "直感型チャレンジャー"
    else:
        message = "ちょっと危ないかも… 闇バイトに気をつけて⚠"
        user_type = "カモにされがち予備軍"

    response = render_template(
        "result.html",
        score=score,
        message=message,
        user_type=user_type,
        result_details=result_details
    )

    session.clear()  # 結果表示後にセッションをクリア
    return response

# --------------------
# 起動
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
