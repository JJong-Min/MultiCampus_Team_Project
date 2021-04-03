from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_result', methods=['GET'])
def recommend_result():
    data = request.args.getlist('title')
    title = ''
    length = len(data)
    for i in range(length) :
            title = title + data[i]
    return render_template("recommend_result.html", title = title, length = length)

@app.route('/portfolio_details_weather_1')
def portfolio_details_weather_1() :
    return render_template("portfolio_details_weather_1.html")

@app.route('/portfolio_details_weather_2')
def portfolio_details_weather_2() :
    return render_template("portfolio_details_weather_2.html")

@app.route('/portfolio_details_board_1')
def portfolio_details_board_1() :
    return render_template("portfolio_details_board_1.html")

@app.route('/portfolio_details_board_2')
def portfolio_details_board_2() :
    return render_template("portfolio_details_board_2.html")

@app.route('/portfolio_details_people_1')
def portfolio_details_people_1() :
    return render_template("portfolio_details_people_1.html")

@app.route('/portfolio_details_people_2')
def portfolio_details_people_2() :
    return render_template("portfolio_details_people_2.html")

@app.route('/drama_details_사생결단_로맨스')
def drama_details_사생결단_로맨스() :
    return render_template("drama_details_사생결단_로맨스.html")

@app.route('/drama_details_세상에서_제일_예쁜_내_딸')
def drama_details_세상에서_제일_예쁜_내_딸() :
    return render_template("drama_details_세상에서_제일_예쁜_내_딸.html")

@app.route('/drama_details_너도_인간이니')
def drama_details_너도_인간이니() :
    return render_template("drama_details_너도_인간이니.html")

@app.route('/drama_details_봄밤')
def drama_details_봄밤() :
    return render_template("drama_details_봄밤.html")

@app.route('/drama_details_신과의_약속')
def drama_details_신과의_약속() :
    return render_template("drama_details_신과의_약속.html")

@app.route('/drama_details_단짠_오피스')
def drama_details_단짠_오피스() :
    return render_template("drama_details_단짠_오피스.html")

@app.route('/drama_details_검법남녀')
def drama_details_검법남녀() :
    return render_template("drama_details_검법남녀.html")

@app.route('/drama_details_데릴남편_오작두')
def drama_details_데릴남편_오작두() :
    return render_template("drama_details_데릴남편_오작두.html")

@app.route('/drama_details_싸이코패스_다이어리')
def drama_details_싸이코패스_다이어리() :
    return render_template("drama_details_싸이코패스_다이어리.html")

@app.route('/drama_details_맛_좀_보실래요')
def drama_details_맛_좀_보실래요() :
    return render_template("drama_details_맛_좀_보실래요.html")

@app.route('/drama_details_더_뱅커')
def drama_details_더_뱅커() :
    return render_template("drama_details_더_뱅커.html")

@app.route('/drama_details_60일_지정생존자')
def drama_details_60일_지정생존자() :
    return render_template("drama_details_60일_지정생존자.html")

@app.route('/drama_details_열여덟의_순간')
def drama_details_열여덟의_순간() :
    return render_template("drama_details_열여덟의_순간.html")

@app.route('/drama_details_보좌관_2_세상을_움직이는_사람들')
def drama_details_보좌관_2_세상을_움직이는_사람들() :
    return render_template("drama_details_보좌관_2_세상을_움직이는_사람들.html")

@app.route('/drama_details_아름다운_세상')
def drama_details_아름다운_세상() :
    return render_template("drama_details_아름다운_세상.html")

@app.route('/drama_details_달리는_조사관')
def drama_details_달리는_조사관() :
    return render_template("drama_details_달리는_조사관.html")

@app.route('/drama_details_웰컴2라이프')
def drama_details_웰컴2라이프() :
    return render_template("drama_details_웰컴2라이프.html")

@app.route('/drama_details_내_뒤에_테리우스')
def drama_details_내_뒤에_테리우스() :
    return render_template("drama_details_내_뒤에_테리우스.html")

@app.route('/drama_details_그남자_오수')
def drama_details_그남자_오수() :
    return render_template("drama_details_그남자_오수.html")

@app.route('/drama_details_이별이_떠났다')
def drama_details_이별이_떠났다() :
    return render_template("drama_details_이별이_떠났다.html")

