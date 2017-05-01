from flask import Flask
from flask import render_template, redirect, url_for, request
import csv
import itertools
import random
import string

app = Flask(__name__)


@app.route('/') # main page
@app.route('/list')
def index():
    readed_story_list = read_data_from_csv()
    return render_template("list.html", story_list=readed_story_list)


@app.route('/story')  # story page
@app.route('/story/<int:story_id>')  # edit page, if id is int <int:story_id>
def story_page(story_id=None):
    return render_template("form.html", story_id=story_id)


def read_data_from_csv():
    story_list = []
    with open(filename="story_list.csv", "r") as csvfile:
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, "story_list.csv")
        for row in csvfile:
            row = row.replace("\n", "")
            row_list = row.split(',')
            story_list.append(row_list)
        return story_list


def generate_random():
    new_story_list = read_data_from_csv()
    non_unic_code = True
    punct_except_spec_char = string.punctuation
    punct_except_spec_char = punct_except_spec_char.replace(";", "")
    while non_unic_code:
        non_unic_code = False
        story_id = []
        for i in range(2):
            story_id.append(random.choice(string.ascii_lowercase))
            story_id.append(random.choice(string.ascii_uppercase))
            story_id.append(random.choice(string.digits))
            story_id.append(random.choice(punct_except_spec_char))
        random.shuffle(story_id)
        story_id = ''.join(story_id)
        for story in range(len(new_story_list)):
            if story_id == new_story_list[story][0]:
                non_unic_code = True
    return story_id


def write_new_data():
    new_story_list = read_data_from_csv()
    story_title = request.form['story_title']
    user_story = request.form['user_story']
    acceptance = request.form['acceptance']
    buisness = request.form['buisness']
    estimation = request.form['estimation']
    status = request.form['status']
    new_datas = [story_title, user_story, acceptance, buisness, estimation, status]
    new_line = list(itertools.chain(*new_datas))
    new_story_list.extend((generate_random(), new_line))
    with open("story_list.csv", "w") as csvfile:
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, "story_list.csv")
        for story in new_story_list:
            row = str(generate_random()) + ';' + ';'.join(story)
            csvfile.write(row + "\n")


def delete_data_from_csv():
    new_story_list = read_data_from_csv()
    for story in new_story_list:
        if story_id in line:
            new_story_list.remove(line)
    with open("story_list.csv", "w") as csvfile:
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, "story_list.csv")
        for story in new_story_list:
            row = ';'.join(story)
            csvfile.write(row + "\n")


if __name__ == "__main__":  # only run your app when the file run directly
    app.run(debug=True)
