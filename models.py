from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Define the File model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    s3_url = db.Column(db.String(255), nullable=False)

    def __init__(self, filename, s3_url):
        self.filename = filename
        self.s3_url = s3_url
