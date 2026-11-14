import datetime
import uuid
from typing import Dict, List, Any, Optional
from database import db, CAREER_GOALS
from models import AgentLog, LearningModule, ModuleResource, Question, UserProfile, AssessmentResult

class ProfilerAgent:
    """Audits learner skills, computes role fit percentage, and identifies critical competency gaps."""
    NAME = "Profiler Agent"
    ROLE = "Competency Auditor & Gap Diagnostician"
    AVATAR = "🔍"

    @classmethod
    def audit_profile(cls, profile: UserProfile, target_role_key: Optional[str] = None) -> Dict[str, Any]:
        role_name = target_role_key or profile.target_role
        career = CAREER_GOALS.get(role_name)
        if not career:
            role_name = "Full Stack Developer"
            career = CAREER_GOALS[role_name]

        required = [s.strip().lower() for s in career.required_skills]
        existing = [s.strip().lower() for s in profile.existing_skills]

        # Case-insensitive substring/token match
        matched = []
        missing = []
        for req in career.required_skills:
            req_l = req.lower()
            if any(req_l in ex or ex in req_l for ex in existing):
                matched.append(req)
            else:
                missing.append(req)

        readiness = int((len(matched) / max(len(career.required_skills), 1)) * 100)
        profile.readiness_score = readiness
        profile.target_role = role_name
        profile.missing_skills = missing

        # Log agent thinking
        log_entry = AgentLog(
            id=f"log_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
            agent_name=cls.NAME,
            agent_role=cls.ROLE,
            avatar=cls.AVATAR,
            action="PROFILE_AUDIT_COMPLETED",
            thought_process=(
                f"Evaluated learner profile against '{role_name}'. "
                f"Matched {len(matched)}/{len(career.required_skills)} core competencies. "
                f"Identified {len(missing)} critical missing skills: {', '.join(missing[:4])}. "
                f"Calculated readiness score at {readiness}%. Handoff to Curriculum Architect initiated."
            ),
            payload={
                "target_role": role_name,
                "readiness_score": readiness,
                "matched_count": len(matched),
                "missing_skills": missing,
                "demand": career.demand
            },
            status="completed"
        )
        db.agent_logs.insert(0, log_entry)

        return {
            "target_role": role_name,
            "readiness_score": readiness,
            "matched_skills": matched,
            "missing_skills": missing,
            "career_details": career.model_dump()
        }

