class InvertedIndexTool():
    def __init__(self) -> None:
        pass

    def __get_term_list(self, documents: list) -> list:
        terms = []
        for document in documents :
            for tf in document["tf"]:
                if tf[0] not in terms :
                    terms.append(tf[0])
        
        return terms
    
    def rank(self, query: list, matrix: dict):
        result = matrix
        total = []
        for q in query :
            if q in result :
                for index, tf in enumerate(result[q]):
                    if index < len(total):
                        total[index] += tf
                    else :
                        total.append(tf)
        return total

    
    def build(self, documents: list) -> list:
        terms = self.__get_term_list(documents=documents)
        result = {term : [] for term in terms}

        self.map = {}
        for index, document in enumerate(documents):
            self.map[index] = document["name"]

        for term in terms :
            for document in documents :
                if any(term in document_term for document_term in document["tf"]):
                    result[term].append([document_tf[1] for document_tf in document["tf"] if document_tf[0] == term][0])
                else :
                    result[term].append(0)
        
        self.matrix = result

        return {"map" : self.map, "result" : result}