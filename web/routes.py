from flask import render_template, request, redirect, url_for
from web.models import Document, Term, TermsDistribution, Deconstructor
from web.tools import preprocess, TFIDF, VSM
from web import app
from web import db

deconstructor = Deconstructor()
preprocessor = preprocess.Preprocessor()
tfdf_calculator = TFIDF.TFIDFTool()
vsm_tool = VSM.VSMTool()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/terms")
def terms():
    documents = get_all_documents(is_get_dist=True)
    terms = {}
    for document in documents:
        for term in document["term_dist"]:
            if term["term"] in terms :
                terms[term["term"]] += term["freq"]
            else:
                terms[term["term"]] = term["freq"]
    
    return render_template("terms.html", title="All terms", terms=terms)

@app.route("/documents")
def show_all_documents():
    documents = get_all_documents()
    return render_template("documents.html", title="All documents" ,documents=documents)

@app.route("/documents/add")
def add():
    return render_template("add.html", title="Add new document")

@app.route("/documents/save", methods=["POST"])
def save():
    title = request.form.get("name")
    content = request.form.get("content")

    new = Document(name=title, content=content)
    db.session.add(new)
    db.session.commit() 
    return redirect(url_for("show_all_documents"))

@app.route("/result")
def result():
    query = request.args.get("q")
    documents = get_all_documents(is_get_dist=True)
    
    tfidf_result = search_using_tfidf(query=query, documents=documents)

    return render_template("result.html", title="Hasil pencarian" ,documents=tfidf_result)

def get_all_documents(is_get_dist=False) -> list :
    documents = Document.query.all()
    documents = deconstructor.bulk_deconstruct(documents)
    if is_get_dist:
        for index, document in enumerate(documents):
            documents[index]["term_dist"] = preprocessor.process(document["content"])
            print("asiap")

    return documents

def search_using_tfidf(query: str, documents: list) -> list:
    query_terms = preprocessor.process(query)
    tfidf_result = tfdf_calculator.calculate_weight(documents=documents)
    result = vsm_tool.rank(documents=tfidf_result["documents"], idf_list=tfidf_result["idf_list"], queries=query_terms)

    return result