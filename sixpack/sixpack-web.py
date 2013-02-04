from flask import Flask, render_template, abort, request, url_for, redirect
import db
from models import Experiment

app = Flask(__name__)
from flask.ext.seasurf import SeaSurf
csrf = SeaSurf(app)

# List of experiments
@app.route("/")
def hello():
    experiments = Experiment.all(db.REDIS)
    return render_template('dashboard.html', experiments=experiments)

# Details for experiment
@app.route("/experiment/<experiment_name>/")
def details(experiment_name):
    experiment = find_or_404(experiment_name)
    return render_template('details.html', experiment=experiment)

# Set winner for an experiment
@app.route("/experiment/<experiment_name>/winner/", methods=['POST'])
def set_winner(experiment_name):
    experiment = find_or_404(experiment_name)
    experiment.set_winner(request.form['alternative_name'])

    return redirect(url_for('details', experiment_name=experiment.name))

# Reset experiment
@app.route("/experiment/<experiment_name>/reset/", methods=['POST'])
def reset_experiment(experiment_name):
    pass

# Reset experiment winner
@app.route("/experiment/<experiment_name>/winner/reset/", methods=['POST'])
def reset_winner(experiment_name):
    experiment = find_or_404(experiment_name)
    experiment.reset_winner()

    return redirect(url_for('details', experiment_name=experiment.name))

# Delete experiment
@app.route("/experiment/<experiment_name>/delete/", methods=['DELETE'])
def delete_experiment(experiment_name):
    pass

# Archive experiment
@app.route("/experiment/<experiment_name>/archive", methods=['POST'])
def archive_experiment(archive_experiment):
    pass

@app.route('/favicon.ico')
def favicon():
    return ''

def find_or_404(experiment_name):
    try:
        return Experiment.find(experiment_name, db.REDIS)
    except:
        abort(404)


# You should change this
app.secret_key = 'OQvHQgJfyNT$lC3K89/!#CJ4RLqAqH3QMIq5LXfW4eh'

if __name__ == "__main__":
    app.run(port=5001, debug=True)