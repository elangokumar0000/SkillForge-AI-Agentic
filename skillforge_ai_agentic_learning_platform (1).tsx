import React, { useState, useEffect, useRef } from 'react';
import {
  Brain,
  Target,
  Cpu,
  CheckCircle2,
  Circle,
  Lock,
  AlertTriangle,
  Sparkles,
  BookOpen,
  Code2,
  Award,
  FolderGit2,
  Send,
  RefreshCw,
  Plus,
  X,
  Play,
  ChevronRight,
  Layers,
  Terminal,
  Zap,
  BarChart3,
  MessageSquare,
  RotateCcw,
  ShieldAlert
} from 'lucide-react';

// ============================================================================
// DOMAIN KNOWLEDGE BASE: ROLES, SKILLS, CURRICULUM & ASSESSMENTS
// ============================================================================

const ROLE_MATRICES = {
  'Full Stack Developer': {
    description: 'End-to-end web engineering across frontend interfaces, backend APIs, and relational databases.',
    requirements: {
      'Python': 70,
      'SQL': 80,
      'HTML/CSS': 85,
      'JavaScript': 90,
      'React': 85,
      'Node.js': 85
    },
    roadmap: [
      {
        id: 'fs-1',
        skill: 'JavaScript',
        title: 'Modern JavaScript (ES6+) & Async Patterns',
        type: 'Course + Lab',
        duration: '2 Weeks',
        resources: [
          { kind: 'Course', name: 'JavaScript.info: Modern JS Deep Dive' },
          { kind: 'Exercise', name: 'Build an Async Promise Task Queue' }
        ],
        remedial: {
          id: 'fs-rem-js',
          skill: 'JavaScript',
          title: 'REMEDIAL: JS Closures, Event Loop & Callbacks Foundations',
          type: 'Interactive Sandbox',
          duration: '4 Days',
          resources: [
            { kind: 'Tutorial', name: 'Visualizing the JS Event Loop Step-by-Step' },
            { kind: 'Exercise', name: '15 Guided Exercises on Scope & Async/Await' }
          ]
        }
      },
      {
        id: 'fs-2',
        skill: 'Node.js',
        title: 'RESTful APIs & Backend Architecture with Node.js',
        type: 'Project Module',
        duration: '2 Weeks',
        resources: [
          { kind: 'Course', name: 'Node.js & Express Production Patterns' },
          { kind: 'Exercise', name: 'Build a JWT-Authenticated Task API + SQL' }
        ],
        remedial: {
          id: 'fs-rem-node',
          skill: 'Node.js',
          title: 'REMEDIAL: Express Middleware & HTTP Request Lifecycle',
          type: 'Guided Workshop',
          duration: '3 Days',
          resources: [
            { kind: 'Tutorial', name: 'Understanding Express Routing & Error Handling' },
            { kind: 'Exercise', name: 'Debug Broken REST Endpoints Lab' }
          ]
        }
      },
      {
        id: 'fs-3',
        skill: 'React',
        title: 'Component Architecture, Hooks & State Management',
        type: 'Capstone Module',
        duration: '3 Weeks',
        resources: [
          { kind: 'Course', name: 'React 19 Patterns & Custom Hooks' },
          { kind: 'Exercise', name: 'Full-Stack Dashboard Connected to Node API' }
        ],
        remedial: {
          id: 'fs-rem-react',
          skill: 'React',
          title: 'REMEDIAL: React Rendering, Props & useEffect Mental Model',
          type: 'Interactive Lab',
          duration: '4 Days',
          resources: [
            { kind: 'Tutorial', name: 'Thinking in React State & Immutability' },
            { kind: 'Exercise', name: 'Fix Stale Closure & Re-render Bugs' }
          ]
        }
      }
    ]
  },
  'Backend Engineer': {
    description: 'Scalable distributed systems, high-throughput APIs, database optimization, and containerization.',
    requirements: {
      'Python': 90,
      'SQL': 90,
      'Node.js': 80,
      'Docker': 80,
      'System Design': 75
    },
    roadmap: [
      {
        id: 'be-1',
        skill: 'Python',
        title: 'High-Performance Async Python & FastAPI',
        type: 'Course + Lab',
        duration: '2 Weeks',
        resources: [
          { kind: 'Course', name: 'AsyncIO & FastAPI Microservices' },
          { kind: 'Exercise', name: 'Rate-Limited API Gateway in Python' }
        ],
        remedial: {
          id: 'be-rem-py',
          skill: 'Python',
          title: 'REMEDIAL: Python Concurrency, Coroutines & Typing',
          type: 'Guided Lab',
          duration: '3 Days',
          resources: [
            { kind: 'Tutorial', name: 'Async/Await Internals in Python' },
            { kind: 'Exercise', name: 'Refactor Sync Endpoints to Async' }
          ]
        }
      },
      {
        id: 'be-2',
        skill: 'Docker',
        title: 'Containerization & CI/CD Pipelines with Docker',
        type: 'Hands-on Lab',
        duration: '1.5 Weeks',
        resources: [
          { kind: 'Course', name: 'Docker Multi-Stage Builds & Compose' },
          { kind: 'Exercise', name: 'Containerize FastAPI + PostgreSQL Stack' }
        ],
        remedial: {
          id: 'be-rem-doc',
          skill: 'Docker',
          title: 'REMEDIAL: Linux Containers, Networking & Volumes',
          type: 'Sandbox',
          duration: '3 Days',
          resources: [
            { kind: 'Tutorial', name: 'Container Networking Demystified' },
            { kind: 'Exercise', name: 'Troubleshoot Multi-Container Bridge Networks' }
          ]
        }
      },
      {
        id: 'be-3',
        skill: 'System Design',
        title: 'Caching, Indexing & Distributed Architecture',
        type: 'Architecture Lab',
        duration: '3 Weeks',
        resources: [
          { kind: 'Course', name: 'Database Indexing & Redis Caching Strategies' },
          { kind: 'Exercise', name: 'Optimize Slow SQL Queries (10x Latency Cut)' }
        ],
        remedial: {
          id: 'be-rem-sys',
          skill: 'System Design',
          title: 'REMEDIAL: B-Tree Indexes, ACID & Load Balancing Basics',
          type: 'Workshop',
          duration: '4 Days',
          resources: [
            { kind: 'Tutorial', name: 'EXPLAIN ANALYZE Query Tuning Guide' },
            { kind: 'Exercise', name: 'Schema Normalization & Index Design' }
          ]
        }
      }
    ]
  },
  'AI / ML Engineer': {
    description: 'Production machine learning pipelines, LLM agent orchestration, vector search, and model deployment.',
    requirements: {
      'Python': 95,
      'SQL': 75,
      'PyTorch': 85,
      'LLM Agents': 85,
      'Vector DBs': 80
    },
    roadmap: [
      {
        id: 'ai-1',
        skill: 'PyTorch',
        title: 'Neural Networks & Deep Learning with PyTorch',
        type: 'Course + Lab',
        duration: '3 Weeks',
        resources: [
          { kind: 'Course', name: 'PyTorch Tensors, Autograd & Training Loops' },
          { kind: 'Exercise', name: 'Train a Custom Transformer Classifier' }
        ],
        remedial: {
          id: 'ai-rem-pt',
          skill: 'PyTorch',
          title: 'REMEDIAL: Matrix Operations, Gradients & Loss Functions',
          type: 'Interactive Lab',
          duration: '4 Days',
          resources: [
            { kind: 'Tutorial', name: 'Linear Algebra & Backprop Visualized' },
            { kind: 'Exercise', name: 'Debug Vanishing Gradients & Tensor Shapes' }
          ]
        }
      },
      {
        id: 'ai-2',
        skill: 'Vector DBs',
        title: 'Embeddings & Retrieval-Augmented Generation (RAG)',
        type: 'Project Module',
        duration: '2 Weeks',
        resources: [
          { kind: 'Course', name: 'Semantic Search, Chunking & pgvector' },
          { kind: 'Exercise', name: 'Build a Hybrid Semantic Document Search Engine' }
        ],
        remedial: {
          id: 'ai-rem-vec',
          skill: 'Vector DBs',
          title: 'REMEDIAL: Cosine Similarity & Embedding Spaces',
          type: 'Workshop',
          duration: '3 Days',
          resources: [
            { kind: 'Tutorial', name: 'How Dense Embeddings Encode Meaning' },
            { kind: 'Exercise', name: 'Tune Chunk Overlap & Top-K Retrieval' }
          ]
        }
      },
      {
        id: 'ai-3',
        skill: 'LLM Agents',
        title: 'Multi-Agent Orchestration & Tool-Use Workflows',
        type: 'Capstone',
        duration: '2.5 Weeks',
        resources: [
          { kind: 'Course', name: 'Cyclic Agent Graphs, Memory & Evaluation' },
          { kind: 'Exercise', name: 'Deploy a Self-Correcting Research Agent' }
        ],
        remedial: {
          id: 'ai-rem-ag',
          skill: 'LLM Agents',
          title: 'REMEDIAL: Structured Outputs, Function Calling & State',
          type: 'Guided Lab',
          duration: '3 Days',
          resources: [
            { kind: 'Tutorial', name: 'Deterministic State Machines for Agents' },
            { kind: 'Exercise', name: 'Build Reliable JSON Tool-Calling Loops' }
          ]
        }
      }
    ]
  },
  'Cybersecurity Analyst': {
    description: 'Threat detection, web application penetration testing, network forensics, and secure DevOps.',
    requirements: {
      'Python': 80,
      'SQL': 75,
      'HTML/CSS': 70,
      'Network Security': 85,
      'Web App Pentesting': 85
    },
    roadmap: [
      {
        id: 'sec-1',
        skill: 'Network Security',
        title: 'Packet Analysis, Firewalls & Intrusion Detection',
        type: 'Course + Lab',
        duration: '2 Weeks',
        resources: [
          { kind: 'Course', name: 'TCP/IP Internals & Wireshark Forensics' },
          { kind: 'Exercise', name: 'Detect Anomaly Signatures in PCAP Logs' }
        ],
        remedial: {
          id: 'sec-rem-net',
          skill: 'Network Security',
          title: 'REMEDIAL: OSI Model, TLS Handshakes & DNS Security',
          type: 'Sandbox',
          duration: '3 Days',
          resources: [
            { kind: 'Tutorial', name: 'Inspecting Encrypted & Unencrypted Traffic' },
            { kind: 'Exercise', name: 'Identify ARP Spoofing & Port Scans' }
          ]
        }
      },
      {
        id: 'sec-2',
        skill: 'Web App Pentesting',
        title: 'OWASP Top 10: SQLi, XSS & Auth Exploitation',
        type: 'Hands-on Lab',
        duration: '2.5 Weeks',
        resources: [
          { kind: 'Course', name: 'Modern Web Vulnerability Exploitation & Patching' },
          { kind: 'Exercise', name: 'Audit & Patch a Vulnerable Web Application' }
        ],
        remedial: {
          id: 'sec-rem-web',
          skill: 'Web App Pentesting',
          title: 'REMEDIAL: HTTP Sessions, Cookies, CSRF & Input Sanitization',
          type: 'Interactive Lab',
          duration: '4 Days',
          resources: [
            { kind: 'Tutorial', name: 'How Parameterized Queries Prevent SQLi' },
            { kind: 'Exercise', name: 'Remediate Reflected & Stored XSS' }
          ]
        }
      }
    ]
  }
};

