from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("./test", schema)

writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b", content=u"The second one is even more interesting!")
writer.add_document(title=u"third document", path=u"/c", content=u"The third one is even more interesting!")
writer.add_document(title=u"sec document", path=u"/d", content=u"The sec one is even more interesting!")
writer.commit()

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("sec*")
    for result in searcher.search(query):
        print(result)
