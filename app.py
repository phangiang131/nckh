from flask import Flask, escape, request, render_template, Response
from service.elasticsearch import find_product
from service.tag_extraction import get_entity_by_tag

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def hello():
    # if request.method == 'GET' or request.method == 'POST':
    #     keyword = request.form.get('search')
    #     product_list = find_product(keyword)
    #     return render_template('index.html', products="<div>ok</div>")

    return render_template('index.html')

@app.route('/ajaxhandler', methods = ['POST','GET'])
def process_products():
    xml = ''
    keyword = request.form.get('keyword')
   
    product_list = find_product(keyword)
    for p in product_list:
        xml = xml + '<p>' + p + '</p>'
    

    return Response(xml, mimetype='application/xml')


@app.route('/model', methods = ['POST','GET'])
def home():    
    return render_template('index_.html')

@app.route('/ajaxhandlermodel', methods = ['POST','GET'])
def process_products_model():
    xml = ''
    keyword = request.form.get('keyword')
    keyword = ' '.join(get_entity_by_tag(keyword))
    product_list = find_product(keyword)
    for p in product_list:
        xml = xml + '<p>' + p + '</p>'
    

    return Response(xml, mimetype='application/xml')
app.run(host='0.0.0.0', port=6350)