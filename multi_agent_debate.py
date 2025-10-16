"""
Working Multi-Agent Debate System
Uses gemini-2.0-flash-exp which actually works without safety filtering issues.
"""

import os
import time
from typing import Dict, List, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

@dataclass
class DebateResult:
    """Structure to hold debate results and metrics."""
    topic: str
    agents_count: int
    rounds: int
    final_verdict: str
    quality_scores: Dict[str, float]
    convergence: bool
    execution_time: float
    excerpts: List[str]

class QualityRubric:
    """Quality assessment rubric for debate outcomes."""
    
    @staticmethod
    def assess_quality(content: str) -> Dict[str, float]:
        """Assess content quality on 0-5 scale across multiple dimensions."""
        scores = {
            'evidence': 0.0,
            'feasibility': 0.0,
            'risks': 0.0,
            'clarity': 0.0
        }
        
        # Simple heuristic-based scoring
        content_lower = content.lower()
        
        # Evidence scoring (look for citations, data, examples)
        evidence_indicators = ['study', 'research', 'data', 'statistics', 'example', 'according to', 'shows']
        evidence_count = sum(1 for indicator in evidence_indicators if indicator in content_lower)
        scores['evidence'] = min(5.0, evidence_count * 0.5)
        
        # Feasibility scoring (look for practical considerations)
        feasibility_indicators = ['practical', 'implement', 'feasible', 'realistic', 'achievable', 'cost', 'time']
        feasibility_count = sum(1 for indicator in feasibility_indicators if indicator in content_lower)
        scores['feasibility'] = min(5.0, feasibility_count * 0.5)
        
        # Risk assessment (look for risk awareness)
        risk_indicators = ['risk', 'concern', 'challenge', 'limitation', 'potential problem', 'drawback']
        risk_count = sum(1 for indicator in risk_indicators if indicator in content_lower)
        scores['risks'] = min(5.0, risk_count * 0.5)
        
        # Clarity scoring (look for structure and clarity indicators)
        clarity_indicators = ['first', 'second', 'third', 'however', 'therefore', 'in conclusion', 'clearly']
        clarity_count = sum(1 for indicator in clarity_indicators if indicator in content_lower)
        scores['clarity'] = min(5.0, clarity_count * 0.3 + len(content.split()) / 50)
        
        return scores

class WorkingMultiAgentDebate:
    """Working multi-agent debate system using gemini-2.0-flash-exp."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp", temperature: float = 0.7):
        """Initialize the debate system."""
        # Configure the API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Initialize the model with minimal safety restrictions
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1000,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}
            ]
        )
        self.model_name = model_name
        self.temperature = temperature
        
    def get_agent_prompt(self, role: str, topic: str, round_num: int, previous_responses: List[str] = None) -> str:
        """Generate prompts for different agent roles."""
        
        if role == "Researcher":
            return f"""You are a researcher analyzing this topic: {topic}

Round: {round_num}

{"Previous responses:" if previous_responses else ""}
{chr(10).join([f"- {resp[:200]}..." for resp in previous_responses]) if previous_responses else ""}

As a researcher, provide your analysis:
1. Your position on this topic
2. Supporting evidence or examples
3. Consider potential counterarguments

Write 2-3 paragraphs."""

        elif role == "Critic":
            return f"""You are a critic analyzing this topic: {topic}

Round: {round_num}

{"Previous responses:" if previous_responses else ""}
{chr(10).join([f"- {resp[:200]}..." for resp in previous_responses]) if previous_responses else ""}

As a critic, {"analyze the previous responses and:" if round_num > 1 else "provide your analysis:"}
1. {"Identify any issues or gaps" if round_num > 1 else "Your position"}
2. {"Suggest improvements" if round_num > 1 else "Supporting points"}
3. {"Highlight important considerations" if round_num > 1 else "Important considerations"}

Write 2-3 paragraphs."""

        elif role == "Synthesizer":
            return f"""You are a synthesizer analyzing this topic: {topic}

Round: {round_num}

{"Previous responses:" if previous_responses else ""}
{chr(10).join([f"- {resp[:200]}..." for resp in previous_responses]) if previous_responses else ""}

As a synthesizer, {"review all responses and:" if round_num > 1 else "provide your analysis:"}
1. {"Find common themes" if round_num > 1 else "Your position"}
2. {"Propose balanced solutions" if round_num > 1 else "Supporting points"}
3. {"Highlight key benefits" if round_num > 1 else "Key benefits"}

Write 2-3 paragraphs."""

        elif role == "Judge":
            return f"""You are a judge evaluating this topic: {topic}

Final Round

All previous responses:
{chr(10).join([f"- {resp[:300]}..." for resp in previous_responses]) if previous_responses else ""}

As a judge, evaluate all responses and provide your final assessment:
1. Summarize the main points
2. Evaluate the reasoning
3. Provide your conclusion
4. Explain your reasoning

