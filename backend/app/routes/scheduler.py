"""
Scheduler Routes

API endpoints to manage the automated weekly pulse report scheduler.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
from app.services.weekly_pulse_scheduler import get_scheduler

router = APIRouter(prefix="/api/scheduler", tags=["scheduler"])


@router.get("/status")
async def get_scheduler_status() -> Dict:
    """
    Get current status of the weekly pulse scheduler.
    
    Returns:
        Scheduler status including next run time and configuration
    """
    scheduler = get_scheduler()
    return scheduler.get_scheduler_status()


@router.post("/start")
async def start_scheduler() -> Dict:
    """
    Start the weekly pulse scheduler.
    
    Returns:
        Confirmation message with next run time
    """
    try:
        scheduler = get_scheduler()
        scheduler.start()
        
        status = scheduler.get_scheduler_status()
        
        return {
            "success": True,
            "message": "Weekly pulse scheduler started successfully",
            "schedule": status['schedule'],
            "next_run": status['next_run_formatted'],
            "recipient": status['recipient_email']
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start scheduler: {str(e)}"
        )


@router.post("/stop")
async def stop_scheduler() -> Dict:
    """
    Stop the weekly pulse scheduler.
    
    Returns:
        Confirmation message
    """
    try:
        scheduler = get_scheduler()
        scheduler.stop()
        
        return {
            "success": True,
            "message": "Weekly pulse scheduler stopped successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop scheduler: {str(e)}"
        )


@router.post("/trigger-now")
async def trigger_weekly_pulse_now() -> Dict:
    """
    Trigger immediate generation and sending of weekly pulse report.
    Useful for testing without waiting for scheduled time.
    
    Returns:
        Confirmation message
    """
    try:
        scheduler = get_scheduler()
        
        # Run the job immediately
        await scheduler.generate_and_send_weekly_pulse()
        
        return {
            "success": True,
            "message": f"Weekly pulse report generated and sent to {scheduler.recipient_email}",
            "recipient": scheduler.recipient_email
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger weekly pulse: {str(e)}"
        )
