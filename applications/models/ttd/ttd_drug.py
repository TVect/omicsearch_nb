from applications.extensions import db


class TTDDrug(db.Model):

    """
        {
            'DRUG__ID': 'D00UZR',
            'TRADNAME': 'Ibrance',
            'DRUGCOMP': 'Onyx Pharmaceuticals; Pfizer',
            'THERCLAS': 'Anticancer Agents',
            'DRUGTYPE': 'Small molecular drug',
            'DRUGINCH': '1S/C24H29N7O2/c1-15-19-14-27-24(28-20-8-7-18(13-26-20)30-11-9-25-10-12-30)29-22(19)31(17-5-3-4-6-17)23(33)21(15)16(2)32/h7-8,13-14,17,25H,3-6,9-12H2,1-2H3,(H,26,27,28,29)',
            'DRUGINKE': 'AHJRHEGDXFFMBM-UHFFFAOYSA-N',
            'DRUGSMIL': 'CC1=C(C(=O)N(C2=NC(=NC=C12)NC3=NC=C(C=C3)N4CCNCC4)C5CCCC5)C(=O)C',
            'HIGHSTAT': 'Approved',
            'COMPCLAS': nan,
            'TTDDRUID': 'D00UZR',
            'DRUGNAME': 'Palbociclib',
            'D_FOMULA': 'C24H29N7O2',
            'PUBCHCID': '5330286',
            'CASNUMBE': 'CAS 571190-30-2',
            'CHEBI_ID': 'CHEBI:85993'
        }
    """

    __tablename__ = 'ttd_drug'


    drug_id = db.Column(db.String(32), primary_key=True, comment="DRUG__ID")
    tradname = db.Column(db.String(128), comment="TRADNAME")
    drugcomp = db.Column(db.String(128), comment="DRUGCOMP")
    therclas = db.Column(db.String(128), comment="THERCLAS")
    drugtype = db.Column(db.String(32), comment="DRUGTYPE")
    druginch = db.Column(db.String(128), comment="DRUGINCH")
    druginke = db.Column(db.String(128), comment="DRUGINKE")
    drugsmil = db.Column(db.String(128), comment="DRUGSMIL")
    highstat = db.Column(db.String(32), comment="HIGHSTAT")
    compclas = db.Column(db.String(128), comment="COMPCLAS")

    drugname = db.Column(db.String(128), comment="DRUGNAME")
    d_fomula = db.Column(db.String(128), comment="D_FOMULA")
    pubchcid = db.Column(db.String(32), comment="PUBCHCID")
    casnumber = db.Column(db.String(32), comment="CASNUMBE")
    chebi_id = db.Column(db.String(32), comment="CHEBI_ID")
