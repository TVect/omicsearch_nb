import datetime
import pandas as pd
import numpy as np
import json
import tqdm

from flask.cli import AppGroup

from applications.extensions import db
from applications.models import HERBHerb, HERBIngredient, HERBTarget, HERBDisease
# from applications.models import herblink_herb_ingredient, herblink_herb_target, herblink_herb_disease, \
#     herblink_ingredient_target, herblink_ingredient_disease, herblink_target_disease
from applications.models import HERBLinkHerbIngredient, HERBLinkHerbTarget, HERBLinkHerbDisease, \
    HERBLinkIngredientTarget, HERBLinkIngredientDisease, HERBLinkTargetDisease, HERBLinkReference


herb_cli = AppGroup("herb")

def init_herb():
    df = pd.read_csv("./dockerdata/DB-HERB/downloaded/HERB_herb_info.txt", sep="\t", chunksize=1000)
    for chunk in df:
        records = []
        for item in chunk.to_dict(orient="records"):
            records.append(
                HERBHerb(
                    herb_id                     = item["Herb_"],
                    herb_pinyin_name            = item["Herb_pinyin_name"],
                    herb_cn_name                = item["Herb_cn_name"],
                    herb_en_name                = item["Herb_en_name"],
                    herb_latin_name             = item["Herb_latin_name"],
                    properties                  = item["Properties"],
                    meridians                   = item["Meridians"],
                    usepart                     = item["UsePart"],
                    function                    = item["Function"],
                    indication                  = item["Indication"],
                    toxicity                    = item["Toxicity"],
                    clinical_manifestations     = item["Clinical_manifestations"],
                    therapeutic_en_class        = item["Therapeutic_en_class"],
                    therapeutic_cn_class        = item["Therapeutic_cn_class"],
                    tcmid_id                   = item["TCMID_id"],
                    tcm_id_id                   = item["TCM_ID_id"],
                    symmap_id                   = item["SymMap_id"],
                    tcmsp_id                    = item["TCMSP_id"],
                )
            )
        db.session.add_all(records)
        db.session.commit()


def init_ingredient():
    df = pd.read_csv(
        "./dockerdata/DB-HERB/downloaded/HERB_ingredient_info.txt",
        sep="\t", index_col=False, chunksize=1000)
    for chunk in df:
        records = []
        for item in chunk.to_dict(orient="records"):
            records.append(
                HERBIngredient(
                    ingredient_id           = item["Ingredient_id"],
                    ingredient_name         = item["Ingredient_name"],
                    alias                   = item["Alias"],
                    ingredient_formula      = item["Ingredient_formula"],
                    ingredient_Smile        = item["Ingredient_Smile"],
                    ingredient_weight       = item["Ingredient_weight"],
                    ob_score                = item["OB_score"],
                    cas_id                  = item["CAS_id"],
                    symmap_id               = item["SymMap_id"],
                    tcmid_id                = item["TCMID_id"],
                    tcmsp_id                = item["TCMSP_id"],
                    tcm_id_id               = item["TCM-ID_id"],
                    pubchem_id              = item["PubChem_id"],
                    drugbank_id             = item["DrugBank_id"],
                )
            )
        db.session.add_all(records)
        db.session.commit()


def init_target():
    df = pd.read_csv("./dockerdata/DB-HERB/downloaded/HERB_target_info.txt", sep="\t", chunksize=1000)
    for chunk in df:
        records = []
        for item in chunk.to_dict(orient="records"):
            records.append(
                HERBTarget(
                    target_id           = item["Target_id"],
                    tax_id              = item["Tax_id"],
                    gene_id             = item["Gene_id"],
                    gene_name           = item["Gene_name"],
                    gene_alias          = item["Gene_alias"],
                    db_xrefs            = item["Db_xrefs"],
                    chromosome          = item["Chromosome"],
                    map_location        = item["Map_location"],
                    description         = item["Description"],
                    type_of_gene        = item["Type_of_gene"],
                    ttd_target_id       = item["TTD_target_id"],
                    ttd_target_type     = item["TTD_target_type"],
                )
            )
        db.session.add_all(records)
        db.session.commit()


def init_disease():
    df = pd.read_csv("./dockerdata/DB-HERB/downloaded/HERB_disease_info.txt", sep="\t", chunksize=1000)
    for chunk in df:
        records = []
        for item in chunk.to_dict(orient="records"):
            records.append(
                HERBDisease(
                    disease_id              = item["Disease_id"],
                    disgenet_disease_id     = item["DisGENet_disease_id"],
                    disease_name            = item["Disease_name"],
                    disease_type            = item["Disease_type"],
                    diseaseclass_mesh       = item["DiseaseClass_MeSH"],
                    diseaseclassname_mesh   = item["DiseaseClassName_MeSH"],
                    hpo_classid             = item["HPO_ClassId"],
                    hpo_classname           = item["HPO_ClassName"],
                    do_classid              = item["DO_ClassId"],
                    do_classname            = item["DO_ClassName"],
                    umls_semantictypeid     = item["UMLS_SemanticTypeId"],
                    umls_semantictypename   = item["UMLS_SemanticTypeName"],
                )
            )
        db.session.add_all(records)
        db.session.commit()



