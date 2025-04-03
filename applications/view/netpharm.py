from flask import Blueprint, render_template, request, jsonify, current_app

from applications.extensions import db
from applications.models import HERBHerb, HERBIngredient, HERBTarget, HERBDisease, \
    HERBLinkHerbDisease, HERBLinkHerbIngredient, HERBLinkHerbTarget, \
    HERBLinkIngredientTarget, HERBLinkIngredientDisease, HERBLinkTargetDisease, HERBLinkReference
from applications.models import TTDDrug, TTDTarget, \
    TTDLinkDrugDisease, TTDLinkDrugTarget, TTDLinkTargetDisease

netpharm_bp = Blueprint('netpharm', __name__, url_prefix='/netpharm')

@netpharm_bp.get('/')
def main():
    return render_template('netpharm/main.html')

@netpharm_bp.get('/herb/target_detail/<target_id>')
def herb_target_detail(target_id):
    target = HERBTarget.query.filter_by(target_id=target_id).first()
    target_info = {
        "target_id": target.target_id,
        "gene_name": target.gene_name,
        "gene_alias": target.gene_alias,
        "db_xrefs": target.db_xrefs,
        "unipro_id": target.unipro_id,
        "tax_id": target.tax_id,
        "chromosome": target.chromosome,
        "map_location": target.map_location,
        "description": target.description,
        "type_of_gene": target.type_of_gene,
        "ttd_target_id": target.ttd_target_id,
        "ttd_target_type": target.ttd_target_type,
        "reference": [],
        "dbname": "herb"
    }

    reference = HERBLinkReference.query.filter_by(target_id=target_id).all()
    target_info["reference"] = [
        {
            "herb_name": record.herb_name, 
            "ingredient_name": record.ingredient_name,
            "pubmed_id": record.pubmed_id
        }
        for record in reference
    ]
    return render_template('netpharm/target_detail.html', target_info=target_info)


