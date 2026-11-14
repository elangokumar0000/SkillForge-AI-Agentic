from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Skill(BaseModel):
    name: str
    category: str = "General"
    level: str = "Beginner"  # Beginner, Intermediate, Advanced
    is_acquired: bool = False

class CareerGoal(BaseModel):
    id: str
    title: str
    description: str
    required_skills: List[str]
    icon: str
    difficulty: str
    demand: str
    avg_salary: str

class ModuleResource(BaseModel):
    title: str
    type: str  # video, article, lab, doc
    url: str
    duration: str

class Question(BaseModel):
    id: str
    text: str
    code_snippet: Optional[str] = None
    options: List[str]
    correct_index: int
    explanation: str
    concept_tag: str

class LearningModule(BaseModel):
    id: str
    title: str
    description: str
    skills_covered: List[str]
    prerequisites: List[str] = []
    estimated_hours: int
    status: str = "locked"  # locked, in_progress, completed, remedial
    is_remedial: bool = False
    remedial_reason: Optional[str] = None
    resources: List[ModuleResource] = []
    questions: List[Question] = []
    score: Optional[int] = None
    order: int = 1

class UserProfile(BaseModel):
    id: str = "learner_001"
    name: str = "Alex Chen"
    avatar: str = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
    target_role: str = "Full Stack Developer"
    existing_skills: List[str] = ["Python", "SQL", "basic HTML"]
    missing_skills: List[str] = ["JavaScript", "React", "Node.js"]
    weekly_hours_commitment: int = 15
    readiness_score: int = 42

class AgentLog(BaseModel):
    id: str
    timestamp: str
    agent_name: str
    agent_role: str
    avatar: str
    action: str
    thought_process: str
    payload: Dict[str, Any] = {}
    status: str = "completed"  # working, completed, alert

class AssessmentSubmission(BaseModel):
    module_id: str
    answers: Dict[str, int]  # question_id -> selected option index

class AssessmentResult(BaseModel):
    module_id: str
    score: int
    passed: bool
    correct_count: int
    total_questions: int
    feedback: str
    weakness_identified: Optional[str] = None
    remedial_module_injected: bool = False
    remedial_module: Optional[LearningModule] = None
    agent_handoffs: List[Dict[str, str]] = []

class ChatMessage(BaseModel):
    sender: str
    text: str
    timestamp: str
    agent_name: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    agent_name: str
    thought_process: str
    roadmap_updated: bool = False
    updated_roadmap: Optional[List[LearningModule]] = None
