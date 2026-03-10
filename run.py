from app import create_app
from app.db import init_db

init_db()
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
