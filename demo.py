#!/usr/bin/env python3
"""
Demo script for Multi-Agent Debate System
Shows a quick example of the working system.
"""

import os
from multi_agent_debate import WorkingMultiAgentDebate

def main():
    """Run a quick demo of the debate system."""
    print("🎭 Multi-Agent Debate Demo")
    print("=" * 40)
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set your GOOGLE_API_KEY in a .env file")
        print("Copy env_example.txt to .env and add your API key")
        return
    
    # Initialize debate system
    print("🤖 Initializing debate system...")
    debate_system = WorkingMultiAgentDebate()
    
    # Demo topic
    topic = "Should libraries invest more in digital resources or physical books?"
    print(f"📝 Topic: {topic}")
    
    # Run a quick 2-agent, 2-round debate
    print("\n🚀 Starting debate (2 agents, 2 rounds)...")
    print("-" * 40)
    
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
        
        print(f"\n📋 Key Excerpts:")
        for i, excerpt in enumerate(result.excerpts, 1):
            print(f"   {i}. {excerpt}")
            
    except Exception as e:
        print(f"❌ Error running debate: {e}")
        print("Make sure you have set your Google API key in .env")

if __name__ == "__main__":
    main()