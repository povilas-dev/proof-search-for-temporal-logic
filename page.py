from flask import Flask, redirect, url_for, render_template, request
import main as prover_main

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sequent", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        sequent_input = request.form["sequent-input"]
        return redirect(url_for("proof", seq=sequent_input))
    else:
        return render_template("proof.html")


@app.route("/proof/<seq>")
def proof(seq):
    (result, result_proof) = prover_main.resolve(seq)
    print("Proof:")
    print(result_proof)
    return render_template("proof.html", sequent=seq, boolean_result=result, proof=result_proof)


if __name__ == "__main__":
    app.run(debug=True)
