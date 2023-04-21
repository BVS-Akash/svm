from flask import Flask,request,render_template,redirect,url_for,jsonify
from svm import svmmodel
import os
app=Flask(__name__)

cf_port = os.getenv("PORT")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    description=str(request.form["input_text"]).lower()
    description=list(description.split(','))
    #if description==[""]:
    #    return redirect(url_for('nodescription'))
    #else:
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




if __name__ == '__main__':
	if cf_port is None:
		app.run(host='0.0.0.0', port=8005, debug=True)
	else:
		app.run(host='0.0.0.0', port=int(cf_port))