from app import app
from models import db, Cupcake


db.drop_all()
db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

c3=Cupcake(
    flavor="lemon",
    size="small",
    rating=7,
    image="https://tinypic.host/images/2024/03/25/vegan-lemon-cupcakes-1..jpeg"

)

c4=Cupcake(
    flavor="lemon",
    size="small",
    rating=9,
    image="https://curric.springboard.com/software-engineering-career-track/default/exercises/flask-cupcakes/_images/cupcake.jpg"

)


db.session.add_all([c1, c2, c3, c4])
db.session.commit()

# {
# 	"cupcake": {
# 		"flavor": "lemon",
# 		"id": 3,
# 		"image": "https://tinypic.host/images/2024/03/25/vegan-lemon-cupcakes-1..jpeg",
# 		"rating": 7.0,
# 		"size": "small"
# 	}
# }
