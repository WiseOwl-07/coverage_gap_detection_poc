"""Quick test script to verify the coverage gap detection system."""
import sys
from pathlib import Path
import json

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.orchestrator import Orchestrator
from app.utils.policy_parser import parse_policy_file

def test_analysis():
    """Test the coverage gap analysis with a sample policy."""
    print("\n" + "="*60)
    print("Coverage Gap Detection POC - Test Run")
    print("="*60 + "\n")
    
    # Load sample policy
    sample_path = "app/data/sample_policies/high_networth_miami.json"
    print(f"📄 Loading sample policy: {sample_path}")
    
    policy_input = parse_policy_file(file_path=sample_path)
    print(f"✅ Policy loaded: {policy_input.policy_number}")
    print(f"   Customer: {policy_input.customer_profile.name}")
    print(f"   Location: ZIP {policy_input.customer_profile.zip_code}")
    print(f"   Existing coverages: {len(policy_input.existing_coverages)}\n")
    
    # Run analysis
    print("🤖 Starting AI agent analysis...")
    print("   This may take 10-20 seconds...\n")
    
    orchestrator = Orchestrator()
    result = orchestrator.analyze_policy(policy_input)
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 ANALYSIS RESULTS")
    print("="*60 + "\n")
    
    print(f"Policy: {result.policy_number}")
    print(f"Customer: {result.customer_name}")
    print(f"Gaps Found: {result.total_gaps_found}")
    print(f"Total Premium Impact: ${result.total_estimated_premium_impact:,.2f}/year\n")
    
    print(f"Summary: {result.analysis_summary}\n")
    
    if result.coverage_gaps:
        print("-" * 60)
        for i, gap in enumerate(result.coverage_gaps, 1):
            print(f"\n{i}. {gap.title}")
            print(f"   Severity: {gap.severity.value}")
            print(f"   Type: {gap.gap_type.value}")
            print(f"   Explanation: {gap.explanation}")
            print(f"   Recommendation: {gap.recommendation}")
            if gap.estimated_annual_premium:
                print(f"   Premium: ${gap.estimated_annual_premium:,.2f}/year")
            if gap.risk_factors:
                print(f"   Risk Factors: {', '.join(gap.risk_factors)}")
        print("\n" + "-" * 60)
    
    print("\n✅ Test completed successfully!")
    print("\n" + "="*60)
    
    return result


if __name__ == "__main__":
    try:
        result = test_analysis()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
