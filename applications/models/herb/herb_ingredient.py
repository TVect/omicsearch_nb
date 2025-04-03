from applications.extensions import db


class HERBIngredient(db.Model):
    """
        {   
            'Ingredient_id': 'HBIN000001',
            'Ingredient_name': '01eanolic acid-3-0-β-D-xylopy-ranoside',
            'Alias': nan,
            'Ingredient_formula': 'C35H56O7',
            'Ingredient_Smile': 'CC1(CCC2(CCC3(C(=CCC4C3(CCC5C4(CCC(C5(C)C)OC6C(C(C(CO6)O)O)O)C)C)C2C1)C)C(=O)O)C',
            'Ingredient_weight': nan,
            'OB_score': nan,
            'CAS_id': nan,
            'SymMap_id': nan,
            'TCMID_id': '36493',
            'TCMSP_id': nan,
            'TCM-ID_id': nan,
            'PubChem_id': nan,
            'DrugBank_id': nan
        }
    """
    __tablename__ = 'herb_ingredient'

    ingredient_id           = db.Column(db.String(32), primary_key=True, comment="Ingredient_id")
    ingredient_name         = db.Column(db.String(64), comment="Ingredient_name")
    alias                   = db.Column(db.String(64), comment="Alias")
    ingredient_formula      = db.Column(db.String(64), comment="Ingredient_formula")
    ingredient_Smile        = db.Column(db.String(128), comment="Ingredient_Smile")
    ingredient_weight       = db.Column(db.String(32), comment="Ingredient_weight")
    ob_score                = db.Column(db.String(32), comment="OB_score")
    cas_id                  = db.Column(db.String(32), comment="CAS_id")
    symmap_id               = db.Column(db.String(32), comment="SymMap_id")
    tcmid_id                = db.Column(db.String(32), comment="TCMID_id")
    tcmsp_id                = db.Column(db.String(32), comment="TCMSP_id")
    tcm_id_id               = db.Column(db.String(32), comment="TCM-ID_id")
    pubchem_id              = db.Column(db.String(32), comment="PubChem_id")
    drugbank_id             = db.Column(db.String(32), comment="DrugBank_id")
