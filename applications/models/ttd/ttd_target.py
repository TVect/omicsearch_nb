from applications.extensions import db


class TTDTarget(db.Model):
    """
        {
            'TARGETID': 'T47101',
            'FORMERID': 'TTDC00024',
            'UNIPROID': 'FGFR1_HUMAN',
            'TARGNAME': 'Fibroblast growth factor receptor 1 (FGFR1)',
            'GENENAME': 'FGFR1',
            'TARGTYPE': 'Successful',
            'SYNONYMS': 'c-fgr; bFGF-R-1; bFGF-R; N-sam; HBGFR; Fms-like tyrosine kinase 2; FLT2; FLT-2; FLG; FGFR-1; FGFBR; CEK; CD331 antigen; CD331; Basic fibroblast growth factor receptor 1; BFGFR',
            'PDBSTRUC': '6MZW; 6MZQ; 6C1O; 6C1C; 6C1B',
            'BIOCLASS': 'Kinase',
            'ECNUMBER': 'EC 2.7.10.1'
        }
    """

    __tablename__ = 'ttd_target'

    target_id = db.Column(db.String(32), primary_key=True, comment="TARGETID")
    unipro_id = db.Column(db.String(64), comment="UNIPROID")
    unipro2_id = db.Column(db.String(64), comment="FORMERID")
    targname = db.Column(db.String(128), comment="TARGNAME")
    genename = db.Column(db.String(32), comment="GENENAME")
    targtype = db.Column(db.String(32), comment="TARGTYPE")
    bioclass = db.Column(db.String(32), comment="BIOCLASS")
    ecnumber = db.Column(db.String(32), comment="ECNUMBER")
