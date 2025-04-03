from applications.extensions import db


class HERBLinkHerbIngredient(db.Model):
    __tablename__ = 'herblink_herb_ingredient'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    herb_id = db.Column(db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id')
    ingredient_id = db.Column(db.String(32), db.ForeignKey("herb_ingredient.ingredient_id"), comment='ingredient id')

    herb = db.relationship('HERBHerb', backref='link_herb_ingredient')
    ingredient = db.relationship('HERBIngredient', backref='link_herb_ingredient')


class HERBLinkHerbTarget(db.Model):
    __tablename__ = 'herblink_herb_target'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    herb_id = db.Column(db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id')
    target_id = db.Column(db.String(32), db.ForeignKey("herb_target.target_id"), comment='target id')

    herb_cn_name = db.Column(db.String(64), comment='herb cn name')

    herb = db.relationship('HERBHerb', backref='link_herb_target')
    target = db.relationship('HERBTarget', backref='link_herb_target')


class HERBLinkHerbDisease(db.Model):
    __tablename__ = 'herblink_herb_disease'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    herb_id = db.Column(db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id')
    disease_id = db.Column(db.String(32), db.ForeignKey("herb_disease.disease_id"), comment='disease id')

    herb_cn_name = db.Column(db.String(64), comment='herb cn name')
    disease_name = db.Column(db.String(64), comment='disease name')

    herb = db.relationship('HERBHerb', backref='link_herb_disease')
    disease = db.relationship('HERBDisease', backref='link_herb_disease')


class HERBLinkIngredientTarget(db.Model):
    __tablename__ = 'herblink_ingredient_target'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    ingredient_id = db.Column(db.String(32), db.ForeignKey("herb_ingredient.ingredient_id"), comment='ingredient id')
    target_id = db.Column(db.String(32), db.ForeignKey("herb_target.target_id"), comment='target id')

    ingredient = db.relationship('HERBIngredient', backref='link_ingredient_target')
    target = db.relationship('HERBTarget', backref='link_ingredient_target')


class HERBLinkIngredientDisease(db.Model):
    __tablename__ = 'herblink_ingredient_disease'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    ingredient_id = db.Column(db.String(32), db.ForeignKey("herb_ingredient.ingredient_id"), comment='ingredient id')
    disease_id = db.Column(db.String(32), db.ForeignKey("herb_disease.disease_id"), comment='disease id')

    ingredient = db.relationship('HERBIngredient', backref='link_ingredient_disease')
    disease = db.relationship('HERBDisease', backref='link_ingredient_disease')


class HERBLinkTargetDisease(db.Model):
    __tablename__ = 'herblink_target_disease'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    target_id = db.Column(db.String(32), db.ForeignKey("herb_target.target_id"), comment='target id')
    disease_id = db.Column(db.String(32), db.ForeignKey("herb_disease.disease_id"), comment='disease id')

    disease_name = db.Column(db.String(64), comment="Disease_name")

    target = db.relationship('HERBTarget', backref='link_target_disease')
    disease = db.relationship('HERBDisease', backref='link_target_disease')


class HERBLinkReference(db.Model):
    __tablename__ = 'herblink_reference'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    herb_id = db.Column(db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id')
    herb_name = db.Column(db.String(32), comment='herb name')
    
    target_id = db.Column(db.String(32), comment='target id')

    ingredient_id = db.Column(db.String(32), comment='ingredient id')
    ingredient_name = db.Column(db.String(32), comment='ingredient name')

    # reference_id = db.Column(db.String(32), comment='reference id')
    pubmed_id = db.Column(db.String(32), comment='pubmed id')
    # pubmed_title = db.Column(db.String(128), comment='pubmed title')


# herblink_herb_ingredient = db.Table(
#     "herblink_herb_ingredient",  # 中间表名称
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='id'),  # 主键
#     db.Column("herb_id", db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id'),  # 属性 外键
#     db.Column("ingredient_id", db.String(32), db.ForeignKey("herb_ingredient.ingredient_id"), comment='ingredient id'),  # 属性 外键
# )

# herblink_herb_target = db.Table(
#     "herblink_herb_target",  # 中间表名称
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='id'),  # 主键
#     db.Column("herb_id", db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id'),  # 属性 外键
#     db.Column("target_id", db.String(32), db.ForeignKey("herb_target.target_id"), comment='target id'),  # 属性 外键
# )

# herblink_herb_disease = db.Table(
#     "herblink_herb_disease",  # 中间表名称
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='id'),  # 主键
#     db.Column("herb_id", db.String(32), db.ForeignKey("herb_herb.herb_id"), comment='herb id'),  # 属性 外键
#     db.Column("disease_id", db.String(32), db.ForeignKey("herb_disease.disease_id"), comment='disease id'),  # 属性 外键
# )

# herblink_ingredient_target = db.Table(
#     "herblink_ingredient_target",  # 中间表名称
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='id'),  # 主键
#     db.Column("ingredient_id", db.String(32), db.ForeignKey("herb_ingredient.ingredient_id"), comment='ingredient id'),  # 属性 外键
#     db.Column("target_id", db.String(32), db.ForeignKey("herb_target.target_id"), comment='target id'),  # 属性 外键
# )

# herblink_ingredient_disease = db.Table(
#     "herblink_ingredient_disease",  # 中间表名称
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='id'),  # 主键
#     db.Column("ingredient_id", db.String(32), db.ForeignKey("herb_ingredient.ingredient_id"), comment='ingredient id'),  # 属性 外键
#     db.Column("disease_id", db.String(32), db.ForeignKey("herb_disease.disease_id"), comment='disease id'),  # 属性 外键
# )

# herblink_target_disease = db.Table(
#     "herblink_target_disease",  # 中间表名称
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='id'),  # 主键
#     db.Column("target_id", db.String(32), db.ForeignKey("herb_target.target_id"), comment='target id'),  # 属性 外键
#     db.Column("disease_id", db.String(32), db.ForeignKey("herb_disease.disease_id"), comment='disease id'),  # 属性 外键
# )
