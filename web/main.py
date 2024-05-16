from flask import Flask,render_template,request,redirect,flash


import requests

app = Flask(__name__)
app.secret_key = "tc,;sv.f;bmgnlmvlrmvlmwdmwsq".encode('utf8')
app.base_url="http://127.0.0.1:5000"
app.template_folder = "templates"
@app.route("/")
def index():
  response = requests.get('http://127.0.0.1:5000/supplier')

  supplier = response.json()
  return render_template("supplier.html",supplier=supplier)
 
if __name__=='__main__':
  app.run(debug=True,port=5001)

