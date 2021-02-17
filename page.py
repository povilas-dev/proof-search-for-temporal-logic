from flask import Flask, redirect, url_for, render_template, request, flash
import prover_output as prover_main

app = Flask(__name__)
app.secret_key = 'supersecret'


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/proof/<seq>")
def proof(seq):
    received_result = prover_main.resolve(seq)
    if isinstance(received_result, prover_main.InvalidInputError):
        flash(received_result.message)
        return render_template("index.html")
    else:
        (result, result_proof, sequent_proof_list, jsonTree) = received_result
        if (result, result_proof, sequent_proof_list,jsonTree) != (False, None, None, None):
            print("Tree: ")
            print(jsonTree)
            print("Proof:")
            proof_list = result_proof.split('\n')
            proof_list.pop()
            proof_list.reverse()
            sequent_proof_list.reverse()
            # for el in sequent_proof_list:
                # print("seq: ", el, "parent:", el.parent_hash)
                # print(el.siblings)
            # tree = build_tree(sequent_proof_list)
            return render_template("proof.html", sequent=seq, boolean_result=result, sequent_list=sequent_proof_list,
                                   proof='\n'.join(map(str, proof_list)), res=jsonTree)
        else:
            return render_template("proof.html", sequent=seq, boolean_result=result, proof=result_proof)


# Message flashing
@app.route("/sequent", methods=["POST", "GET"])
def sequent():
    if request.method == "POST":
        sequent_input = request.form["sequent-input"]
        if len(sequent_input) == 0:
            flash('Įveskite sekvenciją!')
            return redirect(url_for("home"))
        else:
            return redirect(url_for("proof", seq=sequent_input))
    else:
        return render_template("index.html")


# def build_tree(sequent_list):
#     # returns result tree as string html table code
#     depths = map(lambda el: el.depth, sequent_list)
#     max_depth = max(list(depths))
#     result_tree = "<table>"
#     for i in range(max_depth):
#         result_tree += "<tr>" + "<td>" + str(sequent_list[i]) + "</td>" + "</tr>"
#     result_tree += "</table>"
#     print("BUILDING TREE")
#     print(result_tree)
#     return result_tree


if __name__ == "__main__":
    app.run(debug=True)