@netpharm_bp.route("/herb/search", methods=["POST", "GET"])
def herb_search_target():
    """
        搜索查找 药材/药物/疾病 对应的靶点信息
    """
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    drugname = request.args.get("drugname", "").strip()
    disease_name = request.args.get("disease_name", "").strip()

    response_object = {"code": 0, "msg": "", "count": 0, "data": []}

    if (drugname == "") and (disease_name == ""):
        pass
    elif drugname == "":
        # 搜索疾病对应的靶点
        # records = db.session.query(HERBTarget, HERBLinkTargetDisease, HERBDisease)\
        #     .join(HERBTarget).join(HERBDisease)\
        #     .filter(HERBDisease.disease_name.contains(disease_name))
        # paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        # response_object["count"] = paginate_info.total
        # response_object["data"] = [
        #     {"target_id": record[0].target_id,
        #      "gene_id": record[0].gene_id,
        #      "gene_name": record[0].gene_name,
        #      "target_description": record[0].description,
        #      "unipro_id": record[0].unipro_id,
        #      "disease_id": record[2].disease_id,
        #      "disease_name": record[2].disease_name}
        #     for record in paginate_info.items
        # ]
        records = db.session.query(HERBTarget, HERBLinkTargetDisease)\
            .join(HERBTarget)\
            .filter(HERBLinkTargetDisease.disease_name.contains(disease_name))
        paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        response_object["count"] = paginate_info.total
        response_object["data"] = [
            {"target_id": record[0].target_id,
             "gene_id": record[0].gene_id,
             "gene_name": record[0].gene_name,
             "target_description": record[0].description,
             "unipro_id": record[0].unipro_id,
             "disease_id": record[1].disease_id,
             "disease_name": record[1].disease_name}
            for record in paginate_info.items
        ]
    elif disease_name == "":
        # 搜索药物对应的靶点
        # records = db.session.query(HERBHerb, HERBLinkHerbTarget, HERBTarget)\
        #     .join(HERBHerb).join(HERBTarget)\
        #     .filter(HERBHerb.herb_cn_name.contains(drugname))

        # paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        # response_object["count"] = paginate_info.total
        # response_object["data"] = [
        #     {"herb_id": record[0].herb_id,
        #      "herb_cn_name": record[0].herb_cn_name,
        #      "target_id": record[2].target_id,
        #      "gene_id": record[2].gene_id,
        #      "gene_name": record[2].gene_name,
        #      "target_description": record[2].description,
        #      "unipro_id": record[2].unipro_id,
        #      }
        #     for record in paginate_info.items
        # ]
        records = db.session.query(HERBLinkHerbTarget, HERBTarget)\
            .join(HERBLinkHerbTarget)\
            .filter(HERBLinkHerbTarget.herb_cn_name.contains(drugname))

        paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        response_object["count"] = paginate_info.total
        response_object["data"] = [
            {"herb_id": record[0].herb_id,
             "herb_cn_name": record[0].herb_cn_name,
             "target_id": record[1].target_id,
             "gene_id": record[1].gene_id,
             "gene_name": record[1].gene_name,
             "target_description": record[1].description,
             "unipro_id": record[1].unipro_id,
             }
            for record in paginate_info.items
        ]
    else:
        # 同时根据药物和疾病名称进行搜索对应的靶点
        records = db.session.query(HERBHerb, HERBLinkHerbTarget, HERBTarget, HERBLinkTargetDisease, HERBDisease)\
            .join(HERBHerb).join(HERBTarget).join(HERBLinkTargetDisease).join(HERBDisease)\
            .filter(HERBHerb.herb_cn_name.contains(drugname), HERBDisease.disease_name.contains(disease_name))

        paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        response_object["count"] = paginate_info.total
        response_object["data"] = [
            {"herb_id": record[0].herb_id,
             "herb_cn_name": record[0].herb_cn_name,
             "target_id": record[2].target_id,
             "gene_id": record[2].gene_id,
             "gene_name": record[2].gene_name,
             "target_description": record[2].description,
             "unipro_id": record[2].unipro_id,
             "disease_id": record[4].disease_id,
             "disease_name": record[4].disease_name}
            for record in paginate_info.items
        ]
        # records = db.session.query(HERBLinkHerbTarget, HERBTarget, HERBLinkTargetDisease)\
        #     .join(HERBLinkHerbTarget).join(HERBLinkTargetDisease)\
        #     .filter(
        #         HERBLinkHerbTarget.herb_cn_name.contains(drugname),
        #         HERBLinkTargetDisease.disease_name.contains(disease_name)
        #     )
        # paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        # response_object["count"] = paginate_info.total
        # response_object["data"] = [
        #     {"herb_id": record[0].herb_id,
        #      "herb_cn_name": record[0].herb_cn_name,
        #      "target_id": record[1].target_id,
        #      "gene_id": record[1].gene_id,
        #      "gene_name": record[1].gene_name,
        #      "target_description": record[1].description,
        #      "unipro_id": record[1].unipro_id,
        #      "disease_id": record[2].disease_id,
        #      "disease_name": record[2].disease_name}
        #     for record in paginate_info.items
        # ]
    return jsonify(response_object)


@netpharm_bp.get("/ttd/target_detail/<target_id>")
def ttd_target_detail(target_id):
    target = TTDTarget.query.filter_by(target_id=target_id).first()

    target_info = {
        "target_id": target.target_id,
        "unipro_id": target.unipro2_id,
        "targname": target.targname,
        "genename": target.genename,
        "targtype": target.targtype,
        "bioclass": target.bioclass,
        "ecnumber": target.ecnumber,
        "reference": [],
        "dbname": "ttd"
    }
    return render_template('netpharm/target_detail.html', target_info=target_info)


