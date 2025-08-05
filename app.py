from flask import Flask, request, jsonify

from rag.rag import get_answer

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    top_k = data.get("top_k", 3)

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = get_answer(question, top_k)
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)