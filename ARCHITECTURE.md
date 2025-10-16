# Multi-Agent Debate System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Multi-Agent Debate System                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Researcher │    │   Critic    │    │ Synthesizer │     │
│  │             │    │             │    │             │     │
│  │ • Gathers   │    │ • Identifies│    │ • Integrates│     │
│  │   evidence  │    │   flaws     │    │   views     │     │
│  │ • Provides  │    │ • Challenges│    │ • Finds     │     │
│  │   facts     │    │   assumptions│   │   consensus │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│                           ┌─────────────┐                  │
│                           │    Judge    │                  │
│                           │             │                  │
│                           │ • Evaluates │                  │
│                           │ • Decides   │                  │
│                           │ • Verdict   │                  │
│                           └─────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## Debate Flow

### Round 1: Initial Arguments
```
Researcher ──→ [Initial Position + Evidence]
Critic ──────→ [Initial Position + Evidence]  
Synthesizer ─→ [Initial Position + Evidence]
```

### Round 2: Critique & Revision
```
Critic ──────→ [Critique of all arguments]
Researcher ──→ [Revised argument]
Synthesizer ─→ [Synthesis attempt]
```

### Round 3: Final Synthesis
```
Synthesizer ─→ [Final synthesis]
Judge ───────→ [Final verdict]
```

## Quality Assessment

```
┌─────────────────────────────────────────────────────────────┐
│                    Quality Rubric                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Evidence (0-5)     │  Feasibility (0-5)  │  Risks (0-5)   │
│  • Citations        │  • Practical        │  • Risk        │
│  • Data points      │    considerations   │    awareness   │
│  • Examples         │  • Implementation   │  • Limitations│
│                     │    details          │  • Challenges │
│                                                             │
│  Clarity (0-5)      │  Convergence        │  Timing        │
│  • Structure        │  • Agreement        │  • Per round   │
│  • Logic flow       │  • Consensus        │  • Total time  │
│  • Readability      │  • Final verdict    │                │
└─────────────────────────────────────────────────────────────┘
```

## Experiment Framework

### Agent Count Experiments
- **2 Agents**: Researcher + Judge
- **4 Agents**: Researcher + Critic + Synthesizer + Judge

### Round Count Experiments  
- **1 Round**: Initial arguments → Judge verdict
- **3 Rounds**: Arguments → Critique → Synthesis → Judge verdict

### Temperature Experiments
- **Low (0.3)**: More structured, conservative arguments
- **High (0.9)**: More creative, diverse perspectives

## Technical Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    Technical Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Python 3.8+                                                │
│  ├── CrewAI Framework                                       │
│  ├── LangChain Integration                                  │
│  ├── OpenAI GPT Models                                      │
│  └── Quality Assessment Engine                              │
│                                                             │
│  Input: Topic + Configuration                               │
│  ↓                                                          │
│  Agent Creation & Task Assignment                           │
│  ↓                                                          │
│  Sequential Debate Execution                                │
│  ↓                                                          │
│  Quality Scoring & Analysis                                 │
│  ↓                                                          │
│  Results & Metrics Output                                   │
└─────────────────────────────────────────────────────────────┘
```

## Usage Examples

### Basic Debate
```python
debate_system = MultiAgentDebate()
result = debate_system.run_debate(
    topic="Should AI be regulated?",
    agent_count=4,
    rounds=2
)
```

### Experiment Runner
```python
runner = ExperimentRunner()
runner.run_agent_count_experiment()
runner.run_round_count_experiment()
report = runner.generate_report()
```

## Key Features

- **Modular Design**: Easy to add new agent types
- **Configurable**: Adjustable parameters for different experiments
- **Measurable**: Built-in quality assessment and metrics
- **Extensible**: Framework for adding new evaluation criteria
- **Reproducible**: Consistent experiment setup and execution
