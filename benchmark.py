import os
from tqdm import tqdm
import networkx as nx
import json
print(f"\n--- TESTING: REMOVE CHATTY AGENTS ---")

improved_count = 0
total_tests = 0

for i in range(1, 185):  # All conversations
    try:
        with open(f"who_when_data/Who&When/Algorithm-Generated/{i}.json") as f:
            data = json.load(f)

        # Find who caused the original failure
        original_failure_agent = data["mistake_agent"]

        # Measure how chatty each agent is
        agent_chattiness = {}
        for msg in data["history"]:
            agent = msg["name"]
            if agent not in agent_chattiness:
                agent_chattiness[agent] = 0
            agent_chattiness[agent] += len(msg.get("content", ""))

        # Remove the chattiest agent
        if len(agent_chattiness) > 1:  # Only if there's more than one agent
            chattiest_agent = max(agent_chattiness, key=agent_chattiness.get)

            # Check if removing the chattiest agent would have prevented the failure
            if chattiest_agent == original_failure_agent:
                improved_count += 1
                print(
                    f"Conversation {i}: Removing {chattiest_agent} would prevent failure")

        total_tests += 1
    except:
        pass

if total_tests > 0:
    improvement_rate = improved_count / total_tests
    print(
        f"\nResults: Removing chattiest agent would prevent {improved_count}/{total_tests} failures")
    print(f"That's {improvement_rate:.1%} improvement")

# Check if files exist
data_path = "who_when_data/Who&When/Algorithm-Generated/"
if os.path.exists(data_path):
    files = os.listdir(data_path)
    print(f"Found {len(files)} files")
else:
    print(f"Folder doesn't exist: {data_path}")

hits = 0
total = 0
all_agents = {}

for i in tqdm(range(1, 185)):
    try:
        with open(f"who_when_data/Who&When/Algorithm-Generated/{i}.json") as f:
            data = json.load(f)

        # Track agent communication
        for msg in data["history"]:
            agent = msg["name"]
            if agent not in all_agents:
                all_agents[agent] = {'messages': 0, 'chars': 0, 'failures': 0}
            all_agents[agent]['messages'] += 1
            all_agents[agent]['chars'] += len(msg.get("content", ""))

        # Mark failure agents
        if "mistake_agent" in data and data["mistake_agent"] in all_agents:
            all_agents[data["mistake_agent"]]['failures'] += 1

        # Your original graph analysis
        G = nx.DiGraph()
        for msg in data["history"]:
            src = msg["name"]
            tgt = msg.get("name")
            if src and tgt:
                if G.has_edge(src, tgt):
                    G[src][tgt]["weight"] += 1
                else:
                    G.add_edge(src, tgt, weight=1)

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

# Show which agent types cause most problems
tool_failures = 0
analyst_failures = 0
coordinator_failures = 0
tool_count = 0
analyst_count = 0
coordinator_count = 0

for agent, stats in all_agents.items():
    if stats['messages'] > 0:
        avg_length = stats['chars'] / stats['messages']

        if avg_length < 400:
            tool_count += 1
            tool_failures += stats['failures']
        elif avg_length > 1500:
            analyst_count += 1
            analyst_failures += stats['failures']
        else:
            coordinator_count += 1
            coordinator_failures += stats['failures']

print(f"\n--- AGENT TYPE FAILURE RATES ---")
print(
    f"Tool agents: {tool_failures/tool_count:.2f} failures per agent ({tool_count} agents)")
print(
    f"Analyst agents: {analyst_failures/analyst_count:.2f} failures per agent ({analyst_count} agents)")
print(
    f"Coordinator agents: {coordinator_failures/coordinator_count:.2f} failures per agent ({coordinator_count} agents)")
