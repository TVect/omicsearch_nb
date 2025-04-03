from applications.extensions import db


class HERBHerb(db.Model):
    __tablename__ = 'herb_herb'

    herb_id                     = db.Column(db.String(32), primary_key=True, comment="Herb_")
    herb_pinyin_name            = db.Column(db.String(64), comment="Herb_pinyin_name")
    herb_cn_name                = db.Column(db.String(64), comment="Herb_cn_name")
    herb_en_name                = db.Column(db.String(64), comment="Herb_en_name")
    herb_latin_name             = db.Column(db.String(64), comment="Herb_latin_name")
    properties                  = db.Column(db.String(128), comment="Properties")
    meridians                   = db.Column(db.String(128), comment="Meridians")
    usepart                     = db.Column(db.String(128), comment="UsePart")
    function                    = db.Column(db.String(128), comment="Function")
    indication                  = db.Column(db.String(128), comment="Indication")
    toxicity                    = db.Column(db.String(128), comment="Toxicity")
    clinical_manifestations     = db.Column(db.String(128), comment="Clinical_manifestations")
    therapeutic_en_class        = db.Column(db.String(128), comment="Therapeutic_en_class")
    therapeutic_cn_class        = db.Column(db.String(128), comment="Therapeutic_cn_class")
    tcmid_id                   = db.Column(db.String(32), comment="TCMID_id")
    tcm_id_id                   = db.Column(db.String(32), comment="TCM_ID_id")
    symmap_id                   = db.Column(db.String(32), comment="SymMap_id")
    tcmsp_id                    = db.Column(db.String(32), comment="TCMSP_id")
