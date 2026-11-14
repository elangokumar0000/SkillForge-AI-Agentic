from typing import Dict, List
import datetime
from models import CareerGoal, LearningModule, ModuleResource, Question, UserProfile, AgentLog

CAREER_GOALS: Dict[str, CareerGoal] = {
    "Full Stack Developer": CareerGoal(
        id="full_stack",
        title="Full Stack Developer",
        description="Build end-to-end modern web applications from reactive user interfaces to scalable cloud APIs and robust relational databases.",
        required_skills=["HTML/CSS", "JavaScript", "React", "Node.js", "Express", "Python", "SQL", "REST APIs", "Git"],
        icon="Layers",
        difficulty="Intermediate to Advanced",
        demand="🔥 Very High (+24% YoY)",
        avg_salary="$118,000 / yr"
    ),
    "Backend Engineer": CareerGoal(
        id="backend",
        title="Backend Engineer",
        description="Architect resilient distributed systems, database schemas, microservices, high-throughput caching layers, and high-security REST/gRPC endpoints.",
        required_skills=["Python", "SQL", "PostgreSQL", "FastAPI/Django", "Docker", "Redis", "Microservices", "System Design", "Git"],
        icon="Server",
        difficulty="Advanced",
        demand="⚡ High (+20% YoY)",
        avg_salary="$130,000 / yr"
    ),
    "AI/ML Engineer": CareerGoal(
        id="ai_ml",
        title="AI/ML Engineer",
        description="Design and deploy machine learning models, fine-tune LLMs, build RAG pipelines with vector databases, and scale intelligent AI applications.",
        required_skills=["Python", "SQL", "PyTorch/TensorFlow", "Pandas/NumPy", "LLM Orchestration & RAG", "Vector DBs", "Model Deployment", "Git"],
        icon="Cpu",
        difficulty="Advanced",
        demand="🚀 Surging (+42% YoY)",
        avg_salary="$152,000 / yr"
    ),
    "Cybersecurity Analyst": CareerGoal(
        id="cybersecurity",
        title="Cybersecurity Analyst",
        description="Identify zero-day vulnerabilities, audit secure software design, perform penetration testing, implement OWASP controls, and monitor enterprise threat vectors.",
        required_skills=["Network Security", "Python", "Linux & Bash", "Vulnerability Assessment", "Cryptography", "OWASP Top 10", "SIEM & Incident Response"],
        icon="ShieldCheck",
        difficulty="Intermediate to Advanced",
        demand="🛡️ Critical (+30% YoY)",
        avg_salary="$122,000 / yr"
    )
}

def get_initial_profile() -> UserProfile:
    return UserProfile(
        id="learner_001",
        name="Alex Chen",
        avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
        target_role="Full Stack Developer",
        existing_skills=["Python", "SQL", "basic HTML"],
        missing_skills=["JavaScript", "React", "Node.js"],
        weekly_hours_commitment=15,
        readiness_score=42
    )

