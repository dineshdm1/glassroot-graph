# Agent Failure Attribution Using Communication Network Analysis

This project identifies which AI agent caused team failures using network analysis of inter-agent communication patterns.

## Research Finding

Agents with higher communication activity are more likely to be the root cause of team failures. This finding challenges common assumptions about failure attribution in multi-agent systems.

## Performance

- **Accuracy:** 50.8% (64 correct predictions out of 126 test cases)
- **Baseline:** Random selection achieves ~30% accuracy
- **Dataset:** 184 documented failure cases from the Who&When dataset
- **Method:** Activity-weighted network analysis with temporal decay

## Methodology

The approach analyzes communication graphs to identify failure-causing agents:

1. **Graph Construction:** Build directed communication networks from agent interaction logs
2. **Temporal Weighting:** Apply exponential decay to prioritize recent communications
3. **Centrality Analysis:** Calculate multiple network centrality measures
4. **Ensemble Method:** Combine metrics using optimized weights:
   - PageRank: 80%
   - Betweenness Centrality: 15% 
   - Community Detection: 5%

## Technical Implementation

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python first_graph.py

# Compare with baseline
python benchmark.py
```

## Key Files

- `first_graph.py` - Main attribution algorithm implementation
- `benchmark.py` - Baseline comparison method
- `who_when_data/` - Dataset containing 184 failure scenarios
- `requirements.txt` - Required Python packages

## Limitations and Future Work

This approach represents the performance ceiling for observation-based methods. The consistent 50.8% accuracy across multiple enhancement attempts suggests fundamental limits of passive analysis.

**Proposed Next Phase:** Causal validation through counterfactual replay testing. By removing suspected agents and re-running scenarios, we expect to achieve 58-62% accuracy and establish causal relationships.

## Dataset

Research conducted using the Who&When Multi-Agent Dataset for Agent Failure Attribution, available through Hugging Face.

Reference: 
@article{zhang2025agent,
  title={Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems},
  author={Zhang, Shaokun and Yin, Ming and Zhang, Jieyu and Liu, Jiale and Han, Zhiguang and Zhang, Jingyang and Li, Beibin and Wang, Chi and Wang, Huazheng and Chen, Yiran and others},
  journal={arXiv preprint arXiv:2505.00212},
  year={2025}
}


**Source:** [Who&When Dataset]((https://huggingface.co/datasets/Kevin355/Who_and_When))

## License

MIT License - See LICENSE file for details.
