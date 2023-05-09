from math import pow, sqrt

class VSMTool :
    def __init__(self) -> None:
        pass

    # calculate vector
    def __calculate_vector(self, terms_tf_idf: list) -> float :
        total = 0
        for term in terms_tf_idf:
            total += pow(term, 2)
        return sqrt(total)
    
    # calculate dot prodcut
    def __calculate_dot_product(self, query_tf_idf: map, document_terms_tf_idf: map) -> float :
        total = 0
        for term in document_terms_tf_idf:
            if term in query_tf_idf:
                total += pow(document_terms_tf_idf[term], 1) * pow(query_tf_idf[term], 1)
        return total
    
    # sort result
    def __sort(self, documents: list):
        return sorted(documents, key=lambda document: document['similarity'], reverse=True) 

    # calculate and rank
    def rank(self, documents: list, idf_list: map ,queries: list) -> list:
        tf_idf_query = {}

        for query in queries :
            if query["term"] in idf_list :
                tf_idf_query[query["term"]] = idf_list[query["term"]] * query["freq"]
        
        query_vector = self.__calculate_vector([tf_idf_query[term] for term in tf_idf_query])
        final_result = []
        if query_vector > 0 :
            for index, document in enumerate(documents):
                document_vector = self.__calculate_vector([document["tf-idf"][term] for term in document["tf-idf"]])
                documents[index]["vector"] = document_vector
                documents[index]["dot_product"] = self.__calculate_dot_product(tf_idf_query, documents[index]["tf-idf"])
                documents[index]["similarity"] = documents[index]["dot_product"] / (query_vector*documents[index]["vector"])

            final_result = [document for document in documents if document["similarity"] > 0]
            

        result = self.__sort(final_result)
        return result
