import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from pydantic import BaseModel

from database import db, CAREER_GOALS
from models import (
    UserProfile, CareerGoal, LearningModule, AgentLog,
    AssessmentSubmission, AssessmentResult, ChatRequest, ChatResponse
)
from agents import (
    ProfilerAgent, CurriculumArchitectAgent, AssessmentEvaluatorAgent, AIMentorOrchestrator
)

app = FastAPI(
    title="SkillForge AI Backend API",
    description="Multi-Agent Orchestration Engine for Personalized Learning Roadmaps & Self-Healing Loops",
    version="1.0.0"
)

# Enable CORS for frontend Vite dev server (e.g. localhost:5173 or any port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UpdateSkillsRequest(BaseModel):
    skills: List[str]

class SwitchGoalRequest(BaseModel):
    target_role: str

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "SkillForge AI Engine",
        "version": "1.0.0",
        "agents": [
            "Profiler Agent",
            "Curriculum Architect Agent",
            "Assessment Evaluator Agent",
            "AI Mentor Orchestrator"
        ]
    }

@app.get("/api/careers", response_model=Dict[str, CareerGoal])
def get_careers():
    return CAREER_GOALS

@app.get("/api/profile", response_model=UserProfile)
def get_profile():
    return db.profile

@app.post("/api/profile/update-skills")
def update_skills(req: UpdateSkillsRequest):
    db.profile.existing_skills = req.skills
    audit_res = ProfilerAgent.audit_profile(db.profile)
    return {
        "profile": db.profile,
        "gap_analysis": audit_res,
        "message": "Skills updated and profile re-audited by Profiler Agent."
    }

@app.post("/api/profile/switch-goal")
def switch_goal(req: SwitchGoalRequest):
    if req.target_role not in CAREER_GOALS:
        raise HTTPException(status_code=400, detail="Invalid career goal")
    
    # 1. Profiler Agent re-evaluates competencies
    audit = ProfilerAgent.audit_profile(db.profile, target_role_key=req.target_role)
    # 2. Curriculum Architect rebuilds roadmap
    new_roadmap = CurriculumArchitectAgent.generate_roadmap_for_role(req.target_role, db.profile.existing_skills)
    
    return {
        "profile": db.profile,
        "gap_analysis": audit,
        "roadmap": new_roadmap,
        "message": f"Successfully switched target career to {req.target_role}."
    }

@app.get("/api/skills/gap-analysis")
def get_gap_analysis():
    audit = ProfilerAgent.audit_profile(db.profile)
    return audit

@app.get("/api/roadmap", response_model=List[LearningModule])
def get_roadmap():
    return db.roadmap

@app.get("/api/assessments/{module_id}")
def get_assessment(module_id: str):
    for mod in db.roadmap:
        if mod.id == module_id:
            return {
                "module_id": mod.id,
                "module_title": mod.title,
                "questions": [
                    {
                        "id": q.id,
                        "text": q.text,
                        "code_snippet": q.code_snippet,
                        "options": q.options,
                        "concept_tag": q.concept_tag
                    }
                    for q in mod.questions
                ]
            }
    raise HTTPException(status_code=404, detail="Module not found")

@app.post("/api/assessments/{module_id}/submit", response_model=AssessmentResult)
def submit_assessment(module_id: str, sub: AssessmentSubmission):
    result = AssessmentEvaluatorAgent.evaluate(module_id, sub.answers)
    return result

@app.get("/api/agents/logs", response_model=List[AgentLog])
def get_agent_logs():
    return db.agent_logs

@app.get("/api/mentor/chat")
def get_chat_history():
    return {"history": db.chat_history}

@app.post("/api/mentor/chat", response_model=ChatResponse)
def chat_with_mentor(req: ChatRequest):
    response = AIMentorOrchestrator.chat(req.message, req.context)
    return response

@app.post("/api/reset")
def reset_system():
    db.reset()
    return {
        "status": "reset",
        "profile": db.profile,
        "roadmap": db.roadmap,
        "message": "System reset to demo baseline."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
