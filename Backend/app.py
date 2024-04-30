from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/article"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    category = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=db.func.now())
    updated_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    status = db.Column(db.String(100))


@app.route("/")
def index():
    return "Selamat datang di halaman website article!"


@app.route("/article", methods=["POST"])
def create_article():
    data = request.get_json()
    message, code = validate_article(data)
    if code != 200:
        print(message)
        return jsonify({"message": message}), code
    try:
        post = Post(
            title=data["title"],
            content=data["content"],
            category=data["category"],
            status=data["status"],
        )

        db.session.add(post)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Artikel berhasil ditambahkan",
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Artikel gagal ditambahkan", "message": str(e)}), 500


@app.route("/article/<int:limit>/<int:offset>", methods=["GET"])
def get_articles(limit, offset):

    try:
        posts = Post.query.offset(offset).limit(limit).all()

        if not posts:
            return jsonify({"message": "Artikel Tidak Ditemukan"}), 404

        articles = [
            {
                "title": article.title,
                "content": article.content,
                "category": article.category,
                "status": article.status,
            }
            for article in posts
        ]
        return jsonify(articles), 200

    except Exception as e:
        return jsonify({"error": "Data gagal ditampilkan", "message": str(e)}), 500


@app.route("/article/<int:id>", methods=["GET"])
def get_article(id):
    try:
        post = Post.query.get(id)

        if not post:
            return jsonify({"message": "Artikel Tidak Ditemukan"}), 404

        article = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "status": post.status,
        }

        return jsonify(article), 200

    except Exception as e:
        return jsonify({"error": "Artikel gagal ditampilkan", "message": str(e)}), 500


@app.route("/article/<int:id>", methods=["PUT"])
def update_article(id):
    data = request.get_json()
    message, code = validate_article(data)
    if code != 200:
        return jsonify({"message": message}), code
    try:
        post = Post.query.get(id)

        if not post:
            return jsonify({"message": "Artikel tidak ditemukan"}), 404

        post.title = data["title"]
        post.content = data["content"]
        post.category = data["category"]
        post.status = data["status"]

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Artikel berhasil diupdate",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Artikel gagal diupdate", "message": str(e)}), 500


@app.route("/article/<int:id>", methods=["DELETE"])
def delete_article(id):
    try:
        post = Post.query.get(id)

        if not post:
            return jsonify({"message": "Artikel Tidak Ditemukan"}), 404

        db.session.delete(post)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Artikel berhasil dihapus",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Artikel gagal dihapus", "message": str(e)}), 500


def validate_article(data):
    if not all(key in data for key in ("title", "content", "category", "status")):
        return "Data yang dimasukkan tidak lengkap!", 400
    if len(data["title"]) < 20:
        return "Title harus lebih dari 20 karakter", 400
    if len(data["content"]) < 200:
        return "Content harus lebih dari 200 karakter", 400
    if len(data["category"]) < 3:
        return "Category harus lebih dari 3 karakter", 400
    if data["status"] not in ["publish", "draft", "trash"]:
        return "Status harus antara publish, draft, atau trash", 400
    return None, 200


if __name__ == "__main__":
    app.run(debug=True)