def init_link_herb():
    with open("./dockerdata/DB-HERB/spider/saved/herb_details.jsonl") as fr:
        for line in fr:
            records = []
            record = json.loads(line)
            herb_id = record["keyid"]
            ingredient_ids = [item[0]["title"] for item in record["detail"]["herb_ingredient"][1:]]
            target_ids = [item[0]["title"] for item in record["detail"]["herb_target"][1:]]
            disease_ids = [item[0]["title"] for item in record["detail"]["herb_disease"][1:]]
            records.extend(
                [HERBLinkHerbIngredient(herb_id=herb_id, ingredient_id=idx) for idx in ingredient_ids]
            )
            records.extend(
                [HERBLinkHerbTarget(herb_id=herb_id, target_id=idx) for idx in target_ids]
            )
            records.extend(
                [HERBLinkHerbDisease(herb_id=herb_id, disease_id=idx) for idx in disease_ids]
            )
            if len(records) > 0:
                db.session.add_all(records)
                db.session.commit()


def init_link_ingredient():
    with open("./dockerdata/DB-HERB/spider/saved/ingredient_details.jsonl") as fr:
        for line in tqdm.tqdm(fr):
            records = []
            record = json.loads(line)
            ingredient_id = record["keyid"]
            target_ids = [item[0]["title"] for item in record["detail"]["ingredient_target"][1:]]
            disease_ids = [item[0]["title"] for item in record["detail"]["ingredient_disease"][1:]]
            records.extend(
                [HERBLinkIngredientTarget(ingredient_id=ingredient_id, target_id=idx) for idx in target_ids]
            )
            records.extend(
                [HERBLinkIngredientDisease(ingredient_id=ingredient_id, disease_id=idx) for idx in disease_ids]
            )
            if len(records) > 0:
                db.session.add_all(records)
                db.session.commit()


def init_link_target():
    with open("./dockerdata/DB-HERB/spider/saved/target_details.jsonl") as fr:
        for line in tqdm.tqdm(fr):
            records = []
            record = json.loads(line)
            target_id = record["keyid"]
            disease_ids = [item[0]["title"] for item in record["detail"]["target_disease"][1:]]
            records.extend(
                [HERBLinkTargetDisease(target_id=target_id, disease_id=idx) for idx in disease_ids]
            )
            if len(records) > 0:
                db.session.add_all(records)
                db.session.commit()



@herb_cli.command("init_entity")
def init_entity():
    init_herb()
    init_ingredient()
    init_target()
    init_disease()


@herb_cli.command("init_link")
def init_link():
    init_link_herb()
    init_link_ingredient()
    init_link_target()

@herb_cli.command("update")
def update():
    df = pd.read_csv("dockerdata/DB-HERB/downloaded/target_idmapping_2024_11_11.tsv", sep="\t")
    id_mapping = dict(df[["From", "Entry"]].values)
    count0, count1 = 0, 0
    for record in HERBTarget.query.all():
        xrefs = record.db_xrefs      # 'OMIM:138670; HGNC:HGNC:5; Ensembl:ENSG00000121410'
        ensembl_refs = list(filter(lambda item: "Ensembl" in item, xrefs.split(";")))
        if len(ensembl_refs) > 0:
            ensembl_ref = ensembl_refs[0][9:]
            unipro_id = id_mapping.get(ensembl_ref, None)
            if unipro_id is not None:
                count1 += 1
                record.unipro_id = unipro_id
            else:
                count0 += 1
    print(f"counts: count0={count0}, count1={count1}")
    db.session.commit()

@herb_cli.command("add_ref")
def add_ref():
    with open("./dockerdata/DB-HERB/spider/saved/target_details.jsonl") as fr:
        records = []
        for line in tqdm.tqdm(fr):
            record = json.loads(line)
            target_id = record["keyid"]
            for item in record["detail"]["paper_target"][1:]:
                if item[-1] == "Herb":
                    records.append(
                        HERBLinkReference(target_id=target_id, herb_id=item[1], pubmed_id=item[2], herb_name=item[3])
                    )
                elif item[-1] == "Ingredient":
                    records.append(
                        HERBLinkReference(target_id=target_id, ingredient_id=item[1], pubmed_id=item[2], ingredient_name=item[3])
                    )

        db.session.add_all(records)
        db.session.commit()


@herb_cli.command("update01")
def update01():
    for record in HERBLinkHerbTarget.query.all():
        record.herb_cn_name = record.herb.herb_cn_name
    db.session.commit()

    for record in HERBLinkTargetDisease.query.all():
        record.disease_name = record.disease.disease_name
    db.session.commit()
