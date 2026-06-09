from flask import Flask, render_template, request
from openai import OpenAI  # 1. 更改匯入方式
import os

app = Flask(__name__)

# 2. 初始化 Client。它會自動去讀取環境變數 中的 OPENAI_API_KEY
# 如果你想手動填入（不建議公開），可以寫成 client = OpenAI(api_key="你的_API_KEY")
client = OpenAI()

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    
    try:
        # 3. 使用新版的 API 呼叫方式
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini", # 可以簡寫
            temperature=0.5,
        )
        # 4. 新版的解析方式（從物件屬性讀取，而非字典）
        generated_text = response.choices[0].message.content.strip()
        
    except Exception as e:
        # 如果 API 呼叫失敗（例如 Key 錯了或沒錢），把錯誤訊息印在終端機，並顯示給網頁
        print(f"Error: {e}")
        generated_text = f"發生錯誤：{e}"

    return render_template('index.html', response=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
