from web import DATABASE_URI
from sqlalchemy import create_engine
from web import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000))
    terms_dists = db.relationship("TermsDistribution", backref="document", lazy=True)

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    idf = db.Column(db.Integer, default=0)
    terms_dists = db.relationship("TermsDistribution", backref="term", lazy=True)

class TermsDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey("term.id"), nullable=False)
    freq = db.Column(db.Integer, nullable=False)

class Deconstructor:
    def __document_deconstruct(self, object: Document) -> map :
        terms_dists = []
        for term_dist in object.terms_dists :
            terms_dists.append(self.__terms_dists_deconstruct(term_dist))
        document = {
            "id": object.id,
            "name": object.name,
            "content": object.content,
            'terms_dists': terms_dists
        }
        return document
    
    def __term_deconstruct(self, object: Term) -> map :
        terms_dists = []
        for term_dist in object.terms_dists :
            terms_dists.append(self.__terms_dists_deconstruct(term_dist))

        return {
            "id": object.id,
            "name": object.name,
            "idf": object.idf,
            "terms_dists": terms_dists
        }
    
    def __terms_dists_deconstruct(self, object: TermsDistribution) -> map:
        document = {
            "id": object.document.id,
            "name": object.document.name,
            "content": object.document.content,
        }
        term = {
            "id": object.term.id,
            "name": object.term.name,
            "idf": object.term.idf,
        }

        return {
            "id": object.id,
            "document": document,
            "term": term,
        }

    def deconstruct(self, object: any) -> map:
        if isinstance(object, Document):
            return self.__document_deconstruct(object)
        
        elif isinstance(object, Term):
            return self.__term_deconstruct(object)

        elif isinstance(object, TermsDistribution):
            return self.__terms_dists_deconstruct(object)
        
        return {}
    
    def bulk_deconstruct(self, objects: list) -> list :
        result = []
        for object in objects:
            result.append(self.deconstruct(object))
        return result

def migrate():
    engine = create_engine(DATABASE_URI, echo=True)
    db.metadata.create_all(engine)