# run.py

from app import create_app
from app.db_init import init_db 

app = create_app() 
with app.app_context():
    init_db()
if __name__ == '__main__':
    app.run(debug=True) 