def get_initial_roadmap() -> List[LearningModule]:
    return [
        LearningModule(
            id="mod_1_html_css",
            title="Semantic HTML5 & Responsive Tailwind/CSS",
            description="Master semantic web accessibility, flexbox/grid layouts, responsive typography, and mobile-first design patterns.",
            skills_covered=["basic HTML", "HTML/CSS", "Web Accessibility"],
            prerequisites=[],
            estimated_hours=8,
            status="completed",
            is_remedial=False,
            score=95,
            order=1,
            resources=[
                ModuleResource(title="Modern HTML5 Semantic Standards", type="article", url="https://developer.mozilla.org/en-US/docs/Glossary/Semantics", duration="25 mins"),
                ModuleResource(title="Flexbox & CSS Grid Interactive Visualizer", type="lab", url="https://css-tricks.com/snippets/css/a-guide-to-flexbox/", duration="45 mins"),
                ModuleResource(title="Responsive Portfolio Build Lab", type="lab", url="https://web.dev/learn/design", duration="2 hrs")
            ],
            questions=[
                Question(
                    id="q_html_1",
                    text="Which semantic tag is most appropriate for independent, self-contained syndicateable content like a blog post or news story?",
                    options=["<section>", "<article>", "<div>", "<aside>"],
                    correct_index=1,
                    explanation="<article> represents a self-contained composition in a document, page, application, or site, intended to be independently distributable.",
                    concept_tag="Semantic HTML"
                ),
                Question(
                    id="q_html_2",
                    text="What is the key difference between CSS Grid and Flexbox?",
                    options=[
                        "CSS Grid is 2-dimensional (rows & columns) while Flexbox is 1-dimensional (row or column)",
                        "Flexbox only works in modern browsers, Grid is deprecated",
                        "Grid cannot be nested inside Flexbox",
                        "Flexbox uses pixel values only while Grid uses percentages"
                    ],
                    correct_index=0,
                    explanation="Flexbox is designed for one-dimensional layouts (a row or a column), whereas CSS Grid is optimized for two-dimensional layouts (both rows and columns simultaneously).",
                    concept_tag="CSS Architecture"
                ),
                Question(
                    id="q_html_3",
                    text="In responsive design, what does the CSS `rem` unit scale relative to?",
                    options=[
                        "The immediate parent element's font-size",
                        "The root (<html>) element's font-size",
                        "The viewport width",
                        "The screen DPI resolution"
                    ],
                    correct_index=1,
                    explanation="`rem` stands for 'root em' and is relative to the font-size of the root <html> element (usually default 16px).",
                    concept_tag="Responsive Layouts"
                )
            ]
        ),
        LearningModule(
            id="mod_2_js_core",
            title="Modern JavaScript (ES6+), Event Loop & Async",
            description="Deep dive into JavaScript execution context, closures, promises, event loop microtasks, and DOM manipulation essential for modern frameworks.",
            skills_covered=["JavaScript", "Async/Await", "DOM API"],
            prerequisites=["basic HTML"],
            estimated_hours=14,
            status="in_progress",
            is_remedial=False,
            score=None,
            order=2,
            resources=[
                ModuleResource(title="JavaScript Visualized: The Event Loop & Execution Context", type="video", url="https://javascript.info/event-loop", duration="35 mins"),
                ModuleResource(title="Mastering Closures and Lexical Scope in V8", type="article", url="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures", duration="30 mins"),
                ModuleResource(title="Hands-on Async/Await & Fetch Sandbox", type="lab", url="https://javascript30.com", duration="90 mins")
            ],
            questions=[
                Question(
                    id="q_js_1",
                    text="Consider the following code snippet. In what order will the numbers log to the console?",
                    code_snippet="console.log(1);\nsetTimeout(() => console.log(2), 0);\nPromise.resolve().then(() => console.log(3));\nconsole.log(4);",
                    options=["1, 2, 3, 4", "1, 4, 3, 2", "1, 4, 2, 3", "3, 1, 4, 2"],
                    correct_index=1,
                    explanation="Synchronous code executes first (1, 4). Microtasks queue (Promise callbacks) drains before macrotasks queue (setTimeout), so 3 logs before 2.",
                    concept_tag="Event Loop & Microtasks"
                ),
                Question(
                    id="q_js_2",
                    text="What is a closure in JavaScript?",
                    code_snippet="function createCounter() {\n  let count = 0;\n  return () => ++count;\n}",
                    options=[
                        "A function bundled together with references to its lexical environment",
                        "A method that terminates asynchronous loop execution",
                        "A syntax error in ES6 arrow notation",
                        "A technique to convert mutable objects into JSON strings"
                    ],
                    correct_index=0,
                    explanation="A closure is the combination of a function bundled together (enclosed) with references to its surrounding state (lexical environment), granting access to an outer function's scope from an inner function.",
                    concept_tag="Closures & Lexical Scoping"
                ),
                Question(
                    id="q_js_3",
                    text="What does `Array.prototype.reduce()` return when reducing `[10, 20, 30]` with `(acc, cur) => acc + cur, 0`?",
                    code_snippet="const total = [10, 20, 30].reduce((acc, cur) => acc + cur, 0);",
                    options=["[10, 20, 30]", "60", "30", "NaN"],
                    correct_index=1,
                    explanation="Reduce accumulates the items starting from initial value 0: 0 + 10 = 10, 10 + 20 = 30, 30 + 30 = 60.",
                    concept_tag="Functional Array Methods"
                )
            ]
        ),
        LearningModule(
            id="mod_3_react_ui",
            title="React 18 Architecture: Hooks, State & Component Trees",
            description="Build scalable reactive user interfaces using functional components, custom hooks, context, reconciliation algorithms, and component lifecycles.",
            skills_covered=["React", "State Management", "Component Architecture"],
            prerequisites=["JavaScript"],
            estimated_hours=18,
            status="locked",
            is_remedial=False,
            score=None,
            order=3,
            resources=[
                ModuleResource(title="Thinking in React 18: State vs Props", type="doc", url="https://react.dev/learn/thinking-in-react", duration="40 mins"),
                ModuleResource(title="Deep Dive: useEffect vs useLayoutEffect lifecycle", type="video", url="https://react.dev/reference/react/useEffect", duration="35 mins"),
                ModuleResource(title="Interactive Component Tree & Custom Hook Project", type="lab", url="https://react.dev/learn/reusing-logic-with-custom-hooks", duration="2 hrs")
            ],
            questions=[
                Question(
                    id="q_react_1",
                    text="Why must React Hook calls only appear at the top level of a component?",
                    options=[
                        "To guarantee hooks are called in the exact same order on every render for internal state array indexing",
                        "To prevent JavaScript memory leaks in garbage collection",
                        "Because hooks are synchronous promises that block rendering",
                        "Because browsers cannot parse conditional JSX statements"
                    ],
                    correct_index=0,
                    explanation="React relies on the order in which Hooks are called to know which state corresponds to which useState or useEffect call across multiple renders.",
                    concept_tag="React Hook Invariants"
                ),
                Question(
                    id="q_react_2",
                    text="When should `useCallback` primarily be used?",
                    options=[
                        "For every function declared inside every component",
                        "To memoize a callback function definition between renders when passed to optimized child components relying on reference equality",
                        "To trigger asynchronous side effects after DOM painting",
                        "To fetch data from backend GraphQL endpoints"
                    ],
                    correct_index=1,
                    explanation="useCallback caches a function definition between renders, useful when passing callbacks to memoized children that rely on reference equality to prevent unnecessary re-renders.",
                    concept_tag="Performance Optimization"
                ),
                Question(
                    id="q_react_3",
                    text="What is the purpose of the `key` prop when rendering dynamic lists in React?",
                    options=[
                        "It provides a CSS styling hook for list elements",
                        "It acts as a unique identifier for the Virtual DOM reconciliation algorithm to track added, changed, or removed items",
                        "It encrypts the payload transmitted over HTTPS",
                        "It binds click events to the parent component"
                    ],
                    correct_index=1,
                    explanation="Keys help React identify which items have changed, are added, or are removed, giving components stable identity across renders.",
                    concept_tag="Virtual DOM Reconciliation"
                )
            ]
        ),
        LearningModule(
            id="mod_4_node_backend",
            title="Server-Side Node.js, Express & RESTful API Design",
            description="Construct secure, high-performance web servers with Node.js, Express middleware, routing patterns, error handling, and JWT authentication.",
            skills_covered=["Node.js", "Express", "REST APIs", "Authentication"],
            prerequisites=["JavaScript", "React"],
            estimated_hours=16,
            status="locked",
            is_remedial=False,
            score=None,
            order=4,
            resources=[
                ModuleResource(title="Node.js Event-Driven Architecture & Streams", type="video", url="https://nodejs.org/api/stream.html", duration="45 mins"),
                ModuleResource(title="Architecting Robust Express Middleware Pipelines", type="article", url="https://expressjs.com/en/guide/using-middleware.html", duration="30 mins"),
                ModuleResource(title="Build a JWT Auth Microservice Lab", type="lab", url="https://jwt.io/introduction", duration="2.5 hrs")
            ],
            questions=[
                Question(
                    id="q_node_1",
                    text="What is the role of `next()` in an Express middleware function?",
                    options=[
                        "It immediately sends a 200 OK response to the client",
                        "It passes execution control to the next middleware or route handler in the request pipeline",
                        "It restarts the Node process if an error occurs",
                        "It parses the incoming request body as JSON"
                    ],
                    correct_index=1,
                    explanation="next() instructs Express to execute the next middleware function in the stack. If not called, the request hangs.",
                    concept_tag="Express Middleware Pipeline"
                ),
                Question(
                    id="q_node_2",
                    text="Why should computationally intensive CPU tasks (like large matrix math or image processing) be avoided on the main Node.js thread?",
                    options=[
                        "Because Node.js runs on a single-threaded event loop and CPU-bound work blocks all incoming client requests",
                        "Because Node.js does not support 64-bit integers",
                        "Because npm packages cannot run C++ bindings",
                        "Because Express does not allow asynchronous functions"
                    ],
                    correct_index=0,
                    explanation="Node.js executes JavaScript on a single thread. CPU-intensive operations block the event loop, preventing all other connections and I/O from being processed.",
                    concept_tag="Node Single-Threaded Concurrency"
                ),
                Question(
                    id="q_node_3",
                    text="Which HTTP status code is most standard for an authentication failure due to missing or invalid credentials?",
                    options=["401 Unauthorized", "403 Forbidden", "404 Not Found", "500 Internal Error"],
                    correct_index=0,
                    explanation="401 Unauthorized indicates that the request lacks valid authentication credentials for the target resource.",
                    concept_tag="REST API Standards"
                )
            ]
        ),
        LearningModule(
            id="mod_5_sql_db",
            title="Relational Data Modeling with SQL & ORMs",
            description="Design normalized relational schemas, index strategies, foreign keys, transactions, and interface with Node/Python backends.",
            skills_covered=["SQL", "PostgreSQL", "Data Modeling"],
            prerequisites=["Node.js"],
            estimated_hours=14,
            status="locked",
            is_remedial=False,
            score=None,
            order=5,
            resources=[
                ModuleResource(title="PostgreSQL Indexing & Query Execution Plans", type="article", url="https://use-the-index-luke.com", duration="40 mins"),
                ModuleResource(title="Database Normalization from 1NF to 3NF", type="video", url="https://en.wikipedia.org/wiki/Database_normalization", duration="30 mins"),
                ModuleResource(title="Full-Stack Database Integration Lab", type="lab", url="https://www.prisma.io", duration="2 hrs")
            ],
            questions=[
                Question(
                    id="q_sql_1",
                    text="Which SQL clause is used to filter records aggregated by a `GROUP BY` statement?",
                    options=["WHERE", "HAVING", "FILTER", "LIMIT"],
                    correct_index=1,
                    explanation="HAVING filters aggregate groups created by GROUP BY, whereas WHERE filters individual rows before grouping occurs.",
                    concept_tag="SQL Aggregations"
                ),
                Question(
                    id="q_sql_2",
                    text="What does ACID stand for in relational database transactions?",
                    options=[
                        "Atomicity, Consistency, Isolation, Durability",
                        "Asynchronous, Concurrent, Indexed, Distributed",
                        "Access, Cache, Integrity, Delegation",
                        "Authentication, Cryptography, Identity, Directory"
                    ],
                    correct_index=0,
                    explanation="ACID guarantees that database transactions are processed reliably: Atomicity, Consistency, Isolation, and Durability.",
                    concept_tag="Database Transactions"
                ),
                Question(
                    id="q_sql_3",
                    text="What type of SQL join returns all rows from the left table, and matching rows from the right table (with NULLs for non-matches)?",
                    options=["INNER JOIN", "LEFT OUTER JOIN", "CROSS JOIN", "FULL OUTER JOIN"],
                    correct_index=1,
                    explanation="LEFT OUTER JOIN keeps all rows from the left table and matches rows from the right table, filling missing matches with NULL.",
                    concept_tag="SQL Joins"
                )
            ]
        ),
        LearningModule(
            id="mod_6_fullstack_capstone",
            title="Full-Stack Capstone: CI/CD, Containerization & Production",
            description="Integrate frontend, backend, database, Docker containers, automated tests, and deploy a production-grade SaaS web platform.",
            skills_covered=["Full Stack Integration", "Docker", "Git", "CI/CD"],
            prerequisites=["React", "Node.js", "SQL"],
            estimated_hours=22,
            status="locked",
            is_remedial=False,
            score=None,
            order=6,
            resources=[
                ModuleResource(title="Dockerizing Multi-Container React + Node + Postgres Apps", type="video", url="https://docs.docker.com/compose/", duration="50 mins"),
                ModuleResource(title="GitHub Actions CI/CD Pipeline from Scratch", type="article", url="https://docs.github.com/en/actions", duration="35 mins"),
                ModuleResource(title="Production Deployment & Monitoring Checklist", type="doc", url="https://12factor.net/", duration="30 mins")
            ],
            questions=[
                Question(
                    id="q_cap_1",
                    text="What is the primary benefit of a Docker multi-stage build for frontend React applications?",
                    options=[
                        "It produces significantly smaller, secure production container images by discarding node_modules and build tools from the final Nginx container",
                        "It speeds up internet connection bandwidth during runtime",
                        "It automatically rewrites JavaScript code to Rust",
                        "It enables hot-module replacement in production Kubernetes clusters"
                    ],
                    correct_index=0,
                    explanation="Multi-stage builds allow separating build tools (Node.js SDK, npm dev dependencies) from the final runtime image (e.g., lightweight Nginx serving static assets), resulting in lean, secure images.",
                    concept_tag="Container Optimization"
                ),
                Question(
                    id="q_cap_2",
                    text="In a modern 12-Factor App methodology, where should environment-specific configurations (like database credentials and API secrets) reside?",
                    options=[
                        "Hardcoded in Git repository source files",
                        "Injected via Environment Variables at runtime",
                        "Stored in plain text browser LocalStorage",
                        "Written directly into compiled CSS bundles"
                    ],
                    correct_index=1,
                    explanation="12-Factor apps strictly separate configuration from code and store secrets in environment variables.",
                    concept_tag="DevOps & Security"
                ),
                Question(
                    id="q_cap_3",
                    text="What is the purpose of Cross-Origin Resource Sharing (CORS) headers?",
                    options=[
                        "To tell browsers which origins are permitted to access resources on the server",
                        "To accelerate database index lookups",
                        "To compress JSON responses using gzip",
                        "To encrypt websocket packets"
                    ],
                    correct_index=0,
                    explanation="CORS is a browser security mechanism that uses HTTP headers to tell browsers whether a web application running at one origin has permission to access resources from a server at a different origin.",
                    concept_tag="Web Security"
                )
            ]
        )
    ]

