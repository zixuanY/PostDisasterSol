"""
PDPlatform index (main) view.

URLs include:
/
"""
import flask
import PDPlatform
from PDPlatform.views.logic import logic

@PDPlatform.app.route('/', methods=['GET', 'POST'], endpoint='index')
def show_index():
    """Display / route."""
    return flask.render_template("index.html")

def store_info(dic):
    """
    Input: a dictionary. 
    """
    sqldb = PDPlatform.model.get_db()
    cur = sqldb.cursor()

    formid = dic.get('formid')
    id_ = dic.get('id')
    name = dic.get('name')
    age = dic.get('age')
    gender = dic.get('gender')
    height = dic.get('height')
    if 'weight' in dic:
        weight = dic.get('weight')
    location = dic.get('location')
    contact = dic.get('contact')
    condition = dic.get('condition')
    photo = dic.get('photo')

    if formid == '1':
        insertion = (None, id_, name, age, gender, height, None, location, contact, condition, photo)
        statement = 'INSERT INTO relative_side_info '
        statement += 'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    else:
        print("rescue")
        insertion = (None, id_, name, age, gender, height, location, contact, condition, photo)
        statement = 'INSERT INTO rescue_side_info '
        statement += 'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
    sqldb.commit()

@PDPlatform.app.route('/result/', methods=['POST'])
def show_result():
    """Display / route."""
    store_info(flask.request.form)
    context = flask.request.form
    candidates = logic(dict(flask.request.form)) # TODO: currently for testing
    print("candidates:", candidates)
    # candidates = logic({"id":"310105199909032244", "name":"XiaoHua", "age":20, "gender":"female", "height":171, "weight":60, "location":"重庆市", "contact":"1318888889999", "health_cond":"Heart Disease", "photo":""})
    # candidates = [{"Id":1,"Age":25,"Gender":"Male","Photo":"static/assets/victim/actual_victim.png"},{"Id":6,"Age":26,"Gender":"Male","Photo":"static/assets/victim/victim_2.png"},{"Id":6,"Age":20,"Gender":"Male","Photo":"static/assets/victim/victim_3.png"},{"Id":6,"Age":18,"Gender":"Male","Photo":"static/assets/victim/victim_4.png"}]
    return flask.render_template("result.html", candidates = candidates)
