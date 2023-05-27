import preprocess

class IncidenceMatrixTool : 
    def __init__(self) -> None:
        self.preprocessor = preprocess.Preprocessor()

    def __get_term_list(self, documents: list) -> list:
        terms = []
        for document in documents :
            for tf in document["tf"]:
                if tf[0] not in terms :
                    terms.append(tf[0])
        
        return terms
    
    def build(self, documents: list) -> dict:
        terms = self.__get_term_list(documents=documents)
        result = {term : [] for term in terms}

        self.map = {}
        for index, document in enumerate(documents):
            self.map[index] = document["id"]

        for term in terms :
            for document in documents :
                result[term].append(1 if any(term in document_term for document_term in document["tf"]) else 0)

        self.matrix = result
        return {"map" : self.map, "result" : result}
    
    def rank(self, query: str) -> dict:
        tokens = self.preprocessor.process(query)
        selected_terms = []
        for token in tokens:
            if token[0] in self.matrix:
                selected_terms.append(self.matrix[token[0]])
        
        result = []
        for document_tfs in zip(*selected_terms):
            value = 1
            for document_tf in document_tfs:
                value = 1 if document_tf and value else 0
            result.append(value)
        
        return {"map" : self.map, "result" : result}

    def build_and_rank(self, query: str, documents: list) -> dict:
        self.build(documents=documents)
        return self.rank(query=query)