# In-memory storage instance
class SkillForgeDatabase:
    def __init__(self):
        self.profile = get_initial_profile()
        self.roadmap = get_initial_roadmap()
        self.agent_logs: List[AgentLog] = [
            AgentLog(
                id="log_001",
                timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
                agent_name="Profiler Agent",
                agent_role="Competency Auditor & Gap Diagnostician",
                avatar="🔍",
                action="INITIAL_ASSESSMENT_SYNC",
                thought_process="Auditing student skills against 'Full Stack Developer' track. Identified existing proficiencies: Python (High), SQL (Intermediate), basic HTML (Beginner). Detected critical competencies missing: JavaScript, React, Node.js. Match score calculated at 42%.",
                payload={"readiness_score": 42, "critical_gaps": ["JavaScript", "React", "Node.js"], "target_role": "Full Stack Developer"},
                status="completed"
            ),
            AgentLog(
                id="log_002",
                timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
                agent_name="Curriculum Architect Agent",
                agent_role="Dependency Graph & Milestone Planner",
                avatar="📐",
                action="ROADMAP_COMPILED",
                thought_process="Compiled 6-stage dependency-ordered roadmap. Prerequisite path: HTML5/CSS (Completed) -> JavaScript Core (In Progress) -> React 18 (Locked) -> Node/Express (Locked) -> SQL DB (Locked) -> Fullstack Capstone (Locked). Set active diagnostic checkpoint on Module 2.",
                payload={"module_count": 6, "active_module_id": "mod_2_js_core", "estimated_hours": 92},
                status="completed"
            ),
            AgentLog(
                id="log_003",
                timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
                agent_name="AI Mentor Orchestrator",
                agent_role="Cognitive Coach & Self-Healing Sentinel",
                avatar="🧠",
                action="WATCHDOG_ENGAGED",
                thought_process="AI Mentor Orchestrator standing by. Monitoring learner progression on Module 2 (Modern JavaScript). Self-healing loop armed: If diagnostic assessment drops below 60%, will intercept failure and dynamically inject foundational remedial sprint.",
                payload={"status": "ready", "threshold": "60%", "remediation_mode": "Auto-Inject"},
                status="completed"
            )
        ]
        self.chat_history: List[Dict[str, str]] = [
            {
                "sender": "mentor",
                "text": "Hello Alex! 👋 I'm your AI Mentor Orchestrator. I've analyzed your goal to become a Full Stack Developer. You have solid footing in Python and SQL! Right now, we're conquering JavaScript ES6+ and the Event Loop in Module 2. When you're ready, take the 3-question diagnostic assessment!",
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            }
        ]

    def reset(self):
        self.profile = get_initial_profile()
        self.roadmap = get_initial_roadmap()
        self.agent_logs = [
            AgentLog(
                id=f"log_{int(datetime.datetime.now().timestamp())}",
                timestamp=datetime.datetime.now().strftime("%H:%M:%S"),
                agent_name="AI Mentor Orchestrator",
                agent_role="System Reset Engine",
                avatar="🔄",
                action="SYSTEM_RESET_EXECUTED",
                thought_process="Restored database state to hackathon demo baseline. Profile re-initialized to Alex Chen aiming for Full Stack Developer.",
                payload={"status": "reset_successful"},
                status="completed"
            )
        ]
        self.chat_history = [
            {
                "sender": "mentor",
                "text": "System reset complete! Welcome back, Alex. Ready to kick off your Full Stack journey?",
                "timestamp": datetime.datetime.now().strftime("%I:%M %p")
            }
        ]

db = SkillForgeDatabase()