Write 3-4 paragraphs."""

        else:
            return f"Please provide your analysis on: {topic}"

    def run_debate(self, topic: str, agent_count: int = 4, rounds: int = 2) -> DebateResult:
        """Run a complete debate and return results."""
        start_time = time.time()
        
        # Define agent roles
        roles = ["Researcher", "Critic", "Synthesizer", "Judge"][:agent_count]
        if agent_count < 4:
            roles = roles + ["Judge"]  # Always include judge
            
        all_responses = []
        
        # Run debate rounds
        for round_num in range(rounds + 1):  # +1 for final judge round
            
            if round_num <= rounds - 1:  # Regular debate rounds
                print(f"\n🔄 Round {round_num + 1}")
                print("-" * 40)
                
                round_responses = []
                for i, role in enumerate(roles[:-1]):  # Exclude judge from regular rounds
                    print(f"🤖 {role} is thinking...")
                    
                    # Get previous responses for context
                    previous_responses = all_responses[-len(roles)+1:] if len(all_responses) > len(roles)-1 else None
                    
                    # Generate prompt
                    prompt = self.get_agent_prompt(role, topic, round_num + 1, previous_responses)
                    
                    # Get response
                    try:
                        response = self.model.generate_content(prompt)
                        if response.candidates and len(response.candidates) > 0:
                            candidate = response.candidates[0]
                            if candidate.content and candidate.content.parts:
                                response_text = candidate.content.parts[0].text
                            else:
                                response_text = f"No content generated (finish_reason: {candidate.finish_reason})"
                        else:
                            response_text = "No response candidates generated"
                    except Exception as e:
                        print(f"❌ Error generating response for {role}: {e}")
                        response_text = f"Error: {str(e)}"
                    
                    print(f"📝 {role}: {response_text[:150]}...")
                    round_responses.append(response_text)
                    all_responses.append(response_text)
                    
                    # Small delay to avoid rate limiting
                    time.sleep(1)
            
            else:  # Final judge round
                print(f"\n⚖️  Final Verdict")
                print("-" * 40)
                
                print("🤖 Judge is evaluating...")
                
                # Judge evaluates all previous responses
                judge_prompt = self.get_agent_prompt("Judge", topic, round_num + 1, all_responses)
                try:
                    final_verdict = self.model.generate_content(judge_prompt)
                    if final_verdict.candidates and len(final_verdict.candidates) > 0:
                        candidate = final_verdict.candidates[0]
                        if candidate.content and candidate.content.parts:
                            final_verdict_text = candidate.content.parts[0].text
                        else:
                            final_verdict_text = f"No verdict generated (finish_reason: {candidate.finish_reason})"
                    else:
                        final_verdict_text = "No verdict candidates generated"
                except Exception as e:
                    print(f"❌ Error generating verdict: {e}")
                    final_verdict_text = f"Error: {str(e)}"
                
                print(f"📝 Judge: {final_verdict_text[:150]}...")
                all_responses.append(final_verdict_text)
        
        execution_time = time.time() - start_time
        
        # Assess quality
        quality_scores = QualityRubric.assess_quality(final_verdict_text)
        
        # Check for convergence (simple heuristic)
        convergence = any(word in final_verdict_text.lower() for word in 
                         ['consensus', 'agreement', 'conclusion', 'verdict', 'decision'])
        
        # Extract key excerpts
        excerpts = [
            "Debate completed successfully",
            f"Final verdict: {final_verdict_text[:200]}..." if len(final_verdict_text) > 200 else f"Final verdict: {final_verdict_text}"
        ]
        
        return DebateResult(
            topic=topic,
            agents_count=agent_count,
            rounds=rounds,
            final_verdict=final_verdict_text,
            quality_scores=quality_scores,
            convergence=convergence,
            execution_time=execution_time,
            excerpts=excerpts
        )

def main():
    """Main function to run experiments."""
    print("🤖 Working Multi-Agent Debate System")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set your GOOGLE_API_KEY in a .env file")
        print("Copy env_example.txt to .env and add your API key")
        return
    
    # Initialize debate system
    debate_system = WorkingMultiAgentDebate()
    
    # Safe academic topic
    topic = "Should libraries invest more in digital resources or physical books?"
    
    print(f"\n📝 Topic: {topic}")
    print("\n🚀 Starting debate (2 agents, 2 rounds)...")
    
    try:
        result = debate_system.run_debate(topic, agent_count=2, rounds=2)
        
        # Display results
        print("\n📊 RESULTS")
        print("=" * 40)
        print(f"⏱️  Execution Time: {result.execution_time:.2f} seconds")
        print(f"🎯 Quality Scores:")
        for dimension, score in result.quality_scores.items():
            print(f"   {dimension.capitalize()}: {score:.1f}/5.0")
        print(f"🤝 Convergence: {'Yes' if result.convergence else 'No'}")
        
        print(f"\n📝 Final Verdict:")
        print("-" * 20)
        print(result.final_verdict)
        
    except Exception as e:
        print(f"❌ Error running debate: {e}")
        print("Make sure you have set your Google API key in .env")

if __name__ == "__main__":
    main()
