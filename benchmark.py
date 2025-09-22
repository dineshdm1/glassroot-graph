import json
import networkx as nx
from tqdm import tqdm

hits = 0
total = 0

for i in tqdm(range(1, 185)):
    try:
        with open(f"who_when_data/Who&When/Algorithm-Generated/{i}.json") as f:
            data = json.load(f)

        G = nx.DiGraph()
        for msg in data["history"]:
            src = msg["name"]
            tgt = msg.get("name")
            if src and tgt:
                if G.has_edge(src, tgt):
                    G[src][tgt]["weight"] += 1
                else:
                    G.add_edge(src, tgt, weight=1)

        # Gentle ensemble: 70 % PageRank + 20 % Betweenness + 10 % community-size-normalised
        pr = nx.pagerank(G, weight='weight')
        bt = nx.betweenness_centrality(G, weight='weight')
        communities = nx.community.louvain_communities(
            G, weight='weight', seed=42)
        comm_size = {
            n: 1.0 / len([c for c in communities if n in c][0]) for n in G.nodes()}

        ensemble = {n: 0.7*pr[n] + 0.2*bt[n] +
                    0.1*comm_size[n] for n in G.nodes()}
        ranked = sorted(ensemble.items(), key=lambda x: x[1], reverse=True)
        top_guess = ranked[0][0] if ranked else None

        if top_guess == data["mistake_agent"]:
            hits += 1
        total += 1
    except Exception:
        pass

print(f"Ensemble accuracy: {hits}/{total} = {hits/total:.3f}")
