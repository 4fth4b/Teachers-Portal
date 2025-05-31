from app import create_app, db
from flask_migrate import Migrate
from app.models import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_talisman import Talisman
from redis import Redis

app = create_app()
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": "*"}})
Talisman(app, content_security_policy=None)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per 15 minutes"],
)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
