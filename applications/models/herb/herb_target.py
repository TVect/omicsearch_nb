from applications.extensions import db


class HERBTarget(db.Model):
    """
        {   
            'Target_id': 'HBTAR000001',
            'Tax_id': 9606,
            'Gene_id': 1,
            'Gene_name': 'A1BG',
            'Gene_alias': 'A1B; ABG; GAB; HYST2477',
            'Db_xrefs': 'OMIM:138670; HGNC:HGNC:5; Ensembl:ENSG00000121410',
            'Chromosome': '19',
            'Map_location': '19q13.43',
            'Description': 'alpha-1-B glycoprotein',
            'Type_of_gene': 'protein-coding',
            'TTD_target_id': nan,
            'TTD_target_type': '/'
        }
    """
    __tablename__ = 'herb_target'

    target_id           = db.Column(db.String(32), primary_key=True, comment="Target_id")
    tax_id              = db.Column(db.String(32), comment="Tax_id")
    gene_id             = db.Column(db.String(32), comment="Gene_id")
    gene_name           = db.Column(db.String(64), comment="Gene_name")
    gene_alias          = db.Column(db.String(128), comment="Gene_alias")
    db_xrefs            = db.Column(db.String(128), comment="Db_xrefs")
    unipro_id           = db.Column(db.String(64), comment="Uniprot_id")
    chromosome          = db.Column(db.String(32), comment="Chromosome")
    map_location        = db.Column(db.String(64), comment="Map_location")
    description         = db.Column(db.String(64), comment="Description")
    type_of_gene        = db.Column(db.String(64), comment="Type_of_gene")
    ttd_target_id       = db.Column(db.String(32), comment="TTD_target_id")
    ttd_target_type     = db.Column(db.String(64), comment="TCM-TTD_target_type")
