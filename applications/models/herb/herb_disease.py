from applications.extensions import db


class HERBDisease(db.Model):
    """
        {
            'Disease_id': 'HBDIS000001',
            'DisGENet_disease_id': 'C0000727',
            'Disease_name': 'Abdomen, Acute',
            'Disease_type': 'phenotype',
            'DiseaseClass_MeSH': 'C23',
            'DiseaseClassName_MeSH': 'Pathological Conditions, Signs and Symptoms',
            'HPO_ClassId': nan,
            'HPO_ClassName': nan,
            'DO_ClassId': nan,
            'DO_ClassName': nan,
            'UMLS_SemanticTypeId': 'T184',
            'UMLS_SemanticTypeName': 'Sign or Symptom'
        }
    """
    __tablename__ = 'herb_disease'

    disease_id              = db.Column(db.String(32), primary_key=True, comment="Disease_id")
    disgenet_disease_id     = db.Column(db.String(32), comment="DisGENet_disease_id")
    disease_name            = db.Column(db.String(64), comment="Disease_name")
    disease_type            = db.Column(db.String(64), comment="Disease_type")
    diseaseclass_mesh       = db.Column(db.String(128), comment="DiseaseClass_MeSH")
    diseaseclassname_mesh   = db.Column(db.String(128), comment="DiseaseClassName_MeSH")
    hpo_classid             = db.Column(db.String(32), comment="HPO_ClassId")
    hpo_classname           = db.Column(db.String(64), comment="HPO_ClassName")
    do_classid              = db.Column(db.String(64), comment="DO_ClassId")
    do_classname            = db.Column(db.String(64), comment="DO_ClassName")
    umls_semantictypeid     = db.Column(db.String(32), comment="UMLS_SemanticTypeId")
    umls_semantictypename   = db.Column(db.String(64), comment="UMLS_SemanticTypeName")
