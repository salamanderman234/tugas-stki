import InvertedIndexMatrix
import IncidenceMatrix
import preprocess
import TFIDF
import VSM

dummy2 = [
    {"id" : 1,"name":"ad-finem", "content" : "Shipment of gold damaged in a fire"},
    {"id" : 2,"name":"ad-finem1", "content" : "Delivery of silver arrived in a silver truck"},
    {"id" : 3,"name":"ad-finem2", "content" : "Shipment of gold arrived in a truck"},
]

preprocessor = preprocess.Preprocessor()
matrix_builder = InvertedIndexMatrix.InvertedIndexTool()
weighting_tool = TFIDF.TFIDFTool()

cleaned_document = []
for document in dummy2:
    cleaned_document.append({
        "id" : document["id"],
        "name": document["name"],
        "content": document["content"],
        "tf": preprocessor.process(document["content"])
    })
matrix = matrix_builder.build(documents=cleaned_document)
document_weight_list = weighting_tool.process(matrix["result"])

query = "gold silver truck"
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
print(rank_tool.rank(query_weight_list, document_weight_list["tf_idf_list"]))

# print(matrix)