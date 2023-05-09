from math import log10

class TFIDFTool :
    def __init__(self) -> None:
        pass
        
    def calculate_weight(self ,documents: list, lang: str = "eng") -> map:
        documents_container = []

        df = {}
        idf = {}

        for document in documents :
            id = document["id"]
            content = document["content"]
            title = document["name"]
            terms_dist = document["term_dist"]

            for term in terms_dist:
                if term["term"] in df:
                    df[term["term"]] += 1
                else:
                    df[term["term"]] = 1

            new = {
                "id" : id,
                "name": title,
                "content" : content,
                "terms_dist": terms_dist
            }

            documents_container.append(new)
        
        documents_count = len(documents_container)
        for term in df:
            df[term] = documents_count / df[term]
            idf[term] = log10(df[term])
            for index,document in enumerate(documents_container):
                term_dist = list(filter(lambda term_dist: term_dist['term'] == term, documents_container[index]["terms_dist"]))
                # term_dist = next(item for item in documents_container[index]["terms_dist"] if item["term"] == term)
                if "tf-idf" in documents_container[index] and len(term_dist) == 1:
                    documents_container[index]["tf-idf"][term] =  term_dist[0]["freq"] * idf[term]
                elif len(term_dist) == 1:
                    documents_container[index]["tf-idf"] = { term :  term_dist[0]["freq"] * idf[term] }

        result = {
            "idf_list" : idf,
            "documents": documents_container
        }

        return result
