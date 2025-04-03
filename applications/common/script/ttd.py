import datetime
import pandas as pd
import numpy as np
import json
import tqdm

from flask.cli import AppGroup

from applications.extensions import db
from applications.models import TTDDrug, TTDTarget, \
    TTDLinkDrugTarget, TTDLinkDrugDisease, TTDLinkTargetDisease


ttd_cli = AppGroup("ttd")


def init_ttd_drug():
    df = pd.read_json("./dockerdata/DB-TTD/parsed/ttd_drug.json", orient="records", lines=True)
    records = []
    for item in df.to_dict(orient="records"):
        records.append(TTDDrug(drug_id = item["DRUG__ID"], 
                               tradname = item["TRADNAME"],
                               drugcomp = item["DRUGCOMP"],
                               therclas = item["THERCLAS"],
                               drugtype = item["DRUGTYPE"],
                               druginch = item["DRUGINCH"],
                               druginke = item["DRUGINKE"],
                               drugsmil = item["DRUGSMIL"],
                               highstat = item["HIGHSTAT"],
                               compclas = item["COMPCLAS"],
                               drugname = item["DRUGNAME"],
                               d_fomula = item["D_FOMULA"],
                               pubchcid = item["PUBCHCID"],
                               casnumber = item["CASNUMBE"],
                               chebi_id = item["CHEBI_ID"]))

    db.session.add_all(records)
    db.session.commit()


def init_ttd_target():
    df = pd.read_json("./dockerdata/DB-TTD/parsed/ttd_target.json", orient="records", lines=True)
    records = []
    for item in df.to_dict(orient="records"):
        records.append(TTDTarget(target_id = item["TARGETID"],
                                 unipro_id = item["UNIPROID"],
                                 unipro2_id = item["unipro2_id"],
                                 targname = item["TARGNAME"],
                                 genename = item["GENENAME"],
                                 targtype = item["TARGTYPE"],
                                 bioclass = item["BIOCLASS"],
                                 ecnumber = item["ECNUMBER"]))

    db.session.add_all(records)
    db.session.commit()

def init_ttd_link_drug_target():
    df = pd.read_json("./dockerdata/DB-TTD/parsed/ttd_drug_target.json", orient="records", lines=True)
    records = []
    for item in df.to_dict(orient="records"):
        records.append(TTDLinkDrugTarget(target_id = item["TargetID"],
                                         drug_id = item["DrugID"],
                                         highest_status = item["Highest_status"],
                                         moa = item["MOA"]))

    db.session.add_all(records)
    db.session.commit()

def init_ttd_link_drug_disease():
    df = pd.read_json("./dockerdata/DB-TTD/parsed/ttd_drug_disease.json", orient="records", lines=True)
    records = []
    for item in df.to_dict(orient="records"):
        records.append(TTDLinkDrugDisease(drug_id = item["TTDDRUID"],
                                          drugname = item["DRUGNAME"],
                                          indication = item["Indication"],
                                          disease_entry = item["DiseaseEntry"],
                                          clinical_status = item["ClinicalStatus"]))

    db.session.add_all(records)
    db.session.commit()


def init_ttd_link_target_disease():
    df = pd.read_json("./dockerdata/DB-TTD/parsed/ttd_target_disease.json", orient="records", lines=True)
    records = []
    for item in df.to_dict(orient="records"):
        records.append(TTDLinkTargetDisease(target_id = item["TARGETID"],
                                            indication = item["Indication"],
                                            disease_entry = item["DiseaseEntry"],
                                            clinical_status = item["ClinicalStatus"]))

    db.session.add_all(records)
    db.session.commit()

@ttd_cli.command("init")
def init_all():
    print("TTDDrug 数据插入")
    init_ttd_drug()

    print("TTDTarget 数据插入")
    init_ttd_target()

    print("TTDLinkDrugTarget 数据插入")
    init_ttd_link_drug_target()

    print("TTDLinkDrugDisease 数据插入")
    init_ttd_link_drug_disease()

    print("TTDLinkTargetDisease 数据插入")
    init_ttd_link_target_disease()


@ttd_cli.command("drug_update")
def ttd_drug_update():
    df = pd.read_json("./dockerdata/DB-TTD/parsed/ttd_drug_disease.json", orient="records", lines=True)
    for item in df.to_dict(orient="records"):
        drug_id = item["TTDDRUID"]
        drugname = item["DRUGNAME"]
        if drugname:
            TTDDrug.query.filter(TTDDrug.drug_id==drug_id).update({"drugname": drugname})
    db.session.commit()
