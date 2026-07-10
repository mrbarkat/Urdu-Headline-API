from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)
CORS(app) # تاکہ آپ کی ویب سائٹ اس API سے بات کر سکے

@app.route('/render-urdu', methods=['POST'])
def render_urdu():
    try:
        data = request.json
        text = data.get('text', 'کوئی تحریر نہیں')
        
        # ایک شفاف (Transparent) کینوس بنائیں
        img = Image.new('RGBA', (1000, 300), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # جمیل نوری نستعلیق فونٹ لوڈ کریں (سائز 80)
        font_path = "JameelNooriNastaleeq.ttf"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 80)
        else:
            font = ImageFont.load_default()
            
        # تحریر کو کینوس پر ڈرا کریں (Pillow از خود نستعلیق رینڈر کرے گا)
        draw.text((500, 150), text, font=font, fill="black", anchor="mm")
        
        # تصویر کو میموری میں محفوظ کریں
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # تصویر کو واپس فرنٹ اینڈ پر بھیجیں
        return send_file(img_byte_arr, mimetype='image/png')
        
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)