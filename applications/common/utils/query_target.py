

def query_target_from_ttd(drugname, disease_name):
    if (drugname == "") and (disease_name == ""):
        pass
    elif drugname == "":
        # 搜索疾病对应的靶点
        records = db.session.query(TTDTarget, TTDLinkTargetDisease)\
            .join(TTDTarget, TTDTarget.target_id==TTDLinkTargetDisease.target_id)\
            .filter(TTDLinkTargetDisease.indication.contains(disease_name))
        unipro_ids = list(set([record[0].unipro2_id for record in records.all() if record[0].unipro2_id]))
    elif disease_name == "":
        # 搜索药物对应的靶点
        records = db.session.query(TTDTarget, TTDLinkDrugTarget, TTDDrug)\
            .join(TTDTarget, TTDTarget.target_id==TTDLinkDrugTarget.target_id)\
            .join(TTDDrug, TTDDrug.drug_id==TTDLinkDrugTarget.drug_id)\
            .filter(TTDDrug.drugname.contains(drugname))
        unipro_ids = list(set([record[0].unipro2_id for record in records.all() if record[0].unipro2_id]))
    else:
        # 同时根据药物和疾病名称进行搜索对应的靶点
        records = db.session.query(TTDDrug, TTDTarget, TTDLinkDrugTarget, TTDLinkTargetDisease)\
                .join(TTDDrug, TTDDrug.drug_id==TTDLinkDrugTarget.drug_id)\
                .join(TTDTarget, TTDTarget.target_id==TTDLinkDrugTarget.target_id)\
                .join(TTDLinkTargetDisease, TTDTarget.target_id==TTDLinkTargetDisease.target_id)\
                .filter(TTDDrug.drugname.contains(drugname), 
                        TTDLinkTargetDisease.indication.contains(disease_name))
        unipro_ids = list(set([record[1].unipro2_id for record in records.all() if record[1].unipro2_id]))

    return records