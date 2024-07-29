from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, File
from flask_migrate import Migrate
import boto3
import os
from botocore.exceptions import NoCredentialsError

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Create a connection to S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)

# Define a function to upload files to S3
def upload_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        return f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"
    except NoCredentialsError:
        return None
    
    # Define the routes for the application backend

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        s3_url = upload_to_s3(file, app.config['S3_BUCKET'])
        if s3_url:
            new_file = File(filename=file.filename, s3_url=s3_url)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('success', file_url=s3_url))
        else:
            flash('File upload failed')
            return redirect(request.url)

@app.route('/success')
def success():
    file_url = request.args.get('file_url')
    return render_template('success.html', file_url=file_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)