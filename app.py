from flask import Flask, request, jsonify, render_template, url_for, session, redirect, flash
import google.generativeai as genai
from instaFetch import fetch_post
import re
import json
import os

genai.configure(api_key=os.getenv("API_KEY"))
app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        post_url = request.form['post']
        session['post_url'] = post_url
        return redirect(url_for('generated'))
    
    return render_template('home.html')

@app.route('/generated')
def generated():
    post_url = session.get('post_url', None)
    if post_url is None:
        return redirect(url_for('home'))
    shortcode, content, num_images = fetch_post(post_url)

    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "You have to act as an api that will ask me some details about a product and based on all the details that i provide, you will generate all the required information that i need to make it a listing on amazon. The response will be in the format of an api, {title: , store: , Price: , Description: , ProductInformation: {}}, product information will contain all the available technical information, for example if it is a light, then length, watt, etc based on the information that i give only and in description, you can write a little extra about the product if your know"},
            {"role": "model", "parts": "Great, what information do you have ?"},
        ]
    )
    response = chat.send_message(content)
    resp = response.text
    # Remove comments (// and everything after until the end of the line)
    cleaned_resp = re.sub(r'//.*', '', resp)
    match = re.search(r'\{.*\}', cleaned_resp, re.DOTALL)
    if match:

        data = json.loads(match.group(0))
        title = data.get('title', '')
        store = data.get('store', '')
        price = data.get('price', '')
        description = data.get('description', '')
        product_information = data.get('productInformation', {})
    else:
        flash('Could not generate data')
        return redirect(url_for('home'))
    
    return render_template('index.html', title=title, store=store, price=price, description=description, product_information=product_information, shortcode=shortcode, num_images=num_images)
    

if __name__ == '__main__':
    app.run(debug=True)