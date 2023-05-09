from tools.TFIDF import TFIDFTool
from tools.VSM import VSMTool
from tools.preprocess import Preprocessor

query = "gold is silver in Truck."
dummy = [
    {"id" : 1, "content" : "ya ubah kurang lebih gitu, soalnya patch sekarang kan gede banget bukan cuman item sama hero. Map berubah jauh, play style otomatis harus berubah juga"},
    {"id" : 2, "content" : "ubah bukan underestimate sama bang randy. tapi balik lagi, cocok nggak sama 4 lainnya ? percuma datang jauh ke SA kalo 4 lainnya ga cocok sama 1 orang ini"},
    {"id" : 3, "content" : "Q ubah tolong jangan blunder lg pls...agresivitas tolong ditahan...respek Ursa-nya Yaturu"},
    {"id" : 4, "content" : "tsm mengubah problemnya timado lama bet onlinenya, butuh carry yang bisa winning lane kek dreamocel... makanya kek 4 lainnya kureng karena dikorbanin buat timado"},
]

dummy2 = [
    {"id" : 1,"name":"ad-finem", "content" : "Shipment of gold damaged in a fire"},
    {"id" : 2,"name":"ad-finem1", "content" : "Delivery of silver arrived in a silver truck"},
    {"id" : 3,"name":"ad-finem2", "content" : "Shipment of gold arrived in a truck"},
    {"id" : 4,"name":"ad-finem3", "content" : "big chungus gold"},
]

preprocessor = Preprocessor()
cleaned_document = []
for document in dummy2:
    cleaned_document.append({
        "id" : document["id"],
        "name": document["name"],
        "content": document["content"],
        "term_dist": preprocessor.process(document["content"])
    })

tool = TFIDFTool()
result = tool.calculate_weight(cleaned_document)
ranking_tool = VSMTool()
rank_result = ranking_tool.rank(result["documents"], result["idf_list"], preprocessor.process(query))
print("Query :", query)
print("Result : ", rank_result)

