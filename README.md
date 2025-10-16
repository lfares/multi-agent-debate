# Multi-Agent Debate System

A sophisticated multi-agent debate system that orchestrates AI agents with distinct roles to engage in structured debates on various topics.

## Features

- **Multi-Agent Architecture**: 2-4 agents with distinct roles (Researcher, Critic, Synthesizer, Judge)
- **Structured Debate Protocol**: Multiple rounds with argue → critique → revise → verdict flow
- **Quality Assessment**: Heuristic-based scoring across evidence, feasibility, risks, and clarity
- **Experiment Framework**: Systematic testing with configurable parameters
- **Performance Metrics**: Execution time tracking and convergence detection
- **Working AI Integration**: Uses Google Gemini 2.0 Flash Experimental for reliable content generation

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment**:
   ```bash
   cp env_example.txt .env
   # Edit .env and add your Google API key
   ```

3. **Run Demo**:
   ```bash
   python demo.py
   ```

4. **Run Full Experiments**:
   ```bash
   python run_experiments.py
   ```

## Files

- `multi_agent_debate.py` - Core debate system implementation
- `demo.py` - Quick demonstration script
- `run_experiments.py` - Full experiment suite
- `experiment_report.md` - Latest experiment results
- `ARCHITECTURE.md` - Detailed system design
- `ASSIGNMENT_SUMMARY.md` - Assignment compliance documentation

## System Architecture

### Agent Roles

- **Researcher**: Gathers comprehensive information and evidence
- **Critic**: Identifies weaknesses and potential issues in arguments  
- **Synthesizer**: Integrates different perspectives and finds common ground
- **Judge**: Evaluates all arguments and provides final verdict

### Debate Protocol

1. **Round 1**: Initial arguments from all agents (except Judge)
2. **Round 2+**: Critique, synthesis, and revision phases
3. **Final**: Judge provides comprehensive verdict

### Quality Rubric

The system evaluates debates on four dimensions (0-5 scale):
- **Evidence**: Quality and quantity of supporting data
- **Feasibility**: Practical implementation considerations
- **Risks**: Awareness and assessment of potential issues
- **Clarity**: Structure and comprehensibility of arguments

## Experiments

The system includes built-in experiments to test:

- **Agent Count**: 2 vs 4 agents
- **Round Count**: 1 vs 3 rounds
- **Temperature**: Low vs high creativity settings

## Results

The system tracks:
- Execution time per debate
- Quality scores across all dimensions
- Convergence indicators
- Key excerpts from each round

## Example Output

```
🎭 Multi-Agent Debate Demo
========================================
🤖 Initializing debate system...
📝 Topic: Should libraries invest more in digital resources or physical books?

🚀 Starting debate (2 agents, 2 rounds)...
----------------------------------------

🔄 Round 1
----------------------------------------
🤖 Researcher is thinking...
📝 Researcher: My position is that libraries should strategically increase investment in digital resources...
🤖 Critic is thinking...
📝 Critic: While digital resources have benefits, we must consider the limitations...

📊 RESULTS
========================================
⏱️  Execution Time: 24.18 seconds
🎯 Quality Scores:
   Evidence: 0.5/5.0
   Feasibility: 1.0/5.0
   Risks: 0.0/5.0
   Clarity: 5.0/5.0
🤝 Convergence: Yes
```

## Configuration

You can customize the debate system by modifying:

- `model_name`: LLM model to use (default: "gemini-2.0-flash-exp")
- `temperature`: Creativity level (default: 0.7)
- `agent_count`: Number of agents (2-4)
- `rounds`: Number of debate rounds (1-3)

## Requirements

- Python 3.8+
- Google Gemini API key
- Required packages listed in `requirements.txt`

## Assignment Compliance

See `ASSIGNMENT_SUMMARY.md` for how this system meets the assignment requirements.

## System Architecture

See `ARCHITECTURE.md` for detailed system design and component descriptions.