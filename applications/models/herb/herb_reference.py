from applications.extensions import db


# class HERBReference(db.Model):

#     __tablename__ = 'herb_reference'

#     reference_id            = db.Column(db.String(32), primary_key=True, comment="Reference_id")
#     pubmed_id               = db.Column(db.String(32), comment="PubMed_id")
#     reference_title         = db.Column(db.String(512), comment="Reference_title")
#     reference_abstract      = db.Column(db.Text(), comment="Reference_abstract")
#     reference_journal       = db.Column(db.String(64), comment="Reference_journal")
#     experiment_subject      = db.Column(db.String(32), comment="Experiment_subject")
#     experiment_type         = db.Column(db.String(32), comment="Experiment_type")
