from flask import Flask, url_for, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from imageprocessor import ImageProcessor
import gunicorn
from dotenv import load_dotenv
import os

# function from flask documentation to check allowed file names
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# create form to accept files
class ImageForm(FlaskForm):
    file = FileField("Choose Image File", validators=[DataRequired()])
    submit = SubmitField("Create Palette")


load_dotenv()
# Initialize app
app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = "static/photos"




@app.route('/', methods=['GET','POST'])
def homepage():
    forma = ImageForm()

    if forma.validate_on_submit():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("results", filename=filename))


    return render_template("index.html", form=forma)



@app.route('/results/<filename>')
def results(filename):
    full_path = f"static/photos/{filename}"
    print(full_path)
    imgprosobj =ImageProcessor(full_path)
    hexlist = imgprosobj.get_hex_list()
    os.remove(full_path)
    return render_template("results.html", hexcodes=hexlist)


if __name__ == "__main__":
    app.run()