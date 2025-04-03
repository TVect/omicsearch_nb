from applications.extensions import db

class TTDLinkDrugTarget(db.Model):
    """
        {
            'TargetID': 'T87024',
            'DrugID': 'D00RRU',
            'Highest_status': 'Approved',
            'MOA': 'Modulator'
        }
    """

    __tablename__ = 'ttd_link_drug_target'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    target_id = db.Column(db.String(32), comment="TARGETID")
    drug_id = db.Column(db.String(32), comment="DRUGID")
    highest_status = db.Column(db.String(32), comment="HighestStatus")
    moa = db.Column(db.String(32), comment="MOA")


class TTDLinkDrugDisease(db.Model):
    """
        {
            'TTDDRUID': 'DZB84T',
            'DRUGNAME': 'Maralixibat',
            'Indication': 'Pruritus',
            'DiseaseEntry': 'ICD-11: EC90',
            'ClinicalStatus': 'Approved'
        }
    """

    __tablename__ = 'ttd_link_drug_disease'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    drug_id = db.Column(db.String(32), comment="DRUGID")
    drugname = db.Column(db.String(128), comment="DRUGNAME")
    indication = db.Column(db.String(128), comment="Indication")
    disease_entry = db.Column(db.String(32), comment="DiseaseEntry")
    clinical_status = db.Column(db.String(32), comment="ClinicalStatus")


class TTDLinkTargetDisease(db.Model):
    """
        {
            'TARGETID': 'T00033',
            'TARGNAME': 'Transforming growth factor alpha (TGFA)',
            'Indication': 'Chronic kidney disease',
            'DiseaseEntry': '[ICD-11: GB61]',
            'ClinicalStatus': 'Phase 1/2'
        }
    """

    __tablename__ = 'ttd_link_target_disease'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    target_id = db.Column(db.String(32), comment="TARGETID")
    indication = db.Column(db.String(128), comment="Indication")
    disease_entry = db.Column(db.String(32), comment="DiseaseEntry")
    clinical_status = db.Column(db.String(32), comment="ClinicalStatus")

