from math import pow, sqrt

class VSMTool():
    def __init__(self, map: dict) -> None:
        self.map = map

    def __calculate_vector(self, term_tfidf_list: dict) -> dict:
        tfidf_pow = {}
        vector_list = []
        for term, tfidf_list in term_tfidf_list.items():
            for index, tfidf in enumerate(tfidf_list):
                value = pow(tfidf, 2)
                if len(vector_list) >= index + 1:
                    vector_list[index] += value
                else:
                    vector_list.append(value)

                if term in tfidf_pow:
                    tfidf_pow[term].append(value)
                else:
                    tfidf_pow[term] = [value]

        for index, document_vector in enumerate(vector_list):
            vector_list[index] = sqrt(document_vector)
        
        return {
            "tfidf_pow" : tfidf_pow,
            "vector" : vector_list
        }
    
    def __calculate_dot_product(self, query_tfidf_pows: dict, documents_tfidf_pows: dict) -> dict:
        query_time_document = {}
        for term, query_pow in query_tfidf_pows.items():
            if term in documents_tfidf_pows:
                for document_pow in documents_tfidf_pows[term]:
                    value = document_pow*query_pow[0]
                    if term in query_time_document:
                        query_time_document[term].append(value)
                    else:
                        query_time_document[term] = [value]
    
        sum_query_time_document = []
        for key, row in query_time_document.items():
            for index, value in enumerate(row):
                if len(sum_query_time_document) >= index + 1:
                    sum_query_time_document[index] += value
                else:
                    sum_query_time_document.append(value)

        return {
            "query_times_document" : query_time_document,
            "dot_product_list" : sum_query_time_document
        }

    def __calculate_cosine(self, query_vector: float, documents_vector: list, qtd: list) -> list:
        result = {}
        index = 0
        for document_vector, document_qtd in zip(documents_vector, qtd):
            value = 0
            if query_vector*document_vector != 0 and document_qtd != 0:
                value = document_qtd / (query_vector*document_vector)
            result[self.map[index]] = value
            index += 1
        
        return result


    def rank(self, queries_tfidf: dict, documents_tfidf: dict) -> dict:
        filter_documents_tfidf = {}
        for term in queries_tfidf:
            if term in documents_tfidf:
                filter_documents_tfidf[term] = documents_tfidf[term]

        documents_vector = self.__calculate_vector(filter_documents_tfidf)
        query_vector = self.__calculate_vector(queries_tfidf)

        documents_dot_product = self.__calculate_dot_product(query_vector["tfidf_pow"], documents_vector["tfidf_pow"])
        result = {}
        if len(query_vector["vector"]) > 0:
            result = self.__calculate_cosine(query_vector["vector"][0], documents_vector["vector"], documents_dot_product["dot_product_list"])

        sorted_result = {key: value for key, value in sorted(result.items(), key=lambda item: item[1], reverse=True)} 
        return {
            "documents_vector" : documents_vector,
            "query_vector" : query_vector,
            "documents_dot_product" : documents_dot_product,
            "result" : sorted_result
        }