// Assessment Question Bank keyed by skill
const ASSESSMENT_BANK = {
  'JavaScript': [
    {
      q: 'What will `console.log(typeof null)` output in JavaScript, and why is async/await built on Promises?',
      options: [
        '"null" — async/await uses OS threads directly',
        '"object" — async/await is syntactic sugar over Promises and the microtask queue',
        '"undefined" — Promises block the main call stack until resolved',
        '"reference" — async functions execute synchronously'
      ],
      correct: 1
    },
    {
      q: 'In the JavaScript Event Loop, which queue has higher execution priority after the current call stack clears?',
      options: [
        'Macrotask Queue (setTimeout, setInterval)',
        'DOM Rendering Queue',
        'Microtask Queue (Promise.then, queueMicrotask)',
        'Network I/O Callback Pool'
      ],
      correct: 2
    },
    {
      q: 'Which pattern prevents mutating an existing array while adding a new item in modern ES6+?',
      options: [
        'arr.push(newItem)',
        'arr.splice(0, 0, newItem)',
        '[...arr, newItem]',
        'arr.fill(newItem)'
      ],
      correct: 2
    }
  ],
  'Node.js': [
    {
      q: 'In an Express.js middleware function `(req, res, next) => {}`, what happens if you neither send a response nor call `next()`?',
      options: [
        'Express automatically sends a 200 OK response',
        'The client request hangs until it times out',
        'Node.js restarts the worker process',
        'It skips directly to the error handler'
      ],
      correct: 1
    },
    {
      q: 'Why should CPU-intensive synchronous tasks be avoided on the main Node.js thread?',
      options: [
        'Node.js uses a single-threaded event loop for JS execution, so heavy sync work blocks all concurrent requests',
        'V8 cannot compile synchronous loops',
        'PostgreSQL connections drop automatically',
        'HTTP headers become corrupted'
      ],
      correct: 0
    },
    {
      q: 'Which HTTP status code is most appropriate when a client sends invalid payload data to a REST API?',
      options: [
        '201 Created',
        '302 Found',
        '400 Bad Request / 422 Unprocessable Entity',
        '503 Service Unavailable'
      ],
      correct: 2
    }
  ],
  'React': [
    {
      q: 'Why must state updates in React treat objects and arrays as immutable?',
      options: [
        'JavaScript forbids mutating const objects',
        'React uses shallow reference comparison (Object.is) to detect state changes and trigger re-renders',
        'JSX cannot render mutated arrays',
        'Browser localStorage rejects mutated state'
      ],
      correct: 1
    },
    {
      q: 'What causes a stale closure inside a `useEffect` hook?',
      options: [
        'Passing an empty dependency array `[]` while referencing state/props that change over time',
        'Using `useState` more than twice in a component',
        'Returning a cleanup function from `useEffect`',
        'Rendering child components conditionally'
      ],
      correct: 0
    },
    {
      q: 'When should you prefer `useMemo` or derived state over syncing two states with `useEffect`?',
      options: [
        'Never, `useEffect` should sync all derived values',
        'Whenever a value can be calculated directly from existing props or state during render',
        'Only when fetching data from an external API',
        'Only in class components'
      ],
      correct: 1
    }
  ],
  'DEFAULT': [
    {
      q: 'Which architectural practice best ensures maintainability and fault isolation in production software?',
      options: [
        'Coupling database queries directly inside UI event handlers',
        'Separation of concerns with modular interfaces, automated validation, and clear error boundaries',
        'Storing secrets in client-side source files',
        'Disabling logging to save disk I/O'
      ],
      correct: 1
    },
    {
      q: 'When diagnosing a performance bottleneck in a data-driven application, what is the best first step?',
      options: [
        'Rewrite the entire codebase in another language immediately',
        'Profile and measure latency/query execution plans to locate the actual bottleneck',
        'Add random caching layers without TTLs',
        'Increase frontend bundle size'
      ],
      correct: 1
    },
    {
      q: 'How does iterative assessment improve mastery in technical skill acquisition?',
      options: [
        'By skipping foundational prerequisites',
        'By identifying specific conceptual gaps early and reinforcing them with targeted practice',
        'By memorizing syntax without building projects',
        'By avoiding feedback loops'
      ],
      correct: 1
    }
  ]
};