class CurriculumArchitectAgent:
    """Builds and dynamically re-sequences the dependency-ordered learning roadmap."""
    NAME = "Curriculum Architect Agent"
    ROLE = "Dependency Graph & Milestone Planner"
    AVATAR = "📐"

    @classmethod
    def generate_roadmap_for_role(cls, role_name: str, existing_skills: List[str]) -> List[LearningModule]:
        from database import get_initial_roadmap
        career = CAREER_GOALS.get(role_name)
        if not career or role_name == "Full Stack Developer":
            roadmap = get_initial_roadmap()
        elif role_name == "Backend Engineer":
            roadmap = [
                LearningModule(
                    id="be_mod_1",
                    title="Python Deep Dive: AsyncIO, Typing & Metaclasses",
                    description="Advanced Python patterns, generators, concurrency models, and typing protocols.",
                    skills_covered=["Python", "AsyncIO", "OOP"],
                    estimated_hours=12,
                    status="completed",
                    score=92,
                    order=1,
                    resources=[
                        ModuleResource(title="RealPython: AsyncIO in Practice", type="article", url="https://realpython.com/async-io-python/", duration="45 mins"),
                        ModuleResource(title="Python Concurrency Lab", type="lab", url="https://docs.python.org/3/library/asyncio.html", duration="2 hrs")
                    ],
                    questions=[]
                ),
                LearningModule(
                    id="be_mod_2",
                    title="Relational Schema Design & PostgreSQL Optimization",
                    description="ACID transactions, B-Tree indexes, EXPLAIN ANALYZE query planning, and connection pooling.",
                    skills_covered=["SQL", "PostgreSQL", "Database Design"],
                    estimated_hours=16,
                    status="in_progress",
                    score=None,
                    order=2,
                    resources=[
                        ModuleResource(title="High Performance Postgres Indexing", type="article", url="https://use-the-index-luke.com", duration="40 mins"),
                        ModuleResource(title="Postgres EXPLAIN ANALYZE Lab", type="lab", url="https://pgmustard.com", duration="90 mins")
                    ],
                    questions=[
                        Question(
                            id="q_be_1",
                            text="What type of PostgreSQL index is best suited for equality and range queries on sequential numerical data?",
                            options=["B-Tree", "Hash Index", "GIN Index", "BRIN Index"],
                            correct_index=0,
                            explanation="B-Tree indexes are the default and optimal for equality (=) and range queries (<, <=, >, >=).",
                            concept_tag="Database Indexing"
                        ),
                        Question(
                            id="q_be_2",
                            text="In PostgreSQL, what problem does connection pooling solve?",
                            options=[
                                "It reduces overhead of expensive TCP handshakes and per-connection memory allocations in Postgres's process-based architecture",
                                "It automatically converts SQL queries to NoSQL",
                                "It replaces the write-ahead log (WAL)",
                                "It bypasses query syntax validation"
                            ],
                            correct_index=0,
                            explanation="PostgreSQL spawns an OS process per client connection. A pooler like PgBouncer reuses persistent connections to avoid heavy process creation overhead.",
                            concept_tag="Connection Pooling"
                        ),
                        Question(
                            id="q_be_3",
                            text="Which transaction isolation level prevents dirty reads, non-repeatable reads, and phantom reads?",
                            options=["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"],
                            correct_index=3,
                            explanation="Serializable isolation guarantees complete transaction serializability, preventing all read anomalies including phantom reads.",
                            concept_tag="Transaction Isolation"
                        )
                    ]
                ),
                LearningModule(
                    id="be_mod_3",
                    title="Scalable Microservices with FastAPI & Redis Caching",
                    description="Design REST/gRPC endpoints, background tasks, Redis cache eviction strategies, and rate limiting.",
                    skills_covered=["FastAPI", "Redis", "Microservices Architecture"],
                    estimated_hours=20,
                    status="locked",
                    score=None,
                    order=3,
                    resources=[
                        ModuleResource(title="FastAPI Production Architecture", type="video", url="https://fastapi.tiangolo.com", duration="50 mins")
                    ],
                    questions=[]
                ),
                LearningModule(
                    id="be_mod_4",
                    title="Distributed Systems, Message Queues & Docker",
                    description="Implement RabbitMQ/Kafka event streaming, eventual consistency, Docker Compose environments, and system design patterns.",
                    skills_covered=["Docker", "Message Queues", "System Design"],
                    estimated_hours=24,
                    status="locked",
                    score=None,
                    order=4,
                    resources=[],
                    questions=[]
                )
            ]
        elif role_name == "AI/ML Engineer":
            roadmap = [
                LearningModule(
                    id="ai_mod_1",
                    title="Scientific Computing with NumPy, Pandas & Vector Math",
                    description="Vectorized operations, broadcasting, tensor manipulation, and exploratory data analysis.",
                    skills_covered=["Python", "NumPy", "Pandas"],
                    estimated_hours=14,
                    status="completed",
                    score=96,
                    order=1,
                    resources=[],
                    questions=[]
                ),
                LearningModule(
                    id="ai_mod_2",
                    title="Deep Learning Foundations with PyTorch & Gradient Descent",
                    description="Neural network architectures, autograd, backpropagation, activation functions, and PyTorch tensors.",
                    skills_covered=["PyTorch", "Deep Learning", "TensorFlow"],
                    estimated_hours=22,
                    status="in_progress",
                    score=None,
                    order=2,
                    resources=[
                        ModuleResource(title="PyTorch Neural Networks from Scratch", type="video", url="https://pytorch.org/tutorials/", duration="60 mins")
                    ],
                    questions=[
                        Question(
                            id="q_ai_1",
                            text="In PyTorch, what is the role of `loss.backward()` during neural network training?",
                            options=[
                                "It computes the gradients of the loss with respect to all graph leaves (weights) using automatic differentiation",
                                "It immediately updates the weight values using the Adam optimizer",
                                "It resets all gradients to zero",
                                "It normalizes the batch data across channels"
                            ],
                            correct_index=0,
                            explanation="`loss.backward()` traverses the autograd computation graph backwards to compute gradients dLoss/dw for each parameter.",
                            concept_tag="PyTorch Autograd"
                        ),
                        Question(
                            id="q_ai_2",
                            text="Why is the ReLU activation function widely preferred over Sigmoid in deep hidden layers?",
                            options=[
                                "It mitigates the vanishing gradient problem for positive inputs and is computationally fast",
                                "It constrains outputs strictly between -1 and +1",
                                "It eliminates the need for learning rate schedulers",
                                "It is differentiable at x = 0"
                            ],
                            correct_index=0,
                            explanation="Sigmoid saturates at 0 and 1 with tiny derivative, causing vanishing gradients in deep networks. ReLU has constant derivative of 1 for x > 0.",
                            concept_tag="Activation Functions"
                        ),
                        Question(
                            id="q_ai_3",
                            text="What technique prevents deep neural networks from overfitting on small training datasets?",
                            options=["Dropout and L2 weight decay", "Increasing model parameters 10x", "Removing validation sets", "Setting learning rate to 10.0"],
                            correct_index=0,
                            explanation="Dropout randomly deactivates neurons during training, enforcing redundant feature learning and reducing overfitting along with L2 regularization.",
                            concept_tag="Regularization"
                        )
                    ]
                ),
                LearningModule(
                    id="ai_mod_3",
                    title="Generative AI: LLM Fine-Tuning, LoRA & Vector RAG",
                    description="Build Retrieval-Augmented Generation (RAG) with Chroma/Pinecone, embeddings, chunking, and LoRA PEFT fine-tuning.",
                    skills_covered=["LLM Orchestration & RAG", "Vector DBs", "Prompt Engineering"],
                    estimated_hours=24,
                    status="locked",
                    score=None,
                    order=3,
                    resources=[],
                    questions=[]
                ),
                LearningModule(
                    id="ai_mod_4",
                    title="MLOps: Model Quantization, ONNX & Production Serving",
                    description="Quantize models (GGUF/AWQ), serve with vLLM/Triton, implement latency benchmarking and drift monitoring.",
                    skills_covered=["Model Deployment", "MLOps", "vLLM"],
                    estimated_hours=20,
                    status="locked",
                    score=None,
                    order=4,
                    resources=[],
                    questions=[]
                )
            ]
        else: # Cybersecurity Analyst
            roadmap = [
                LearningModule(
                    id="sec_mod_1",
                    title="TCP/IP Network Protocols & Packet Analysis",
                    description="Deep packet inspection with Wireshark, OSI layers, DNS/TLS handshake analysis, and subnetting.",
                    skills_covered=["Network Security", "Linux & Bash"],
                    estimated_hours=14,
                    status="completed",
                    score=90,
                    order=1,
                    resources=[],
                    questions=[]
                ),
                LearningModule(
                    id="sec_mod_2",
                    title="Web Application Security & OWASP Top 10 Exploitation",
                    description="Hands-on SQL injection, XSS, CSRF, SSRF, broken access control, and defense-in-depth mitigation.",
                    skills_covered=["OWASP Top 10", "Vulnerability Assessment", "Web Security"],
                    estimated_hours=18,
                    status="in_progress",
                    score=None,
                    order=2,
                    resources=[
                        ModuleResource(title="PortSwigger Web Security Academy: SQLi & XSS", type="lab", url="https://portswigger.net/web-security", duration="90 mins")
                    ],
                    questions=[
                        Question(
                            id="q_sec_1",
                            text="What is the most effective defense against SQL Injection vulnerabilities?",
                            options=[
                                "Parameterized queries (prepared statements) with bound variables",
                                "Base64 encoding client input before sending to database",
                                "Filtering out the word 'SELECT' with regex",
                                "Disabling client-side JavaScript execution"
                            ],
                            correct_index=0,
                            explanation="Parameterized queries ensure that user input is treated strictly as data, never executable SQL commands, completely neutralizing injection attacks.",
                            concept_tag="SQL Injection Defense"
                        ),
                        Question(
                            id="q_sec_2",
                            text="Which HTTP response header tells modern browsers to strictly disallow loading inside an iframe to prevent clickjacking?",
                            options=["X-Frame-Options: DENY", "Access-Control-Allow-Origin: *", "Content-Type: text/html", "Cache-Control: no-cache"],
                            correct_index=0,
                            explanation="X-Frame-Options: DENY (and CSP frame-ancestors 'none') prevents any domain from framing the content, protecting against clickjacking attacks.",
                            concept_tag="Clickjacking Mitigation"
                        ),
                        Question(
                            id="q_sec_3",
                            text="What is the core distinction between Stored (Persistent) XSS and Reflected XSS?",
                            options=[
                                "Stored XSS payload is permanently persisted on the server database, executing for every visitor who loads the page",
                                "Reflected XSS only affects mobile browsers",
                                "Stored XSS requires physical access to the server hardware",
                                "Reflected XSS cannot steal authentication session cookies"
                            ],
                            correct_index=0,
                            explanation="In Stored XSS, malicious payload is saved to server storage (e.g. comment database) and rendered into pages for subsequent users.",
                            concept_tag="Cross-Site Scripting (XSS)"
                        )
                    ]
                ),
                LearningModule(
                    id="sec_mod_3",
                    title="Applied Cryptography & Public Key Infrastructure (PKI)",
                    description="AES symmetric encryption, RSA/ECC asymmetric pairs, hashing with SHA-256/bcrypt, and certificate validation.",
                    skills_covered=["Cryptography", "PKI", "Auth Protocols"],
                    estimated_hours=16,
                    status="locked",
                    score=None,
                    order=3,
                    resources=[],
                    questions=[]
                ),
                LearningModule(
                    id="sec_mod_4",
                    title="SIEM Threat Hunting, SOC Operations & Incident Response",
                    description="Log ingestion with Elastic/Splunk, writing YARA rules, detecting lateral movement, and incident containment.",
                    skills_covered=["SIEM & Incident Response", "Threat Hunting"],
                    estimated_hours=20,
                    status="locked",
                    score=None,
                    order=4,
                    resources=[],
                    questions=[]
                )
            ]

        db.roadmap = roadmap

        log_entry = AgentLog(
            id=f"log_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
            agent_name=cls.NAME,
            agent_role=cls.ROLE,
            avatar=cls.AVATAR,
            action="CURRICULUM_PIVOTED",
            thought_process=(
                f"Generated customized learning graph for target track '{role_name}'. "
                f"Constructed {len(roadmap)} dependency-ordered modules. "
                f"Active learning gate set to Module #{2}: '{roadmap[1].title}'. "
                f"Synchronized with AI Mentor Orchestrator for proactive checkpoint monitoring."
            ),
            payload={
                "target_role": role_name,
                "total_modules": len(roadmap),
                "active_module": roadmap[1].title if len(roadmap) > 1 else roadmap[0].title
            },
            status="completed"
        )
        db.agent_logs.insert(0, log_entry)

        return roadmap

