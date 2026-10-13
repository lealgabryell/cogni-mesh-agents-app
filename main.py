from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
from app.graph.builder import cognimesh_app
from app.core.config import settings
from app.core.utils import content_to_text

# Define Request and Response Schemas
class ArticleRequest(BaseModel):
    topic: str

class ArticleResponse(BaseModel):
    topic: str
    final_output: str
    revisions_made: int
    research_data_points: int

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Autonomous Multi-Agent Content Engine API",
    version="1.0.0"
)

# Configure CORS (Crucial for future Frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with your frontend URL (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the primary endpoint
@app.post(f"{settings.API_V1_STR}/generate-article", response_model=ArticleResponse)
async def generate_article(request: ArticleRequest):
    """
    Triggers the CogniMesh multi-agent workflow to research, draft, 
    review, and format a technical article based on a given topic.
    """
    try:
        # Prepare the initial state
        initial_state = {
            "topic": request.topic,
            "research_data": [],
            "draft_content": "",
            "review_feedback": "",
            "revision_count": 0,
            "is_approved": False,
            "final_output": ""
        }
        
        # Execute the LangGraph workflow
        # Note: This is a synchronous call that runs multiple LLMs, so it might take 15-30 seconds.
        print(f"\n🚀 API REQUEST RECEIVED: Starting workflow for '{request.topic}'\n")
        final_state = cognimesh_app.invoke(initial_state)
        
        # Return the structured response to the frontend
        return ArticleResponse(
            topic=final_state["topic"],
            final_output=final_state["final_output"],
            revisions_made=final_state["revision_count"],
            research_data_points=len(final_state.get("research_data", []))
        )
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

# Define the download endpoint for the generated article
@app.post(f"{settings.API_V1_STR}/generate-article/download", response_class=Response)
async def generate_article_download(request: ArticleRequest):
    """
    Executa o fluxo e retorna um arquivo .md pronto para ser baixado e aberto em qualquer editor.
    """
    try:
        initial_state = {
            "topic": request.topic,
            "research_data": [],
            "draft_content": "",
            "review_feedback": "",
            "revision_count": 0,
            "is_approved": False,
            "final_output": ""
        }
        
        final_state = cognimesh_app.invoke(initial_state)
        clean_output = content_to_text(final_state["final_output"])
        
        # Gera nome do arquivo amigável
        filename = request.topic.lower().replace(" ", "_")[:30] + ".md"
        
        return Response(
            content=clean_output,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health Check endpoint
@app.get("/health")
def health_check():
    """Simple endpoint to verify if the API is running."""
    return {"status": "online", "project": settings.PROJECT_NAME}