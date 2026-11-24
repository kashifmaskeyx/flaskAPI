# models.py
# The Game table 
from extensions import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    platform = db.Column(db.String(50), nullable=False, default="PC")
    status = db.Column(db.String(20), nullable=False, default="backlog")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "platform": self.platform,
            "status": self.status,
        }