class AssessmentEvaluatorAgent:
    """Evaluates question submissions, calculates score, and triggers self-healing on failure."""
    NAME = "Assessment Evaluator Agent"
    ROLE = "Mastery Verification & Diagnostic Evaluator"
    AVATAR = "⚖️"

    @classmethod
    def evaluate(cls, module_id: str, answers: Dict[str, int]) -> AssessmentResult:
        # Find module
        target_mod = None
        target_idx = -1
        for idx, mod in enumerate(db.roadmap):
            if mod.id == module_id:
                target_mod = mod
                target_idx = idx
                break

        if not target_mod or not target_mod.questions:
            # Fallback mock evaluation
            return AssessmentResult(
                module_id=module_id,
                score=100,
                passed=True,
                correct_count=3,
                total_questions=3,
                feedback="Assessment completed successfully."
            )

        total_q = len(target_mod.questions)
        correct_count = 0
        weaknesses = []

        for q in target_mod.questions:
            user_ans = answers.get(q.id)
            if user_ans is not None and user_ans == q.correct_index:
                correct_count += 1
            else:
                weaknesses.append(q.concept_tag)

        score_pct = int((correct_count / total_q) * 100)
        passed = score_pct >= 60

        target_mod.score = score_pct

        handoffs = []

        if passed:
            target_mod.status = "completed"
            # Unlock next module
            if target_idx + 1 < len(db.roadmap):
                if db.roadmap[target_idx + 1].status == "locked":
                    db.roadmap[target_idx + 1].status = "in_progress"

            # Add newly mastered skills to user profile
            for sk in target_mod.skills_covered:
                if sk not in db.profile.existing_skills:
                    db.profile.existing_skills.append(sk)
                if sk in db.profile.missing_skills:
                    db.profile.missing_skills.remove(sk)

            # Re-audit profile with ProfilerAgent
            audit = ProfilerAgent.audit_profile(db.profile)

            # Log evaluator reasoning
            eval_log = AgentLog(
                id=f"log_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
                agent_name=cls.NAME,
                agent_role=cls.ROLE,
                avatar=cls.AVATAR,
                action="ASSESSMENT_PASSED",
                thought_process=(
                    f"Verified module '{target_mod.title}' assessment. "
                    f"Learner scored {score_pct}% ({correct_count}/{total_q} correct). "
                    f"Threshold (60%) surpassed. Module marked COMPLETED. "
                    f"Unlocked downstream milestone '{db.roadmap[target_idx + 1].title if target_idx + 1 < len(db.roadmap) else 'Certification'}'. "
                    f"Updated skills inventory and notified AI Mentor Orchestrator."
                ),
                payload={
                    "module_id": module_id,
                    "score": score_pct,
                    "passed": True,
                    "skills_awarded": target_mod.skills_covered
                },
                status="completed"
            )
            db.agent_logs.insert(0, eval_log)

            handoffs.append({
                "from": cls.NAME,
                "to": AIMentorOrchestrator.NAME,
                "signal": "MILESTONE_UNLOCKED",
                "details": f"Learner mastered {target_mod.title} with {score_pct}% score."
            })

            return AssessmentResult(
                module_id=module_id,
                score=score_pct,
                passed=True,
                correct_count=correct_count,
                total_questions=total_q,
                feedback=f"Excellent work! You demonstrated mastery with {score_pct}%. The next learning stage is now unlocked.",
                remedial_module_injected=False,
                agent_handoffs=handoffs
            )

        else:
            # FAILED (< 60%) -> TRIGGER SELF-HEALING LOOP
            weakness_summary = ", ".join(weaknesses) if weaknesses else "Foundational execution logic"
            
            # Log evaluator alert
            eval_log = AgentLog(
                id=f"log_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
                agent_name=cls.NAME,
                agent_role=cls.ROLE,
                avatar=cls.AVATAR,
                action="ASSESSMENT_FAILED_ALERT",
                thought_process=(
                    f"CRITICAL DIAGNOSTIC ALERT: Learner scored {score_pct}% ({correct_count}/{total_q} correct) on '{target_mod.title}'. "
                    f"Falling below mastery threshold (60%). Diagnosed severe gaps in: {weakness_summary}. "
                    f"EMERGENCY HANDOFF TO AI MENTOR ORCHESTRATOR to trigger automated self-healing remediation pipeline."
                ),
                payload={
                    "module_id": module_id,
                    "score": score_pct,
                    "passed": False,
                    "weaknesses": weaknesses,
                    "handoff_target": AIMentorOrchestrator.NAME
                },
                status="alert"
            )
            db.agent_logs.insert(0, eval_log)

            # Delegate to AI Mentor Orchestrator to inject remedial module
            remedial_mod = AIMentorOrchestrator.inject_remedial_module(
                failed_module=target_mod,
                failed_index=target_idx,
                weaknesses=weaknesses,
                score=score_pct
            )

            handoffs.append({
                "from": cls.NAME,
                "to": AIMentorOrchestrator.NAME,
                "signal": "SELF_HEALING_DISPATCH",
                "details": f"Sub-threshold score ({score_pct}%). Dispatched remediation requirement for {weakness_summary}."
            })

            return AssessmentResult(
                module_id=module_id,
                score=score_pct,
                passed=False,
                correct_count=correct_count,
                total_questions=total_q,
                feedback=(
                    f"Score: {score_pct}%. To ensure solid mastery, the AI Mentor Orchestrator has activated the Self-Healing Loop "
                    f"and automatically inserted a targeted Remedial Foundational Module into your roadmap before advancing."
                ),
                weakness_identified=weakness_summary,
                remedial_module_injected=True,
                remedial_module=remedial_mod,
                agent_handoffs=handoffs
            )

