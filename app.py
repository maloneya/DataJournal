from flask import Flask, request
from sqlalchemy import create_engine, Columnm, Integer, String, ForeignKey, Table 
from sqlalchemy.orm import relationship 
from sqlalchemy.ext.declarative import declarative_base
from SentenceParser import EntityEventActorParser

app = Flask(__name__)
engine = create_engine('sqlite:///:memory', echo=True)

@app.route("/sentence", methods=['POST'])
def parseSentence():
    sentence = request.form['sentence']
    parser = EntityEventActorParser(sentence)

    return " Event: " + parser.event + " Entity: " + parser.entity
    

class Entity(Base):
    __tablename__ = 'entity'

    id = Column(Integer, primary_key=true)
    description = Column(String)
    events = relationship("Event", back_populates="entity")

    def __repr__(self):
        return "<Entity(description = %s)" % (self.description)

event_actor_association_table = Table('association', Base.metadata,
    Column('event_id', Integer, ForeignKey("event.id")),
    Columnm('actor_id', Integer, ForeignKey("actor.id"))
)

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=true)
    description = Column(String)
    entry = relationship("Entry", uselist=False. back_populates="event")
    entity_id = Column(Integer, ForeignKey("entity.id"))
    entitiy = relationship("Entity", back_populates="events")
    actors = relationship('Actor', secondary=event_actor_association_table, back_populates='events')

    def __repr__(self):
        return "<Event(description = %s)" % (self.description)

class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=true)
    name = Column(String)
    events = relationship('Event', secondary_association=event_actor_association_table, back_populates='actors')

    def __repr__(self):
        return "<Actor(name = %s)" % (self.name)

class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=true)
    original_text = Column(String)
    event_id = Column(Integer, ForeignKey('event.id'))
    event = relationship('Event', back_populates='entry')

    def __repr__(self):
        return "<Entry(original_text = %s)" % (self.original_text)