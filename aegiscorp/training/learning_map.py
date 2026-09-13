"""AegisCorp OS — Role Training Encyclopedia Version 2.0 (Authoritative Learning Map).

Research Snapshot: 13 September 2026.
Contains complete learning maps, training resource links, and authoritative reference works /
encyclopedia citations for all 48 enterprise roles across the Board, C-suite, and 7 departmental ladders:
- 11 Master Learning Tracks with starting resources and rationales.
- Curated Primary Training Resources (MIT OpenCourseWare, Harvard, Google Career Certificates,
  Microsoft Learn, NIST CSF 2.0 & AI RMF, OWASP, GitHub Awesome collections, Coursera).
- Authoritative Reference Works & Encyclopedias (Wiley Encyclopedia of Management, Oxford Research
  Encyclopedia, Encyclopedia of Software Engineering, Encyclopedia of Financial Models,
  The Encyclopedia of Human-Computer Interaction 2nd Ed., Encyclopedia in Operations Management 2026,
  The Encyclopedia of Human Resource Management, Encyclopedia of Business Analytics and Optimization, etc.).
- Evidence Recording Metadata complying with Blueprint Section 28.2.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import time


class TrainingResource(BaseModel):
    title: str
    track: str
    url: str
    description: str
    provider: str
    is_primary: bool = True


class BookReference(BaseModel):
    title: str
    publisher: str
    url: str
    role_focus: str
    description: str


class EvidenceMetadata(BaseModel):
    url: str
    retrieved_at: float = Field(default_factory=time.time)
    source_type: str  # "academic", "industry_certification", "government_standard", "curated_oss"
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    license_terms: str


class RoleLearningMap(BaseModel):
    role_id: str
    role_title: str
    department: str
    level: str  # e.g. "Board", "C-suite", "VP", "Director", "Senior Manager", "Manager", "Lead", "Senior IC", "IC", "Junior IC", "Coordinator", "Associate", "Supervisor"
    core_capability_profile: str
    role_focus_summary: str
    training_resources: List[TrainingResource]
    book_references: List[BookReference]
    evidence_policy_note: str = "Store URL, retrieval timestamp, source type, relevance and license terms (Blueprint §28.2)."


class MasterLearningTrack(BaseModel):
    track_id: str
    name: str
    starting_resources: str
    link: str
    why_it_matters: str


# =============================================================================
# 11 MASTER LEARNING TRACKS (Blueprint Section 2)
# =============================================================================

MASTER_LEARNING_STACK: List[MasterLearningTrack] = [
    MasterLearningTrack(
        track_id="ai_ml",
        name="AI / ML",
        starting_resources="MIT Artificial Intelligence; Microsoft AI Fundamentals; Google AI / Career Certificates",
        link="https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/",
        why_it_matters="Concepts, problem solving, learning systems",
    ),
    MasterLearningTrack(
        track_id="software_cs",
        name="Software / CS",
        starting_resources="CS50; Meta/IBM software certificates; GitHub Awesome Machine Learning",
        link="https://cs50.harvard.edu/",
        why_it_matters="Programming, CS foundations, projects",
    ),
    MasterLearningTrack(
        track_id="cybersecurity_privacy",
        name="Cybersecurity / Privacy",
        starting_resources="NIST CSF + AI RMF; Microsoft Security Engineer; OWASP resources",
        link="https://www.nist.gov/cyberframework",
        why_it_matters="Governance, security, privacy, secure engineering",
    ),
    MasterLearningTrack(
        track_id="cloud_architecture",
        name="Cloud / Architecture",
        starting_resources="Google Professional Cloud Architect; Microsoft Learn; AWS Training",
        link="https://cloud.google.com/learn/certification/cloud-architect",
        why_it_matters="Secure/reliable/cost-aware systems",
    ),
    MasterLearningTrack(
        track_id="product",
        name="Product",
        starting_resources="GitHub Awesome Product Management; Google UX; experimentation / analytics programs",
        link="https://github.com/dend/awesome-product-management",
        why_it_matters="Discovery, roadmap, experiments, product economics",
    ),
    MasterLearningTrack(
        track_id="business_strategy",
        name="Business / Strategy",
        starting_resources="MIT Sloan Entrepreneurship; MIT Advanced Strategy; Harvard management/leadership",
        link="https://ocw.mit.edu/pages/entrepreneurship/",
        why_it_matters="Strategy, scaling, governance, leadership",
    ),
    MasterLearningTrack(
        track_id="finance_economics",
        name="Finance / Economics",
        starting_resources="MIT Principles of Microeconomics; MIT Entrepreneurial Finance; OpenStax business/economics",
        link="https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/",
        why_it_matters="Economics, valuation, capital allocation",
    ),
    MasterLearningTrack(
        track_id="operations",
        name="Operations",
        starting_resources="MIT Operations Management",
        link="https://ocw.mit.edu/courses/15-760a-operations-management-spring-2002/",
        why_it_matters="Process, capacity, supply chain, quality",
    ),
    MasterLearningTrack(
        track_id="people_hr",
        name="People / HR",
        starting_resources="MIT organizational leadership resources; Harvard management; OpenStax Psychology",
        link="https://ocw.mit.edu/courses/15-394-designing-and-leading-the-entrepreneurial-organization-spring-2003/",
        why_it_matters="Org design, behavior, talent, leadership",
    ),
    MasterLearningTrack(
        track_id="sales_negotiation",
        name="Sales / Negotiation",
        starting_resources="Harvard Negotiation; Salesforce learning pathways",
        link="https://pll.harvard.edu/subject/negotiation",
        why_it_matters="Negotiation, account strategy, decision-making",
    ),
    MasterLearningTrack(
        track_id="marketing",
        name="Marketing",
        starting_resources="Google Digital Marketing; GitHub Awesome Marketing",
        link="https://grow.google/intl/en_in/certificates/",
        why_it_matters="Growth, analytics, channel and brand systems",
    ),
]


# =============================================================================
# SHARED BOOK REFERENCES CATALOG
# =============================================================================

BOOKS = {
    "wiley_management": BookReference(
        title="Wiley Encyclopedia of Management",
        publisher="Wiley",
        url="https://onlinelibrary.wiley.com/doi/book/10.1002/9781118785317",
        role_focus="Enterprise governance, strategy, and organizational management",
        description="Broad reference across strategy, governance, organization, innovation and management.",
    ),
    "oxford_business": BookReference(
        title="Oxford Research Encyclopedia of Business and Management",
        publisher="Oxford University Press",
        url="https://academic.oup.com/edited-volume/61793",
        role_focus="Business research, innovation, and strategic organization",
        description="Peer-reviewed reference articles across strategy, entrepreneurship, HR, organization, technology and innovation.",
    ),
    "sage_leadership": BookReference(
        title="Encyclopedia of Leadership (SAGE)",
        publisher="SAGE Publications",
        url="https://www.sagepub.com/shop/buy-a-book/encyclopedia-of-leadership-1-220818",
        role_focus="Executive leadership, corporate culture, and organizational contexts",
        description="Leadership theories, practices, cases, styles and organizational contexts.",
    ),
    "financial_models": BookReference(
        title="Encyclopedia of Financial Models",
        publisher="Wiley",
        url="https://onlinelibrary.wiley.com/doi/book/10.1002/9781118182635",
        role_focus="Valuation, risk, financial econometrics, and quantitative modeling",
        description="Advanced reference for valuation, asset pricing, risk, financial econometrics and quantitative financial modeling.",
    ),
    "business_analytics": BookReference(
        title="Encyclopedia of Business Analytics and Optimization",
        publisher="IGI Global",
        url="https://www.igi-global.com/book/encyclopedia-business-analytics-optimization/90651",
        role_focus="Big data analytics, optimization, and decision support",
        description="Reference on big data analytics, optimization, visualization, data mining, decision support and supply-chain analytics.",
    ),
    "palgrave_entrepreneurship": BookReference(
        title="The Palgrave Encyclopedia of Entrepreneurship",
        publisher="Springer / Palgrave",
        url="https://link.springer.com/referencework/10.1007/978-3-030-68128-9",
        role_focus="Venture creation, scaling ecosystems, and innovation leadership",
        description="Comprehensive reference on entrepreneurship, venture creation, growth and entrepreneurial ecosystems.",
    ),
    "operations_management_2026": BookReference(
        title="Encyclopedia in Operations Management (2026)",
        publisher="Elsevier",
        url="https://shop.elsevier.com/books/encyclopedia-in-operations-management/choi/978-0-443-28993-4",
        role_focus="Operations strategy, Industry 4.0, digital transformation, and analytics",
        description="Current operations reference covering Industry 4.0, digital transformation, sustainability, agile methods and analytics.",
    ),
    "software_engineering": BookReference(
        title="Encyclopedia of Software Engineering",
        publisher="Wiley",
        url="https://onlinelibrary.wiley.com/doi/book/10.1002/0471028959",
        role_focus="Software architecture, design, testing, distributed systems, and process",
        description="Software engineering reference covering architecture, design, testing, configuration, databases, distributed systems and process.",
    ),
    "information_systems": BookReference(
        title="Encyclopedia of Information Systems",
        publisher="Elsevier",
        url="https://shop.elsevier.com/books/encyclopedia-of-information-systems/bidgoli/978-0-08-091794-8",
        role_focus="Enterprise information systems, databases, security, and AI",
        description="Reference across information systems, databases, security, AI, ERP, project management and technology management.",
    ),
    "ml_data_mining": BookReference(
        title="Encyclopedia of Machine Learning and Data Mining",
        publisher="Springer",
        url="https://link.springer.com/referencework/10.1007/978-1-4899-7687-1",
        role_focus="Machine learning, statistical learning, RL, and data mining",
        description="Large reference covering machine learning, data mining, statistical learning, reinforcement learning and applications.",
    ),
    "wiley_marketing": BookReference(
        title="Wiley International Encyclopedia of Marketing",
        publisher="Wiley",
        url="https://onlinelibrary.wiley.com/doi/book/10.1002/9781444316568",
        role_focus="Marketing strategy, consumer behavior, research, and communications",
        description="Six-volume marketing reference covering strategy, research, consumer behavior, communications, product and international marketing.",
    ),
    "human_computer_interaction": BookReference(
        title="The Encyclopedia of Human-Computer Interaction, 2nd Ed.",
        publisher="Interaction Design Foundation",
        url="https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed",
        role_focus="UX, interaction design, requirements engineering, and usability",
        description="Free online encyclopedia covering UX, interaction design, requirements engineering, usability and related topics.",
    ),
    "human_resource_management": BookReference(
        title="The Encyclopedia of Human Resource Management",
        publisher="Wiley",
        url="https://onlinelibrary.wiley.com/doi/book/10.1002/9781118364741",
        role_focus="Talent management, performance, learning, and workforce systems",
        description="Comprehensive HRM reference covering talent, performance, learning, employee relations and workforce practice.",
    ),
}


# =============================================================================
# 48 ROLE LEARNING MAPS (Blueprint Section 3)
# =============================================================================

ROLE_LEARNING_MAPS: Dict[str, RoleLearningMap] = {}


def _register_learning_map(lm: RoleLearningMap):
    ROLE_LEARNING_MAPS[lm.role_id] = lm


# 1. BOARD OF DIRECTORS
_register_learning_map(RoleLearningMap(
    role_id="board",
    role_title="Board of Directors",
    department="Enterprise Leadership",
    level="Board",
    core_capability_profile="Corporate governance, fiduciary reasoning, strategy, capital allocation, risk, technology and AI governance, scenario planning.",
    role_focus_summary="Enterprise governance, fiduciary oversight and long-horizon value.",
    training_resources=[
        TrainingResource(title="MIT Advanced Strategy", track="Business / Strategy", url="https://ocw.mit.edu/courses/15-963-advanced-strategy-spring-2008/", description="Competitive advantage and long-term strategy.", provider="MIT OCW"),
        TrainingResource(title="Harvard Management & Leadership", track="Business / Strategy", url="https://pll.harvard.edu/subject/management-leadership", description="Leadership, strategy and executive decision-making.", provider="Harvard"),
        TrainingResource(title="MIT Microeconomics", track="Finance / Economics", url="https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/", description="Market structure and decision analysis.", provider="MIT OCW"),
        TrainingResource(title="NIST AI RMF", track="Cybersecurity / Privacy", url="https://www.nist.gov/itl/ai-risk-management-framework", description="Trustworthy AI risk management.", provider="NIST"),
        TrainingResource(title="NIST CSF 2.0", track="Cybersecurity / Privacy", url="https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20", description="Enterprise cyber-risk governance.", provider="NIST"),
    ],
    book_references=[
        BOOKS["wiley_management"],
        BOOKS["oxford_business"],
        BOOKS["sage_leadership"],
        BOOKS["financial_models"],
    ],
))

# 2. CHIEF EXECUTIVE OFFICER
_register_learning_map(RoleLearningMap(
    role_id="ceo",
    role_title="Chief Executive Officer",
    department="Enterprise Leadership",
    level="C-suite",
    core_capability_profile="Strategy, corporate finance, org design, competitive strategy, negotiation, technology literacy and decision-making under uncertainty.",
    role_focus_summary="Enterprise strategy, leadership, scaling and capital allocation.",
    training_resources=[
        TrainingResource(title="MIT Advanced Strategy", track="Business / Strategy", url="https://ocw.mit.edu/courses/15-963-advanced-strategy-spring-2008/", description="Long-term competitive advantage.", provider="MIT OCW"),
        TrainingResource(title="MIT Scaling Entrepreneurial Ventures", track="Business / Strategy", url="https://ocw.mit.edu/courses/15-392-scaling-entrepreneurial-ventures-spring-2026/", description="Leadership, culture, operations and governance at scale.", provider="MIT OCW"),
        TrainingResource(title="Harvard Negotiation", track="Sales / Negotiation", url="https://pll.harvard.edu/subject/negotiation", description="High-stakes bargaining and decision-making.", provider="Harvard"),
        TrainingResource(title="Harvard Management & Leadership", track="Business / Strategy", url="https://pll.harvard.edu/subject/management-leadership", description="Executive leadership curriculum.", provider="Harvard"),
    ],
    book_references=[
        BOOKS["wiley_management"],
        BOOKS["sage_leadership"],
        BOOKS["palgrave_entrepreneurship"],
        BOOKS["oxford_business"],
    ],
))

# 3. CHIEF FINANCIAL OFFICER
_register_learning_map(RoleLearningMap(
    role_id="cfo",
    role_title="Chief Financial Officer",
    department="Finance",
    level="C-suite",
    core_capability_profile="Advanced valuation, forecasting, capital structure, treasury, portfolio theory, audit, tax literacy and probabilistic finance.",
    role_focus_summary="Financial modeling, valuation, risk and executive decision support.",
    training_resources=[
        TrainingResource(title="MIT Entrepreneurial Finance", track="Finance / Economics", url="https://ocw.mit.edu/courses/15-431-entrepreneurial-finance-spring-2011/", description="Funding, valuation and private-market finance.", provider="MIT OCW"),
        TrainingResource(title="MIT Microeconomics", track="Finance / Economics", url="https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/", description="Market and firm decision models.", provider="MIT OCW"),
        TrainingResource(title="Google Data Analytics", track="Data / Analytics", url="https://www.coursera.org/professional-certificates/google-data-analytics", description="Data cleaning, analysis, visualization and decision support.", provider="Google / Coursera"),
    ],
    book_references=[
        BOOKS["financial_models"],
        BOOKS["business_analytics"],
        BOOKS["wiley_management"],
        BOOKS["oxford_business"],
    ],
))

# 4. CHIEF OPERATING OFFICER
_register_learning_map(RoleLearningMap(
    role_id="coo",
    role_title="Chief Operating Officer",
    department="Operations",
    level="C-suite",
    core_capability_profile="Operations research, supply chain, capacity, quality, program management, risk and automation.",
    role_focus_summary="Operations strategy, process excellence, analytics and execution.",
    training_resources=[
        TrainingResource(title="MIT Operations Management", track="Operations", url="https://ocw.mit.edu/courses/15-760a-operations-management-spring-2002/", description="Process, supply chain, quality and design.", provider="MIT OCW"),
        TrainingResource(title="MIT Introduction to Operations Management", track="Operations", url="https://ocw.mit.edu/courses/15-761-introduction-to-operations-management-spring-2013/", description="Capacity, inventory, sustainability and risk.", provider="MIT OCW"),
        TrainingResource(title="Google Project Management", track="Operations", url="https://grow.google/intl/en_in/certificates/", description="Structured delivery and stakeholder management.", provider="Google"),
    ],
    book_references=[
        BOOKS["operations_management_2026"],
        BOOKS["business_analytics"],
        BOOKS["wiley_management"],
        BOOKS["oxford_business"],
    ],
))

# 5. CHIEF TECHNOLOGY OFFICER
_register_learning_map(RoleLearningMap(
    role_id="cto",
    role_title="Chief Technology Officer",
    department="Technology",
    level="C-suite",
    core_capability_profile="Software architecture, distributed systems, AI/ML, cybersecurity, data engineering, reliability, research-to-production and IP.",
    role_focus_summary="Technology strategy, software systems, information systems and AI.",
    training_resources=[
        TrainingResource(title="MIT Artificial Intelligence", track="AI / ML", url="https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/", description="Knowledge representation, learning and intelligent systems.", provider="MIT OCW"),
        TrainingResource(title="Google Professional Cloud Architect", track="Cloud / Architecture", url="https://cloud.google.com/learn/certification/cloud-architect", description="Secure, reliable, optimized cloud architectures.", provider="Google Cloud"),
        TrainingResource(title="Microsoft Security Engineer", track="Cybersecurity / Privacy", url="https://learn.microsoft.com/en-us/training/career-paths/security-engineer", description="Secure systems and security engineering.", provider="Microsoft Learn"),
        TrainingResource(title="Awesome Machine Learning", track="AI / ML", url="https://github.com/josephmisiti/awesome-machine-learning", description="Curated ML frameworks, tools, courses and projects.", provider="GitHub"),
    ],
    book_references=[
        BOOKS["software_engineering"],
        BOOKS["information_systems"],
        BOOKS["ml_data_mining"],
        BOOKS["wiley_management"],
    ],
))

# 6. CHIEF MARKETING OFFICER
_register_learning_map(RoleLearningMap(
    role_id="cmo",
    role_title="Chief Marketing Officer",
    department="Marketing",
    level="C-suite",
    core_capability_profile="Marketing science, psychology, positioning, experimentation, analytics, attribution, competitive intelligence and crisis communication.",
    role_focus_summary="Marketing strategy, customer insight, analytics and brand systems.",
    training_resources=[
        TrainingResource(title="Google Career Certificates", track="Marketing", url="https://grow.google/intl/en_in/certificates/", description="Digital marketing and analytics training.", provider="Google"),
        TrainingResource(title="Awesome Marketing", track="Marketing", url="https://github.com/ronakganatra/awesome-marketing", description="Living resource collection for marketers.", provider="GitHub"),
        TrainingResource(title="OpenStax resources", track="People / HR", url="https://openstax.org/openstax-assignable-subject-resource-guides", description="Open educational material including Psychology.", provider="OpenStax"),
    ],
    book_references=[
        BOOKS["wiley_marketing"],
        BOOKS["business_analytics"],
        BOOKS["wiley_management"],
        BOOKS["oxford_business"],
    ],
))

# 7. CHIEF REVENUE OFFICER
_register_learning_map(RoleLearningMap(
    role_id="cro",
    role_title="Chief Revenue Officer",
    department="Revenue",
    level="C-suite",
    core_capability_profile="Sales science, GTM, pipeline math, negotiation, pricing, account growth, territory and partner strategy.",
    role_focus_summary="Revenue strategy, customer economics, sales and market execution.",
    training_resources=[
        TrainingResource(title="Harvard Negotiation", track="Sales / Negotiation", url="https://pll.harvard.edu/subject/negotiation", description="Negotiation and decision-making.", provider="Harvard"),
        TrainingResource(title="Coursera career certificates", track="Sales / Negotiation", url="https://www.coursera.org/certificates/launch-your-career", description="Sales development and sales operations pathways.", provider="Coursera"),
        TrainingResource(title="MIT Microeconomics", track="Finance / Economics", url="https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/", description="Pricing, demand and firm behavior.", provider="MIT OCW"),
    ],
    book_references=[
        BOOKS["wiley_marketing"],
        BOOKS["business_analytics"],
        BOOKS["wiley_management"],
        BOOKS["oxford_business"],
    ],
))

# 8. CHIEF HUMAN RESOURCES OFFICER
_register_learning_map(RoleLearningMap(
    role_id="chro",
    role_title="Chief Human Resources Officer",
    department="People",
    level="C-suite",
    core_capability_profile="Organizational psychology, talent strategy, compensation, learning, employee relations, analytics and succession.",
    role_focus_summary="People strategy, leadership, organizational behavior and HR systems.",
    training_resources=[
        TrainingResource(title="MIT Entrepreneurial Organization", track="People / HR", url="https://ocw.mit.edu/courses/15-394-designing-and-leading-the-entrepreneurial-organization-spring-2003/", description="Organizational architecture, behavior and leadership.", provider="MIT OCW"),
        TrainingResource(title="Harvard Management & Leadership", track="Business / Strategy", url="https://pll.harvard.edu/subject/management-leadership", description="Leadership and people management.", provider="Harvard"),
        TrainingResource(title="OpenStax resources", track="People / HR", url="https://openstax.org/openstax-assignable-subject-resource-guides", description="Psychology and business foundations.", provider="OpenStax"),
    ],
    book_references=[
        BOOKS["human_resource_management"],
        BOOKS["sage_leadership"],
        BOOKS["wiley_management"],
        BOOKS["oxford_business"],
    ],
))

# 9. CHIEF PRODUCT OFFICER
_register_learning_map(RoleLearningMap(
    role_id="cpo",
    role_title="Chief Product Officer",
    department="Product",
    level="C-suite",
    core_capability_profile="Product strategy, user research, experimentation, analytics, roadmaps, economics, ecosystems and responsible AI.",
    role_focus_summary="Product strategy, UX, technology context and customer value.",
    training_resources=[
        TrainingResource(title="Awesome Product Management", track="Product", url="https://github.com/dend/awesome-product-management", description="Curated PM resources, tools and learning.", provider="GitHub"),
        TrainingResource(title="Google UX Design", track="Product", url="https://grow.google/intl/ssa-en/google-career-certificates/ux-design/", description="Research, prototyping and user testing.", provider="Google"),
        TrainingResource(title="Coursera certificates", track="Product", url="https://www.coursera.org/professional-certificates", description="Includes AI product manager and related paths.", provider="Coursera"),
    ],
    book_references=[
        BOOKS["human_computer_interaction"],
        BOOKS["wiley_marketing"],
        BOOKS["information_systems"],
        BOOKS["wiley_management"],
    ],
))

# -----------------------------------------------------------------------------
# ENGINEERING LADDER (8 Roles)
# -----------------------------------------------------------------------------

_eng_books = [
    BOOKS["software_engineering"],
    BOOKS["information_systems"],
    BOOKS["ml_data_mining"],
    BOOKS["business_analytics"],
]

_eng_resources_standard = [
    TrainingResource(title="CS50", track="Software / CS", url="https://cs50.harvard.edu/", description="Programming and computer science fundamentals.", provider="Harvard"),
    TrainingResource(title="Google Cloud Architect", track="Cloud / Architecture", url="https://cloud.google.com/learn/certification/cloud-architect", description="Architecture, reliability and optimization.", provider="Google Cloud"),
    TrainingResource(title="NIST CSF", track="Cybersecurity / Privacy", url="https://www.nist.gov/cyberframework", description="Cybersecurity risk foundations.", provider="NIST"),
    TrainingResource(title="OWASP", track="Cybersecurity / Privacy", url="https://owasp.org/", description="Application-security knowledge and testing resources.", provider="OWASP"),
    TrainingResource(title="Awesome Machine Learning", track="AI / ML", url="https://github.com/josephmisiti/awesome-machine-learning", description="ML tools, courses and research.", provider="GitHub"),
]

_eng_resources_devsec = _eng_resources_standard + [
    TrainingResource(title="Microsoft secure software development", track="Cybersecurity / Privacy", url="https://learn.microsoft.com/en-us/training/paths/secure-software-development-for-cybersecurity/", description="Security across the software lifecycle.", provider="Microsoft Learn"),
]

_register_learning_map(RoleLearningMap(
    role_id="vp_eng",
    role_title="VP Engineering",
    department="Engineering",
    level="VP",
    core_capability_profile="Large-scale architecture, org design, reliability, technical strategy, security, AI-assisted engineering and technical debt economics.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_devsec,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="director_eng",
    role_title="Director Engineering",
    department="Engineering",
    level="Director",
    core_capability_profile="Architecture review, distributed systems, delivery planning, testing, security, performance and incident management.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_standard,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sr_eng_mgr",
    role_title="Senior Engineering Manager",
    department="Engineering",
    level="Senior Manager",
    core_capability_profile="Delivery, architecture literacy, leadership, risk, forecasting, hiring and incident leadership.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_standard,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="eng_mgr",
    role_title="Engineering Manager",
    department="Engineering",
    level="Manager",
    core_capability_profile="Engineering management, planning, estimation, quality, coaching and incident response.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_standard,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="tech_lead",
    role_title="Tech Lead / Staff Engineer",
    department="Engineering",
    level="Technical IC",
    core_capability_profile="First-principles design, trade-offs, performance, reliability, security, mentoring and prototyping.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_devsec,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sr_swe",
    role_title="Senior Software Engineer",
    department="Engineering",
    level="Senior IC",
    core_capability_profile="Advanced programming, system design, testing, security, performance, debugging and research.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_devsec,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="swe",
    role_title="Software Engineer",
    department="Engineering",
    level="IC",
    core_capability_profile="Software fundamentals, algorithms, APIs, databases, testing, debugging, secure coding and version control.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_devsec,
    book_references=_eng_books,
))

_register_learning_map(RoleLearningMap(
    role_id="junior_eng",
    role_title="Junior Engineer",
    department="Engineering",
    level="Junior IC",
    core_capability_profile="Programming fundamentals, algorithms, testing, debugging, secure development and rapid learning.",
    role_focus_summary="Engineering role-specific reference depth.",
    training_resources=_eng_resources_devsec,
    book_references=_eng_books,
))

# -----------------------------------------------------------------------------
# PRODUCT LADDER (6 Roles)
# -----------------------------------------------------------------------------

_prod_books = [
    BOOKS["human_computer_interaction"],
    BOOKS["wiley_marketing"],
    BOOKS["information_systems"],
    BOOKS["oxford_business"],
]

_prod_resources = [
    TrainingResource(title="Awesome Product Management", track="Product", url="https://github.com/dend/awesome-product-management", description="Product strategy, discovery, analytics and roadmaps.", provider="GitHub"),
    TrainingResource(title="Google UX Design", track="Product", url="https://grow.google/intl/ssa-en/google-career-certificates/ux-design/", description="Prototyping and user testing.", provider="Google"),
    TrainingResource(title="Google Data Analytics", track="Data / Analytics", url="https://www.coursera.org/professional-certificates/google-data-analytics", description="Data analysis and visualization.", provider="Google / Coursera"),
    TrainingResource(title="Coursera Professional Certificates", track="Product", url="https://www.coursera.org/professional-certificates", description="Role-oriented programs including AI product, analytics and project management.", provider="Coursera"),
]

_register_learning_map(RoleLearningMap(
    role_id="vp_prod",
    role_title="VP Product",
    department="Product",
    level="VP",
    core_capability_profile="Portfolio strategy, product economics, customer intelligence, experimentation, org design and GTM alignment.",
    role_focus_summary="Product role-specific reference depth.",
    training_resources=_prod_resources,
    book_references=_prod_books,
))

_register_learning_map(RoleLearningMap(
    role_id="director_prod",
    role_title="Director Product",
    department="Product",
    level="Director",
    core_capability_profile="Portfolio management, discovery, analytics, cross-functional execution, roadmap optimization and product risk.",
    role_focus_summary="Product role-specific reference depth.",
    training_resources=_prod_resources,
    book_references=_prod_books,
))

_register_learning_map(RoleLearningMap(
    role_id="gpm",
    role_title="Group Product Manager",
    department="Product",
    level="GPM",
    core_capability_profile="Multi-product strategy, analytics, research, experimentation, coaching and business cases.",
    role_focus_summary="Product role-specific reference depth.",
    training_resources=_prod_resources,
    book_references=_prod_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sr_pm",
    role_title="Senior Product Manager",
    department="Product",
    level="Senior PM",
    core_capability_profile="Advanced discovery, research, analytics, experimentation, roadmap and delivery leadership.",
    role_focus_summary="Product role-specific reference depth.",
    training_resources=_prod_resources,
    book_references=_prod_books,
))

_register_learning_map(RoleLearningMap(
    role_id="pm",
    role_title="Product Manager",
    department="Product",
    level="PM",
    core_capability_profile="Discovery, requirements, user research, metrics, experimentation and roadmap execution.",
    role_focus_summary="Product role-specific reference depth.",
    training_resources=_prod_resources,
    book_references=_prod_books,
))

_register_learning_map(RoleLearningMap(
    role_id="apm",
    role_title="Associate Product Manager",
    department="Product",
    level="APM",
    core_capability_profile="Customer discovery, analytics, competitive research, requirements and experiment support.",
    role_focus_summary="Product role-specific reference depth.",
    training_resources=_prod_resources,
    book_references=_prod_books,
))

# -----------------------------------------------------------------------------
# SALES LADDER (5 Roles)
# -----------------------------------------------------------------------------

_sales_books = [
    BOOKS["wiley_marketing"],
    BOOKS["oxford_business"],
    BOOKS["wiley_management"],
    BOOKS["sage_leadership"],
]

_sales_resources = [
    TrainingResource(title="Harvard Negotiation", track="Sales / Negotiation", url="https://pll.harvard.edu/subject/negotiation", description="Decision-making and bargaining.", provider="Harvard"),
    TrainingResource(title="Coursera sales pathways", track="Sales / Negotiation", url="https://www.coursera.org/certificates/launch-your-career", description="Sales development and operations.", provider="Coursera"),
    TrainingResource(title="MIT Microeconomics", track="Finance / Economics", url="https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/", description="Pricing, market structure and firm behavior.", provider="MIT OCW"),
]

_register_learning_map(RoleLearningMap(
    role_id="reg_sales_dir",
    role_title="Regional Sales Director",
    department="Sales",
    level="Director",
    core_capability_profile="Regional strategy, enterprise sales leadership, forecasting, negotiation, channel strategy and talent development.",
    role_focus_summary="Sales role-specific reference depth.",
    training_resources=_sales_resources,
    book_references=_sales_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sales_mgr",
    role_title="Sales Manager",
    department="Sales",
    level="Manager",
    core_capability_profile="Pipeline, forecasting, coaching, territory planning, negotiation and revenue analytics.",
    role_focus_summary="Sales role-specific reference depth.",
    training_resources=_sales_resources,
    book_references=_sales_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sales_team_lead",
    role_title="Team Lead",
    department="Sales",
    level="Lead",
    core_capability_profile="Deal strategy, coaching, pipeline analytics, account planning and objection handling.",
    role_focus_summary="Sales role-specific reference depth.",
    training_resources=_sales_resources,
    book_references=_sales_books,
))

_register_learning_map(RoleLearningMap(
    role_id="ae",
    role_title="Account Executive",
    department="Sales",
    level="IC",
    core_capability_profile="Consultative selling, discovery, value engineering, negotiation, commercial modeling and account strategy.",
    role_focus_summary="Sales role-specific reference depth.",
    training_resources=_sales_resources,
    book_references=_sales_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sdr",
    role_title="SDR",
    department="Sales",
    level="Junior IC",
    core_capability_profile="Market research, prospecting, qualification, messaging experiments, CRM and signal prioritization.",
    role_focus_summary="Sales role-specific reference depth.",
    training_resources=_sales_resources,
    book_references=_sales_books,
))

# -----------------------------------------------------------------------------
# MARKETING LADDER (5 Roles)
# -----------------------------------------------------------------------------

_mktg_books = [
    BOOKS["wiley_marketing"],
    BOOKS["business_analytics"],
    BOOKS["wiley_management"],
    BOOKS["oxford_business"],
]

_mktg_resources = [
    TrainingResource(title="Google Career Certificates", track="Marketing", url="https://grow.google/intl/en_in/certificates/", description="Digital marketing and e-commerce.", provider="Google"),
    TrainingResource(title="Awesome Marketing", track="Marketing", url="https://github.com/ronakganatra/awesome-marketing", description="Living collection of marketing resources.", provider="GitHub"),
    TrainingResource(title="Google Data Analytics", track="Data / Analytics", url="https://www.coursera.org/professional-certificates/google-data-analytics", description="Analytics and measurement.", provider="Google / Coursera"),
]

_register_learning_map(RoleLearningMap(
    role_id="vp_mktg",
    role_title="VP Marketing",
    department="Marketing",
    level="VP",
    core_capability_profile="Enterprise marketing strategy, brand/growth, market intelligence, attribution and budget optimization.",
    role_focus_summary="Marketing role-specific reference depth.",
    training_resources=_mktg_resources,
    book_references=_mktg_books,
))

_register_learning_map(RoleLearningMap(
    role_id="director_mktg",
    role_title="Director Marketing",
    department="Marketing",
    level="Director",
    core_capability_profile="Campaign portfolio, audience strategy, performance analytics, content/channel optimization and brand governance.",
    role_focus_summary="Marketing role-specific reference depth.",
    training_resources=_mktg_resources,
    book_references=_mktg_books,
))

_register_learning_map(RoleLearningMap(
    role_id="mktg_mgr",
    role_title="Marketing Manager",
    department="Marketing",
    level="Manager",
    core_capability_profile="Campaign planning, growth experiments, content, analytics, budget and cross-functional execution.",
    role_focus_summary="Marketing role-specific reference depth.",
    training_resources=_mktg_resources,
    book_references=_mktg_books,
))

_register_learning_map(RoleLearningMap(
    role_id="mktg_spec",
    role_title="Marketing Specialist",
    department="Marketing",
    level="Specialist",
    core_capability_profile="Channel expertise, content optimization, SEO/SEM, experimentation and audience analytics.",
    role_focus_summary="Marketing role-specific reference depth.",
    training_resources=_mktg_resources,
    book_references=_mktg_books,
))

_register_learning_map(RoleLearningMap(
    role_id="mktg_coord",
    role_title="Marketing Coordinator",
    department="Marketing",
    level="Coordinator",
    core_capability_profile="Campaign operations, research/reporting, content coordination, data hygiene and vendor coordination.",
    role_focus_summary="Marketing role-specific reference depth.",
    training_resources=_mktg_resources,
    book_references=_mktg_books,
))

# -----------------------------------------------------------------------------
# FINANCE LADDER (5 Roles)
# -----------------------------------------------------------------------------

_fin_books = [
    BOOKS["financial_models"],
    BOOKS["business_analytics"],
    BOOKS["wiley_management"],
    BOOKS["oxford_business"],
]

_fin_resources = [
    TrainingResource(title="MIT Entrepreneurial Finance", track="Finance / Economics", url="https://ocw.mit.edu/courses/15-431-entrepreneurial-finance-spring-2011/", description="Valuation, funding and capital decisions.", provider="MIT OCW"),
    TrainingResource(title="MIT Microeconomics", track="Finance / Economics", url="https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/", description="Demand, firm behavior and markets.", provider="MIT OCW"),
    TrainingResource(title="Google Data Analytics", track="Data / Analytics", url="https://www.coursera.org/professional-certificates/google-data-analytics", description="Financial/decision analytics foundations.", provider="Google / Coursera"),
]

_register_learning_map(RoleLearningMap(
    role_id="vp_fin",
    role_title="VP Finance",
    department="Finance",
    level="VP",
    core_capability_profile="Corporate finance, FP&A, capital allocation, risk-adjusted investment, investor communications and controls.",
    role_focus_summary="Finance role-specific reference depth.",
    training_resources=_fin_resources,
    book_references=_fin_books,
))

_register_learning_map(RoleLearningMap(
    role_id="fin_dir",
    role_title="Finance Director",
    department="Finance",
    level="Director",
    core_capability_profile="Planning, forecasting, reporting, controls, audit readiness, scenarios and business partnering.",
    role_focus_summary="Finance role-specific reference depth.",
    training_resources=_fin_resources,
    book_references=_fin_books,
))

_register_learning_map(RoleLearningMap(
    role_id="fin_mgr",
    role_title="Finance Manager",
    department="Finance",
    level="Manager",
    core_capability_profile="Budgeting, variance, cash flow, controls, operational finance and forecasting.",
    role_focus_summary="Finance role-specific reference depth.",
    training_resources=_fin_resources,
    book_references=_fin_books,
))

_register_learning_map(RoleLearningMap(
    role_id="sr_fin_analyst",
    role_title="Senior Analyst",
    department="Finance",
    level="Senior IC",
    core_capability_profile="Advanced analysis, forecasting, modeling, valuation, scenarios and decision support.",
    role_focus_summary="Finance role-specific reference depth.",
    training_resources=_fin_resources,
    book_references=_fin_books,
))

_register_learning_map(RoleLearningMap(
    role_id="fin_analyst",
    role_title="Financial Analyst",
    department="Finance",
    level="IC",
    core_capability_profile="Modeling, data analysis, budget tracking, variance analysis, research and reporting.",
    role_focus_summary="Finance role-specific reference depth.",
    training_resources=_fin_resources,
    book_references=_fin_books,
))

# -----------------------------------------------------------------------------
# OPERATIONS LADDER (5 Roles)
# -----------------------------------------------------------------------------

_ops_books = [
    BOOKS["operations_management_2026"],
    BOOKS["business_analytics"],
    BOOKS["wiley_management"],
    BOOKS["oxford_business"],
]

_ops_resources = [
    TrainingResource(title="MIT Operations Management", track="Operations", url="https://ocw.mit.edu/courses/15-760a-operations-management-spring-2002/", description="Process, supply chain and quality.", provider="MIT OCW"),
    TrainingResource(title="MIT Introduction to Operations Management", track="Operations", url="https://ocw.mit.edu/courses/15-761-introduction-to-operations-management-spring-2013/", description="Capacity, risk, quality and revenue management.", provider="MIT OCW"),
    TrainingResource(title="Google Project Management", track="Operations", url="https://grow.google/intl/en_in/certificates/", description="Delivery and execution discipline.", provider="Google"),
]

_register_learning_map(RoleLearningMap(
    role_id="vp_ops",
    role_title="VP Operations",
    department="Operations",
    level="VP",
    core_capability_profile="Enterprise operations strategy, optimization, capacity, supply chain, process engineering and risk.",
    role_focus_summary="Operations role-specific reference depth.",
    training_resources=_ops_resources,
    book_references=_ops_books,
))

_register_learning_map(RoleLearningMap(
    role_id="ops_dir",
    role_title="Operations Director",
    department="Operations",
    level="Director",
    core_capability_profile="Operational planning, process optimization, quality, resources, continuity and analytics.",
    role_focus_summary="Operations role-specific reference depth.",
    training_resources=_ops_resources,
    book_references=_ops_books,
))

_register_learning_map(RoleLearningMap(
    role_id="ops_mgr",
    role_title="Operations Manager",
    department="Operations",
    level="Manager",
    core_capability_profile="Daily execution, workflow, capacity, quality, team coordination and KPI management.",
    role_focus_summary="Operations role-specific reference depth.",
    training_resources=_ops_resources,
    book_references=_ops_books,
))

_register_learning_map(RoleLearningMap(
    role_id="ops_sup",
    role_title="Supervisor",
    department="Operations",
    level="Supervisor",
    core_capability_profile="Frontline leadership, work allocation, QA, safety, escalation and coaching.",
    role_focus_summary="Operations role-specific reference depth.",
    training_resources=_ops_resources,
    book_references=_ops_books,
))

_register_learning_map(RoleLearningMap(
    role_id="ops_assoc",
    role_title="Operations Associate",
    department="Operations",
    level="Associate",
    core_capability_profile="Process execution, data accuracy, problem solving, documentation, quality and improvement.",
    role_focus_summary="Operations role-specific reference depth.",
    training_resources=_ops_resources,
    book_references=_ops_books,
))

# -----------------------------------------------------------------------------
# PEOPLE LADDER (5 Roles)
# -----------------------------------------------------------------------------

_people_books = [
    BOOKS["human_resource_management"],
    BOOKS["sage_leadership"],
    BOOKS["wiley_management"],
    BOOKS["oxford_business"],
]

_people_resources = [
    TrainingResource(title="MIT Entrepreneurial Organization", track="People / HR", url="https://ocw.mit.edu/courses/15-394-designing-and-leading-the-entrepreneurial-organization-spring-2003/", description="Org design, culture and leadership.", provider="MIT OCW"),
    TrainingResource(title="Harvard Management & Leadership", track="Business / Strategy", url="https://pll.harvard.edu/subject/management-leadership", description="Leadership and management.", provider="Harvard"),
    TrainingResource(title="OpenStax resources", track="People / HR", url="https://openstax.org/openstax-assignable-subject-resource-guides", description="Psychology and behavior foundations.", provider="OpenStax"),
]

_register_learning_map(RoleLearningMap(
    role_id="vp_people",
    role_title="VP People",
    department="People",
    level="VP",
    core_capability_profile="People strategy, workforce planning, org design, leadership, compensation and people analytics.",
    role_focus_summary="People role-specific reference depth.",
    training_resources=_people_resources,
    book_references=_people_books,
))

_register_learning_map(RoleLearningMap(
    role_id="hr_dir",
    role_title="HR Director",
    department="People",
    level="Director",
    core_capability_profile="Talent systems, workforce planning, employee relations, policy governance, analytics and succession.",
    role_focus_summary="People role-specific reference depth.",
    training_resources=_people_resources,
    book_references=_people_books,
))

_register_learning_map(RoleLearningMap(
    role_id="hr_mgr",
    role_title="HR Manager",
    department="People",
    level="Manager",
    core_capability_profile="Hiring ops, performance management, relations, policy execution, coaching and workforce reporting.",
    role_focus_summary="People role-specific reference depth.",
    training_resources=_people_resources,
    book_references=_people_books,
))

_register_learning_map(RoleLearningMap(
    role_id="hrbp",
    role_title="HR Business Partner",
    department="People",
    level="HRBP",
    core_capability_profile="Org consulting, manager coaching, workforce analytics, change management and talent planning.",
    role_focus_summary="People role-specific reference depth.",
    training_resources=_people_resources,
    book_references=_people_books,
))

_register_learning_map(RoleLearningMap(
    role_id="hr_coord",
    role_title="HR Generalist / Coordinator",
    department="People",
    level="Generalist",
    core_capability_profile="HR operations, recruiting coordination, lifecycle admin, policy support, data quality and confidentiality.",
    role_focus_summary="People role-specific reference depth.",
    training_resources=_people_resources,
    book_references=_people_books,
))


# =============================================================================
# HIGH-VALUE REFERENCE LIBRARY (Blueprint Section 5)
# =============================================================================

HIGH_VALUE_REFERENCE_LIBRARY = [
    {"name": "MIT OpenCourseWare — Artificial Intelligence", "url": "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/", "focus": "AI fundamentals, knowledge representation, problem solving and learning."},
    {"name": "MIT OpenCourseWare — Principles of Microeconomics", "url": "https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/", "focus": "Economics foundations for strategy, pricing and market analysis."},
    {"name": "MIT OpenCourseWare — Operations Management", "url": "https://ocw.mit.edu/courses/15-760a-operations-management-spring-2002/", "focus": "Operations and supply-chain principles."},
    {"name": "MIT OpenCourseWare — Advanced Strategy", "url": "https://ocw.mit.edu/courses/15-963-advanced-strategy-spring-2008/", "focus": "Long-term competitive advantage and strategic management."},
    {"name": "MIT OpenCourseWare — Scaling Entrepreneurial Ventures", "url": "https://ocw.mit.edu/courses/15-392-scaling-entrepreneurial-ventures-spring-2026/", "focus": "Scaling leadership, governance, operations, GTM and culture."},
    {"name": "MIT OpenCourseWare — Entrepreneurial Finance", "url": "https://ocw.mit.edu/courses/15-431-entrepreneurial-finance-spring-2011/", "focus": "Valuation, fundraising, financing and venture finance."},
    {"name": "MIT OpenCourseWare — Entrepreneurial Organization", "url": "https://ocw.mit.edu/courses/15-394-designing-and-leading-the-entrepreneurial-organization-spring-2003/", "focus": "Org design, culture, behavior, leadership and HR."},
    {"name": "Harvard — Management & Leadership", "url": "https://pll.harvard.edu/subject/management-leadership", "focus": "Leadership, strategy, negotiation and management offerings."},
    {"name": "Harvard — Negotiation", "url": "https://pll.harvard.edu/subject/negotiation", "focus": "Negotiation and decision-making training."},
    {"name": "Google Career Certificates — India", "url": "https://grow.google/intl/en_in/certificates/", "focus": "AI, cybersecurity, data analytics, digital marketing, project management, UX and IT."},
    {"name": "Google Professional Cloud Architect", "url": "https://cloud.google.com/learn/certification/cloud-architect", "focus": "Cloud architecture and reliability."},
    {"name": "Microsoft Learn — Security Engineer", "url": "https://learn.microsoft.com/en-us/training/career-paths/security-engineer", "focus": "Security engineering role training."},
    {"name": "Microsoft Learn — AI Security Fundamentals", "url": "https://learn.microsoft.com/en-us/training/paths/ai-security-fundamentals/", "focus": "AI security controls and testing."},
    {"name": "NIST — Cybersecurity Framework 2.0", "url": "https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20", "focus": "Cybersecurity risk governance."},
    {"name": "NIST — AI Risk Management Framework", "url": "https://www.nist.gov/itl/ai-risk-management-framework", "focus": "Trustworthy AI risk management."},
    {"name": "OWASP", "url": "https://owasp.org/", "focus": "Application security knowledge and resources."},
    {"name": "GitHub — Awesome Machine Learning", "url": "https://github.com/josephmisiti/awesome-machine-learning", "focus": "Curated ML resources and tools."},
    {"name": "GitHub — Awesome Product Management", "url": "https://github.com/dend/awesome-product-management", "focus": "PM resources and learning."},
    {"name": "GitHub — Awesome Marketing", "url": "https://github.com/ronakganatra/awesome-marketing", "focus": "Curated marketing resources."},
    {"name": "Coursera Professional Certificates", "url": "https://www.coursera.org/professional-certificates", "focus": "Role-oriented pathways across IT, data, sales/marketing and business."},
]


# =============================================================================
# HELPER QUERY FUNCTIONS
# =============================================================================

def get_role_learning_map(role_id: str) -> Optional[RoleLearningMap]:
    """Retrieve learning map for a given role ID."""
    return ROLE_LEARNING_MAPS.get(role_id)


def list_role_learning_maps() -> List[RoleLearningMap]:
    """Retrieve learning maps for all 48 roles."""
    return list(ROLE_LEARNING_MAPS.values())


def get_master_learning_stack() -> List[MasterLearningTrack]:
    """Retrieve the 11 blueprint master learning tracks."""
    return MASTER_LEARNING_STACK


def get_high_value_reference_library() -> List[Dict[str, str]]:
    """Retrieve the high-value reference library index."""
    return HIGH_VALUE_REFERENCE_LIBRARY


def search_learning_resources(query: str) -> List[Dict[str, Any]]:
    """Search training resources and book references across all 48 roles."""
    q = query.lower()
    results = []
    
    for r_id, lm in ROLE_LEARNING_MAPS.items():
        # Match resources
        for res in lm.training_resources:
            if q in res.title.lower() or q in res.description.lower() or q in res.track.lower():
                results.append({
                    "role_id": r_id,
                    "role_title": lm.role_title,
                    "type": "training_resource",
                    "title": res.title,
                    "track": res.track,
                    "url": res.url,
                    "description": res.description,
                    "provider": res.provider,
                })
        # Match books
        for bk in lm.book_references:
            if q in bk.title.lower() or q in bk.description.lower() or q in bk.publisher.lower() or q in bk.role_focus.lower():
                results.append({
                    "role_id": r_id,
                    "role_title": lm.role_title,
                    "type": "book_reference",
                    "title": bk.title,
                    "publisher": bk.publisher,
                    "url": bk.url,
                    "role_focus": bk.role_focus,
                    "description": bk.description,
                })

    return results
