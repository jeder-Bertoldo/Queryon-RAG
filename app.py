from flask import Flask
from routes.chat_routes import chat_routes
from routes.upload_routes import upload_routes
from services.faiss_service import initialize_faiss

app = Flask(__name__, template_folder='templates')

initialize_faiss()

# Registro dos blueprints
app.register_blueprint(chat_routes)
app.register_blueprint(upload_routes)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
