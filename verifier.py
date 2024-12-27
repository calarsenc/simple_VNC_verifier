import csv

def read_edges(csv_path):
    """
    Reads a CSV with rows [source_node, target_node, weight],
    skipping the first row as a header.
    Returns a dict of {(src, tgt) : weight}.
    """
    edges = {}
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row. Remove if no header.
        for row in reader:
            src, tgt, w_str = row
            weight = int(w_str)
            edges[(src, tgt)] = weight
    return edges

def read_mapping(mapping_csv):
    """
    Reads a CSV with rows [male_node_id, female_node_id],
    skipping the first row as a header.
    Returns a dict: male_node -> female_node
    """
    mapping = {}
    with open(mapping_csv, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row. Remove if no header.
        for row in reader:
            male_id, female_id = row
            mapping[male_id] = female_id
    return mapping

def verify_mapping(male_edges_csv, female_edges_csv, mapping_csv):
    """
    1) Checks the submitted mapping is a valid 1:1 mapping.
    2) Computes and prints the alignment score under that mapping.
    """
    # --- Read edges ---
    male_edges = read_edges(male_edges_csv)
    female_edges = read_edges(female_edges_csv)
    
    # --- Read mapping (f: male_node -> female_node) ---
    mapping = read_mapping(mapping_csv)
    
    # --- Gather all male/female nodes that appear in edges ---
    male_nodes_in_edges = set()
    for (m_src, m_tgt) in male_edges.keys():
        male_nodes_in_edges.add(m_src)
        male_nodes_in_edges.add(m_tgt)

    female_nodes_in_edges = set()
    for (f_src, f_tgt) in female_edges.keys():
        female_nodes_in_edges.add(f_src)
        female_nodes_in_edges.add(f_tgt)
    
    # 1) Check that every male_node in male_edges is mapped
    unmapped = male_nodes_in_edges - set(mapping.keys())
    if unmapped:
        raise ValueError(f"Not all male nodes are mapped! Missing: {unmapped}")
    
    # 2) Check that the mapping is injective (no repeated female nodes)
    mapped_female_nodes = list(mapping.values())
    if len(set(mapped_female_nodes)) != len(mapped_female_nodes):
        raise ValueError("Mapping is not 1:1. Some female nodes are used more than once.")

    # --- Compute alignment score ---
    # alignment = Σ min( E_M(x,y), E_F(f(x), f(y)) ) for all x,y in VM
    alignment = 0
    for (m_src, m_tgt), w_male in male_edges.items():
        f_src = mapping[m_src]
        f_tgt = mapping[m_tgt]
        w_female = female_edges.get((f_src, f_tgt), 0)
        alignment += min(w_male, w_female)

    print("Verification successful!")
    print(f"Alignment score = {alignment}")

# --- Run the verification directly ---
verify_mapping(
    'male_connectome_graph.csv',
    'female_connectome_graph.csv',
    'benchmark.csv'
)