from flask import Flask, redirect, url_for, render_template, request, flash
import prover_output as prover_main

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/proof/<seq>")
def proof(seq):
    (result, result_proof) = prover_main.resolve(seq)
    print("Proof:")
    proof_list = result_proof.split('\n')
    proof_list.pop()
    proof_list.reverse()
    print(proof_list)

    return render_template("proof.html", sequent=seq, boolean_result=result, proof='\n'.join(map(str, proof_list)))


# Message flashing
@app.route("/sequent", methods=["POST", "GET"])
def sequent():
    if request.method == "POST":
        req = request.form
        sequent_input = request.form["sequent-input"]
        if len(sequent_input) == 0:
            flash('Įveskite sekvenciją!')
            return redirect(url_for("home"))
        else:
            return redirect(url_for("proof", seq=sequent_input))
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
