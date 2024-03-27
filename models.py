from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below
    
class Cupcake(db.Model):
    """Cupcake Model!"""

    __tablename__ = "cupcakes"

    def __repr__(self):
        c=self
        return f"<cupcake id={c.id} flavor={c.flavor} size={c.size} rating={c.rating} image={c.image}"
    
    def serialize_cupcake(self):
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
            }


    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    flavor=db.Column(db.Text,
                        nullable=False)
    size=db.Column(db.Text,
                        nullable=False)
    rating=db.Column(db.Float,
                  nullable=False)
    image=db.Column(db.Text, 
                        nullable=False,
                        default='https://tinyurl.com/demo-cupcake')
    