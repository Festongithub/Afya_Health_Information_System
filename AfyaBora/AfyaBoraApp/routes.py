from AfyaBoraApp import app 

@app.route('/')
@app.route('/index')
def index():
    return "<h2> Hello world </h2>"
 