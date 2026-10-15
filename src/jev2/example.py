import json
from urllib.request import Request, urlopen

import os
from dotenv import load_dotenv

# .env holds a line like: JEV_API_KEY=your_api_key_here
load_dotenv()
API_KEY = os.environ["JEV_API_KEY"]
URL = "https://api.typesafe.ai/v1/systemone"


def jev(state, **questions):
    body = json.dumps({"model": "jev-latest", "state": state, "questions": questions}).encode()
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    with urlopen(Request(URL, body, headers)) as r:
        return json.load(r)["answers"]

state = "내 API 키였네;;"

answers = jev(
    state,
    choice_question={
        "type": "choice",
        "instructions": "이 사람 감정은 어떤 상태인가요?",
        "criteria": {
            "기쁨": "긍정적인 반응, 행복한 감정",
            "중립": "감정이 특별히 긍정적이거나 부정적이지 않음",
            "슬픔": "부정적인 반응, 우울한 감정",
        },
    },
    noul_question={
        "type": "noul",
        "instructions": "지금 이 사람 감정이 기쁜 상태인가요?"
    },
    choice_intensity={
        "type": "choice",
        "instructions": "이 사람 감정이 지금 얼마나 격한가요?",
        "criteria": {
            "0": "중립; 특별히 긍정적이거나 부정적이지 않음.",
            "1": "약한 감정; 감정이 조금 드러나지만 은근하게 느껴짐",
            "2": "보통 감정; 감정이 어느 정도 드러나지만 강하지 않음",
            "3": "강한 감정; 감정이 뚜렷하게 드러나고 격하게 느껴짐.",
        },
    },
    intensity={
        "type": "score",
        "instructions": "이 사람 감정이 지금 얼마나 격한가요?",
        "criteria": [
            "중립; 특별히 긍정적이거나 부정적이지 않음.",
            "약한 감정; 감정이 조금 드러나지만 은근하게 느껴짐",
            "보통 감정; 감정이 어느 정도 드러나지만 강하지 않음",
            "강한 감정; 감정이 뚜렷하게 드러나고 격하게 느껴짐.",
        ],
    },
)


print(json.dumps(answers, indent=2, ensure_ascii=False))
print(answers["noul_question"]["noul"], answers["choice_question"]["choice"], answers["intensity"]["score"], answers["choice_intensity"]["choice"])
