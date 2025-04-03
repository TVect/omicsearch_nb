import pandas as pd
import networkx as nx
from urllib.parse import urlencode

def string_map(gene:list, species:int)->pd.DataFrame:
    r"""A Python library to find the gene name in string-db

    Arguments:
        gene: The gene list to analysis PPI
        species: NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).
    
    Returns:
        res: the dataframe of query gene and new gene
    
    """
    import requests ## python -m pip install requests
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "get_string_ids"
    params = {

        "identifiers" : "\r".join(gene), # your protein list
        "species" : species, # species NCBI identifier 
        "limit" : 1, # only one (best) identifier per input protein
        "echo_query" : 1, # see your input identifiers in the output
        "caller_identity" : "www.awesome_app.org" # your app name

    }
    request_url = "/".join([string_api_url, output_format, method])
    response = requests.post(request_url, data=params)
    res=pd.DataFrame(columns=['queryItem','queryIndex','stringId','ncbiTaxonId','taxonName','preferredName','annotation'])
    res['queryItem']=[j.strip().split("\t")[0] for j in response.text.strip().split("\n")]
    res['queryIndex']=[j.strip().split("\t")[1] for j in response.text.strip().split("\n")]
    res['stringId']=[j.strip().split("\t")[2] for j in response.text.strip().split("\n")]
    res['ncbiTaxonId']=[j.strip().split("\t")[3] for j in response.text.strip().split("\n")]
    res['taxonName']=[j.strip().split("\t")[4] for j in response.text.strip().split("\n")]
    res['preferredName']=[j.strip().split("\t")[5] for j in response.text.strip().split("\n")]
    res['annotation']=[j.strip().split("\t")[6] for j in response.text.strip().split("\n")]

    return res


def string_interaction(gene:list,species:int) -> pd.DataFrame:
    r"""A Python library to analysis the protein-protein interaction network by string-db
  
    Arguments:
        gene: The gene list to analysis PPI
        species: NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).
    
    Returns:
        res: the dataframe of protein-protein interaction
    
    """
    import requests ## python -m pip install requests
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "network"
    request_url = "/".join([string_api_url, output_format, method])
    my_genes = gene

    params = {

        "identifiers" : "%0d".join(my_genes), # your protein
        "species" : species, # species NCBI identifier 
        "caller_identity" : "www.awesome_app.org" # your app name

    }
    response = requests.post(request_url, data=params)
    res=pd.DataFrame()
    res['stringId_A']=[j.strip().split("\t")[0] for j in response.text.strip().split("\n")]
    res['stringId_B']=[j.strip().split("\t")[1] for j in response.text.strip().split("\n")]
    res['preferredName_A']=[j.strip().split("\t")[2] for j in response.text.strip().split("\n")]
    res['preferredName_B']=[j.strip().split("\t")[3] for j in response.text.strip().split("\n")]
    res['ncbiTaxonId']=[j.strip().split("\t")[4] for j in response.text.strip().split("\n")]
    res['score']=[j.strip().split("\t")[5] for j in response.text.strip().split("\n")]
    res['nscore']=[j.strip().split("\t")[6] for j in response.text.strip().split("\n")]
    res['fscore']=[j.strip().split("\t")[7] for j in response.text.strip().split("\n")]
    res['pscore']=[j.strip().split("\t")[8] for j in response.text.strip().split("\n")]
    res['ascore']=[j.strip().split("\t")[9] for j in response.text.strip().split("\n")]
    res['escore']=[j.strip().split("\t")[10] for j in response.text.strip().split("\n")]
    res['dscore']=[j.strip().split("\t")[11] for j in response.text.strip().split("\n")]
    res['tscore']=[j.strip().split("\t")[12] for j in response.text.strip().split("\n")]
    return res


def generate_G(gene:list,species:int,score:float=0.4) -> nx.Graph:
    r"""A Python library to get the PPI network in string-db

    Arguments:
        gene: The gene list to analysis PPI
        species: NCBI taxon identifiers (e.g. Human is 9606, see: STRING organisms).
        score: The threshold of protein A and B interaction

    Returns:
        G: the networkx object of PPI in query gene list
    
    """
    
    a=string_interaction(gene,species)
    b=a.drop_duplicates()
    b.head()
    G = nx.Graph()
    G.add_nodes_from(set(b['preferredName_A'].tolist()+b['preferredName_B'].tolist()))

    #Connect nodes
    for i in b.index:
        col_label = b.loc[i]['preferredName_A']
        row_label = b.loc[i]['preferredName_B']
        if(float(b.loc[i]['score'])>score):
            G.add_edge(col_label,row_label)
    return G

def calc_hub_gene(
        genes_or_proteins=[],
        species=9606,
        score=0.4
):
    if genes_or_proteins == []:
        return []
    # 正规化为 StringDB 表示的基因列表
    # print(genes_or_proteins)
    # gene_mapping = ov.bulk.string_map(genes_or_proteins, species)
    gene_mapping = string_map(genes_or_proteins, species)

    gene_list = [
        [item["queryItem"], item["preferredName"], item["stringId"], item["taxonName"], item["annotation"]]
        for item in gene_mapping.to_dict(orient='records')
    ]

    # ppi_graph = ov.bulk.generate_G([item[1] for item in gene_list], species, score=score)
    ppi_graph = generate_G([item[1] for item in gene_list], species, score=score)
    degree_centrality_map = nx.degree_centrality(ppi_graph)
    degree_map = nx.degree(ppi_graph)
    # katz_centrality_map = nx.katz_centrality(ppi_graph)
    closeness_centrality_map = nx.closeness_centrality(ppi_graph)
    betweenness_centrality_map = nx.betweenness_centrality(ppi_graph)

    records = []
    for gene_item in gene_list:
        if gene_item[1] in degree_centrality_map:
            records.append(
                {
                    'query_item': gene_item[0],
                    'gene': gene_item[1],
                    "string_id": gene_item[2],
                    "taxon_name": gene_item[3],
                    # "annotation": gene_item[4],
                    'degree': degree_map[gene_item[1]],
                    'degree_centrality': degree_centrality_map[gene_item[1]],
                    # 'katz_centrality': katz_centrality_map[gene_item[1]],
                    'closeness_centrality': closeness_centrality_map[gene_item[1]],
                    'betweenness_centrality': betweenness_centrality_map[gene_item[1]]
                }
            )

    return records


if __name__ == '__main__':
    test_proteins = ['P00491', 'P43235', 'P29965', 'Q08210', 'P21453', 'Q07343', 'P41143', 
                     'P14780', 'Q8NER1', 'P14679', 'P27815', 'P35228', 'P01730', 'P35367', 
                     'Q15116', 'P19838; Q00653; Q04206; Q01201; Q04864', 'Q08499']

    test_genes = ['NOS2', 'OPRD1', 'CTSK', 'TRPV1', 'TYR', 'Malaria DHOdehase', 
                  'NFKB1; NFKB2; RELA; RELB; REL', 'PDE4D', 'MMP9', 'PDCD1', 
                  'CD40LG', 'PNP', 'S1PR1', 'PDE4A', 'PDE4B', 'HRH1', 'CD4']

    import pandas as pd
    print(pd.DataFrame(calc_hub_gene(test_genes)))
    print(pd.DataFrame(calc_hub_gene(test_proteins)))