@netpharm_bp.route("/ttd/search", methods=["POST", "GET"])
def ttd_search_target():
    """
        搜索查找 药物/疾病 对应的靶点信息
    """
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    drugname = request.args.get("drugname", "ROLIPRAM").strip()
    disease_name = request.args.get("disease_name", "rheumatoid").strip()

    response_object = {"code": 0, "msg": "", "count": 0, "data": []}

    if (drugname == "") and (disease_name == ""):
        pass
    elif drugname == "":
        # 搜索疾病对应的靶点
        records = db.session.query(TTDTarget, TTDLinkTargetDisease)\
            .join(TTDTarget, TTDTarget.target_id==TTDLinkTargetDisease.target_id)\
            .filter(TTDLinkTargetDisease.indication.contains(disease_name))

        paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        response_object["count"] = paginate_info.total
        response_object["data"] = [
            {"target_id": record[0].target_id,
            "unipro_id": record[0].unipro2_id,
            "targname": record[0].targname,
            "genename": record[0].genename,
            "targtype": record[0].targtype,
            "bioclass": record[0].bioclass,
            "ecnumber": record[0].ecnumber,
            "disease_entry": record[1].disease_entry,
            "disease_name": record[1].indication}
            for record in paginate_info.items
        ]
    elif disease_name == "":
        # 搜索药物对应的靶点
        records = db.session.query(TTDTarget, TTDLinkDrugTarget, TTDDrug)\
            .join(TTDTarget, TTDTarget.target_id==TTDLinkDrugTarget.target_id)\
            .join(TTDDrug, TTDDrug.drug_id==TTDLinkDrugTarget.drug_id)\
            .filter(TTDDrug.drugname.contains(drugname))

        paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        response_object["count"] = paginate_info.total
        response_object["data"] = [
            {"target_id": record[0].target_id,
             "unipro_id": record[0].unipro2_id,
             "targname": record[0].targname,
             "genename": record[0].genename,
             "targtype": record[0].targtype,
             "bioclass": record[0].bioclass,
             "ecnumber": record[0].ecnumber,
             "drugname": record[2].drugname}
            for record in paginate_info.items
        ]
    else:
        # 同时根据药物和疾病名称进行搜索对应的靶点
        records = db.session.query(TTDDrug, TTDTarget, TTDLinkDrugTarget, TTDLinkTargetDisease)\
                .join(TTDDrug, TTDDrug.drug_id==TTDLinkDrugTarget.drug_id)\
                .join(TTDTarget, TTDTarget.target_id==TTDLinkDrugTarget.target_id)\
                .join(TTDLinkTargetDisease, TTDTarget.target_id==TTDLinkTargetDisease.target_id)\
                .filter(TTDDrug.drugname.contains(drugname), 
                        TTDLinkTargetDisease.indication.contains(disease_name))
        
        paginate_info = records.paginate(page=page, per_page=limit, error_out=False)
        response_object["count"] = paginate_info.total
        response_object["data"] = [
            {"drugname": record[0].drugname,
             "target_id": record[1].target_id,
             "unipro_id": record[1].unipro2_id,
             "targname": record[1].targname,
             "genename": record[1].genename,
             "targtype": record[1].targtype,
             "bioclass": record[1].bioclass,
             "ecnumber": record[1].ecnumber,
             "disease_entry": record[3].disease_entry,
             "disease_name": record[3].indication}
            for record in paginate_info.items
        ]

        # response_object["count"] = records.count()
        # response_object["data"] = [
        #     {"drugname": record[0].drugname,
        #      "target_id": record[1].target_id,
        #      "unipro_id": record[1].unipro2_id,
        #      "targname": record[1].targname,
        #      "genename": record[1].genename,
        #      "targtype": record[1].targtype,
        #      "bioclass": record[1].bioclass,
        #      "ecnumber": record[1].ecnumber,
        #      "disease_entry": record[3].disease_entry,
        #      "disease_name": record[3].indication}
        #     for record in records.offset((page - 1) * limit).limit(limit).all()
        # ]

    return jsonify(response_object)