@app.route('/drama_details_마더')
def drama_details_마더() :
    return render_template("drama_details_마더.html")

@app.route('/drama_details_미스터_기간제')
def drama_details_미스터_기간제() :
    return render_template("drama_details_미스터_기간제.html")

@app.route('/drama_details_간택_여인들의_전쟁')
def drama_details_간택_여인들의_전쟁() :
    return render_template("drama_details_간택_여인들의_전쟁.html")

@app.route('/drama_details_마녀의_사랑')
def drama_details_마녀의_사랑() :
    return render_template("drama_details_마녀의_사랑.html")

@app.route('/drama_details_아스달_연대기')
def drama_details_아스달_연대기() :
    return render_template("drama_details_아스달_연대기.html")

@app.route('/drama_details_흉부외과_심장을_훔친_의사들')
def drama_details_흉부외과_심장을_훔친_의사들() :
    return render_template("drama_details_흉부외과_심장을_훔친_의사들.html")

@app.route('/drama_details_뷰티_인사이드')
def drama_details_뷰티_인사이드() :
    return render_template("drama_details_뷰티_인사이드.html")

@app.route('/drama_details_녹두꽃')
def drama_details_녹두꽃() :
    return render_template("drama_details_녹두꽃.html")

@app.route('/drama_details_구해줘_2')
def drama_details_구해줘_2() :
    return render_template("drama_details_구해줘_2.html")

@app.route('/drama_details_설렘주의보')
def drama_details_설렘주의보() :
    return render_template("drama_details_설렘주의보.html")

@app.route('/drama_details_황금정원')
def drama_details_황금정원() :
    return render_template("drama_details_황금정원.html")

@app.route('/drama_details_힙합왕_나스나길')
def drama_details_힙합왕_나스나길() :
    return render_template("drama_details_힙합왕_나스나길.html")

@app.route('/drama_details_신의_퀴즈_리부트')
def drama_details_신의_퀴즈_리부트() :
    return render_template("drama_details_신의_퀴즈_리부트.html")

@app.route('/drama_details_레벨업')
def drama_details_레벨업() :
    return render_template("drama_details_레벨업.html")

@app.route('/drama_details_식샤를_합시다_3_비긴즈')
def drama_details_식샤를_합시다_3_비긴즈() :
    return render_template("drama_details_식샤를_합시다_3_비긴즈.html")

@app.route('/drama_details_제3의_매력')
def drama_details_제3의_매력() :
    return render_template("drama_details_제3의_매력.html")

@app.route('/drama_details_쌉니다_천리마마트')
def drama_details_쌉니다_천리마마트() :
    return render_template("drama_details_쌉니다_천리마마트.html")

@app.route('/drama_details_여우각시별')
def drama_details_여우각시별() :
    return render_template("drama_details_여우각시별.html")

@app.route('/drama_details_그녀로_말할_것_같으면')
def drama_details_그녀로_말할_것_같으면() :
    return render_template("drama_details_그녀로_말할_것_같으면.html")

@app.route('/drama_details_최고의_이혼')
def drama_details_최고의_이혼() :
    return render_template("drama_details_최고의_이혼.html")

@app.route('/drama_details_모두의_거짓말')
def drama_details_모두의_거짓말() :
    return render_template("drama_details_모두의_거짓말.html")

@app.route('/random')
def random():
    return render_template('Random_forest.html')

@app.route('/gradient')
def gradient():
    return render_template('Gradient_Boosting.html')

@app.route('/regression')
def regression():
    return render_template('Regression_model.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['userId']
    return redirect('/')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/login_pro', methods=['POST'])
def login_pro():
    userId = request.form['userId']
    pwd = request.form['pwd']
    result = db.login_result(userId, pwd)
    if result:

        session['userId'] = userId
        return render_template('index.html')
    else:
        return redirect('login')

@app.route('/join_pro', methods=['POST'])
def join_pro():
    userId = request.form['userId']
    pwd = request.form['pwd']
    userName = request.form['userName']
   
    if db.get_member_one(userId):
        return render_template('fail.html')
    else:
        db.add_member(userId, userName, pwd)
        return render_template('success.html')

app.run(host='127.0.0.1', port=5000, debug=True)