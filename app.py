from flask import Flask, render_template, request, session
import calendar
from datetime import datetime

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'cheie_secreta_pentru_sesiune'
app.config['my_variable']='da'
events = []

def get_current_year():
    return datetime.now().year

@app.route('/', methods=['GET', 'POST'])
def index():
    year = session.get('year', datetime.now().year)
    month = session.get('month', datetime.now().month)

    if request.method == 'POST':
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))

    session['year'] = year
    session['month'] = month
    app.config['my_variable']=year

    selected_date = datetime(year, month, 1).date()
    month_name = selected_date.strftime('%B')

    cal = calendar.monthcalendar(year, month)

    if request.method == 'POST':
        if 'clear' in request.form:
            events.clear()
        else:
            event_name = request.form.get('event_name')
            event_date_str = request.form.get('event_date')
            if event_date_str and event_name:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
                events.append({'name': event_name, 'date': event_date})

    selected_events = [event for event in events if event['date'].year == year and event['date'].month == month]

    return render_template('site.html', events=selected_events, year=year, month=month, month_name=month_name, calendar=cal)

@app.route('/view_event/<int:year>/<int:month>/<int:day>', methods=['GET'])
def view_event(year, month, day):
    selected_date = app.config['my_variable']
    return render_template('event.html', selected_date=selected_date)

@app.route('/event')
def event():
    return render_template('event.html')

if __name__ == '__main__':
    app.run(debug=True)
