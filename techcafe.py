from flask import Flask, render_template, url_for

techcafeApp = Flask(__name__)

@techcafeApp.route('/')
def home():
    return render_template('home.html')

@techcafeApp.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    techcafeApp.run(port=3300,debug=True)



    
    