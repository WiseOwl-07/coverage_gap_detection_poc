"""FastAPI routes for the coverage gap analysis API."""
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Optional
import json

from app.core.models import PolicyInput, AnalysisResult
from app.agents.orchestrator import Orchestrator
from app.utils.policy_parser import parse_policy_file
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
orchestrator = Orchestrator()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Coverage Gap Detection API"}


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_coverage(
    policy_file: Optional[UploadFile] = File(None),
    policy_json: Optional[str] = None
):
    """
    Analyze policy for coverage gaps.
    
    Args:
        policy_file: Optional uploaded policy file (JSON or PDF)
        policy_json: Optional JSON string with policy data
    
    Returns:
        AnalysisResult with identified coverage gaps
    """
    try:
        # Parse policy input
        if policy_file:
            content = await policy_file.read()
            policy_input = parse_policy_file(file_content=content.decode('utf-8'))
        elif policy_json:
            policy_input = parse_policy_file(file_content=policy_json)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either policy_file or policy_json must be provided"
            )
        
        logger.info(f"Received policy analysis request for {policy_input.policy_number}")
        
        # Run analysis
        result = orchestrator.analyze_policy(policy_input)
        
        logger.info(f"Analysis completed: {result.total_gaps_found} gaps found")
        
        return result
        
    except ValueError as e:
        logger.error(f"Invalid policy data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze-json", response_model=AnalysisResult)
async def analyze_coverage_json(policy_input: PolicyInput):
    """
    Analyze policy for coverage gaps (accepts PolicyInput model directly).
    
    Args:
        policy_input: PolicyInput model with customer and coverage data
    
    Returns:
        AnalysisResult with identified coverage gaps
    """
    try:
        logger.info(f"Received policy analysis request for {policy_input.policy_number}")
        
        # Run analysis
        result = orchestrator.analyze_policy(policy_input)
        
        logger.info(f"Analysis completed: {result.total_gaps_found} gaps found")
        
        return result
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