@netpharm_bp.route("/herb/hub_gene", methods=["POST", "GET"])
def herb_hub_gene():
    """ HERB 结果中进行 hub gene 计算
    """
    drugname = request.args.get("drugname", "").strip()
    disease_name = request.args.get("disease_name", "").strip()

    response_object = {"code": 0, "msg": "", "count": 0, "data": []}

    unipro_ids = []
    if (drugname == "") and (disease_name == ""):
        pass
    elif drugname == "":
        # 搜索疾病对应的靶点
        records = db.session.query(HERBTarget, HERBLinkTargetDisease, HERBDisease)\
            .join(HERBTarget).join(HERBDisease)\
            .filter(HERBDisease.disease_name.contains(disease_name))
        unipro_ids = list(set([record[0].unipro_id for record in records.all()]))
    elif disease_name == "":
        # 搜索药物对应的靶点
        records = db.session.query(HERBHerb, HERBLinkHerbTarget, HERBTarget)\
            .join(HERBHerb).join(HERBTarget)\
            .filter(HERBHerb.herb_cn_name.contains(drugname))
        unipro_ids = list(set([record[2].unipro_id for record in records.all()]))
    else:
        # 同时根据药物和疾病名称进行搜索对应的靶点
        # records = db.session.query(HERBHerb, HERBLinkHerbTarget, HERBTarget, HERBLinkTargetDisease, HERBDisease)\
        #     .join(HERBHerb).join(HERBTarget).join(HERBLinkTargetDisease).join(HERBDisease)\
        #     .filter(HERBHerb.herb_cn_name.contains(drugname), HERBDisease.disease_name.contains(disease_name))
        # unipro_ids = list(set([record[2].unipro_id for record in records.all()]))

        records = db.session.query(HERBLinkHerbTarget, HERBTarget, HERBLinkTargetDisease)\
            .join(HERBLinkHerbTarget).join(HERBLinkTargetDisease)\
            .filter(HERBLinkHerbTarget.herb_cn_name.contains(drugname), HERBLinkTargetDisease.disease_name.contains(disease_name))
        unipro_ids = list(set([record[1].unipro_id for record in records.all()]))

    current_app.logger.info(f"unipro_ids: {unipro_ids}")
    from applications.common.utils.ppi import calc_hub_gene
    hub_genes, ppi_fig, enr_fig = calc_hub_gene(unipro_ids)
    response_object["data"] = hub_genes
    response_object["count"] = len(hub_genes)
    # current_app.logger.info(f"hub_genes: {hub_genes}")

    response_object["ppi_fig"] = ""
    response_object["enr_fig"] = ""
    import base64
    from io import BytesIO
    buf = BytesIO()
    ppi_fig[0].savefig(buf, format="png", bbox_inches="tight")
    response_object["ppi_fig"] = base64.b64encode(buf.getbuffer()).decode("ascii")

    buf = BytesIO()
    enr_fig.savefig(buf, format="png", bbox_inches="tight")
    response_object["enr_fig"] = base64.b64encode(buf.getbuffer()).decode("ascii")

    return jsonify(response_object)


@netpharm_bp.route("/ttd/hub_gene", methods=["POST", "GET"])
def ttd_hub_gene():
    """ TTD 结果中进行 hub gene 计算
    """
    drugname = request.args.get("drugname", "ROLIPRAM").strip()
    disease_name = request.args.get("disease_name", "rheumatoid").strip()

    response_object = {"code": 0, "msg": "", "count": 0, "data": []}

    unipro_ids = []
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

    current_app.logger.info(f"unipro_ids: {unipro_ids}")
    from applications.common.utils.ppi import calc_hub_gene
    hub_genes, ppi_fig, enr_fig = calc_hub_gene(unipro_ids)
    response_object["data"] = hub_genes
    response_object["count"] = len(hub_genes)
    # current_app.logger.info(f"hub_genes: {hub_genes}")

    response_object["ppi_fig"] = ""
    response_object["enr_fig"] = ""
    import base64
    from io import BytesIO
    buf = BytesIO()
    ppi_fig[0].savefig(buf, format="png", bbox_inches="tight")
    response_object["ppi_fig"] = base64.b64encode(buf.getbuffer()).decode("ascii")

    buf = BytesIO()
    enr_fig.savefig(buf, format="png", bbox_inches="tight")
    response_object["enr_fig"] = base64.b64encode(buf.getbuffer()).decode("ascii")


    return jsonify(response_object)
