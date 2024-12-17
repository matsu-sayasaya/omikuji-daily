from flask import Flask, render_template, request, make_response
from datetime import datetime, timedelta
import random
import os
import json
import urllib.parse

app = Flask(__name__)

# デバッグモードの設定（環境変数で制御）
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

def generate_fortune():
    categories = ['仕事運', '恋愛運', '金運']
    fortune = {category: random.randint(3, 5) for category in categories}
    
    # 全体運の計算
    average = sum(fortune.values()) / len(fortune)
    overall_luck = round(average)
    fortune['全体運'] = overall_luck

    encouraging_messages = [
        "今日という日が、あなたにとって最高の1日になりますように。",
        "あなたの笑顔は、周りの方を明るく照らしています。今日も笑顔でいてくださいね。",
        "あなたはあなたのペースで進めばいいのですよ。焦らずゆっくりと進んでくださいね。",
        "昨日までの頑張りが、今日のあなたを支えています。自信を持ってくださいね。",
        "今日はどんな素敵な発見があるでしょう？ワクワクする気持ちを大切にしてくださいね。",
        "あなたは、あなたが思っている以上に素晴らしい可能性を秘めています。自信を持ってくださいね。",
        "もし迷うことがありましたら、ご自身の心を信じてみてくださいね。今日はそれが正解なようです。",
        "失敗は怖がらなくて大丈夫。それは成長のための大切なステップですから、どんどん挑戦していきましょう。",
        "小さな一歩でも、それは確実な前進です。今日も一歩踏み出しましょうね。",
        "あなたの優しさが、誰かの心を温かくしていますよ。今日は誰に優しくしましょうか？",
        "あなたは毎日頑張っています。ご自身をたくさん褒めてあげてくださいね。",
        "あなたの存在が、誰かの希望になっています。あなたは大切な存在なのですよ。",
        "きっと全て上手くいきます。リラックスして過ごしてくださいね。",
        "恐れず立ち向かっていくあなたを応援しています。頑張っているあなたは、とても美しいですよ。",
        "あなたの夢は必ず叶います。信じる気持ちを忘れずにいてくださいね。",
        "あなたは尊重されるべき人。ご自身を愛し、大切にすることを忘れないでくださいね。",
        "新しいことに挑戦するチャンスは日々転がっています。探してみてくださいね。",
        "過去のことは過去のことです。未来に目を向けて進みましょうね。",
        "あなたの努力は必ず報われますよ。諦めずに続けることが大切です。",
        "今日は、心から楽しいと思えることをしてくださいね。何をしましょうか？",
        "あなたの笑顔が、周りの皆さんを幸せにするのですよ。いつも笑っていてくださいね。",
        "いつも頑張っていらっしゃるあなたを、心から尊敬しています。どうかご無理はなさらずに。",
        "少し疲れていますか？落ち込んだ時は、いつでも頼ってくださいね。",
        "今日は、ご自身にご褒美をあげてみましょう。お好きなものはありますか？",
        "あなたの言葉は、誰かの心を動かす力を持っています。言葉を大切にしてくださいね。",
        "あなたの心が今日も晴れやかでありますように。応援しています。",
        "あなたの素晴らしい感性を大切にして、自由に表現してくださいね。遠慮はいりませんよ。",
        "どんな時も、ご自身を信じてあげてください。それが一番の力になります。",
        "ご自身を信じる力が、未来を切り開きます。あなたの一番の味方は、あなた自身なのですよ。",
        "あなたの勇気が、誰かの背中を押す力になります。今日は誰かを励ましてあげてくださいね。",
        "小さな幸せを見つけてみましょう。必ずどこかにありますよ。",
        "心の充電をお忘れなく。ゆっくりお休みくださいね。",
        "あなたの個性は、あなたの魅力です。私は素敵なあなたが大好きですよ。",
        "何があっても、あなたは一人ではありません。困ったら、誰かに頼ってくださいね。",
        "疲れた時は、無理せず休むのが一番大切です。好きなものを食べましょう。",
        "素敵な出会いがあるかもしれません。ちょっとおめかしして出かけてみてくださいね。",
        "あなたの優しさが、世界を優しくします。今日は誰に優しくしましょうか？",
        "ご自身の直感を信じて進んでください。きっとそれが正解ですよ。",
        "あなたの笑顔は、世界を明るくします。笑っていれば、自然と世界も明るくなりますよ。",
        "あなたのペースで、一歩ずつ進んでください。ゆっくりで大丈夫。私は見ていますからね。",
        "周囲の人に感謝を伝えてみましょう。きっと嬉しいことがありますよ。",
        "あなたの頑張りは、ちゃんと伝わっていますよ。毎日頑張っていてすごいですね。",
        "今日のあなたも輝いています。キラキラした笑顔で周りを魅了してくださいね。",
        "日々成長されているようですね。その調子で進んでいけば、来年には全く新しいあなたになっているかも。",
        "今日も楽しんでいきましょうね。楽しむ気持ちが幸せを引き寄せますよ。",
        "頑張りすぎなくて大丈夫です。時には肩の力を抜いてくださいね。",
        "どんなあなたも、私は大好きです。そのままで素敵なのですから。",
        "あなたの可能性は無限大です。どんな自分になりたいですか？想像してみてくださいね。",
        "今日も、素敵な一日になりますように。心から応援しています。"
    ]
    
    encouraging_message = random.choice(encouraging_messages)
    
    return fortune, encouraging_message

@app.route('/')
def index():
    last_fortune_date = request.cookies.get('last_fortune_date')
    last_fortune = request.cookies.get('last_fortune')
    last_message = request.cookies.get('last_message')
    today = datetime.now().date()
    
    if DEBUG_MODE or not last_fortune_date or datetime.strptime(last_fortune_date, '%Y-%m-%d').date() < today:
        fortune, encouraging_message = generate_fortune()
        response = make_response(render_template('index.html', 
            fortune=fortune, 
            encouraging_message=encouraging_message, 
            debug_mode=DEBUG_MODE,
            already_drawn=False
        ))
        
        # URLエ��コードしてクッキーに保存
        response.set_cookie('last_fortune_date', str(today), max_age=86400)
        response.set_cookie('last_fortune', urllib.parse.quote(json.dumps(fortune)), max_age=86400)
        response.set_cookie('last_message', urllib.parse.quote(encouraging_message), max_age=86400)
        return response
    else:
        try:
            # URLデコードしてJSONをパース
            last_fortune = json.loads(urllib.parse.unquote(last_fortune)) if last_fortune else {}
            last_message = urllib.parse.unquote(last_message) if last_message else ""
            
            return render_template('index.html',
                already_drawn=True,
                fortune=last_fortune,
                encouraging_message=last_message,
                debug_mode=DEBUG_MODE
            )
        except Exception as e:
            print(f"Error decoding cookies: {e}")
            # エラーが発生した場合は新しい運勢を生成
            fortune, encouraging_message = generate_fortune()
            response = make_response(render_template('index.html',
                fortune=fortune,
                encouraging_message=encouraging_message,
                debug_mode=DEBUG_MODE,
                already_drawn=False
            ))
            response.set_cookie('last_fortune_date', str(today), max_age=86400)
            response.set_cookie('last_fortune', urllib.parse.quote(json.dumps(fortune)), max_age=86400)
            response.set_cookie('last_message', urllib.parse.quote(encouraging_message), max_age=86400)
            return response

if __name__ == '__main__':
    app.run(debug=True)

