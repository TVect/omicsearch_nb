import io
import random
import base64
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

async def plot_ppi():
    from io import BytesIO
    import omicverse as ov
    ov.utils.ov_plot_set()

    gene_list=['FAA4','POX1','FAT1','FAS2','FAS1','FAA1','OLE1','YJU3','TGL3','INA1','TGL5']
    gene_type_dict=dict(zip(gene_list,['Type1']*5+['Type2']*6))
    gene_color_dict=dict(zip(gene_list,['#F7828A']*5+['#9CCCA4']*6))

    ppi=ov.bulk.pyPPI(gene=gene_list,
                      gene_type_dict=gene_type_dict,
                      gene_color_dict=gene_color_dict,
                      species=4932)
    ppi.interaction_analysis()
    fig = ppi.plot_network()
    buf = BytesIO()
    fig[0].savefig(buf, format="png")
    # Embed the result in the html output.
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    return Response(buf.getvalue(), mimetype='image/png')


def ppi_network_by_genes(gene_list):
    from io import BytesIO
    import omicverse as ov
    ov.utils.ov_plot_set()

    gene_list=['FAA4','POX1','FAT1','FAS2','FAS1','FAA1','OLE1','YJU3','TGL3','INA1','TGL5']
    gene_type_dict=dict(zip(gene_list,['Type1']*5+['Type2']*6))
    gene_color_dict=dict(zip(gene_list,['#F7828A']*5+['#9CCCA4']*6))

    ppi=ov.bulk.pyPPI(gene=gene_list,
                      gene_type_dict=gene_type_dict,
                      gene_color_dict=gene_color_dict,
                      species=4932)
    ppi.interaction_analysis()
    fig = ppi.plot_network()
    buf = BytesIO()
    fig[0].savefig(buf, format="png")
    # Embed the result in the html output.
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    return Response(buf.getvalue(), mimetype='image/png')



def add_routes(app):
    app.add_url_rule('/plot', view_func=plot_ppi, methods=['GET'])
