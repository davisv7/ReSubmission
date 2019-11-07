from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired
from main import *

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'stuff'


# https://snipnyet.com/adierebel/59f46bff77da1511c3503532/multiple-checkbox-field-using-wtforms-with-flask-wtf/
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


@app.route('/', methods=['GET', 'POST'])
def index():
    class FormProject(FlaskForm):
        url = StringField(
            label="Article URL:",
            validators=[DataRequired()]
        )
        subreddits = MultiCheckboxField(
            label='Default Subs:',
            # validators=[DataRequired()],
            choices=get_def_subs()
        )
        othersubs = TextAreaField('Other Subs?')

    form = FormProject()
    if form.validate_on_submit():
        url = form.url.data
        subreddits = form.subreddits.data
        othersubs = list(filter(lambda x: len(x) != 0, form.othersubs.data.split('\r\n')))
        # ^ removes newline characters and empty lines
        subreddits += othersubs
        print(url, subreddits, flush=True)
        print(f'Posting will complete @ {get_time((len(subreddits) - 1) * 11)}', flush=True)
        post_to_subs(url, subreddits)

        return render_template('base.html', form=form)
    else:
        print('invalid', flush=True)
        return render_template('base.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
