from flask import Flask, url_for, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<p>%r</p> <a href="/admin/delete/%s">Delete</a>' % (self.content, self.id)

@app.route('/', methods=['GET'])
def index():
    feedback = request.args.get("feedback")
    if feedback:
        feedback = Feedback(content=feedback)
        db.session.add(feedback)
        db.session.commit()
        return 'Thanks for sending your feedback'
    else:
        return 'Please, send your feedback'

@app.route('/admin/', methods=['GET'])
def admin():
    password = request.args.get("password")
    if password == 'secret':
        feedbacks = Feedback.query.all()
        return render_template_string("<div>%s</div>" % feedbacks)
    else:
        return 'Wrong Password'

@app.route('/admin/delete/<int:id>', methods=['GET'])
def delete(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    return 'The feedback has been deleted'

if __name__ == "__main__":
    app.run(debug=True)
