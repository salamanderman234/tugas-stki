from flask import render_template, request, redirect, url_for
from web.models import Document, Term, TermsDistribution, Deconstructor
from web import app
from web import db
from web.tools import InvertedIndexMatrix, TFIDF, preprocess, VSM

deconstructor = Deconstructor()
matrix_builder = InvertedIndexMatrix.InvertedIndexTool()
tfidf_builder = TFIDF.TFIDFTool()
preprocessor = preprocess.Preprocessor()

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


def get_all_documents(is_get_dist=False) -> list :
    documents = Document.query.all()
    documents = deconstructor.bulk_deconstruct(documents)
    if is_get_dist:
        for index, document in enumerate(documents):
            documents[index]["tf"] = preprocessor.process(document["content"])

    return documents

@app.route("/result")
def result():
    query = request.args.get("q")
    documents = get_all_documents(is_get_dist=True)
    
    tfidf_vsm_result = search_using_tfidf(query=query, documents=documents)
    

    return render_template("result.html", title="Hasil pencarian" ,tfidf_vsm_result=tfidf_vsm_result, documents=documents)

def search_using_tfidf(query: str, documents: list) -> list:
    matrix = matrix_builder.build(documents=documents)
    document_weight_list = tfidf_builder.process(matrix["result"])
    query_matrix = matrix_builder.build(documents=[{
        "id" : "-1",
        "content": query,
        "tf": preprocessor.process(query)
    }])
    query_weight_list = {}
    for query_term, query_tf in query_matrix["result"].items():
        if query_term in document_weight_list["idf_list"]:
            if query_term not in query_weight_list:
                query_weight_list[query_term] = [document_weight_list["idf_list"][query_term] * query_tf[0]]
    rank_tool = VSM.VSMTool(matrix["map"])
    result = rank_tool.rank(query_weight_list, document_weight_list["tf_idf_list"])

    return {
        "matrix" : matrix,
        "query_matrix": query_matrix,
        "query_tfidf" : query_weight_list,
        "document_tfidf" : document_weight_list,
        "vsm_result" : result
    }