from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import reviews, analysis, reports, email, scheduler
from app.services.weekly_pulse_scheduler import get_scheduler
from app.services.review_importer import ReviewImporter

# Create FastAPI application
app = FastAPI(
    title="App Review Insights Analyzer",
    description="Generate weekly pulse reports from app store reviews using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(reviews.router)
app.include_router(analysis.router)
app.include_router(reports.router)
app.include_router(email.router)
app.include_router(scheduler.router)


# Start scheduler on application startup
@app.on_event("startup")
async def startup_event():
    """Initialize and start the weekly pulse scheduler and auto-import sample data"""
    try:
        # Start the weekly pulse scheduler
        scheduler_instance = get_scheduler()
        scheduler_instance.start()
        
        # Auto-import sample review data
        importer = ReviewImporter()
        sample_reviews = importer.auto_import_sample_data(weeks=settings.REVIEW_WEEKS_RANGE)
        
        if sample_reviews:
            # Add to the reviews database
            from app.routes.reviews import reviews_db
            reviews_db.extend(sample_reviews)
            print(f"✅ Auto-imported {len(sample_reviews)} sample reviews from sample_data directory")
        else:
            print("⚠️ No sample reviews found in sample_data directory")
            
    except Exception as e:
        print(f"Warning: Failed to complete startup initialization: {e}")


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "App Review Insights Analyzer API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with scheduler status and review count"""
    from app.routes.reviews import reviews_db
    
    scheduler_status = get_scheduler().get_scheduler_status()
    
    return {
        "status": "healthy",
        "groq_configured": bool(settings.GROQ_API_KEY),
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "smtp_configured": bool(settings.SENDER_EMAIL and settings.SENDER_PASSWORD),
        "scheduler_running": scheduler_status['is_running'],
        "next_scheduled_run": scheduler_status['next_run_formatted'],
        "reviews_loaded": len(reviews_db),
        "auto_import_enabled": True
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
