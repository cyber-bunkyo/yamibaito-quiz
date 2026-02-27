import csv
import random

# バリエーションパーツ
usernames = ["副業バイト速報", "学生応援バイト", "簡単日払いWORKS", "速攻バイト便", "夜バイト情報局"]
handles = ["@fukugyo_now", "@baito_campus", "@easyjob_tokyo", "@soku_baito", "@night_baito"]
time_options = ["30分前", "1時間前", "2時間前", "昨日", "3日前"]
hashtags_list = [
    "#副業 #高収入", "#短期バイト #日払い", "#夜勤 #未経験OK", "#在宅ワーク #怪しい？", "#闇バイト #注意"
]

# 闇バイト・普通バイト候補
danger_baito = [
    {
        "content": "【高額バイト】\n日給8万円✨即日現金手渡し！\n履歴書不要・個人情報一切ナシ！\nまずはDM📩",
        "hashtags": hashtags_list[0],
        "answer": "×",
        "explanation": "異常に高い報酬（8万円）、即現金手渡し、匿名性が強い募集は闇バイトの典型です。個人情報を渡さず応募できる＝責任の所在が不明なケースが多く、非常に危険です。"
    },
    {
        "content": "【未経験歓迎】\n口座開設するだけで3万円💸\n学生大歓迎！\n今すぐLINE追加→",
        "hashtags": hashtags_list[4],
        "answer": "×",
        "explanation": "報酬のわりに作業が簡単すぎる場合は要注意。口座売買・名義貸しの可能性があり、犯罪に加担するリスクが高いです。"
    }
]

normal_baito = [
    {
        "content": "【カフェバイト募集】\n週2日〜OK☕️シフト自由♪\n時給1200円＋交通費支給🚃\n学生・未経験歓迎！",
        "hashtags": hashtags_list[1],
        "answer": "〇",
        "explanation": "勤務地・時給・シフト条件が明確で、応募条件も一般的。安全なアルバイトです。"
    },
    {
        "content": "【イベントスタッフ】\n週末限定🎪時給1500円＋交通費！\n友達と応募OK👭",
        "hashtags": hashtags_list[2],
        "answer": "〇",
        "explanation": "仕事内容が具体的で、条件も現実的です。応募方法も明示されているため安心な募集です。"
    }
]

# ミックスして10問分生成
all_quizzes = []
for i in range(1, 11):
    if random.random() < 0.5:
        quiz = random.choice(danger_baito)
    else:
        quiz = random.choice(normal_baito)

    entry = {
        "id": i,
        "username": random.choice(usernames),
        "handle": random.choice(handles),
        "time_ago": random.choice(time_options),
        "content": quiz["content"],
        "hashtags": quiz["hashtags"],
        "answer": quiz["answer"],
        "explanation": quiz["explanation"]
    }
    all_quizzes.append(entry)

# CSV書き出し
with open("static/data/quiz_x_sample_2.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "username", "handle", "time_ago", "content", "hashtags", "answer", "explanation"
    ])
    writer.writeheader()
    writer.writerows(all_quizzes)
