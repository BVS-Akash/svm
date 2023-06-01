from flask import Flask,request,render_template,redirect,url_for,jsonify
from flask_cors import CORS
from svm import svmmodel
from vendor import vendor_model
import os
app=Flask(__name__)
CORS(app)


cf_port = os.getenv("PORT")


@app.route('/')
def home():
    return " "


@app.route('/submit',methods=['GET'])
def submit():
    #flag=str(request.form['flag'])
    # parser = reqparse.RequestParser()
     # parser.add_argument('flag', required=True)
    flag = request.args.get('flag')
    if flag=='1':
        description=request.args.get('description').lower()
        description=list(description.split(','))
        output=svmmodel(description)
        jl=[]
        for i in range(len(description)):
            d={}
            d['description']=description[i]
            d['glaccount']=output[i][0]
            d['costcenter']=output[i][1]
            jl.append(d)
        ddr={}
        ddr['referenceModel']='description'
        ddr['results']=jl
        return jsonify(ddr)
    if flag=='2':
        vendor_names=str(request.args.get("input_text")).lower()
        vendor_names=list(vendor_names.split(','))
        output=vendor_model(vendor_names)
        jl=[]
        for i in range(len(vendor_names)):
            d={}
            d['vendor_name']=vendor_names[i]
            d['vendor_code']=output[i]
            jl.append(d)
        ddr={}
        ddr['referncemodel']='vendor_name'
        ddr['results']=jl
        return jsonify(ddr)



if __name__ == '__main__':
	if cf_port is None:
		app.run(host='0.0.0.0', port=8007, debug=True)
	else:
		app.run(host='0.0.0.0', port=int(cf_port))
