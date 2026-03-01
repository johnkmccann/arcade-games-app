import logging
import json
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.api.routes import games
from app.services.games import register_default_games

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Register games on startup
@app.on_event("startup")
async def startup_event():
    """Initialize games on startup"""
    logger.info("\n" + "="*80)
    logger.info("🎮 STARTUP: Registering default games...")
    register_default_games()
    logger.info("✅ Games registered successfully")
    logger.info("="*80 + "\n")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses"""
    start_time = time.time()
    
    # Log request
    method = request.method
    path = request.url.path
    query_params = dict(request.query_params) if request.query_params else {}
    
    # Try to read the body
    body = None
    if method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
            if body:
                body = body.decode('utf-8')
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    pass  # Keep as string if not JSON
        except:
            pass
    
    # Log request details
    request_info = f"\n{'='*80}\n📨 INCOMING REQUEST\n{'='*80}\n"
    request_info += f"  Method: {method}\n"
    request_info += f"  Path: {path}\n"
    if query_params:
        request_info += f"  Query Params: {json.dumps(query_params, indent=2)}\n"
    if body:
        if isinstance(body, dict):
            request_info += f"  Body: {json.dumps(body, indent=2)}\n"
        else:
            request_info += f"  Body: {body}\n"
    
    logger.info(request_info)
    
    # Call the endpoint
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log response
        response_info = f"\n📤 RESPONSE\n"
        response_info += f"  Status: {response.status_code}\n"
        response_info += f"  Duration: {duration:.3f}s\n"
        
        # Try to read response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        if response_body:
            try:
                response_data = json.loads(response_body.decode('utf-8'))
                response_info += f"  Body: {json.dumps(response_data, indent=2)}\n"
            except:
                response_info += f"  Body: {response_body.decode('utf-8', errors='ignore')}\n"
        
        response_info += f"{'='*80}\n"
        logger.info(response_info)
        
        # Return response with body re-attached
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    except Exception as e:
        duration = time.time() - start_time
        error_info = f"\n❌ ERROR\n"
        error_info += f"  Duration: {duration:.3f}s\n"
        error_info += f"  Exception: {type(e).__name__}\n"
        error_info += f"  Message: {str(e)}\n"
        error_info += f"  Details: {repr(e)}\n"
        error_info += f"{'='*80}\n"
        logger.error(error_info, exc_info=True)
        raise


# Include routers
app.include_router(games.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Arcade Games API!"}