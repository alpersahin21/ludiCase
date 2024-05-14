from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

# read files
with open('data/users.json') as f:
    users_data = json.load(f)

with open('data/simulations.json') as f:
    simulations_data = json.load(f)

# create DataFrames
users_df = pd.DataFrame(users_data['users'])
simulations_df = pd.DataFrame(simulations_data['simulations'])

# Calculate total users per company
company_user_counts = users_df.merge(simulations_df, on='simulation_id') \
                              .groupby('company_name') \
                              .size() \
                              .reset_index(name='total_users')

# Calculate total users per day
users_df['signup_datetime'] = pd.to_datetime(users_df['signup_datetime'], unit='d', origin='1899-12-30')
daily_user_counts = users_df.set_index('signup_datetime').resample('D').size().cumsum().reset_index()
daily_user_counts.columns = ['dates', 'counts']

@app.route('/')
def index():
    return render_template('index.html', tables=[company_user_counts.to_html(classes='table table-striped', header="true")], daily_user_counts=daily_user_counts.to_dict(orient='list'))

if __name__ == '__main__':
    app.run(debug=True)
