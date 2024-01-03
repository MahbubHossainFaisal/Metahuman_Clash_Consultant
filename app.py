from flask import Flask, jsonify, send_file, request,render_template
from flask_cors import CORS
import requests
import pickle
import numpy
import pandas
import urllib.request

df = pickle.load(open('./artifacts/df.pkl','rb'))
similarity = pickle.load(open('./artifacts/similarity_score.pkl','rb'))
top_100 = pickle.load(open('./artifacts/top_100.pkl','rb'))
app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    data = []
    index_list = top_100.index.tolist()
    for i in range(len(index_list)):
        x = df.iloc[index_list[i]]
        data.append([x['name'], f'../static/images/image{index_list[i]}.png'])

    return render_template('index.html',data=data)


    

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_metahumans',methods=['post'])
def recommend():
    mh = request.form.get('user_input')

    # Check if the hero name is in the DataFrame
    if mh not in df['name'].values:
        print(f"Hero '{mh}' not found in the DataFrame.")
        return []

    mh_index = df[df['name'] == mh].index
    #print(mh_index)
    if len(mh_index) == 0:
        print(f"Hero '{mh}' not found in the DataFrame.")
        return []

    mh_index = mh_index[0]
    distances = similarity[mh_index]
    hero_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    heroes = [x[0] for x in hero_list]
    df_reordered = df.reindex(heroes)
    alignment_mh = df[df['name'] == mh]['Alignment'].iloc[0]
    custom_cols = ['name','Alignment','Creator','Species','Gender','Speed','Strength','IQ','Power','Tier','Level']
    user_input = df[df['name'] == mh][custom_cols].values.tolist()
    index_value=df[df['name']==mh].index[0]
    user_input[0].append(f'../static/images/image{index_value}.png')
    print(user_input)

    ans = df_reordered[df_reordered['Alignment'] != alignment_mh]
    index_list = ans.head().index.tolist()
    data = []
    for i in range(len(index_list)):
        item = []
        x = df.iloc[index_list[i]]
        item.append(x['name'])
        item.append(x['Alignment'])
        item.append(x['Creator'])
        item.append(x['Species'])
        item.append(x['Gender'])
        item.append(x['Speed'])
        item.append(x['Strength'])
        item.append(x['IQ'])
        item.append(x['Power'])
        item.append(x['Tier'])
        item.append(x['Level'])
        item.append(f'../static/images/image{index_list[i]}.png')
        data.append(item)
        print(item)
    print(data)
    return render_template('recommend.html',data=data,user=user_input)

@app.route('/reference')
def reference_ui():
    return render_template('reference.html',data=list(df['name'].unique()))

if __name__ == '__main__':
    app.run(debug=True)