class AIMentorOrchestrator:
    """Supervises the learning journey, executes self-healing remediation, and converses with learner."""
    NAME = "AI Mentor Orchestrator"
    ROLE = "Cognitive Coach & Self-Healing Sentinel"
    AVATAR = "🧠"

    @classmethod
    def inject_remedial_module(cls, failed_module: LearningModule, failed_index: int, weaknesses: List[str], score: int) -> LearningModule:
        remedial_id = f"remedial_{uuid.uuid4().hex[:6]}"
        weak_str = " & ".join(weaknesses[:2]) if weaknesses else "Foundations"

        remedial_mod = LearningModule(
            id=remedial_id,
            title=f"🚨 Remedial Lab: {weak_str} Deep Dive",
            description=(
                f"Automated Self-Healing Module synthesized by AI Mentor Orchestrator following assessment score of {score}%. "
                f"Focused on bridging identified diagnostic misconceptions: {', '.join(weaknesses)}."
            ),
            skills_covered=[f"Remedial: {w}" for w in weaknesses] or ["Concept Review"],
            prerequisites=[failed_module.title],
            estimated_hours=6,
            status="in_progress",
            is_remedial=True,
            remedial_reason=f"Triggered by score of {score}% on {failed_module.title} (Weakness: {', '.join(weaknesses)})",
            score=None,
            order=failed_module.order + 1,
            resources=[
                ModuleResource(
                    title=f"Visual Interactive Guide: Demystifying {weak_str}",
                    type="video",
                    url="https://javascript.info",
                    duration="25 mins"
                ),
                ModuleResource(
                    title="Hands-on Step-by-Step Debugging Sandbox",
                    type="lab",
                    url="https://codepen.io",
                    duration="45 mins"
                ),
                ModuleResource(
                    title="Cheat Sheet: Common Pitfalls & Edge Cases",
                    type="article",
                    url="https://developer.mozilla.org",
                    duration="20 mins"
                )
            ],
            questions=[
                Question(
                    id=f"q_rem_1_{remedial_id}",
                    text=f"Remedial Concept Check: When dealing with {weak_str}, what is the foundational mental model to remember?",
                    options=[
                        "Call stack executes synchronously; asynchronous callbacks wait in queues (microtasks drain first, then macrotasks)",
                        "Code executes in completely random parallel threads without deterministic order",
                        "Async operations bypass memory management entirely",
                        "JavaScript locks the CPU until network requests complete"
                    ],
                    correct_index=0,
                    explanation="JavaScript is single-threaded; sync code finishes on the call stack before microtasks (Promises) and macrotasks (timers) are dequeued.",
                    concept_tag="Execution Model"
                ),
                Question(
                    id=f"q_rem_2_{remedial_id}",
                    text="How can you guarantee error handling in asynchronous Promise chains?",
                    options=[
                        "Using `.catch()` or wrapping `await` calls inside `try ... catch` blocks",
                        "Omitting `return` statements from arrow functions",
                        "Using `console.error` inside a synchronous loop",
                        "Promises cannot fail in modern V8 engines"
                    ],
                    correct_index=0,
                    explanation="Using `.catch()` or `try ... catch` blocks with async/await guarantees unhandled promise rejections are cleanly trapped.",
                    concept_tag="Async Error Handling"
                ),
                Question(
                    id=f"q_rem_3_{remedial_id}",
                    text="Why does an inner function retain access to variables declared in its outer scope even after the outer function has returned?",
                    options=[
                        "Due to Lexical Closures, where the inner function maintains an internal reference to the outer lexical environment record",
                        "Because the browser writes the variables to disk cookies",
                        "Because all JavaScript variables are globally static",
                        "Because the garbage collector runs only on page reload"
                    ],
                    correct_index=0,
                    explanation="Closures retain an active reference to the outer scope's Lexical Environment record, preventing garbage collection.",
                    concept_tag="Lexical Scope Retention"
                )
            ]
        )

        # Re-sequence roadmap: mark the failed module as 'needs_remediation' or keep in_progress,
        # and insert the remedial module immediately after it!
        # Re-order the rest
        insert_pos = failed_index + 1
        db.roadmap.insert(insert_pos, remedial_mod)
        for i, mod in enumerate(db.roadmap):
            mod.order = i + 1

        # Lock downstream modules until remedial module is completed
        for mod in db.roadmap[insert_pos + 1:]:
            mod.status = "locked"

        # Log AI Mentor self-healing action
        mentor_log = AgentLog(
            id=f"log_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
            agent_name=cls.NAME,
            agent_role=cls.ROLE,
            avatar=cls.AVATAR,
            action="SELF_HEALING_MODULE_INJECTED",
            thought_process=(
                f"INTERCEPTED FAILURE SIGNAL from Assessment Evaluator. "
                f"Synthesized targeted remedial module '{remedial_mod.title}' tailored to weaknesses: {', '.join(weaknesses)}. "
                f"Auto-injected into roadmap position #{insert_pos + 1}. "
                f"Locked downstream modules to prevent learning debt accumulation. "
                f"Sent notification to learner's AI Mentor chat panel."
            ),
            payload={
                "injected_module_id": remedial_id,
                "title": remedial_mod.title,
                "position": insert_pos + 1,
                "targeted_weaknesses": weaknesses
            },
            status="completed"
        )
        db.agent_logs.insert(0, mentor_log)

        # Add message to chat history
        db.chat_history.append({
            "sender": "mentor",
            "text": (
                f"⚠️ **Self-Healing Intercept**: You scored {score}% on '{failed_module.title}'. "
                f"No worries at all—this is where real learning happens! "
                f"I've analyzed your responses and diagnosed a specific gap in **{weak_str}**. "
                f"I have automatically injected a customized **Remedial Lab** right into your roadmap to cement these fundamentals before we proceed to React. "
                f"Let's tackle it together!"
            ),
            "timestamp": datetime.datetime.now().strftime("%I:%M %p")
        })

        return remedial_mod

    @classmethod
    def chat(cls, user_message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        msg_lower = user_message.lower()
        roadmap_updated = False
        reply = ""
        thought = ""

        # Check for dynamic roadmap alteration requests
        if any(w in msg_lower for w in ["add", "include", "inject", "want to learn"]) and any(s in msg_lower for s in ["typescript", "ts", "graphql", "tailwind", "next.js", "nextjs", "docker"]):
            # Dynamically inject custom module
            new_skill = "TypeScript" if "type" in msg_lower else "GraphQL" if "graphql" in msg_lower else "Next.js" if "next" in msg_lower else "Docker"
            new_mod_id = f"custom_mod_{uuid.uuid4().hex[:6]}"
            new_module = LearningModule(
                id=new_mod_id,
                title=f"⚡ Elective Sprint: {new_skill} Essentials & Modern Tooling",
                description=f"Dynamically inserted by AI Mentor Orchestrator upon learner request. Covers {new_skill} real-world architecture and practices.",
                skills_covered=[new_skill],
                prerequisites=["JavaScript"],
                estimated_hours=10,
                status="in_progress" if len(db.roadmap) <= 3 else "locked",
                score=None,
                order=len(db.roadmap) + 1,
                resources=[
                    ModuleResource(title=f"Official {new_skill} Handbook & Patterns", type="doc", url="https://www.typescriptlang.org", duration="40 mins"),
                    ModuleResource(title=f"Hands-on {new_skill} Production Sandbox", type="lab", url="https://stackblitz.com", duration="90 mins")
                ],
                questions=[
                    Question(
                        id=f"q_{new_skill.lower()}_1",
                        text=f"What is the principal benefit of introducing {new_skill} to a high-scale codebase?",
                        options=[
                            "Static type analysis catching errors during compile time rather than runtime",
                            "Faster CPU execution speeds in native assembly",
                            "Automatic database schema migrations",
                            "Zero CSS bundle size"
                        ],
                        correct_index=0,
                        explanation=f"{new_skill} provides type safety and tooling enhancements that eliminate large classes of runtime type errors.",
                        concept_tag=f"{new_skill} Core Benefits"
                    ),
                    Question(
                        id=f"q_{new_skill.lower()}_2",
                        text=f"How does {new_skill} handle backward compatibility with existing legacy code?",
                        options=[
                            "Through gradual typing, ambient declarations (.d.ts), and strictness compiler flags",
                            "By deleting all non-typed files automatically",
                            "By requiring complete ground-up rewrites",
                            "It does not support legacy code"
                        ],
                        correct_index=0,
                        explanation=f"Gradual adoption allows teams to type files incrementally using compiler flags.",
                        concept_tag="Migration Strategy"
                    ),
                    Question(
                        id=f"q_{new_skill.lower()}_3",
                        text=f"Which config file controls the {new_skill} compiler rules?",
                        options=["tsconfig.json", "package.json", "babel.config.js", "webpack.config.js"],
                        correct_index=0,
                        explanation="tsconfig.json specifies root files and compiler options.",
                        concept_tag="Tooling"
                    )
                ]
            )
            db.roadmap.append(new_module)
            roadmap_updated = True

            thought = (
                f"Learner expressed interest in learning '{new_skill}'. "
                f"Orchestrated with Curriculum Architect to synthesize dynamic elective module '{new_module.title}'. "
                f"Appended to roadmap with interactive diagnostic questions and lab resources. "
                f"Roadmap re-indexed."
            )

            reply = (
                f"Great idea! Adding **{new_skill}** is a tremendous boost for a modern engineering profile. "
                f"I've coordinated with our Curriculum Architect and dynamically updated your roadmap to include a specialized sprint: "
                f"**'{new_module.title}'**! You can explore the resources and challenge the assessment whenever you're ready."
            )

        elif "explain" in msg_lower or "event loop" in msg_lower or "closure" in msg_lower or "async" in msg_lower:
            thought = "Learner requested conceptual clarification on core JavaScript runtime architecture."
            reply = (
                "Here is how the **JavaScript Event Loop** operates under the hood:\n\n"
                "1. **Call Stack**: Executes synchronous functions (LIFO). When you call `console.log(1)`, it runs immediately.\n"
                "2. **Web APIs & Timers**: When you call `setTimeout(..., 0)`, the browser starts a timer outside the V8 engine.\n"
                "3. **Microtask Queue (High Priority)**: `Promise.then` callbacks and `queueMicrotask` queue here. *Crucial*: Whenever the Call Stack empties, V8 drains the ENTIRE microtask queue before touching macrotasks!\n"
                "4. **Macrotask Queue**: Timers (`setTimeout`, `setInterval`) wait here and execute only after all microtasks are drained.\n\n"
                "That's why `Promise.resolve().then(...)` runs before `setTimeout(...)` even if the timeout delay is 0ms!"
            )
        elif "why did i fail" in msg_lower or "remedial" in msg_lower:
            thought = "Learner asked about assessment failure reasons and remedial rationale."
            reply = (
                "When taking Module 2, our Assessment Evaluator identified misunderstandings around **Execution Order (Microtasks vs Macrotasks)** and **Lexical Scoping Closures**.\n\n"
                "Our platform uses **Self-Healing Adaptive Loops**: instead of letting you proceed to React (where asynchronous state updates would cause compounding confusion), "
                "we injected a targeted remedial lab to solidify your foundations. Once you take the 3 remedial questions, the next stage unlocks!"
            )
        elif "career" in msg_lower or "job" in msg_lower or "salary" in msg_lower:
            thought = "Learner queried career path trajectories."
            curr_goal = db.profile.target_role
            career = CAREER_GOALS.get(curr_goal, CAREER_GOALS["Full Stack Developer"])
            reply = (
                f"You're currently pursuing **{curr_goal}**! 🚀\n\n"
                f"- **Market Demand**: {career.demand}\n"
                f"- **Average Compensation**: {career.avg_salary}\n"
                f"- **Your Readiness**: {db.profile.readiness_score}%\n\n"
                f"You can switch career tracks at any time using the top selector (Full Stack Developer, Backend Engineer, AI/ML Engineer, Cybersecurity Analyst), and our Profiler & Architect will re-tailor your entire curriculum in real time."
            )
        else:
            thought = f"Synthesizing personalized mentorship response for learner input: '{user_message}'."
            reply = (
                f"I'm right here with you! You're making solid progress on your journey toward becoming a **{db.profile.target_role}**. "
                f"Your current readiness score is **{db.profile.readiness_score}%**.\n\n"
                f"Here are a few things you can do right now:\n"
                f"- Review active module resources in the **Adaptive Roadmap**\n"
                f"- Take a **3-question interactive assessment** to test your knowledge\n"
                f"- Ask me to **'Inject TypeScript'** or explain complex concepts like closures or async/await!"
            )

        # Log AI Mentor reasoning
        log_entry = AgentLog(
            id=f"log_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
            agent_name=cls.NAME,
            agent_role=cls.ROLE,
            avatar=cls.AVATAR,
            action="CHAT_INTERACTION_HANDLED",
            thought_process=thought,
            payload={
                "user_prompt": user_message,
                "roadmap_updated": roadmap_updated
            },
            status="completed"
        )
        db.agent_logs.insert(0, log_entry)

        # Save to chat history
        db.chat_history.append({"sender": "user", "text": user_message, "timestamp": datetime.datetime.now().strftime("%I:%M %p")})
        db.chat_history.append({"sender": "mentor", "text": reply, "timestamp": datetime.datetime.now().strftime("%I:%M %p")})

        return {
            "reply": reply,
            "agent_name": cls.NAME,
            "thought_process": thought,
            "roadmap_updated": roadmap_updated,
            "updated_roadmap": db.roadmap if roadmap_updated else None
        }