const AGENT_META = {
  profiler: {
    name: 'Profiler & Gap Agent',
    role: 'Skill Matrix & Role Analyzer',
    color: 'text-cyan-400',
    bg: 'bg-cyan-500/10',
    border: 'border-cyan-500/30',
    dot: 'bg-cyan-400'
  },
  architect: {
    name: 'Curriculum Architect',
    role: 'Dependency Roadmap Builder',
    color: 'text-violet-400',
    bg: 'bg-violet-500/10',
    border: 'border-violet-500/30',
    dot: 'bg-violet-400'
  },
  evaluator: {
    name: 'Assessment Evaluator',
    role: 'Diagnostic & Mastery Grader',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10',
    border: 'border-amber-500/30',
    dot: 'bg-amber-400'
  },
  mentor: {
    name: 'AI Mentor Orchestrator',
    role: 'Adaptive Guidance & Re-Router',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/30',
    dot: 'bg-emerald-400'
  }
};

// ============================================================================
// MAIN APPLICATION COMPONENT
// ============================================================================

export default function App() {
  // Learner Profile State (Pre-loaded with PromptWars Sample Scenario)
  const [profile, setProfile] = useState({
    name: 'Aarav Sharma',
    title: 'CS Undergraduate • 3rd Year',
    targetRole: 'Full Stack Developer',
    skills: {
      'Python': 78,
      'SQL': 75,
      'HTML/CSS': 72,
      'JavaScript': 20,
      'React': 10,
      'Node.js': 15
    },
    certifications: [
      'Python for Data & Scripting (Coursera)',
      'Relational Databases & SQL Fundamentals'
    ],
    projects: [
      'Student Attendance CLI & SQLite Tracker (Python, SQL)',
      'Personal Portfolio Static Webpage (HTML/CSS)'
    ]
  });

  // Dynamic Roadmap State
  const [roadmapModules, setRoadmapModules] = useState([]);
  // Multi-Agent Live Activity Logs
  const [agentLogs, setAgentLogs] = useState([]);
  const [activeAgentPulse, setActiveAgentPulse] = useState(null);

  // Skill Add Form State
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillLevel, setNewSkillLevel] = useState(65);

  // Interactive Assessment Modal State
  const [activeQuizModule, setActiveQuizModule] = useState(null);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);

  // AI Mentor Chat State
  const [chatMessages, setChatMessages] = useState([
    {
      id: 'welcome-1',
      sender: 'mentor',
      text: "Hi Aarav! I've coordinated with our Profiler and Curriculum Architect agents. You already have a solid foundation in Python (78%), SQL (75%), and HTML/CSS (72%). To reach your Full Stack Developer goal, we've prioritized JavaScript, Node.js, and React. Ready to tackle Module 1 or test an adaptive simulation?"
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard' | 'agents'

  const logsEndRef = useRef(null);
  const chatEndRef = useRef(null);

  // Helper to push timestamped agent logs with visual pulse
  const pushAgentLog = (agentKey, message, badge = null) => {
    const now = new Date();
    const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    setActiveAgentPulse(agentKey);
    setAgentLogs((prev) => [
      {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        agent: agentKey,
        message,
        badge,
        timestamp
      },
      ...prev.slice(0, 39)
    ]);
    setTimeout(() => {
      setActiveAgentPulse((curr) => (curr === agentKey ? null : curr));
    }, 1200);
  };

  // Build / Recompute Roadmap whenever targetRole changes or on initial mount
  const generateRoadmapForRole = (roleName, currentSkills, triggerReason = 'Initial Profile Scan') => {
    const roleConfig = ROLE_MATRICES[roleName];
    if (!roleConfig) return;

    const gaps = [];
    Object.entries(roleConfig.requirements).forEach(([skill, reqScore]) => {
      const userScore = currentSkills[skill] || 0;
      if (userScore < reqScore) {
        gaps.push(`${skill} (-${reqScore - userScore}%)`);
      }
    });

    pushAgentLog(
      'profiler',
      `[${triggerReason}] Scanned profile against "${roleName}". Identified ${gaps.length} skill gaps: ${gaps.length ? gaps.join(', ') : 'None (Role Ready!)'}.`,
      'GAP ANALYSIS'
    );

    setTimeout(() => {
      const builtModules = roleConfig.roadmap.map((mod, idx) => {
        const userScore = currentSkills[mod.skill] || 0;
        const reqScore = roleConfig.requirements[mod.skill] || 80;
        const alreadyMastered = userScore >= reqScore;
        return {
          ...mod,
          status: alreadyMastered ? 'completed' : idx === 0 ? 'in-progress' : 'locked',
          isRemedial: false,
          lastScore: alreadyMastered ? userScore : null
        };
      });

      // Ensure first non-completed module is unlocked
      const firstPendingIdx = builtModules.findIndex((m) => m.status !== 'completed');
      if (firstPendingIdx !== -1) {
        builtModules[firstPendingIdx].status = 'in-progress';
        for (let i = firstPendingIdx + 1; i < builtModules.length; i++) {
          if (builtModules[i].status !== 'completed') {
            builtModules[i].status = 'locked';
          }
        }
      }

      setRoadmapModules(builtModules);

      pushAgentLog(
        'architect',
        `Constructed ${builtModules.length}-stage dependency learning path for ${roleName} with curated labs & exercises.`,
        'ROADMAP BUILT'
      );
    }, 350);
  };

  // Initial Bootstrapping
  useEffect(() => {
    generateRoadmapForRole(profile.targetRole, profile.skills, 'Session Boot');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Handle Career Goal Switch
  const handleRoleChange = (newRole) => {
    if (newRole === profile.targetRole) return;
    setProfile((prev) => ({ ...prev, targetRole: newRole }));

    pushAgentLog(
      'mentor',
      `Learner pivoted career goal from "${profile.targetRole}" to "${newRole}". Triggering multi-agent re-routing...`,
      'GOAL PIVOT'
    );

    generateRoadmapForRole(newRole, profile.skills, 'Career Goal Pivot');

    setChatMessages((prev) => [
      ...prev,
      {
        id: `pivot-${Date.now()}`,
        sender: 'mentor',
        text: `Career target updated to **${newRole}**! Our Profiler Agent re-evaluated your existing Python & SQL strengths against ${newRole} benchmarks, and the Curriculum Architect rebuilt your personalized roadmap.`
      }
    ]);
  };

  // Handle Adding or Updating a Skill
  const handleAddSkill = (e) => {
    e.preventDefault();
    const trimmed = newSkillName.trim();
    if (!trimmed) return;

    const updatedSkills = {
      ...profile.skills,
      [trimmed]: Number(newSkillLevel)
    };

    setProfile((prev) => ({
      ...prev,
      skills: updatedSkills
    }));
    setNewSkillName('');

    pushAgentLog(
      'profiler',
      `Updated skill telemetry: ${trimmed} set to ${newSkillLevel}%. Recalculating role readiness...`,
      'SKILL UPDATE'
    );

    generateRoadmapForRole(profile.targetRole, updatedSkills, 'Skill Telemetry Update');
  };

  // Open Interactive Assessment Modal
  const openAssessment = (mod) => {
    setActiveQuizModule(mod);
    setQuizAnswers({});
    setQuizResult(null);
    pushAgentLog(
      'evaluator',
      `Generated diagnostic micro-assessment for "${mod.title}" (${mod.skill}).`,
      'ASSESSMENT READY'
    );
  };

  // Core Adaptive Loop: Evaluate Quiz & Trigger AI Mentor Re-Routing if Score < 60%
  const evaluateQuizScore = (mod, scorePct) => {
    setQuizResult(scorePct);

    if (scorePct < 60) {
      // 1. Evaluator logs failure
      pushAgentLog(
        'evaluator',
        `Assessment scored ${scorePct}% on ${mod.skill} (Below 60% mastery threshold). Escalating to AI Mentor.`,
        'LOW SCORE ALERT'
      );

      // 2. AI Mentor intervenes and instructs Curriculum Architect to inject Remedial Module
      setTimeout(() => {
        pushAgentLog(
          'mentor',
          `Detected foundational gap in ${mod.skill} (${scorePct}%). Instructing Curriculum Architect to inject Remedial Sandbox before advancing.`,
          'ADAPTIVE INTERVENTION'
        );

        setRoadmapModules((prev) => {
          const targetIdx = prev.findIndex((m) => m.id === mod.id);
          if (targetIdx === -1) return prev;

          const updated = [...prev];
          updated[targetIdx] = {
            ...updated[targetIdx],
            lastScore: scorePct
          };

          // Inject remedial module right before current module if not already injected
          const remedialTemplate = mod.remedial;
          const alreadyHasRemedial = prev.some(
            (m) => m.isRemedial && m.skill === mod.skill && m.status !== 'completed'
          );

          if (remedialTemplate && !alreadyHasRemedial) {
            const remedialModule = {
              id: `${remedialTemplate.id}-${Date.now()}`,
              skill: mod.skill,
              title: remedialTemplate.title,
              type: remedialTemplate.type,
              duration: remedialTemplate.duration,
              resources: remedialTemplate.resources,
              status: 'in-progress',
              isRemedial: true,
              lastScore: null
            };
            // Pause main module until remedial is completed
            updated[targetIdx].status = 'locked';
            updated.splice(targetIdx, 0, remedialModule);
          }

          return updated;
        });

        pushAgentLog(
          'architect',
          `Injected "${mod.remedial?.title || `Remedial ${mod.skill} Lab`}" into active roadmap and locked downstream modules until mastery.`,
          'REMEDIAL INJECTED'
        );

        setChatMessages((prev) => [
          ...prev,
          {
            id: `remedial-${Date.now()}`,
            sender: 'mentor',
            text: `I noticed you scored **${scorePct}%** on the **${mod.skill}** diagnostic. Don't worry—that's exactly why I'm here! I collaborated with the Curriculum Architect to insert a targeted **${mod.remedial?.title || `${mod.skill} Foundations Lab`}** right at the top of your active path so you can master the core concepts before moving forward.`
          }
        ]);
      }, 450);
    } else {
      // Passed Assessment (>= 60%)
      pushAgentLog(
        'evaluator',
        `Assessment passed with ${scorePct}% on ${mod.skill}! Updating learner skill proficiency.`,
        'MASTERY VERIFIED'
      );

      // Boost skill proficiency in profile
      const roleReq = ROLE_MATRICES[profile.targetRole]?.requirements[mod.skill] || 85;
      const currentVal = profile.skills[mod.skill] || 20;
      const boostedVal = mod.isRemedial
        ? Math.min(roleReq - 10, Math.max(currentVal + 25, 55))
        : Math.max(currentVal, roleReq);

      setProfile((prev) => ({
        ...prev,
        skills: {
          ...prev.skills,
          [mod.skill]: boostedVal
        }
      }));

      // Mark module completed & unlock next module
      setRoadmapModules((prev) => {
        const idx = prev.findIndex((m) => m.id === mod.id);
        if (idx === -1) return prev;
        const updated = [...prev];
        updated[idx] = {
          ...updated[idx],
          status: 'completed',
          lastScore: scorePct
        };
        if (idx + 1 < updated.length && updated[idx + 1].status === 'locked') {
          updated[idx + 1] = {
            ...updated[idx + 1],
            status: 'in-progress'
          };
        }
        return updated;
      });

      setTimeout(() => {
        pushAgentLog(
          'mentor',
          `Updated ${mod.skill} proficiency to ${boostedVal}% and unlocked the next roadmap stage.`,
          'PROGRESS SYNCED'
        );
      }, 300);

      setChatMessages((prev) => [
        ...prev,
        {
          id: `pass-${Date.now()}`,
          sender: 'mentor',
          text: `Awesome work scoring **${scorePct}%** on **${mod.title}**! Your verified **${mod.skill}** proficiency is now **${boostedVal}%**, and I've unlocked your next module.`
        }
      ]);
    }
  };

  const handleSubmitQuiz = () => {
    if (!activeQuizModule) return;
    const questions = ASSESSMENT_BANK[activeQuizModule.skill] || ASSESSMENT_BANK.DEFAULT;
    let correctCount = 0;
    questions.forEach((item, idx) => {
      if (quizAnswers[idx] === item.correct) correctCount++;
    });
    const pct = Math.round((correctCount / questions.length) * 100);
    evaluateQuizScore(activeQuizModule, pct);
  };

  // One-click Demo Simulation Trigger for Hackathon Judges
  const triggerLowScoreSimulation = () => {
    const activeMod =
      roadmapModules.find((m) => m.status === 'in-progress' && !m.isRemedial) ||
      roadmapModules.find((m) => !m.isRemedial) ||
      roadmapModules[0];
    if (!activeMod) return;
    evaluateQuizScore(activeMod, 33);
  };

  // Interactive AI Mentor Chat Handler
  const handleSendMessage = (e) => {
    e.preventDefault();
    const text = chatInput.trim();
    if (!text) return;

    setChatMessages((prev) => [
      ...prev,
      { id: `user-${Date.now()}`, sender: 'user', text }
    ]);
    setChatInput('');

    const lower = text.toLowerCase();
    setTimeout(() => {
      let reply = '';
      const activeMod = roadmapModules.find((m) => m.status === 'in-progress');
      const roleReqs = ROLE_MATRICES[profile.targetRole]?.requirements || {};
      const missingSkills = Object.entries(roleReqs)
        .filter(([sk, req]) => (profile.skills[sk] || 0) < req)
        .map(([sk]) => sk);

      if (lower.includes('gap') || lower.includes('missing') || lower.includes('weak')) {
        reply = missingSkills.length
          ? `For **${profile.targetRole}**, our Profiler Agent identified key skill gaps in **${missingSkills.join(', ')}**. Your strongest assets are **${Object.entries(profile.skills)
              .filter(([, v]) => v >= 70)
              .map(([k]) => k)
              .join(', ')}**.`
          : `You've closed all primary skill gaps for **${profile.targetRole}**! You are ready for capstone portfolio builds and mock interviews.`;
      } else if (lower.includes('next') || lower.includes('recommend') || lower.includes('what should')) {
        reply = activeMod
          ? `Your immediate priority is **${activeMod.title}** (${activeMod.duration}). Start with "${activeMod.resources[0]?.name}" and then take the diagnostic check to verify mastery.`
          : `All current modules are complete! Try switching your target career role in the top bar to test cross-role adaptation.`;
      } else if (lower.includes('backend') || lower.includes('ai') || lower.includes('cyber')) {
        const target = lower.includes('backend')
          ? 'Backend Engineer'
          : lower.includes('ai')
          ? 'AI / ML Engineer'
          : 'Cybersecurity Analyst';
        handleRoleChange(target);
        return;
      } else {
        reply = `I'm actively monitoring your **${profile.targetRole}** trajectory (${readinessPct}% role readiness). ${
          activeMod
            ? `Currently focused on **${activeMod.skill}** via "${activeMod.title}".`
            : 'All modules completed!'
        } Ask me about your **skill gaps**, **next steps**, or click **"Simulate Low Quiz Score"** to watch our agents adapt in real time.`;
      }

      pushAgentLog('mentor', `Responded to learner query with personalized context for ${profile.targetRole}.`, 'GUIDANCE');
      setChatMessages((prev) => [
        ...prev,
        { id: `mentor-${Date.now()}`, sender: 'mentor', text: reply }
      ]);
    }, 300);
  };

  // Compute Overall Role Readiness Score
  const currentRoleConfig = ROLE_MATRICES[profile.targetRole] || ROLE_MATRICES['Full Stack Developer'];
  const roleSkillEntries = Object.entries(currentRoleConfig.requirements);
  const readinessPct = Math.round(
    roleSkillEntries.reduce((acc, [skill, req]) => {
      const userVal = profile.skills[skill] || 0;
      return acc + Math.min(100, (userVal / req) * 100);
    }, 0) / roleSkillEntries.length
  );

  const completedCount = roadmapModules.filter((m) => m.status === 'completed').length;
  const roadmapProgressPct = roadmapModules.length
    ? Math.round((completedCount / roadmapModules.length) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30">
      {/* =====================================================================
          TOP NAVIGATION & AGENTIC STATUS HEADER
      ===================================================================== */}
      <header className="sticky top-0 z-30 border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
        <div className="max-w-[1440px] mx-auto px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-4">
          {/* Brand Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-violet-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold tracking-tight text-white">SkillForge AI</h1>
                <span className="text-[11px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30">
                  Agentic Learning OS
                </span>
              </div>
              <p className="text-xs text-slate-400">Multi-Agent Adaptive Career & Skill-Gap Platform</p>
            </div>
          </div>

          {/* Target Career Goal Selector */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5">
              <Target className="w-4 h-4 text-cyan-400 shrink-0" />
              <span className="text-xs text-slate-400 hidden sm:inline">Target Role:</span>
              <select
                value={profile.targetRole}
                onChange={(e) => handleRoleChange(e.target.value)}
                className="bg-transparent text-sm font-semibold text-white focus:outline-none cursor-pointer pr-1"
              >
                {Object.keys(ROLE_MATRICES).map((role) => (
                  <option key={role} value={role} className="bg-slate-900 text-white">
                    {role}
                  </option>
                ))}
              </select>
            </div>

            {/* Judge Demo Trigger Button */}
            <button
              onClick={triggerLowScoreSimulation}
              title="Simulates failing an assessment (<60%) to trigger live AI Mentor + Curriculum Architect remedial re-routing"
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 transition cursor-pointer"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>Simulate Low Quiz Score</span>
            </button>
          </div>
        </div>

        {/* Live 4-Agent Status Strip */}
        <div className="border-t border-slate-800/60 bg-slate-900/50">
          <div className="max-w-[1440px] mx-auto px-4 sm:px-6 py-2 flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex items-center gap-2 text-slate-400">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              <span className="font-medium text-slate-300">Active Agent Mesh:</span>
            </div>
            <div className="flex flex-wrap items-center gap-2 sm:gap-4">
              {Object.entries(AGENT_META).map(([key, meta]) => {
                const isPulsing = activeAgentPulse === key;
                return (
                  <div
                    key={key}
                    className={`flex items-center gap-2 px-2.5 py-1 rounded-lg border transition-all duration-300 ${
                      isPulsing
                        ? `${meta.bg} ${meta.border} scale-105 shadow-sm`
                        : 'bg-slate-900/80 border-slate-800/80'
                    }`}
                  >
                    <span
                      className={`w-2 h-2 rounded-full ${meta.dot} ${
                        isPulsing ? 'animate-ping' : ''
                      }`}
                    />
                    <span className={`font-medium ${meta.color}`}>{meta.name}</span>
                    <span className="hidden lg:inline text-slate-500">• {meta.role}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </header>

      {/* =====================================================================
          MAIN 3-COLUMN WORKSPACE
      ===================================================================== */}
      <main className="max-w-[1440px] mx-auto px-4 sm:px-6 py-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* -------------------------------------------------------------------
            LEFT COLUMN (3 Cols): LEARNER PROFILE, SKILLS, PROJECTS & CERTS
        ------------------------------------------------------------------- */}
        <section className="lg:col-span-3 space-y-6">
          {/* Learner Identity & Readiness Card */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <div className="flex items-center gap-3.5">
              <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-lg font-bold text-white shrink-0">
                AS
              </div>
              <div>
                <h2 className="font-bold text-white text-base">{profile.name}</h2>
                <p className="text-xs text-slate-400">{profile.title}</p>
              </div>
            </div>

            {/* Role Readiness Meter */}
            <div className="mt-5 p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="text-slate-400 font-medium">Role Match Readiness</span>
                <span className="font-bold text-cyan-400">{readinessPct}%</span>
              </div>
              <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400 transition-all duration-500"
                  style={{ width: `${readinessPct}%` }}
                />
              </div>
              <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">
                Target: <span className="text-slate-200 font-semibold">{profile.targetRole}</span>
              </p>
            </div>
          </div>

          {/* Current Skill Inventory + Add Skill */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Code2 className="w-4 h-4 text-indigo-400" />
                <span>Skill Inventory</span>
              </h3>
              <span className="text-[11px] text-slate-400">
                {Object.keys(profile.skills).length} Tracked
              </span>
            </div>

            <div className="space-y-2.5 max-h-60 overflow-y-auto pr-1">
              {Object.entries(profile.skills).map(([skill, score]) => {
                const isStrong = score >= 70;
                return (
                  <div
                    key={skill}
                    className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/70 flex items-center justify-between"
                  >
                    <div>
                      <div className="text-xs font-semibold text-slate-200">{skill}</div>
                      <div className="text-[10px] text-slate-500">
                        {isStrong ? 'Verified Strength' : 'Developing / Gap'}
                      </div>
                    </div>
                    <span
                      className={`text-xs font-bold px-2 py-0.5 rounded-md ${
                        isStrong
                          ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                          : 'bg-amber-500/15 text-amber-300 border border-amber-500/30'
                      }`}
                    >
                      {score}%
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Add / Update Skill Form */}
            <form onSubmit={handleAddSkill} className="mt-4 pt-4 border-t border-slate-800 space-y-2.5">
              <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                Add / Update Skill
              </div>
              <input
                type="text"
                placeholder="e.g., Docker, PyTorch, React..."
                value={newSkillName}
                onChange={(e) => setNewSkillName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              <div className="flex items-center gap-2">
                <input
                  type="range"
                  min="10"
                  max="100"
                  step="5"
                  value={newSkillLevel}
                  onChange={(e) => setNewSkillLevel(e.target.value)}
                  className="flex-1 accent-indigo-500 cursor-pointer"
                />
                <span className="text-xs font-mono text-slate-300 w-9 text-right">
                  {newSkillLevel}%
                </span>
              </div>
              <button
                type="submit"
                className="w-full py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Sync Skill with Profiler Agent</span>
              </button>
            </form>
          </div>

          {/* Projects & Certifications */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5 mb-2.5">
                <FolderGit2 className="w-3.5 h-3.5 text-cyan-400" />
                <span>Verified Projects</span>
              </h3>
              <ul className="space-y-2">
                {profile.projects.map((proj, i) => (
                  <li
                    key={i}
                    className="text-xs text-slate-300 bg-slate-950/60 border border-slate-800/70 rounded-lg p-2.5"
                  >
                    {proj}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5 mb-2.5">
                <Award className="w-3.5 h-3.5 text-amber-400" />
                <span>Certifications</span>
              </h3>
              <ul className="space-y-2">
                {profile.certifications.map((cert, i) => (
                  <li
                    key={i}
                    className="text-xs text-slate-300 bg-slate-950/60 border border-slate-800/70 rounded-lg p-2.5"
                  >
                    {cert}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* -------------------------------------------------------------------
            CENTER COLUMN (5 Cols): SKILL-GAP ANALYSIS & ADAPTIVE ROADMAP
        ------------------------------------------------------------------- */}
        <section className="lg:col-span-5 space-y-6">
          {/* Skill Gap Comparison Card */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-cyan-400" />
                <span>Skill-Gap Analysis: {profile.targetRole}</span>
              </h3>
              <div className="flex items-center gap-3 text-[11px]">
                <span className="flex items-center gap-1 text-slate-300">
                  <span className="w-2.5 h-2.5 rounded-sm bg-indigo-500 inline-block" /> Yours
                </span>
                <span className="flex items-center gap-1 text-slate-400">
                  <span className="w-2.5 h-2.5 rounded-sm border border-cyan-400 border-dashed inline-block" /> Target
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-400 mb-4">{currentRoleConfig.description}</p>

            <div className="space-y-3.5">
              {roleSkillEntries.map(([skill, reqScore]) => {
                const userScore = profile.skills[skill] || 0;
                const gap = Math.max(0, reqScore - userScore);
                const isMet = gap === 0;

                return (
                  <div key={skill} className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-slate-200">{skill}</span>
                        {isMet ? (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 font-medium">
                            Strength Met
                          </span>
                        ) : (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/15 text-rose-300 border border-rose-500/30 font-medium">
                            Gap: -{gap}%
                          </span>
                        )}
                      </div>
                      <span className="font-mono text-slate-400">
                        <strong className="text-white">{userScore}%</strong> / {reqScore}%
                      </span>
                    </div>

                    {/* Comparative Bar */}
                    <div className="relative h-3 w-full bg-slate-950 rounded-full border border-slate-800 overflow-hidden">
                      {/* Target Benchmark Marker */}
                      <div
                        className="absolute top-0 bottom-0 border-r-2 border-dashed border-cyan-400 z-10"
                        style={{ width: `${reqScore}%` }}
                      />
                      {/* User Current Proficiency Fill */}
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
                          isMet
                            ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
                            : 'bg-gradient-to-r from-indigo-500 to-violet-500'
                        }`}
                        style={{ width: `${Math.min(100, userScore)}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Personalized Adaptive Learning Roadmap */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Layers className="w-4 h-4 text-violet-400" />
                  <span>Adaptive Learning Roadmap</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Sequenced by Curriculum Architect • Dynamically re-routed by AI Mentor
                </p>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-violet-300">{roadmapProgressPct}%</div>
                <div className="text-[10px] text-slate-400">
                  {completedCount}/{roadmapModules.length} Modules
                </div>
              </div>
            </div>

            {/* Roadmap Module Cards */}
            <div className="space-y-3.5">
              {roadmapModules.map((mod, index) => {
                const isCompleted = mod.status === 'completed';
                const isInProgress = mod.status === 'in-progress';
                const isLocked = mod.status === 'locked';

                return (
                  <div
                    key={mod.id}
                    className={`rounded-xl border p-4 transition-all ${
                      mod.isRemedial
                        ? 'bg-amber-950/25 border-amber-500/50 shadow-lg shadow-amber-500/5'
                        : isInProgress
                        ? 'bg-indigo-950/25 border-indigo-500/50 shadow-lg shadow-indigo-500/5'
                        : isCompleted
                        ? 'bg-slate-950/60 border-emerald-500/30'
                        : 'bg-slate-950/40 border-slate-800/80 opacity-75'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-start gap-3">
                        {/* Status Icon */}
                        <div className="mt-0.5">
                          {isCompleted ? (
                            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                          ) : mod.isRemedial ? (
                            <ShieldAlert className="w-5 h-5 text-amber-400 animate-pulse" />
                          ) : isInProgress ? (
                            <Circle className="w-5 h-5 text-indigo-400" />
                          ) : (
                            <Lock className="w-5 h-5 text-slate-600" />
                          )}
                        </div>

                        <div>
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                              Stage {index + 1} • {mod.skill}
                            </span>
                            {mod.isRemedial && (
                              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40">
                                AI Mentor Remedial Injection
                              </span>
                            )}
                            <span className="text-[11px] text-slate-400">{mod.duration}</span>
                          </div>

                          <h4 className="font-bold text-sm text-white mt-1.5">{mod.title}</h4>

                          {/* Curated Resources */}
                          <div className="mt-2.5 space-y-1.5">
                            {mod.resources.map((res, rIdx) => (
                              <div
                                key={rIdx}
                                className="flex items-center gap-2 text-xs text-slate-300 bg-slate-900/90 px-2.5 py-1.5 rounded-lg border border-slate-800/80"
                              >
                                <BookOpen className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                                <span className="text-[10px] font-semibold uppercase text-cyan-300">
                                  {res.kind}:
                                </span>
                                <span className="truncate">{res.name}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Action Footer */}
                    <div className="mt-3.5 pt-3 border-t border-slate-800/70 flex items-center justify-between">
                      <div className="text-xs text-slate-400">
                        {mod.lastScore !== null ? (
                          <span>
                            Last Diagnostic Score:{' '}
                            <strong
                              className={
                                mod.lastScore >= 60 ? 'text-emerald-400' : 'text-rose-400'
                              }
                            >
                              {mod.lastScore}%
                            </strong>
                          </span>
                        ) : (
                          <span>Type: {mod.type}</span>
                        )}
                      </div>

                      {!isLocked && (
                        <button
                          onClick={() => openAssessment(mod)}
                          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                            isCompleted
                              ? 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                              : mod.isRemedial
                              ? 'bg-amber-500 hover:bg-amber-400 text-slate-950'
                              : 'bg-indigo-600 hover:bg-indigo-500 text-white'
                          }`}
                        >
                          <Play className="w-3 h-3" />
                          <span>{isCompleted ? 'Retake Quiz' : 'Take Skill Assessment'}</span>
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* -------------------------------------------------------------------
            RIGHT COLUMN (4 Cols): LIVE MULTI-AGENT CONSOLE & AI MENTOR CHAT
        ------------------------------------------------------------------- */}
        <section className="lg:col-span-4 space-y-6">
          {/* Live Multi-Agent Collaboration Feed */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col h-[360px]">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-400" />
                <span>Multi-Agent Collaboration Log</span>
              </h3>
              <span className="flex items-center gap-1.5 text-[11px] text-emerald-400 font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                Live Stream
              </span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2.5 pr-1 font-mono text-xs">
              {agentLogs.map((log) => {
                const meta = AGENT_META[log.agent] || AGENT_META.mentor;
                return (
                  <div
                    key={log.id}
                    className={`p-2.5 rounded-xl border ${meta.bg} ${meta.border} transition-all`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className={`font-bold text-[11px] ${meta.color}`}>{meta.name}</span>
                      <div className="flex items-center gap-1.5">
                        {log.badge && (
                          <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-slate-950/80 text-slate-200 border border-slate-700">
                            {log.badge}
                          </span>
                        )}
                        <span className="text-[10px] text-slate-500">{log.timestamp}</span>
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-200 leading-relaxed font-sans">
                      {log.message}
                    </p>
                  </div>
                );
              })}
              <div ref={logsEndRef} />
            </div>
          </div>

          {/* Interactive AI Mentor Assistant */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col h-[410px]">
            <div className="flex items-center justify-between mb-3 pb-2.5 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">AI Mentor Orchestrator</h3>
                  <p className="text-[10px] text-slate-400">
                    Adaptive guidance & live path recalibration
                  </p>
                </div>
              </div>
            </div>

            {/* Chat History */}
            <div className="flex-1 overflow-y-auto space-y-3 pr-1">
              {chatMessages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[88%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed ${
                      msg.sender === 'user'
                        ? 'bg-indigo-600 text-white rounded-br-sm'
                        : 'bg-slate-950 border border-slate-800 text-slate-200 rounded-bl-sm'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>

            {/* Quick Prompt Chips */}
            <div className="flex flex-wrap gap-1.5 mt-3 mb-2">
              {[
                'What are my skill gaps?',
                'What should I learn next?',
                'Pivot to AI / ML Engineer'
              ].map((prompt) => (
                <button
                  key={prompt}
                  type="button"
                  onClick={() => {
                    setChatInput(prompt);
                  }}
                  className="text-[10px] px-2.5 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition cursor-pointer"
                >
                  {prompt}
                </button>
              ))}
            </div>

            {/* Chat Input */}
            <form onSubmit={handleSendMessage} className="flex items-center gap-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask AI Mentor or request a role pivot..."
                className="flex-1 px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
              <button
                type="submit"
                className="p-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white transition cursor-pointer"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </section>
      </main>

      {/* =====================================================================
          INTERACTIVE SKILL ASSESSMENT MODAL
      ===================================================================== */}
      {activeQuizModule && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-5">
            <div className="flex items-start justify-between gap-4 border-b border-slate-800 pb-4">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/15 text-amber-300 border border-amber-500/30">
                  Assessment Evaluator Agent
                </span>
                <h3 className="text-lg font-bold text-white mt-1.5">{activeQuizModule.title}</h3>
                <p className="text-xs text-slate-400">
                  Score &ge; 60% to verify mastery, or &lt; 60% to trigger AI Mentor remedial adaptation.
                </p>
              </div>
              <button
                onClick={() => setActiveQuizModule(null)}
                className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Questions List */}
            <div className="space-y-4 max-h-[55vh] overflow-y-auto pr-1">
              {(ASSESSMENT_BANK[activeQuizModule.skill] || ASSESSMENT_BANK.DEFAULT).map(
                (item, qIdx) => (
                  <div
                    key={qIdx}
                    className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2.5"
                  >
                    <p className="text-xs font-semibold text-white">
                      {qIdx + 1}. {item.q}
                    </p>
                    <div className="space-y-1.5">
                      {item.options.map((opt, oIdx) => {
                        const selected = quizAnswers[qIdx] === oIdx;
                        return (
                          <button
                            key={oIdx}
                            type="button"
                            onClick={() =>
                              setQuizAnswers((prev) => ({ ...prev, [qIdx]: oIdx }))
                            }
                            className={`w-full text-left px-3 py-2 rounded-lg text-xs border transition cursor-pointer ${
                              selected
                                ? 'bg-indigo-600/25 border-indigo-500 text-white font-medium'
                                : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700'
                            }`}
                          >
                            {opt}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                )
              )}
            </div>

            {/* Quiz Result Banner */}
            {quizResult !== null && (
              <div
                className={`p-3.5 rounded-xl border text-xs flex items-center justify-between ${
                  quizResult >= 60
                    ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-200'
                    : 'bg-amber-500/15 border-amber-500/40 text-amber-200'
                }`}
              >
                <div>
                  <strong>Diagnostic Score: {quizResult}%</strong> —{' '}
                  {quizResult >= 60
                    ? 'Mastery verified! Next module unlocked.'
                    : 'Below 60% threshold. AI Mentor injected a Remedial Module into your roadmap!'}
                </div>
              </div>
            )}

            {/* Modal Footer Buttons */}
            <div className="flex items-center justify-between pt-2 border-t border-slate-800">
              <button
                type="button"
                onClick={() => evaluateQuizScore(activeQuizModule, 33)}
                className="text-xs text-amber-400 hover:text-amber-300 underline cursor-pointer"
              >
                Quick-Fail (33%) to Test Remedial Loop
              </button>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setActiveQuizModule(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 cursor-pointer"
                >
                  Close
                </button>
                <button
                  type="button"
                  onClick={handleSubmitQuiz}
                  className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white cursor-pointer"
                >
                  Submit to Evaluator Agent
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
