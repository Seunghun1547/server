from flask import Flask
# html 문서를 load
# 단, templates 폴더에 있는 html만 바라볼 수 있다
# 터미널에서 mkdir templates
from flask import render_template 
from flask import request, redirect, make_response
from aws import detect_labels_local_file as label
from aws import compare_faces as faces
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 서버 주소 / 로 들어오면
# return html문서
@app.route("/")
def index():
    return render_template("home.html")

# 1. day13.py에 /compare라는 경로 만들기
# 2. home.html에 입력태그(form) 하나 추가, 이미지 2개를 (file1, file2)전송
# 3. compare에서 받은 이미지 2개를 static폴더에 잘 저장
# 4. aws.py안에 compare_faces 그 결과를 문자열로 "동일 인물일 확률은 15.24% 입니다" 리턴
# 5. compare에서 리턴된 문자열을 받아서 웹 상에 출력
@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]

            f1_filename = secure_filename(f1.filename)
            f2_filename = secure_filename(f2.filename)

            f1.save("static/" + f1_filename)
            f2.save("static/" + f2_filename)

            r = faces("static/" + f1_filename, "static/" + f2_filename)
            return r
            
    except:
        return "얼굴 비교 실패"

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]
            
            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일 등을
            # 마음대로 저장할 수 없음
            # 서버에 클라이언트가 보낸 이미지를 저장
            f.save("static/" + filename)
            r = label("static/" + filename)
            return r
        
    except:
        return "감지 실패"

@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"

@app.route("/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            # login_id, login_pw
            # get -> request.args
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            if (login_id == "nayeho") and (login_pw == "1234"):
                # 로그인 성공 -> 로그인 성공 페이지로 이동
                # nayeho님 환영합니다

                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)

                return response
            else:
                # 로그인 실패 -> / 경로로 다시 이동
                return redirect("/")
    except:
        return "로그인 실패"
    
@app.route("/login/success")
def login_success():

    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__ == "__main__":
    # 1. host
    # 2. port
    # localhost=127.0.0.1
    # 내 아이피 주소 : 0.0.0.0
    app.run(host="0.0.0.0")