from applications.view.netpharm import netpharm_bp

def init_bps(app):
    app.register_blueprint(netpharm_bp)

    from applications.view.plot import add_routes
    add_routes(app)
