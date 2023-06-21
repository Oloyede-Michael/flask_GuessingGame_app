from flask import Flask, render_template, redirect, request, session, url_for
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'


@app.route('/',methods=['GET','POST'])
def name():
    if request.method == 'POST':
        session['name'] = request.form['username']
        return redirect('/root')
    return render_template('name.html')

@app.route('/root',methods=['GET','POST'])
def root():
    if not 'random' in session:
        session['random'] = random.randint(1, 20)
        session['status'] = 'new'
        session['guesses'] = 0
    print('Status This Session:', session['status'])
    print('Random Number This Session:', session['random'])
    return render_template('index.html', randNum=session['random'], status=session['status'], guesses=session['guesses'])

@app.route('/guess', methods=['POST'])
def guess():
    if request.form['guess-value']: #Check to see if the user actually entered a valid value
        if int(request.form['guess-value']) > session['random']:
            session['status'] = 'high'
        elif int(request.form['guess-value']) < session['random']:
            session['status'] = 'low'
        else:
            session['status'] = 'win'
        session['guesses'] += 1
        if session['status'] != 'win' and session['guesses'] >= 5:
            session['status'] = 'lose'
    return redirect(url_for("root"))

@app.route('/destroy_session')
def destroy():
    session.clear()
    print('Session Cleared')
    return redirect(url_for("root"))

@app.route('/End_game')
def End():
    if request.method == 'Post':
        pass
    return 'End Of game'


@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry! No response. Try again.'

if __name__=="__main__":
    app.run(debug=True)