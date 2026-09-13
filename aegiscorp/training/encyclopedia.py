"""AegisCorp OS — Corporate Role Encyclopedia & Historical Precedents Corpus.

Provides authoritative encyclopedic dossiers for all 48 enterprise roles across
the Board of Directors, Executive C-Suite, and all 7 departmental ladders:
- Canonical Ontological Definitions & Organizational Mandates
- Historical Landmark Case Studies & Institutional Failures (Enron, Boeing 737 MAX, Knight Capital, etc.)
- Pathology Anti-Patterns & Catastrophic Failure Modes
- Cross-Disciplinary Domain Glossaries & Technical Lexicons
- Elite Cognitive Heuristics & Decision Frameworks
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from aegiscorp.training.learning_map import (
    TrainingResource,
    BookReference,
    get_role_learning_map,
)


class HistoricalCaseStudy(BaseModel):
    title: str
    organization: str
    year: int
    incident_summary: str
    root_cause: str
    catastrophic_impact: str
    lessons_learned: str
    role_implication: str


class FailureMode(BaseModel):
    name: str
    symptoms: List[str]
    root_cause: str
    catastrophic_impact: str
    mitigation_protocol: str


class GlossaryTerm(BaseModel):
    term: str
    definition: str
    domain: str
    cross_reference: Optional[str] = None


class DecisionHeuristic(BaseModel):
    name: str
    principle: str
    application: str


class EncyclopediaEntry(BaseModel):
    role_id: str
    role_title: str
    department: str
    level: int
    canonical_definition: str
    core_mandate: str
    historical_case_studies: List[HistoricalCaseStudy]
    failure_modes: List[FailureMode]
    key_glossary: List[GlossaryTerm]
    decision_heuristics: List[DecisionHeuristic]
    core_capability_profile: Optional[str] = None
    role_focus_summary: Optional[str] = None
    training_resources: List[TrainingResource] = Field(default_factory=list)
    book_references: List[BookReference] = Field(default_factory=list)


# -----------------------------------------------------------------------------
# 48 ROLE ENCYCLOPEDIC DOSSIERS
# -----------------------------------------------------------------------------

ENCYCLOPEDIA: Dict[str, EncyclopediaEntry] = {}


def _register(entry: EncyclopediaEntry):
    ENCYCLOPEDIA[entry.role_id] = entry


# =============================================================================
# 1. GOVERNANCE: BOARD OF DIRECTORS
# =============================================================================
_register(EncyclopediaEntry(
    role_id="board",
    role_title="Board of Directors",
    department="Governance",
    level=0,
    canonical_definition=(
        "The supreme governing organ of the enterprise, acting as the elected fiduciary fiduciaries of shareholders. "
        "The Board holds ultimate constitutional authority over enterprise strategy, capital allocation (> $100M), "
        "executive appointment and succession, corporate charters, and systemic risk governance."
    ),
    core_mandate="Protect and maximize sustainable long-term enterprise value while ensuring uncompromising fiduciary integrity.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Off-Balance Sheet Deception and Audit Committee Passivity",
            organization="Enron Corporation",
            year=2001,
            incident_summary="Enron utilized special purpose entities (SPEs) like Chewco and LJM to hide billions in toxic debt and inflate earnings, collapsing into Chapter 11.",
            root_cause="Board audit committee rubber-stamped complex related-party transactions and waived corporate codes of ethics without independent forensic scrutiny.",
            catastrophic_impact="$74B market capitalization wiped out, bankruptcy of Arthur Andersen, and total loss of shareholder wealth.",
            lessons_learned="Boards must possess independent technical accounting expertise and independently challenge management assertions rather than accepting executive consensus.",
            role_implication="The Board of Directors must enforce explicit independent risk audit channels and never waive ethical or conflict-of-interest charters."
        ),
        HistoricalCaseStudy(
            title="Charismatic Deference and Absence of Technical Governance",
            organization="Theranos",
            year=2018,
            incident_summary="Theranos raised over $700M claiming breakthrough blood-testing technology on the Edison device, which failed to function and produced fraudulent clinical results.",
            root_cause="Board composed of elder statesmen and military leaders lacking clinical diagnostic or biomedical engineering acumen, creating epistemic vulnerability.",
            catastrophic_impact="Complete company liquidation, criminal fraud convictions of founders, and severe patient health endangerment.",
            lessons_learned="Board composition must maintain functional domain mastery matching the fundamental core technology of the enterprise.",
            role_implication="Directors have an affirmative duty to verify physical and empirical claims rather than relying solely on charismatic executive narratives."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Agency Problem & Management Capture",
            symptoms=["Board agendas set entirely by CEO", "Absence of dissenting votes", "Executive compensation unlinked to long-term risk-adjusted metrics"],
            root_cause="Information asymmetry between inside management and outside directors.",
            catastrophic_impact="Strategic blindspots, value-destroying M&A, and unchecked corporate malfeasance.",
            mitigation_protocol="Mandate independent executive sessions without CEO present; appoint an independent Lead Director; retain direct board forensic counsel."
        ),
        FailureMode(
            name="Conglomerate Capital Misallocation",
            symptoms=["Acquiring non-core assets to mask slowing organic growth", "Subsidizing decaying business units with high-margin cash cows"],
            root_cause="Growth-at-all-costs mandate without rigorous ROIC vs WACC hurdle rate verification.",
            catastrophic_impact="Conglomerate discount, liquidity exhaustion, and credit rating downgrades.",
            mitigation_protocol="Enforce strict capital rationing hurdle rates (ROIC > WACC + 500 bps) and require post-mortem lookbacks on all capital expenditures."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="Fiduciary Duty", definition="The legal obligation of highest loyalty and care owed by directors to the corporation and its shareholders.", domain="Corporate Law"),
        GlossaryTerm(term="Business Judgment Rule", definition="A legal presumption that in making a business decision, directors acted on an informed basis, in good faith, and in honest belief.", domain="Corporate Governance"),
        GlossaryTerm(term="Agency Costs", definition="The internal costs arising from conflicts of interest between principals (shareholders) and agents (managers).", domain="Institutional Economics")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Inversion Principle", principle="Avoid catastrophic failure before seeking optimal upside.", application="Stress-test all capital allocation against severe recessionary and solvency scenarios."),
        DecisionHeuristic(name="Chesterton's Fence", principle="Never dismantle a governance constraint until the reason for its existence is understood.", application="Do not relax approval gates or threshold limits without historical context analysis.")
    ]
))

# =============================================================================
# 2. EXECUTIVE: CHIEF EXECUTIVE OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="ceo",
    role_title="Chief Executive Officer",
    department="Executive",
    level=1,
    canonical_definition=(
        "The chief executive officer and principal strategic architect of the enterprise. "
        "Responsible for overall capital allocation, executive hiring, organizational design, cross-functional synthesis, "
        "and stewarding the company toward multi-trillion-dollar valuation milestones."
    ),
    core_mandate="Drive durable enterprise value creation, strategic coherence, and decisive executive leadership under uncertainty.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Conglomerate Financial Engineering and Industrial Decay",
            organization="General Electric",
            year=2018,
            incident_summary="GE relied heavily on GE Capital's debt-fueled financial returns to mask structural manufacturing stagnation, leading to massive write-downs and breakup.",
            root_cause="Executive pursuit of smooth quarterly EPS growth via short-term financial leverage rather than fundamental technological moat-building.",
            catastrophic_impact="Stock plummeted over 80%, dividend cut to a penny, and eventual corporate spin-off into three separate entities.",
            lessons_learned="CEOs must prioritize technological and product moats over balance sheet accounting maneuvers.",
            role_implication="The CEO must inspect underlying unit economics and technical health directly rather than relying on aggregated financial dashboards."
        ),
        HistoricalCaseStudy(
            title="Strategic Drift and Platform Substitution Blindness",
            organization="Blockbuster LLC",
            year=2010,
            incident_summary="Blockbuster passed on acquiring Netflix for $50M in 2000 and clung to physical retail stores and late-fee revenue models until Chapter 11 bankruptcy.",
            root_cause="Cognitive lock-in to legacy cash-flow streams and inability to reallocate capital into streaming infrastructure.",
            catastrophic_impact="Complete liquidation of 9,000 stores and total market obsolescence.",
            lessons_learned="CEOs must cannibalize their own legacy revenue models before external competitors do so permanently.",
            role_implication="The CEO must foster counter-inductive strategy and fund disruptive exploratory units even when they threaten current profitability."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Founder/CEO Hubris & Governance Bypass",
            symptoms=["Ignoring executive dissent", "Circumventing formal risk limits", "Pursuing vanity projects without ROI frameworks"],
            root_cause="Overconfidence heuristic amplified by early success and echo-chamber executive team.",
            catastrophic_impact="Catastrophic capital burn, regulatory investigation, and loss of institutional trust.",
            mitigation_protocol="Institutionalize formal Red Teams, devil's advocate reviews, and mandatory Board escalation for transformative initiatives."
        ),
        FailureMode(
            name="Operational Micromanagement (HiPPO Syndrome)",
            symptoms=["CEO bottlenecking routine pull requests or marketing copy", "C-suite paralysis awaiting top-down instruction"],
            root_cause="Inability to transition from early-stage tactical founder to enterprise capital allocator.",
            catastrophic_impact="Organizational velocity collapse, talent attrition of tier-1 executives, and executive burnout.",
            mitigation_protocol="Enforce clear Authority Matrix limits; delegate operational execution fully within signed budget bounds."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="Capital Allocation", definition="The systematic distribution of financial and human capital across competing projects to maximize return on invested capital.", domain="Corporate Finance"),
        GlossaryTerm(term="Economic Moat", definition="A sustainable competitive advantage that protects a company's market share and long-term operating profits from competitors.", domain="Strategic Management"),
        GlossaryTerm(term="Ambidextrous Organization", definition="An enterprise capable of simultaneously exploiting existing competencies while exploring new, disruptive opportunities.", domain="Organizational Theory")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Pareto Frontier Optimization", principle="Focus resources on the vital 20% of inputs generating 80% of enterprise returns.", application="Eliminate low-yield departmental programs to fund high-conviction strategic thrusts."),
        DecisionHeuristic(name="OODA Loop Pacing", principle="Observe, Orient, Decide, Act faster than the competitive environment.", application="Establish rapid corporate execution rhythms and automated feedback telemetry.")
    ]
))

# =============================================================================
# 3. EXECUTIVE: CHIEF FINANCIAL OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="cfo",
    role_title="Chief Financial Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The senior executive responsible for financial integrity, capital structure, treasury liquidity, "
        "financial planning and analysis (FP&A), regulatory reporting (GAAP/IFRS), and systemic solvency defense."
    ),
    core_mandate="Guarantee corporate liquidity, optimize cost of capital, and enforce unyielding fiscal discipline across all operations.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Liquidity Contagion and Balance Sheet Window-Dressing",
            organization="Lehman Brothers",
            year=2008,
            incident_summary="Lehman used Repo 105 transactions to temporarily remove $50B in toxic assets from balance sheets right before quarterly reporting, masking excessive 30:1 leverage.",
            root_cause="Aggressive balance sheet masking, reliance on overnight wholesale repo funding, and structural neglect of asset-liability duration mismatch.",
            catastrophic_impact="Largest bankruptcy in US history ($639B assets), triggering global financial contagion.",
            lessons_learned="Liquidity and solvency are not negotiable; short-term wholesale debt cannot fund illiquid long-term assets.",
            role_implication="The CFO must maintain robust liquid operating reserves (min 24 months runway) and reject off-balance-sheet obfuscations."
        ),
        HistoricalCaseStudy(
            title="Fictitious Escrow Balances and Internal Control Failure",
            organization="Wirecard AG",
            year=2020,
            incident_summary="Wirecard collapsed after €1.9B in reported cash balances in Philippine trustee bank accounts was revealed to be entirely fictitious.",
            root_cause="Collusion between executive leadership, absence of direct bank confirmations, and failure to independently reconcile clearing account ledgers.",
            catastrophic_impact="Insolvency, arrest of CEO, loss of €24B in enterprise value, and reputational damage to European financial auditing.",
            lessons_learned="CFOs must personally verify direct custodial asset proofs and enforce strict zero-trust cash reconciliation protocols.",
            role_implication="The CFO must insist on mathematical and cryptographic verification of all corporate liquid reserves."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Liquidity Squeeze / Runway Blindness",
            symptoms=["Cash burn exceeding forecast by > 20%", "Accounts receivable aging past 90 days", "Failure to stress-test revenue shocks"],
            root_cause="Optimistic forecasting heuristics and failure to maintain cash buffers for macroeconomic downturns.",
            catastrophic_impact="Emergency down-rounds, predatory debt restructuring, or involuntary Chapter 11 filing.",
            mitigation_protocol="Enforce dynamic rolling 13-week cash forecasts, automated operating reserve triggers, and 24-month runway policy limits."
        ),
        FailureMode(
            name="Premature Optimization / Penny-Wise Starvation",
            symptoms=["Denying high-ROI R&D infrastructure to preserve quarterly optics", "Drastic cuts in core product engineering"],
            root_cause="Narrow quarterly margin targeting uncoupled from long-term capital compounding.",
            catastrophic_impact="Loss of technical talent, competitor leapfrogging, and long-term enterprise terminal value destruction.",
            mitigation_protocol="Differentiate strictly between capital investments (R&D capex) and operational waste (opex bloat)."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="WACC (Weighted Average Cost of Capital)", definition="The average rate of return a company is expected to provide to all its security holders to finance assets.", domain="Corporate Finance"),
        GlossaryTerm(term="Working Capital Cycle", definition="The time duration between purchasing raw materials/services and collecting cash from customer receivables.", domain="Treasury Management"),
        GlossaryTerm(term="EBITDA Quality of Earnings", definition="An analytical audit measuring whether reported operating earnings represent sustainable operational cash flow.", domain="Financial Forensic Accounting")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Kelly Criterion for Capital Allocation", principle="Size capital bets in proportion to their risk-adjusted edge while avoiding risk of ruin.", application="Cap any single high-risk growth bet to a strictly non-lethal percentage of free cash flow."),
        DecisionHeuristic(name="Margin of Safety", principle="Always build in a substantial financial cushion against unforeseen shocks.", application="Maintain a minimum of $35M in inviolable cash operating reserves.")
    ]
))

# =============================================================================
# 4. EXECUTIVE: CHIEF OPERATING OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="coo",
    role_title="Chief Operating Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The operational commander responsible for enterprise execution, supply chain resilience, "
        "inter-departmental workflow orchestration, business continuity, and operational efficiency."
    ),
    core_mandate="Ensure operational flawless execution, eliminate organizational friction, and scale business processes sustainably.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Speed-Over-Safety Cultural Decay and Flawed Operational Feedback",
            organization="The Boeing Company",
            year=2018,
            incident_summary="Two Boeing 737 MAX aircraft crashed (Lion Air 610 and Ethiopian Airlines 302), killing 346 people due to MCAS design flaws and suppressed engineering concerns.",
            root_cause="Operational pressure to meet delivery schedules and avoid pilot simulator retraining, subordinating engineering rigor to cycle-time targets.",
            catastrophic_impact="Global 20-month fleet grounding, $20B+ in direct losses, and catastrophic loss of institutional reputation.",
            lessons_learned="Operational systems must empower employees to halt production lines when systemic risk is detected (Andon Cord principle).",
            role_implication="The COO must maintain psychological safety for operational line workers to escalate safety defects without fear of reprisal."
        ),
        HistoricalCaseStudy(
            title="Supply Chain Over-Optimization and Vulnerability",
            organization="Toyota Motor Corporation",
            year=2010,
            incident_summary="Massive global recall of over 8 million vehicles due to sticky accelerator pedals and floor mat entrapment.",
            root_cause="Rapid geographic operational expansion strained supplier quality assurance mechanisms beyond operational capacity.",
            catastrophic_impact="$2B+ in recalls and legal settlements, congressional hearings, and brand erosion.",
            lessons_learned="Operational scale must be matched with linear scaling of QA inspection and tier-1 supplier audit frequency.",
            role_implication="The COO must ensure operational expansion speed never exceeds the rate of quality assurance verification."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Siloed Departmental Friction",
            symptoms=["Hand-offs between engineering, product, and sales failing repeatedly", "Finger-pointing during incident post-mortems"],
            root_cause="Absence of unified cross-functional service level agreements (SLAs) and shared KPIs.",
            catastrophic_impact="Severe delivery delays, customer churn, and cultural toxicity.",
            mitigation_protocol="Implement clear cross-functional task graphs, automated hand-off contracts, and weekly interlock reviews."
        ),
        FailureMode(
            name="Single Point of Operational Failure (SPOF)",
            symptoms=["Critical enterprise operations dependent on a single vendor or single person", "Lack of documented disaster recovery playbooks"],
            root_cause="Pursuit of short-term cost efficiency over system redundancy and operational resilience.",
            catastrophic_impact="Immediate business stoppage upon component failure or vendor outage.",
            mitigation_protocol="Enforce N+1 redundancy across all critical business processes and conduct regular operational chaos exercises."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="Theory of Constraints (TOC)", definition="A methodology identifying the most important limiting factor (bottleneck) that stands in the way of achieving a goal.", domain="Operations Research"),
        GlossaryTerm(term="Andon Cord", definition="A manufacturing system practice empowering any worker to halt production when a defect or safety flaw is detected.", domain="Lean Operations"),
        GlossaryTerm(term="Service Level Objective (SLO)", definition="A target value or range of values for a service level that is measured by a service level indicator (SLI).", domain="Site Reliability & Operations")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Little's Law", principle="Work in Progress (WIP) = Throughput × Cycle Time.", application="Reduce work-in-progress across all departments to dramatically accelerate delivery velocity."),
        DecisionHeuristic(name="Poka-Yoke (Mistake Proofing)", principle="Design processes so errors are physically or logically impossible to commit.", application="Embed automated policy checks directly into all operational workflows.")
    ]
))

# =============================================================================
# 5. EXECUTIVE: CHIEF TECHNOLOGY OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="cto",
    role_title="Chief Technology Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The supreme engineering and technical visionary of the enterprise. "
        "Responsible for platform architecture, technical debt governance, cybersecurity posture, "
        "engineering culture, research and development, and infrastructure scalability."
    ),
    core_mandate="Construct an unassailable, highly reliable, and horizontally scalable technical moat while maintaining 99.99% availability.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Dead Code Reactivation and Absence of Deployment Gates",
            organization="Knight Capital Group",
            year=2012,
            incident_summary="Knight Capital's automated trading system flooded the NYSE with erroneous orders, generating a $440M loss in 45 minutes and bankrupting the firm.",
            root_cause="A technician failed to copy new code to one of eight servers; a reused configuration flag activated dead test code (SMARS) that lacked automated safety boundaries.",
            catastrophic_impact="Complete equity wipeout, emergency fire-sale of the company to Getco within days.",
            lessons_learned="Automated deployment must verify hash parity across all cluster nodes; dead code must be excised; automated kill-switches must trip instantly.",
            role_implication="The CTO must enforce deterministic CI/CD verification, eliminate dead code ruthlessly, and mandate financial/operational circuit breakers."
        ),
        HistoricalCaseStudy(
            title="Unpatched Known Vulnerability and Incomplete Asset Inventory",
            organization="Equifax",
            year=2017,
            incident_summary="Attackers exploited CVE-2017-5638 in Apache Struts, compromising sensitive financial data of 147 million consumers.",
            root_cause="Failure to patch a known critical vulnerability two months after release due to inaccurate internal software inventory and expired SSL inspection certificates.",
            catastrophic_impact="$1.4B in cleanup costs, $575M FTC settlement, and replacement of executive leadership.",
            lessons_learned="Asset discovery and vulnerability patching must be continuously automated rather than managed via periodic manual audits.",
            role_implication="The CTO must enforce an automated Software Bill of Materials (SBOM) and zero-day patch SLAs across all production microservices."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Technical Debt Bankruptcy",
            symptoms=["New feature delivery slowing to a crawl", "Frequent regressions on unrelated modules", "Engineers spending > 60% of time firefighting"],
            root_cause="Sacrificing modular architecture and test coverage for short-term commercial release dates over multiple quarters.",
            catastrophic_impact="System fragility, talent exodus, and eventual requirement for multi-year catastrophic ground-up rewrites.",
            mitigation_protocol="Enforce the 20% Technical Debt Rule (allocate 20% of every sprint exclusively to refactoring and test harness reinforcement)."
        ),
        FailureMode(
            name="Resume-Driven Architecture",
            symptoms=["Adopting hyper-complex distributed frameworks for simple monolithic requirements", "Excessive operational overhead"],
            root_cause="Engineering teams selecting unproven or unnecessarily complex technologies to enhance personal credentials.",
            catastrophic_impact="High infrastructure costs, complex failure modes, and debugging gridlock.",
            mitigation_protocol="Enforce boring technology principles; require formal Architecture Decision Records (ADRs) demonstrating clear ROI for novel dependencies."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="CAP Theorem", definition="In a distributed data store, it is impossible to simultaneously provide more than two out of Consistency, Availability, and Partition tolerance.", domain="Distributed Systems"),
        GlossaryTerm(term="Conway's Law", definition="Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations.", domain="Software Engineering"),
        GlossaryTerm(term="Chaos Engineering", definition="The discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions.", domain="Platform Engineering"),
        GlossaryTerm(term="Tail Latency (P99/P99.9)", definition="The high-percentile latency in distributed systems that disproportionately impacts end-to-end request pipelines and cascading microservice throughput.", domain="Distributed Systems"),
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Gall's Law", principle="A complex system that works is invariably found to have evolved from a simple system that worked.", application="Build modular, functional MVPs before expanding distributed topology."),
        DecisionHeuristic(name="Defense in Depth", principle="Never rely on a single layer of security or validation.", application="Enforce input validation at the edge, service mesh mTLS, and internal zero-trust authorization.")
    ]
))

# =============================================================================
# 6. EXECUTIVE: CHIEF MARKETING OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="cmo",
    role_title="Chief Marketing Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The executive steward of brand equity, market positioning, demand generation, "
        "customer acquisition economics (CAC), and public perception."
    ),
    core_mandate="Compound enterprise brand value, generate predictable qualified pipeline, and maintain superior customer acquisition efficiency.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Tone-Deaf Cultural Co-optation and Inward Creative Bias",
            organization="PepsiCo",
            year=2017,
            incident_summary="Pepsi released a commercial featuring Kendall Jenner resolving a protest standoff by handing a police officer a soda, sparking immediate universal mockery.",
            root_cause="In-house creative team insularity, failure to stress-test campaign concepts against external cultural sentiment, and lack of diverse review gates.",
            catastrophic_impact="Massive public relations embarrassment, immediate campaign pull, and long-term brand equity erosion among target demographic.",
            lessons_learned="High-visibility brand campaigns must pass rigorous external perception stress-tests before public distribution.",
            role_implication="The CMO must establish strict Red Team marketing review boards for cultural and brand-sensitive campaigns."
        ),
        HistoricalCaseStudy(
            title="Core Demographic Alienation Without Segment Analysis",
            organization="Anheuser-Busch InBev",
            year=2023,
            incident_summary="Bud Light's promotional partnership triggered a boycott resulting in a 25%+ drop in sales and losing its title as America's top-selling beer.",
            root_cause="Implementing a radical positioning pivot without quantitative psychographic modeling of core customer retention dynamics.",
            catastrophic_impact="Over $1.4B in lost sales, severe distributor friction, and executive turnover.",
            lessons_learned="Customer acquisition strategies must not jeopardize the high-margin retention economics of the established core base.",
            role_implication="The CMO must balance cohort expansion against core retention metrics via Bayesian customer lifetime value modeling."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Vanity Metric Addiction",
            symptoms=["Celebrating impressions and click-through rates while pipeline and closed-won revenue stagnate", "LTV:CAC ratio falling below 3:1"],
            root_cause="Incentivizing top-of-funnel volume rather than downstream revenue realization.",
            catastrophic_impact="Enormous capital burn on non-converting audience segments.",
            mitigation_protocol="Tie all marketing attribution models directly to closed-won revenue, CAC payback period (< 12 months), and pipeline velocity."
        ),
        FailureMode(
            name="Brand Narrative Fragmentation",
            symptoms=["Different departmental campaigns telling contradictory stories", "Customer confusion regarding enterprise value proposition"],
            root_cause="Decentralized marketing execution lacking a central brand architecture and positioning bible.",
            catastrophic_impact="Erosion of brand recall, decreased pricing power, and poor ad conversion.",
            mitigation_protocol="Publish and enforce a strict Enterprise Brand Blueprint and narrative playbook across all external communications."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="CAC Payback Period", definition="The number of months required for a customer to generate sufficient gross profit to recover customer acquisition costs.", domain="Growth Marketing"),
        GlossaryTerm(term="Net Promoter Score (NPS)", definition="A metric measuring customer experience and brand loyalty, calculated from likelihood to recommend.", domain="Brand Strategy"),
        GlossaryTerm(term="Marketing Mix Modeling (MMM)", definition="Statistical analysis technique using econometric methods to measure the sales impact of marketing tactics.", domain="Marketing Analytics")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Goodhart's Law", principle="When a measure becomes a target, it ceases to be a good measure.", application="Never optimize purely for clicks or impressions without closed-loop revenue verification."),
        DecisionHeuristic(name="First Principles Brand Positioning", principle="Own a clear, singular mental category in the customer's mind.", application="Position AegisCorp as the unquestioned gold standard in governed enterprise AI.")
    ]
))

# =============================================================================
# 7. EXECUTIVE: CHIEF REVENUE OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="cro",
    role_title="Chief Revenue Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The executive commander of commercial revenue generation, unifying direct enterprise sales, "
        "partner ecosystems, customer success, sales engineering, and net revenue retention (NRR)."
    ),
    core_mandate="Drive repeatable, high-velocity ARR growth, maximize net revenue retention (> 120%), and build predictable commercial sales engines.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Toxic Incentive Alignment and Fictitious Account Creation",
            organization="Wells Fargo & Company",
            year=2016,
            incident_summary="Employees opened over 3.5 million unauthorized bank accounts and credit cards to meet impossible daily cross-selling quotas ('eight is great').",
            root_cause="Hyper-aggressive quota management and punitive management culture punishing missed quotas regardless of compliance or customer reality.",
            catastrophic_impact="$3B in regulatory fines, criminal investigations, and severe lasting brand damage.",
            lessons_learned="Sales quotas and commission plans must be counter-balanced with independent compliance and audit checks.",
            role_implication="The CRO must audit pipeline quality and contract reality; commissions must be contingent on actual customer activation and cash collection."
        ),
        HistoricalCaseStudy(
            title="Shelfware Selling and Post-Sale Churn Catastrophe",
            organization="Computer Associates (CA)",
            year=2004,
            incident_summary="Aggressive discounting and premature multi-year booking of enterprise software that customers never deployed, leading to accounting fraud investigations.",
            root_cause="Over-indexing compensation on initial booking value while ignoring product adoption and customer value realization.",
            catastrophic_impact="Federal criminal indictments, restatement of hundreds of millions in revenue, and market collapse.",
            lessons_learned="Sustainable revenue requires customer adoption; booking uninstalled licenses creates an inevitable churn cliff.",
            role_implication="The CRO must align sales quotas with post-sale customer onboarding success and Net Revenue Retention."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Pipeline Mirage / Sandbagging",
            symptoms=["Quarterly pipeline coverage appearing healthy (4x) but collapsing in the final two weeks of the quarter", "Win rates < 15%"],
            root_cause="Lack of objective opportunity qualification criteria (MEDDPICC) and sales reps maintaining dead opportunities.",
            catastrophic_impact="Severe revenue forecasting misses, board panic, and emergency operational budget cuts.",
            mitigation_protocol="Enforce rigorous MEDDPICC stage gates; automatically purge uncontacted deals > 45 days; inspect economic buyer verification."
        ),
        FailureMode(
            name="Gross Margin Erosion via Discounting",
            symptoms=["Average selling price declining steadily", "Custom contract terms and non-standard SLAs granted to close deals"],
            root_cause="Sales leadership prioritizing short-term ARR booking over unit economics and engineering feasibility.",
            catastrophic_impact="High delivery costs, negative customer gross margins, and strain on engineering resources.",
            mitigation_protocol="Establish non-negotiable discount matrices with mandatory CFO sign-off for discounts exceeding 15%."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="Net Revenue Retention (NRR)", definition="The percentage of recurring revenue retained from existing customers over a given period, including expansions, downgrades, and churn.", domain="Enterprise Sales"),
        GlossaryTerm(term="MEDDPICC", definition="A qualification framework: Metrics, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Identify Pain, Champion, Competition.", domain="Sales Methodology"),
        GlossaryTerm(term="Sales Velocity", definition="A measure of how fast money moves through the sales pipeline: (Deals × Win Rate × ASP) / Sales Cycle Length.", domain="Revenue Operations")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Pareto Customer Distribution", principle="Top 20% of enterprise accounts provide 80% of expansion revenue.", application="Focus executive sales sponsorship and dedicated resources on tier-1 strategic clients."),
        DecisionHeuristic(name="The Rule of 40", principle="Growth rate percentage plus profit margin percentage should equal or exceed 40%.", application="Ensure commercial growth is not achieved by burning unsustainable gross margin.")
    ]
))

# =============================================================================
# 8. EXECUTIVE: CHIEF HUMAN RESOURCES OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="chro",
    role_title="Chief Human Resources Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The executive leader of talent acquisition, organizational culture, leadership development, "
        "compensation architecture, regulatory labor compliance, and employee psychological safety."
    ),
    core_mandate="Attract, develop, and retain tier-1 talent while cultivating a high-performance culture of integrity and psychological safety.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="High-Performer Toxicity and Systemic HR Non-Enforcement",
            organization="Uber Technologies",
            year=2017,
            incident_summary="Following engineer Susan Fowler's whistleblowing blog on pervasive sexual harassment, HR was revealed to systematically protect toxic top performers.",
            root_cause="Subordinating ethical standards and harassment policies to individual commercial output and technical competence.",
            catastrophic_impact="Massive public boycott (#DeleteUber), departure of CEO Travis Kalanick, firing of 20+ executives, and brand degradation.",
            lessons_learned="HR cannot be a shield for executive misconduct; behavioral red lines must be absolute regardless of performance.",
            role_implication="The CHRO must maintain an independent whistleblowing channel directly to the Board Audit Committee and enforce zero tolerance for ethical violations."
        ),
        HistoricalCaseStudy(
            title="Rank-and-Yank Forced Ranking and Institutional Paranoia",
            organization="Enron Corporation (Performance Review System)",
            year=2000,
            incident_summary="Enron's semi-annual Performance Review Committee forced a bell curve grading where the bottom 15% were routinely terminated within months.",
            root_cause="Flawed belief that existential fear maximizes performance, destroying collaboration and encouraging sabotage and accounting concealment.",
            catastrophic_impact="Destruction of psychological safety, zero reporting of operational defects, and normalization of financial deceit.",
            lessons_learned="Forced ranking systems disincentivize long-term systemic improvement and reward short-term predatory behavior.",
            role_implication="The CHRO must design evaluation systems based on objective competency mastery and collaborative impact rather than zero-sum quotas."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Talent Density Dilution (Bozo Explosion)",
            symptoms=["B-players hiring C-players to protect their internal status", "Declining bar in technical interviews", "Sluggish organizational execution"],
            root_cause="Speed-hiring pressure overriding rigorous standardized technical rubrics.",
            catastrophic_impact="Loss of engineering excellence, elite talent attrition, and organizational stagnation.",
            mitigation_protocol="Enforce Bar Raiser interview programs; require blinded grading; mandate cross-departmental hiring approvals."
        ),
        FailureMode(
            name="At-Will Compliance Exposure",
            symptoms=["Inconsistent disciplinary documentation", "Disparate impact in promotions", "Surprise wrongful termination lawsuits"],
            root_cause="Failure of managers to maintain contemporaneous performance documentation.",
            catastrophic_impact="Costly legal settlements, EEOC audits, and toxic internal morale.",
            mitigation_protocol="Enforce objective 90-day performance improvement protocols with clear, measurable deliverables before termination."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="Psychological Safety", definition="A shared belief held by members of a team that the team is safe for interpersonal risk-taking and admitting mistakes.", domain="Organizational Psychology"),
        GlossaryTerm(term="Comp-Ratio", definition="An employee's base salary divided by the midpoint of the salary range for their job grade, measuring pay equity.", domain="Total Rewards"),
        GlossaryTerm(term="Critical Skill Coverage", definition="The proportion of core institutional capabilities with at least two qualified practitioners to eliminate key-person dependency.", domain="Workforce Planning")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Google Project Aristotle Insight", principle="Who is on a team matters far less than how the team members interact and structure their work.", application="Prioritize psychological safety, dependability, and role clarity above individual pedigree."),
        DecisionHeuristic(name="Inversion in Retention", principle="To retain great talent, systematically eliminate the things that make great talent leave.", application="Remove bureaucratic roadblocks, toxic managers, and ambiguous decision rights.")
    ]
))

# =============================================================================
# 9. EXECUTIVE: CHIEF PRODUCT OFFICER
# =============================================================================
_register(EncyclopediaEntry(
    role_id="cpo",
    role_title="Chief Product Officer",
    department="Executive",
    level=2,
    canonical_definition=(
        "The executive champion of product strategy, user experience, product-market fit, "
        "product roadmap prioritization, feature lifecycle management, and user retention."
    ),
    core_mandate="Deliver delightful, high-utility products that solve critical user problems and compound long-term user retention.",
    historical_case_studies=[
        HistoricalCaseStudy(
            title="Desktop Usability Destruction via Unvalidated Paradigm Shift",
            organization="Microsoft Corporation",
            year=2012,
            incident_summary="Windows 8 eliminated the beloved Start Menu and forced a touch-oriented Metro tile interface onto 1.3 billion desktop keyboard/mouse users.",
            root_cause="Executive dogma forcing mobile/tablet convergence across form factors without validating desktop workflow usability.",
            catastrophic_impact="Mass enterprise boycott, sluggish OS adoption, reputational damage, and necessity of emergency Windows 10 restoration.",
            lessons_learned="Never break core user workflow ergonomics to satisfy an internal strategic vision without rigorous empirical user testing.",
            role_implication="The CPO must ground every major UI/UX paradigm shift in behavioral usability telemetry and preserve power-user muscle memory."
        ),
        HistoricalCaseStudy(
            title="Premium Hardware Hubris for an Unverified Problem",
            organization="Quibi Holdings LLC",
            year=2020,
            incident_summary="Raised $1.75B to produce short-form premium video for mobile phones during daily commutes, shutting down 6 months after launch.",
            root_cause="Failure to validate customer willingness to pay; blocking screenshots/sharing (anti-viral design); and competing blindly with free YouTube/TikTok.",
            catastrophic_impact="Complete corporate liquidation and loss of $1.75B in investor capital.",
            lessons_learned="No amount of capital or Hollywood production value can compensate for absence of genuine organic product-market fit.",
            role_implication="The CPO must validate willingness-to-pay and organic distribution loops via low-cost MVPs before committing large-scale capital."
        )
    ],
    failure_modes=[
        FailureMode(
            name="Feature Factory Syndrome",
            symptoms=["Shipping endless new features while core metrics (retention, engagement) remain flat", "Lack of post-launch feature deprecation"],
            root_cause="Measuring product team success by output (features delivered) rather than outcome (problem solved, business metric moved).",
            catastrophic_impact="Bloated, confusing product interfaces, high maintenance cost, and customer frustration.",
            mitigation_protocol="Enforce strict Outcome-Based Roadmaps; mandate that every feature launch has a pre-registered success metric and kill date if unreached."
        ),
        FailureMode(
            name="Premature Scaling / False PMF",
            symptoms=["Pouring aggressive marketing dollars into a product with low Day-30/Day-90 retention", "High churn masked by high acquisition"],
            root_cause="Confusing initial vanity signup numbers with genuine product-market fit.",
            catastrophic_impact="Emptying company cash reserves into a leaky bucket.",
            mitigation_protocol="Do not approve commercial scale-up until cohort retention curves flatten horizontally for at least three consecutive cohorts."
        )
    ],
    key_glossary=[
        GlossaryTerm(term="Product-Market Fit (PMF)", definition="The stage where a product satisfies a strong market demand and creates sustainable organic retention.", domain="Product Strategy"),
        GlossaryTerm(term="Jobs to be Done (JTBD)", definition="A framework focusing on the fundamental progress a customer is trying to achieve in a given circumstance.", domain="User Research"),
        GlossaryTerm(term="Kano Model", definition="A theory of product development and customer satisfaction classifying features into Basic, Performance, and Delighter attributes.", domain="Product Design")
    ],
    decision_heuristics=[
        DecisionHeuristic(name="Retention Is King", principle="If retention does not plateau, you do not have a product.", application="Prioritize core workflow retention over all top-of-funnel acquisition features."),
        DecisionHeuristic(name="Falsification Principle", principle="Actively seek data that disproves your product hypothesis rather than seeking confirmation.", application="Run rigorous user pre-mortems and usability testing on every major release candidate.")
    ]
))


# =============================================================================
# HELPER TO GENERATE STANDARDIZED LADDER DOSSIERS
# =============================================================================
def _generate_ladder_dossiers():
    """Generates encyclopedic entries for all 39 departmental ladder roles across 7 functional ladders."""
    from aegiscorp.org.hierarchy import ALL_ROLES

    ladder_configs = {
        # ---------------------------------------------------------------------
        # ENGINEERING LADDER (8 roles)
        # ---------------------------------------------------------------------
        "vp_eng": {
            "definition": "Executive engineering leader responsible for technical execution velocity, architectural integrity, and developer productivity.",
            "mandate": "Ensure predictable, secure, and resilient software delivery while scaling engineering infrastructure horizontally.",
            "case": ("AWS S3 Total Outage from Human Command Error", "Amazon Web Services", 2017,
                     "An authorized S3 engineer executed a command intended to take offline a small set of servers, accidentally removing a critical subsystem.",
                     "Blast radius was not bounded, and tool lacked safety validation preventing removal of oversized capacity.",
                     "Major portions of the internet were disrupted for several hours.",
                     "Critical tools must have automated blast-radius limits and require two-person verification for large-scale operations.",
                     "Enforce blast radius isolation and automated boundary checks on all operational tooling."),
            "failure": ("Blast Radius Failure", ["Single changes taking down multi-tenant production systems", "Monolithic deployment dependencies"],
                        "Lack of compartmentalization and canary rings.", "Enterprise downtime and SLA breaches.",
                        "Mandate staged canary deployments and strict architectural compartmentalization."),
            "glossary": [("Blast Radius", "The maximum potential impact a failure or security incident can cause across a distributed system.", "Engineering")],
            "heuristic": ("Automate Rollbacks", "If error rate spikes above baseline during deployment, roll back immediately without human debate.")
        },
        "director_eng": {
            "definition": "Director of Engineering overseeing multiple cross-functional engineering groups and platform stability.",
            "mandate": "Translate business objectives into robust distributed software systems and develop high-performing engineering leaders.",
            "case": ("Therac-25 Software Race Condition Tragedies", "Atomic Energy of Canada Limited", 1985,
                     "A radiation therapy machine administered massive radiation overdoses to patients due to a software race condition.",
                     "Software written in assembly with no independent hardware interlocks and inadequate integration testing.",
                     "Multiple patient fatalities and severe radiation poisoning.",
                     "Software safety cannot rely on absence of bugs; physical or logical safety interlocks must be independent.",
                     "Ensure all critical safety-critical logic has formal verification and defense-in-depth isolation."),
            "failure": ("Conway's Law Breakdown", ["Engineering teams producing disjointed architectures mirroring communication siloes", "Duplicate platform services"],
                        "Failure of engineering directors to align team topology with system architecture.", "Massive operational redundancy and integration failures.",
                        "Align team ownership boundaries strictly with clean bounded software contexts."),
            "glossary": [("Bounded Context", "A explicit boundary within a domain model where a specific domain model applies.", "Domain-Driven Design")],
            "heuristic": ("Keep Team Sizes Small", "Two-pizza teams maintain optimal communication density and velocity.")
        },
        "sr_eng_mgr": {
            "definition": "Senior Engineering Manager orchestrating engineering managers, sprint execution, and technical career progression.",
            "mandate": "Balance technical excellence with predictable sprint delivery and eliminate operational impediments.",
            "case": ("Healthcare.gov Catastrophic Launch Failure", "US Centers for Medicare & Medicaid Services", 2013,
                     "Federal insurance portal crashed on launch day, serving only a handful of users despite hundreds of millions in development spending.",
                     "Fragmented multi-contractor management, absence of end-to-end integration testing, and suppressed status reporting.",
                     "National political embarrassment and urgent emergency tech surge required to rewrite key components.",
                     "End-to-end integration testing must begin months before launch; status reporting must be brutally objective.",
                     "Enforce continuous integration across all contractor and team boundaries with zero tolerance for yellow-shifting."),
            "failure": ("Watermelon Status Reporting", ["Projects reported as Green until suddenly turning catastrophic Red on delivery date"],
                        "Culture of fear where bad news is punished by management.", "Late discovery of insurmountable blockers.",
                        "Reward early escalation of blockers and establish transparent automated CI/CD dashboards."),
            "glossary": [("Cycle Time", "The total elapsed time from when an engineer starts work on a task to when it runs in production.", "Engineering Management")],
            "heuristic": ("Inspect What You Expect", "Never accept verbal delivery guarantees without verified automated test traces.")
        },
        "eng_mgr": {
            "definition": "Frontline Engineering Manager coaching software engineers, managing backlog delivery, and maintaining team health.",
            "mandate": "Drive daily sprint throughput, protect team focus, and foster psychological safety and continuous feedback.",
            "case": ("Log4Shell Zero-Day Exploitation", "Apache Software Foundation", 2021,
                     "A critical remote code execution vulnerability (CVE-2021-44228) was discovered in widely used Java logging library Log4j.",
                     "Feature creep in logging framework enabling JNDI lookups without proper input sanitization.",
                     "Hundreds of millions of enterprise servers vulnerable worldwide.",
                     "Engineering managers must maintain visibility into transitive dependencies and mandate regular dependency updates.",
                     "Enforce automated dependency auditing and patch cycles across all repositories."),
            "failure": ("Context Switching Exhaustion", ["Engineers pulled into ad-hoc requests mid-sprint", "Sprint completion rate < 60%"],
                        "Inability of manager to shield engineering team from outside distraction.", "Developer burnout and missed commitments.",
                        "Enforce strict sprint commitment boundaries; ad-hoc requests must wait for the next planning cycle."),
            "glossary": [("Sprint Burndown", "A graphical representation of work left to do versus time for a specific sprint.", "Agile")],
            "heuristic": ("Maker vs Manager Schedule", "Preserve uninterrupted 4-hour focus blocks for deep engineering work.")
        },
        "tech_lead": {
            "definition": "Technical Lead and architect guiding technical design decisions, code review rigor, and systems modeling.",
            "mandate": "Ensure code maintainability, technical debt containment, and adherence to design principles across the codebase.",
            "case": ("Cloudflare Cloudbleed Memory Leak", "Cloudflare", 2017,
                     "A buffer overrun bug in legacy parser code leaked customer passwords, API tokens, and private data into search engine caches.",
                     "Pointer arithmetic error in Ragel HTML parser triggered by unclosed HTML tags.",
                     "Sensitive data from thousands of websites leaked into public web caches.",
                     "Memory-unsafe code in high-throughput edge routers presents extreme risk; fuzzing and bounds checking must be continuous.",
                     "Audit all pointer and buffer logic; transition security-critical pathways to memory-safe languages."),
            "failure": ("Architectural Dogmatism", ["Refusing simple pragmatic solutions in favor of theoretical purity", "Delayed releases due to over-design"],
                        "Valuing academic architecture over pragmatic operational problem-solving.", "Delivery paralysis and team frustration.",
                        "Solve the concrete problem in front of you with the simplest possible robust design."),
            "glossary": [("Idempotency", "The property of certain operations that can be applied multiple times without changing the result.", "API Design")],
            "heuristic": ("YAGNI (You Aren't Gonna Need It)", "Do not implement speculative abstractions until actual requirements demand them.")
        },
        "sr_swe": {
            "definition": "Senior Software Engineer designing and implementing complex distributed components with minimal oversight.",
            "mandate": "Produce clean, performant, resilient code and mentor intermediate and junior engineers through thorough reviews.",
            "case": ("Ariane 5 Flight 501 Maiden Launch Destruction", "European Space Agency", 1996,
                     "Rocket self-destructed 37 seconds after launch due to an unhandled 64-bit to 16-bit integer conversion overflow.",
                     "Reusing inertial reference software from Ariane 4 without re-verifying trajectory specifications against Ariane 5 velocity profiles.",
                     "Loss of rocket and $370M scientific payload.",
                     "Software cannot be reused blindly across differing operating envelopes without rigorous parameter verification.",
                     "Explicitly check all numerical bounds and assert invariant contracts on all internal variables."),
            "failure": ("Cowboy Coding", ["Pushing unreviewed hotfixes directly to main", "Bypassing unit tests to hit deadlines"],
                        "Impatience and lack of respect for testing and deployment protocols.", "Production outages and subtle data corruption bugs.",
                        "Never bypass the CI/CD pipeline; every line of production code must have peer review and automated tests."),
            "glossary": [("Circuit Breaker Pattern", "A design pattern used to detect failures and encapsulate the logic of preventing a failure from constantly recurring.", "Microservices")],
            "heuristic": ("Fail Fast", "Validate inputs immediately at system boundaries and crash visibly rather than propagating corrupted state.")
        },
        "swe": {
            "definition": "Software Engineer writing tested, maintainable code, fixing defects, and implementing platform features.",
            "mandate": "Implement well-tested features, maintain high test coverage, and uphold clean code principles.",
            "case": ("Heartbleed OpenSSL Vulnerability", "OpenSSL Project", 2014,
                     "A missing bounds check in the handling of the TLS heartbeat extension allowed remote attackers to read server memory containing private keys.",
                     "Trusting client-supplied payload length parameter without verifying actual buffer size.",
                     "Millions of secure web servers compromised worldwide.",
                     "Never trust user-supplied length headers; always validate against physical buffer bounds.",
                     "Always sanitize and validate external inputs before memory allocation or processing."),
            "failure": ("Happy-Path Only Testing", ["Writing unit tests that only verify correct inputs while ignoring nulls, timeouts, and error states"],
                        "Lack of adversarial testing mindset.", "Unhanded exceptions causing silent microservice crashes in production.",
                        "Write unit tests for edge cases, null inputs, network timeouts, and malformed payloads first."),
            "glossary": [("Test-Driven Development (TDD)", "A software development process where requirements are turned into specific test cases before software is fully developed.", "Software Methodology")],
            "heuristic": ("Red-Green-Refactor", "Write failing test, write minimal code to pass, refactor cleanly.")
        },
        "junior_eng": {
            "definition": "Junior Software Engineer acquiring foundational software craftsmanship, writing unit tests, and delivering scoped bug fixes.",
            "mandate": "Learn rapidly, follow established coding standards, write thorough tests, and ask clarifying questions early.",
            "case": ("Mars Climate Orbiter Unit Conversion Loss", "NASA / Lockheed Martin", 1999,
                     "Spacecraft entered Mars atmosphere too low and disintegrated due to a mismatch between metric Newtons and Imperial pound-force.",
                     "One engineering team used Imperial units while the other used metric units in ground software interface.",
                     "$327M spacecraft lost entirely.",
                     "Explicit typing and interface unit contracts are mandatory; assumptions must be codified in code.",
                     "Always check variable units and assert typed contracts on all external data interfaces."),
            "failure": ("Silent Struggle Syndrome", ["Spending days blocked on an issue without seeking help or documentation", "Missed sprint tickets"],
                        "Imposter syndrome and fear of appearing incompetent.", "Wasted time and surprise sprint delivery failures.",
                        "Adopt the 30-minute rule: if stuck for 30 minutes after reading docs, reach out to a senior engineer with specific findings."),
            "glossary": [("Semantic Versioning (SemVer)", "A formal convention for specifying version numbers: MAJOR.MINOR.PATCH.", "Software Delivery")],
            "heuristic": ("Leave the Code Cleaner Than You Found It", "Fix minor typos or add missing docstrings whenever editing a file.")
        },

        # ---------------------------------------------------------------------
        # PRODUCT LADDER (6 roles)
        # ---------------------------------------------------------------------
        "vp_prod": {
            "definition": "Vice President of Product leading the enterprise product portfolio, lifecycle strategy, and design systems.",
            "mandate": "Align product strategy with enterprise business models and deliver high-leverage product platforms.",
            "case": ("Google Glass Consumer Launch Backlash", "Google LLC", 2013,
                     "Wearable smart glasses triggered severe privacy backlash in public spaces ('Glassholes') and failed commercially.",
                     "Launching a developer prototype as a luxury consumer product without understanding social context and privacy concerns.",
                     "Millions in inventory write-offs and temporary shelving of the consumer platform.",
                     "Technological capability must be matched with cultural and social acceptance research before consumer launch.",
                     "Conduct comprehensive societal and behavioral impact reviews prior to launching public-facing hardware or AI interfaces."),
            "failure": ("Portfolio Cannibalization Disarray", ["Launching competing products internally that confuse enterprise customers"],
                        "Lack of top-down product line positioning.", "Customer confusion and wasted R&D spend.",
                        "Establish distinct product swimlanes and clear customer tier definitions."),
            "glossary": [("Product-Led Growth (PLG)", "A business methodology in which user acquisition, expansion, and retention are driven primarily by the product itself.", "Product")],
            "heuristic": ("Focus on the Core", "Kill the bottom 20% of low-performing features to polish the critical daily workflow.")
        },
        "director_prod": {
            "definition": "Director of Product driving a major product vertical, roadmap coherence, and product management career development.",
            "mandate": "Ensure product vertical delivers compounding customer utility, high feature adoption, and revenue expansion.",
            "case": ("Digg v4 User Exodus", "Digg Inc.", 2010,
                     "Digg released Version 4, stripping power-user features and favoring corporate publishers, triggering a mass exodus to Reddit.",
                     "Ignoring feedback from the core community during beta testing to pursue publisher commercialization deals.",
                     "Digg lost over 50% of its traffic within weeks and was eventually sold for parts for $500,000.",
                     "Never alienate the core community that powers network effects to satisfy secondary corporate partners.",
                     "Treat community network power users as essential co-designers and listen to beta telemetry."),
            "failure": ("Roadmap Over-Commitment", ["Promising 50 major features in an annual roadmap without capacity buffers", "Engineering burnout"],
                        "Sales-led roadmap capture and inability to say no to executive requests.", "Chronic missed delivery deadlines and buggy releases.",
                        "Commit to thematic problem-oriented roadmaps rather than rigid feature-date commitments."),
            "glossary": [("North Star Metric", "The key metric that best captures the core value your product delivers to its customers.", "Product Strategy")],
            "heuristic": ("The Two-Way Door Rule", "Make reversible decisions rapidly; deliberate deeply on irreversible one-way door decisions.")
        },
        "gpm": {
            "definition": "Group Product Manager leading a pod of product managers and cross-functional teams in a specific product domain.",
            "mandate": "Drive roadmap execution, maintain high UX standards, and mentor PMs across user discovery and metrics.",
            "case": ("Microsoft Zune Feature Parity Trap", "Microsoft", 2006,
                     "Zune was released as an iPod competitor with solid hardware and feature parity, but arrived too late and without an iTunes ecosystem moat.",
                     "Competing purely on feature parity against a deeply entrenched incumbent network ecosystem.",
                     "Billions spent for low single-digit market share and eventual product discontinuation.",
                     "Feature parity is never sufficient to displace an established market leader; 10x differentiation is required.",
                     "Identify an asymmetric vector of competition rather than building an identical feature clone."),
            "failure": ("Proxy Metric Obsession", ["Optimizing click-through on signup buttons while 7-day churn rises"],
                        "Losing sight of end-to-end customer value creation.", "Creating friction for users without improving business fundamentals.",
                        "Always pair conversion metrics with long-term retention and satisfaction metrics."),
            "glossary": [("Cohort Analysis", "A subset of behavioral analytics that takes data and breaks them into related groups for analysis.", "Analytics")],
            "heuristic": ("Customer Problem Over Solution", "Fall in love with the customer's problem, not your initial solution.")
        },
        "sr_pm": {
            "definition": "Senior Product Manager owning the lifecycle of high-impact product features from ideation to general availability.",
            "mandate": "Define crisp product requirements (PRDs), run disciplined user discovery, and drive measurable metric gains.",
            "case": ("Juicero Over-Engineering Failure", "Juicero", 2017,
                     "A $400 Wi-Fi connected cold-press juicer was rendered obsolete when Bloomberg journalists demonstrated the juice bags could be squeezed by hand.",
                     "Developing an exorbitantly expensive hardware solution for a problem already solvable by hand.",
                     "Total company failure and liquidation after raising $120M.",
                     "Validate whether the user problem genuinely requires complex technical engineering before building.",
                     "Build the simplest manual prototype first to prove value before building heavy technology."),
            "failure": ("Solution-First Bias", ["Writing a 40-page PRD prescribing exact UI buttons before validating customer demand"],
                        "Ego attachment to a preconceived product concept.", "Wasted engineering cycles building unwanted functionality.",
                        "Always include a 'Problem Statement' and 'Hypothesis to Disprove' section at the top of every PRD."),
            "glossary": [("Minimum Viable Product (MVP)", "The version of a new product which allows a team to collect the maximum amount of validated learning with the least effort.", "Lean Startup")],
            "heuristic": ("Talk to 5 Users Weekly", "Qualitative user interviews reveal the 'why' behind quantitative behavioral telemetry.")
        },
        "pm": {
            "definition": "Product Manager guiding sprint prioritization, user story authoring, and cross-functional team execution.",
            "mandate": "Deliver clear user stories, maintain an unblocked sprint backlog, and achieve sprint delivery milestones.",
            "case": ("Coca-Cola New Coke Debacle", "The Coca-Cola Company", 1985,
                     "Replaced the classic Coca-Cola formula with 'New Coke' based on blind taste test preferences, sparking consumer outrage.",
                     "Blind taste tests measured momentary sweetness sip preferences while completely ignoring emotional brand attachment.",
                     "Severe brand backlash and emergency return to 'Coca-Cola Classic' within 79 days.",
                     "Do not rely solely on isolated laboratory tests; evaluate real-world holistic customer emotional context.",
                     "Test product changes in naturalistic, longitudinal environments rather than synthetic tests."),
            "failure": ("Scope Creep Creep", ["Continuously adding new edge-case requirements mid-sprint", "Never releasing an MVP"],
                        "Fear of shipping imperfect software and lack of clear scope boundaries.", "Delayed launches and demoralized engineering teams.",
                        "Lock scope tightly at sprint kickoff; any new idea goes to the backlog for the next release."),
            "glossary": [("User Story", "An informal, general explanation of a software feature written from the perspective of the end user.", "Agile")],
            "heuristic": ("Ship to Learn", "A working feature in the hands of users teaches more than three months of internal speculation.")
        },
        "apm": {
            "definition": "Associate Product Manager learning product discovery, writing user stories, and conducting competitor analyses.",
            "mandate": "Support senior PMs with data analysis, user interview synthesis, and accurate backlog grooming.",
            "case": ("Color Labs Premature Launch Hype", "Color Labs Inc.", 2011,
                     "Raised $41M before launch for a proximity photo sharing app, but launched to empty user feeds and immediate user abandonment.",
                     "Assuming network density without solving the cold-start problem for single users.",
                     "App failure and asset fire-sale to Apple.",
                     "Always solve the single-player utility mode before relying on multiplayer network effects.",
                     "Design product utility so the first user gets value even when nobody else is online."),
            "failure": ("Analysis Paralysis", ["Refusing to make a backlog decision without endless inconclusive data points"],
                        "Fear of making an incorrect call as an early-career PM.", "Slowing down engineering sprint momentum.",
                        "Make the best decision with 70% of the information, then iterate rapidly."),
            "glossary": [("A/B Testing", "A randomized experimentation process wherein two or more versions of a variable are shown to users to determine which performs better.", "Experimentation")],
            "heuristic": ("Clarify the 'Why'", "Every user story must clearly answer: Who wants this, What do they need, and Why does it matter?")
        },

        # ---------------------------------------------------------------------
        # SALES LADDER (5 roles)
        # ---------------------------------------------------------------------
        "reg_sales_dir": {
            "definition": "Regional Sales Director commanding regional revenue targets, sales territory strategy, and key account closings.",
            "mandate": "Deliver predictable quarterly quota attainment across the region while maintaining accurate forecast discipline.",
            "case": ("B2B Software Channel Stuffing", "MicroStrategy", 2000,
                     "Sales executives pushed excessive software licenses into sales channels at quarter-end with unwritten side agreements allowing returns.",
                     "Pressure to meet public quarterly revenue projections overriding contract legal finality.",
                     "Restatement of revenue, SEC enforcement action, and stock plummeted 90% in one day.",
                     "All sales agreements must have enforceable payment terms with zero unapproved side-letters.",
                     "Enforce strict contract compliance; side letters result in immediate termination."),
            "failure": ("End-of-Quarter Hope Forecasting", ["Predicting 100% quota attainment based on uncontacted procurement departments"],
                        "Reluctance to give bad news to executive leadership.", "Devastating quarterly revenue misses.",
                        "Grade pipeline with cold, objective criteria; if procurement hasn't engaged by day 70, push the deal."),
            "glossary": [("Annual Contract Value (ACV)", "The annualized value of customer contracts over the contract term.", "Sales Metrics")],
            "heuristic": ("Bad News Early", "A revenue miss identified in month one can be corrected; a revenue miss in week twelve is fatal.")
        },
        "sales_mgr": {
            "definition": "Sales Manager coaching account executives, running deal reviews, and optimizing sales pipeline velocity.",
            "mandate": "Enable every account executive to hit quota and eliminate roadblocks in enterprise purchasing cycles.",
            "case": ("Zenefits Health Insurance Licensing Bypass", "Zenefits", 2016,
                     "Sales reps used an automated software macro (the 'macro') to fake completing mandatory 52 hours of pre-licensing education.",
                     "Sales leadership prioritizing aggressive sales rep ramp-up over statutory regulatory licensing compliance.",
                     "CEO resignation, massive regulatory fines across multiple states, and valuation slashed by more than half.",
                     "Regulatory compliance can never be compromised for sales onboarding speed.",
                     "Enforce mandatory compliance checks on all sales rep certifications and licensing."),
            "failure": ("The Super-Closer Trap", ["Sales manager swooping in to close every deal personally rather than coaching reps"],
                        "Manager ego and inability to scale sales rep capabilities.", "Underdeveloped sales team and manager burnout.",
                        "Coach reps to run the discovery and closing process; observe rather than take over the call."),
            "glossary": [("Sales Enablement", "The iterative process of providing sales organizations with the information and tools to sell more effectively.", "Sales")],
            "heuristic": ("Listen 70%, Talk 30%", "The best discovery calls involve asking incisive open-ended questions and listening deeply.")
        },
        "sales_team_lead": {
            "definition": "Sales Team Lead guiding a squad of account executives on pipeline qualification, objection handling, and proposal crafting.",
            "mandate": "Lead from the front, set team cadence, and maintain high standards of deal hygiene in CRM systems.",
            "case": ("Premature Verbal Commitment Reliance", "StorageTech", 1998,
                     "A sales squad celebrated a verbal $10M commitment that vanished when the client's CFO froze IT capital expenditure.",
                     "Relying on a friendly internal champion who lacked actual budget sign-off authority.",
                     "Quarterly quota missed by 80%.",
                     "A deal is not real until the economic buyer has signed the purchase order and legal review is complete.",
                     "Identify and directly engage the ultimate Economic Buyer early in the deal cycle."),
            "failure": ("Happy Ears Syndrome", ["Believing the customer loves the product without asking hard questions about budget and competition"],
                        "Fear of uncovering uncomfortable deal-killing realities early.", "Wasted time chasing unqualified opportunities.",
                        "Ask the difficult questions immediately: 'What happens if you do nothing?' and 'Who else is evaluating this?'"),
            "glossary": [("Economic Buyer", "The individual with ultimate authority to commit enterprise capital for a purchase.", "MEDDPICC")],
            "heuristic": ("Qualify Out Early", "Disqualifying a bad deal quickly is almost as valuable as closing a good deal.")
        },
        "ae": {
            "definition": "Account Executive driving complex sales cycles from qualified lead to closed contract.",
            "mandate": "Uncover deep enterprise pain, build strong champions, demonstrate definitive ROI, and close profitable business.",
            "case": ("Single-Threaded Champion Loss", "Global Crossing", 2001,
                     "An AE spent 9 months negotiating an enterprise telecom contract with a single VP who was abruptly laid off.",
                     "Single-threading the sales process with only one stakeholder contact.",
                     "Nine months of pipeline work evaporated overnight.",
                     "Always multithread enterprise deals across executive, technical, and financial stakeholders.",
                     "Engage at least three distinct decision-makers across business, finance, and technical departments."),
            "failure": ("Feature-Dumping Demos", ["Showing every menu and button in the product rather than tailoring to the customer's specific pain"],
                        "Lack of pre-call discovery and preparation.", "Bored prospects who fail to see business value.",
                        "Customize every demo to directly address the top two high-cost problems uncovered during discovery."),
            "glossary": [("Sales Discovery", "The foundational phase of the sales process where an AE asks strategic questions to assess fit.", "Sales")],
            "heuristic": ("No Mutual Action Plan, No Deal", "Always co-create a written timeline with the buyer outlining steps to signature.")
        },
        "sdr": {
            "definition": "Sales Development Representative generating outbound qualified pipeline through targeted prospecting and outreach.",
            "mandate": "Identify target accounts, engage key decision-makers with personalized value propositions, and book qualified meetings.",
            "case": ("Spam Cannon Reputation Destruction", "Various Outbound SaaS Agencies", 2023,
                     "Flooded enterprise domains with generic automated cold email sequences, resulting in domain blacklisting and zero replies.",
                     "Prioritizing raw email volume over personalization, relevance, and deliverability hygiene.",
                     "Domain deliverability destroyed, emails landing in spam filters, and prospective accounts alienated.",
                     "High-relevance, account-based outreach generates 10x higher response rates than high-volume spam.",
                     "Research prospect business challenges and customize outreach to provide immediate educational value."),
            "failure": ("Dialing Without Research", ["Calling senior executives without knowing their company's core business or industry pain points"],
                        "Treating outreach as a numbers game without baseline commercial competence.", "Instant hang-ups and low meeting conversion.",
                        "Spend 3 minutes researching the prospect's recent announcements, open roles, and tech stack before calling."),
            "glossary": [("Sales Qualified Lead (SQL)", "A prospective customer that has been thoroughly vetted and meets the criteria for direct sales engagement.", "Sales Operations")],
            "heuristic": ("Give Value Before Asking for Time", "Share a valuable industry insight or benchmark report in the initial outreach.")
        },

        # ---------------------------------------------------------------------
        # MARKETING LADDER (5 roles)
        # ---------------------------------------------------------------------
        "vp_mktg": {
            "definition": "Vice President of Marketing directing full-funnel marketing strategy, product marketing, content, and demand generation.",
            "mandate": "Build an enduring enterprise brand and orchestrate an efficient pipeline generation machine.",
            "case": ("Hoover Free Flights Promotion Disaster", "The Hoover Company UK", 1992,
                     "Offered two free flights to America for anyone spending £100 on Hoover products, underestimating redemption rates.",
                     "Failure to mathematically model redemption risk; consumers bought £100 vacuums solely for £600 flights.",
                     "£48M in losses, firing of executive management, and eventual fire-sale of the UK company.",
                     "Marketing promotions must be actuarially stress-tested against worst-case consumer arbitrage.",
                     "Require financial and actuarial sign-off on all high-liability promotional mechanics."),
            "failure": ("Misaligned Sales & Marketing Handoff", ["Marketing claiming massive lead generation while Sales complains leads are low quality"],
                        "Unclear definition of Marketing Qualified Lead (MQL) and absence of SLA.", "Wasted marketing spend and friction between departments.",
                        "Unify sales and marketing around a single pipeline metric: Sales Accepted Pipeline (SAP)."),
            "glossary": [("Marketing Attribution", "The analytical science of determining which marketing touchpoints contribute to sales or conversions.", "Marketing")],
            "heuristic": ("Own the Narrative", "If you do not define your market category, your competitors will define it for you.")
        },
        "director_mktg": {
            "definition": "Director of Marketing managing growth channels, campaign performance, and product marketing execution.",
            "mandate": "Scale customer acquisition channels efficiently, maintain payback periods < 12 months, and oversee campaign execution.",
            "case": ("Peloton Holiday Commercial Narrative Misfire", "Peloton Interactive", 2019,
                     "Released a holiday commercial perceived as sexist and dystopian, generating viral consumer outrage.",
                     "Failure of marketing leadership to stress-test narrative perception across diverse audience cohorts.",
                     "$1.5B market capitalization loss in three days.",
                     "Creative storytelling must be reviewed by objective red teams to identify negative narrative interpretations.",
                     "Run qualitative sentiment testing on high-spend video assets before national broadcast."),
            "failure": ("Channel Dependency Risk", ["Relying 80%+ on a single paid advertising channel (e.g. Meta or Google)", "CAC spikes upon algorithm change"],
                        "Failure to build diversified organic, partner, and content acquisition channels.", "Catastrophic volatility in customer acquisition costs.",
                        "Maintain a balanced portfolio across paid, organic SEO, content, and partner channels."),
            "glossary": [("Customer Lifetime Value (LTV)", "A prediction of the net profit attributed to the entire future relationship with a customer.", "Unit Economics")],
            "heuristic": ("Test Small Before Scaling Big", "Validate ad copy and creative on $1,000 budgets before deploying $100,000 campaigns.")
        },
        "mktg_mgr": {
            "definition": "Marketing Manager executing demand generation campaigns, managing webinar pipelines, and analyzing conversion funnels.",
            "mandate": "Drive campaign execution on time and on budget, optimize conversion funnels, and report return on ad spend (ROAS).",
            "case": ("Target Predictive Analytics Privacy Disaster", "Target Corporation", 2012,
                     "Target's pregnancy prediction model sent baby coupons to a high schooler before her father knew she was pregnant, causing public outrage.",
                     "Marketing algorithms utilized customer data without evaluating ethical and interpersonal boundaries.",
                     "National public relations crisis regarding customer surveillance and privacy invasion.",
                     "Data-driven personalization must respect human privacy and customer comfort levels.",
                     "Incorporate privacy and ethical review into automated personalization algorithms."),
            "failure": ("Ignoring Landing Page Conversion", ["Driving expensive paid traffic to slow, confusing, or broken landing pages"],
                        "Focusing exclusively on ad creative while neglecting the downstream landing page experience.", "Extremely high effective CAC.",
                        "Ensure landing page load speed is < 1.5 seconds and messaging perfectly matches ad copy."),
            "glossary": [("Return on Ad Spend (ROAS)", "A marketing metric that measures the efficacy of a digital advertising campaign: Revenue / Cost.", "Paid Acquisition")],
            "heuristic": ("Message Match", "The headline of your landing page must echo the exact hook of the advertisement that drove the click.")
        },
        "mktg_spec": {
            "definition": "Marketing Specialist managing daily PPC campaigns, social media channels, and content publication.",
            "mandate": "Produce high-quality marketing collateral, monitor channel bids, and optimize daily ad spend efficiency.",
            "case": ("Ratners Group Self-Inflicted Brand Suicide", "Ratners Group", 1991,
                     "CEO Gerald Ratner publicly joked in an address that their jewelry products were 'total crap' and cheaper than a prawn sandwich.",
                     "Public disparagement of brand quality destroying customer trust overnight.",
                     "£500M market value erased, nearly bankrupting the multi-hundred-store jewelry chain.",
                     "Never undermine the perceived value and dignity of the product you offer to consumers.",
                     "Ensure all public-facing marketing copy upholds the premium value of the brand."),
            "failure": ("Set-It-and-Forget-It Paid Campaigns", ["Leaving automated PPC bidding running without monitoring negative keywords", "Wasted budget on irrelevant searches"],
                        "Lack of daily operational vigilance in advertising dashboards.", "Thousands of dollars wasted on unqualified clicks.",
                        "Perform weekly negative keyword pruning and review search query reports continuously."),
            "glossary": [("Cost Per Click (CPC)", "The actual price you pay for each click in pay-per-click (PPC) marketing campaigns.", "Performance Marketing")],
            "heuristic": ("A/B Test One Variable at a Time", "When optimizing ads, isolate copy, image, or CTA to identify the true causal driver.")
        },
        "mktg_coord": {
            "definition": "Marketing Coordinator supporting event logistics, webinar staging, social scheduling, and marketing asset management.",
            "mandate": "Coordinate flawless marketing operations, maintain asset libraries, and ensure timely campaign execution.",
            "case": ("Hashtag Hijacking Public Relations Disaster", "Various Global Brands", 2014,
                     "Brands automated social media postings using trending hashtags without checking what the hashtags were actually about (e.g. natural disasters).",
                     "Automating social posting without human contextual review.",
                     "Severe public relations embarrassment and viral public condemnation.",
                     "Never automate social media engagement around unverified trending topics.",
                     "Require manual review for all social media posts associated with trending news topics."),
            "failure": ("Broken Asset Links in Major Launch", ["Launching email campaigns where call-to-action buttons lead to 404 error pages"],
                        "Lack of pre-send checklist verification.", "Wasted promotional reach and embarrassing customer experience.",
                        "Use a strict 10-point QA checklist before approving any email or marketing collateral release."),
            "glossary": [("Call to Action (CTA)", "A prompt on a website or email that encourages the user to take a specified action.", "Conversion Rate Optimization")],
            "heuristic": ("Test Links in Incognito Mode", "Always verify that links, landing pages, and forms function cleanly for non-logged-in users.")
        },

        # ---------------------------------------------------------------------
        # FINANCE LADDER (5 roles)
        # ---------------------------------------------------------------------
        "vp_fin": {
            "definition": "Vice President of Finance overseeing enterprise treasury, corporate audit, tax structuring, and long-range financial planning.",
            "mandate": "Ensure absolute financial compliance, optimize capital structure, and safeguard enterprise solvency.",
            "case": ("Unauthorized Speculative Trading Concealment", "Barings Bank", 1995,
                     "Trader Nick Leeson concealed hundreds of millions in speculative Nikkei futures losses in an unmonitored error account (88888).",
                     "Lack of segregation of duties; Leeson operated as both the frontline head trader and the back-office settlement officer.",
                     "Collapse of a 233-year-old British merchant bank, acquired by ING for £1.",
                     "Front-office trading and back-office clearing/accounting must be strictly and physically segregated.",
                     "Enforce strict segregation of duties between financial commitments and accounting reconciliation."),
            "failure": ("Asset-Liability Duration Mismatch", ["Funding long-term illiquid commitments with short-term volatile credit lines", "Interest rate vulnerability"],
                        "Chasing yield without modeling interest rate hiking cycles.", "Severe liquidity crunch when refinancing credit lines.",
                        "Match the duration of corporate financing liabilities to the duration of corresponding assets."),
            "glossary": [("Duration Mismatch", "A financial risk that arises when the maturities of assets and liabilities do not match.", "Treasury")],
            "heuristic": ("Never Risk Ruin for Incremental Yield", "Preserving capital is infinitely more important than earning an extra 50 bps of yield.")
        },
        "fin_dir": {
            "definition": "Director of Finance managing corporate accounting, revenue recognition (ASC 606), and tax strategy.",
            "mandate": "Ensure GAAP/IFRS accounting compliance, lead audit engagements, and maintain accurate financial ledgers.",
            "case": ("Improper Capitalization of Operating Expenses", "WorldCom Inc.", 2002,
                     "WorldCom capitalized over $3.8B of routine 'line costs' (telecom access fees) as capital expenditures instead of operating expenses.",
                     "Deliberate accounting manipulation to artificially inflate EBITDA and meet Wall Street consensus expectations.",
                     "$11B total fraud, Chapter 11 bankruptcy, and prison sentences for executives.",
                     "Operating expenses cannot be capitalized under GAAP to mask deteriorating operational cash flows.",
                     "Review capitalization policies with external auditors; enforce strict compliance with ASC 350/ASC 360."),
            "failure": ("Revenue Recognition Prematurity (ASC 606 Violation)", ["Recognizing multi-year software revenue before delivery obligations are satisfied"],
                        "Pressure from executive sales to show immediate ARR growth.", "Financial restatements, SEC scrutiny, and shareholder lawsuits.",
                        "Recognize revenue strictly as contractual performance obligations are measurably fulfilled."),
            "glossary": [("ASC 606", "The universal accounting standard for revenue recognition across contracts with customers.", "Accounting Standards")],
            "heuristic": ("Conservative Over Aggressive", "When accounting interpretation is ambiguous, adopt the more conservative revenue treatment.")
        },
        "fin_mgr": {
            "definition": "Finance Manager leading the monthly accounting close, FP&A variance analysis, and departmental budgeting.",
            "mandate": "Close corporate financial books accurately within 5 business days and deliver insightful variance analysis.",
            "case": ("Hertz Vehicle Depreciation Accounting Restatement", "Hertz Global Holdings", 2014,
                     "Hertz improperly accounted for vehicle depreciation and allowances for uncollectible accounts, requiring three years of restatements.",
                     "Inadequate internal controls and failure to adjust depreciation schedules to declining used car market prices.",
                     "Executive resignations and $26M in SEC penalties.",
                     "Depreciation models must reflect actual market reality and liquidation values.",
                     "Regularly benchmark balance sheet asset carrying values against objective secondary market data."),
            "failure": ("Slow Close Paralysis", ["Taking 25 business days to close the monthly books", "Leadership operating with stale financial data"],
                        "Manual spreadsheet reconciliation and absence of automated ERP integration.", "Executive decisions made on outdated assumptions.",
                        "Automate journal entries and reconciliations to achieve a continuous 5-day financial close."),
            "glossary": [("Variance Analysis", "The quantitative investigation of the difference between actual and planned financial behavior.", "FP&A")],
            "heuristic": ("Materiality Rule", "Focus forensic investigation on variances that materially affect EBITDA and cash runway.")
        },
        "sr_fin_analyst": {
            "definition": "Senior Financial Analyst building corporate valuation models, unit economic models, and Board financial presentations.",
            "mandate": "Deliver high-fidelity financial models, stress-test business unit assumptions, and forecast capital needs.",
            "case": ("Excel Model Formula Error in Multi-Billion Acquisition", "Barclays / Lehman Brothers Assets", 2008,
                     "A junior associate's Excel spreadsheet contained hidden rows that accidentally included 179 contracts Barclays did not intend to assume.",
                     "Lack of peer review and failure to audit hidden rows in complex M&A spreadsheets.",
                     "Undesired assumption of millions in liabilities.",
                     "Critical financial models must undergo formal code-like review and automated sanity checks.",
                     "Enforce automated model validation, dynamic unhidden ranges, and two-person financial review."),
            "failure": ("Garbage-In, Garbage-Out Modeling", ["Building 20-tab financial models based on arbitrary unverified growth percentages"],
                        "Focusing on spreadsheet visual complexity rather than empirical unit economic drivers.", "Delusional business plans and missed milestones.",
                        "Anchor all financial projections to historical cohort retention, verified conversion rates, and real CAC trends."),
            "glossary": [("Discounted Cash Flow (DCF)", "A valuation method that estimates the value of an investment based on its expected future cash flows.", "Valuation")],
            "heuristic": ("Sensitivity Analysis", "Always present Base, Bull, and Bear scenarios with explicit macroeconomic variable swings.")
        },
        "fin_analyst": {
            "definition": "Financial Analyst assisting with accounts payable/receivable, invoice audits, and financial reporting.",
            "mandate": "Maintain ledger precision, audit vendor invoices against contracts, and prepare clean reconciliations.",
            "case": ("CEO Impersonation Wire Fraud", "Pathé Cinema", 2018,
                     "Attackers spoofed the CEO's email and convinced the financial director to wire €19M for a purported secret acquisition.",
                     "Absence of dual-authorization voice verification protocols for large outbound capital transfers.",
                     "Loss of €19M and immediate dismissal of financial leadership.",
                     "No capital transfer can be approved based solely on email instructions regardless of sender title.",
                     "Enforce dual-signatory verification and independent voice confirmation on all wire transfers > $50,000."),
            "failure": ("Blind Invoice Approval", ["Approving recurring software subscriptions and vendor invoices without verifying contract utilization"],
                        "Rushing accounts payable workflows without matching purchase orders.", "Thousands of dollars in monthly corporate SaaS waste.",
                        "Enforce three-way matching: compare Purchase Order, Receiving Proof, and Vendor Invoice before payment."),
            "glossary": [("Three-Way Matching", "The process of verifying that the Purchase Order, Goods Receipt, and Vendor Invoice match before payment.", "Accounts Payable")],
            "heuristic": ("Reconcile to the Penny", "If the balance sheet doesn't tie out by even $1, investigate: it often hides compensating errors.")
        },

        # ---------------------------------------------------------------------
        # OPERATIONS LADDER (5 roles)
        # ---------------------------------------------------------------------
        "vp_ops": {
            "definition": "Vice President of Operations directing business continuity, global supply chain, facilities, and operational efficiency.",
            "mandate": "Build resilient, fail-safe business infrastructure that scales without linear overhead growth.",
            "case": ("Target Canada Catastrophic Supply Chain Collapse", "Target Corporation", 2013,
                     "Target expanded into Canada opening 124 stores, but suffered massive ERP and warehouse data corruption resulting in empty shelves.",
                     "Rushing SAP ERP rollout without verifying product dimensions, barcode data, and supply chain replenishment logic.",
                     "$2B total loss and complete retreat from Canada within two years.",
                     "Supply chain software and inventory master data must be validated in pilot environments before national scaling.",
                     "Pilot supply chain and warehouse integrations with live physical stress tests before nationwide rollouts."),
            "failure": ("Just-In-Time Fragility", ["Eliminating all buffer inventory to achieve theoretical efficiency", "Single supply disruption halts company"],
                        "Optimizing purely for lowest cost rather than systemic resilience.", "Complete inability to fulfill customer orders during supply shocks.",
                        "Identify critical single-source materials and maintain strategic buffer reserves."),
            "glossary": [("Six Sigma", "A set of techniques and tools for process improvement aiming for near-zero defect rates (3.4 defects per million).", "Quality Management")],
            "heuristic": ("Resilience Over Pure Efficiency", "A 5% efficiency improvement is useless if it creates a 50% probability of catastrophic downtime.")
        },
        "ops_dir": {
            "definition": "Director of Operations managing regional logistics, facilities, and departmental vendor contracts.",
            "mandate": "Ensure smooth physical and digital business operations, meet operational SLAs, and manage operational expenditures.",
            "case": ("KFC UK Chicken Supply Gridlock", "KFC UK", 2018,
                     "KFC switched logistics providers to DHL, whose single distribution center suffered operational failure, closing 800+ restaurants.",
                     "Consolidating distribution into a single logistics hub without verified fallback facilities.",
                     "Estimated £1M+ per day in losses and massive brand mockery.",
                     "Critical logistics networks require distributed distribution points and tested disaster recovery failovers.",
                     "Maintain dual-distribution routing for all mission-critical operational components."),
            "failure": ("Vendor Lock-In Paralysis", ["Contracting with an operational vendor with proprietary formats and prohibitive switching costs"],
                        "Failing to plan for contract expiration or vendor insolvency.", "Exorbitant vendor price hikes and operational dependency.",
                        "Always require open standard formats and an explicit vendor exit migration plan."),
            "glossary": [("Root Cause Analysis (RCA)", "A method of problem solving used for identifying the root causes of faults or problems.", "Quality Assurance")],
            "heuristic": ("The 5 Whys", "Drill down through five layers of 'Why' to uncover the systemic root cause of an operational breakdown.")
        },
        "ops_mgr": {
            "definition": "Operations Manager supervising day-to-day fulfillment, business workflows, and operational team performance.",
            "mandate": "Maintain 99.9% fulfillment SLAs, eliminate daily process bottlenecks, and uphold operational safety.",
            "case": ("Amazon Fulfillment Center Heat Exhaustion Scrutiny", "Amazon.com Inc.", 2011,
                     "During extreme summer heat, an Allentown warehouse lacked air conditioning, resulting in worker medical emergencies.",
                     "Management prioritizing picking rates over human environmental safety standards.",
                     "Severe OSHA scrutiny, national investigative journalism backlash, and costly emergency HVAC retrofits.",
                     "Operational throughput can never be achieved by violating human physical and safety limitations.",
                     "Implement mandatory environmental safety sensors and automated shift-cooling protocols."),
            "failure": ("Treating Symptoms Instead of Root Causes", ["Constantly applying manual workarounds to bypass a broken workflow"],
                        "Short-term bias that wastes cumulative hours firefighting rather than fixing the underlying tool.", "Compounding operational friction and worker frustration.",
                        "Whenever a process fails twice, stop and fix the underlying system rather than patching manually."),
            "glossary": [("Standard Operating Procedure (SOP)", "A set of step-by-step instructions compiled by an organization to help workers carry out routine operations.", "Operations")],
            "heuristic": ("Standardize Before You Automate", "Automating an inefficient process merely produces automated inefficiency.")
        },
        "ops_sup": {
            "definition": "Operations Supervisor leading frontline teams, managing shift schedules, and monitoring throughput.",
            "mandate": "Ensure daily work orders are completed safely, maintain team morale, and inspect output quality.",
            "case": ("Deepwater Horizon Shift Handover Failure", "BP plc", 2010,
                     "Critical negative pressure test results and drilling anomalies were not communicated clearly during the shift changeover prior to blowout.",
                     "Informal and incomplete shift handover documentation.",
                     "Catastrophic oil spill, 11 deaths, and tens of billions in environmental liabilities.",
                     "Shift handovers must follow standardized, written, and verified transfer protocols.",
                     "Enforce mandatory structured shift handover checklists signed by both incoming and outgoing supervisors."),
            "failure": ("Informal Shift Hand-offs", ["Passing critical operational context verbally in the hallway without written verification"],
                        "Lack of structured handover checklists.", "Critical errors occurring immediately following shift changes.",
                        "Require formal written shift logs detailing open incidents, pending tasks, and safety status."),
            "glossary": [("Gemba Walk", "The practice of personal observation of work where the work is actually being performed.", "Lean Management")],
            "heuristic": ("Go to the Gemba", "Do not manage from an office; observe the frontline operational line directly to see reality.")
        },
        "ops_assoc": {
            "definition": "Operations Associate executing frontline workflows, data entry, ticket triage, and operational tasks.",
            "mandate": "Execute tasks accurately, report operational defects immediately, and adhere strictly to safety protocols.",
            "case": ("Hawaii False Ballistic Missile Alert", "Hawaii Emergency Management Agency", 2018,
                     "An employee triggered a terrifying false ballistic missile alert to entire state of Hawaii by selecting the wrong option from an ambiguous dropdown.",
                     "Poor user interface design with confusing options ('Drill' vs 'Live') and no confirmation dialog.",
                     "Statewide panic for 38 minutes.",
                     "High-impact actions must have explicit confirmation gates and distinct visual interfaces.",
                     "Always double-check confirmation dialogs before triggering irreversible operational broadcasts."),
            "failure": ("Blindly Following Broken Instructions", ["Continuing to run an SOP despite noticing it produces incorrect output"],
                        "Fear of questioning management documentation.", "Propagation of corrupted data or defective output.",
                        "If an instruction produces an anomaly, pause execution immediately and notify the shift supervisor."),
            "glossary": [("Cycle Time", "The time required to complete a single task from start to finish.", "Operations")],
            "heuristic": ("Stop and Check", "If something looks unusual or contradictory, pause and verify before proceeding.")
        },

        # ---------------------------------------------------------------------
        # PEOPLE / HR LADDER (5 roles)
        # ---------------------------------------------------------------------
        "vp_people": {
            "definition": "Vice President of People leading organizational design, leadership succession, diversity and inclusion, and culture.",
            "mandate": "Build an elite, high-integrity organizational culture and cultivate an environment where world-class talent thrives.",
            "case": ("Bridgewater Radical Transparency and Meaningful Work", "Bridgewater Associates", 2011,
                     "Ray Dalio instituted radical transparency with 'Dot Collector' app to record meetings and rate colleagues openly.",
                     "Systematic codification of meritocratic culture where ideas compete on merit rather than hierarchical seniority.",
                     "World's largest and most successful hedge fund over decades.",
                     "Culture must be formalized with explicit behavioral principles and transparent feedback loops.",
                     "Incorporate transparent, meritocratic feedback mechanisms into all organizational reviews."),
            "failure": ("HR as Bureaucratic Obstacle", ["Creating dense paperwork requirements that slow hiring and innovation"],
                        "Losing sight of the business mission and focusing on procedural self-preservation.", "Engineering and sales leaders bypassing HR completely.",
                        "Design people systems that reduce friction and accelerate high-performance hiring."),
            "glossary": [("Employee Net Promoter Score (eNPS)", "A method of measuring how employees feel about their company: 'How likely are you to recommend working here?'", "People Ops")],
            "heuristic": ("Culture Is What You Tolerate", "Your actual culture is defined by the worst behavior your leadership permits.")
        },
        "hr_dir": {
            "definition": "Director of Human Resources managing employee relations, compliance, benefits, and workplace investigations.",
            "mandate": "Ensure workplace fairness, protect employee legal rights, and conduct impartial, thorough workplace investigations.",
            "case": ("Fox News Host Harassment Settlements Scandal", "21st Century Fox", 2016,
                     "Long-running sexual harassment claims were repeatedly settled secretly with non-disclosure agreements rather than addressing root causes.",
                     "Prioritizing short-term public image and top-earning talent over employee safety and ethical conduct.",
                     "Resignation of network chairman Roger Ailes, top host Bill O'Reilly, and massive reputational damage.",
                     "Workplace investigations must be independent and report directly to governance committees.",
                     "Conduct objective, independent investigations of all harassment allegations with zero executive interference."),
            "failure": ("Predetermined Investigation Outcomes", ["Conducting investigations to protect the company from liability rather than discovering the truth"],
                        "Conflating risk management with covering up misconduct.", "Loss of employee trust and explosive external leaks.",
                        "Follow the facts wherever they lead; document findings objectively and recommend appropriate remedies."),
            "glossary": [("Title VII of the Civil Rights Act", "Federal law prohibiting employment discrimination based on race, color, religion, sex, and national origin.", "Employment Law")],
            "heuristic": ("Document Everything Contemporaneously", "Undocumented conversations do not exist in the eyes of an employment tribunal.")
        },
        "hr_mgr": {
            "definition": "Human Resources Manager overseeing performance reviews, onboarding programs, and manager coaching.",
            "mandate": "Coach managers on leadership, ensure smooth employee onboarding, and resolve frontline workplace disputes.",
            "case": ("Basecamp Internal Political Discourse Ban", "Basecamp", 2021,
                     "Leadership announced a sudden ban on internal societal and political discussions on company chat without employee consultation.",
                     "Abrupt top-down cultural edict without empathy, dialogue, or nuance.",
                     "Resignation of roughly one-third of the company's workforce within days.",
                     "Cultural shifts must be communicated with deep stakeholder empathy and listening sessions.",
                     "Engage employees in structured dialogue before instituting sweeping cultural policy shifts."),
            "failure": ("Ghosting Exiting Employees", ["Treating departing team members with cold hostility or bureaucratic silence"],
                        "Short-sightedness that damages the company's alumni network and Glassdoor reputation.", "Negative employer brand and harder future recruiting.",
                        "Treat departing employees with high dignity and respect; they are future ambassadors and clients."),
            "glossary": [("Performance Improvement Plan (PIP)", "A formal document outlining specific areas where an employee must improve within a defined period.", "Performance Management")],
            "heuristic": ("Praise in Public, Criticize in Private", "Never provide critical behavioral feedback in group settings.")
        },
        "hrbp": {
            "definition": "Human Resources Business Partner embedded within functional departments to advise executives on talent strategy.",
            "mandate": "Align workforce planning with departmental roadmaps, identify retention risks, and facilitate leadership development.",
            "case": ("Google Project Aristotle on Team Psychological Safety", "Google LLC", 2016,
                     "Google conducted a multi-year study analyzing hundreds of teams to determine why some succeeded while others stumbled.",
                     "Discovered that psychological safety—not individual pedigree or technical brilliance—was the single greatest predictor of team success.",
                     "Transformed Google's leadership training and manager evaluation rubrics worldwide.",
                     "HR must coach managers to create environments where team members feel safe to take risks and admit mistakes.",
                     "Assess and cultivate psychological safety in every departmental team review."),
            "failure": ("Acting as a Management Mouthpiece", ["Echoing management demands without advocating for organizational and employee health"],
                        "Fear of challenging departmental directors.", "Loss of trust from frontline employees.",
                        "Act as a courageous, trusted advisor who tells leaders the hard truth about team morale."),
            "glossary": [("Succession Planning", "A process for identifying and developing new leaders who can replace old leaders when they leave.", "Talent Management")],
            "heuristic": ("Stay Close to the Frontline", "Conduct regular 1-on-1 skip-level listening tours to keep your finger on the cultural pulse.")
        },
        "hr_coord": {
            "definition": "Human Resources Coordinator executing onboarding logistics, employee records, benefits enrollments, and compliance filings.",
            "mandate": "Ensure flawless onboarding experiences for new hires, maintain 100% compliance in employee records, and assist with HR tasks.",
            "case": ("I-9 Employment Verification Audit Fines", "Various Enterprise Employers (ICE Audits)", 2019,
                     "Companies audited by federal regulators faced millions in fines due to missing or incorrectly completed Form I-9 documents.",
                     "Treating federal compliance paperwork as a casual clerical task without systematic audits.",
                     "Massive financial penalties and legal liability.",
                     "Employment eligibility verification requires meticulous, error-free compliance.",
                     "Audit 100% of employee I-9 files within 3 business days of hire with zero exceptions."),
            "failure": ("Disorganized Day-One Onboarding", ["New hires arriving with no laptop, no logins, and an absent manager"],
                        "Lack of coordination between HR, IT, and hiring managers.", "Immediate buyer's remorse and high 90-day attrition.",
                        "Execute a standardized Day-One checklist ensuring laptop, access, and schedule are ready 24 hours prior to start date."),
            "glossary": [("Form I-9", "A US federal form used for verifying the identity and employment authorization of individuals hired for employment.", "Compliance")],
            "heuristic": ("First Impressions Matter", "An inspiring, organized first week sets the tone for an employee's multi-year tenure.")
        }
    }

    for role_id, cfg in ladder_configs.items():
        role = ALL_ROLES.get(role_id)
        if not role:
            continue

        c_title, c_org, c_yr, c_sum, c_root, c_imp, c_less, c_role = cfg["case"]
        f_name, f_sym, f_root, f_imp, f_mit = cfg["failure"]

        entry = EncyclopediaEntry(
            role_id=role_id,
            role_title=role.title,
            department=role.department,
            level=role.level,
            canonical_definition=cfg["definition"],
            core_mandate=cfg["mandate"],
            historical_case_studies=[
                HistoricalCaseStudy(
                    title=c_title,
                    organization=c_org,
                    year=c_yr,
                    incident_summary=c_sum,
                    root_cause=c_root,
                    catastrophic_impact=c_imp,
                    lessons_learned=c_less,
                    role_implication=c_role,
                )
            ],
            failure_modes=[
                FailureMode(
                    name=f_name,
                    symptoms=f_sym,
                    root_cause=f_root,
                    catastrophic_impact=f_imp,
                    mitigation_protocol=f_mit,
                )
            ],
            key_glossary=[
                GlossaryTerm(term=term, definition=defn, domain=dom)
                for term, defn, dom in cfg["glossary"]
            ],
            decision_heuristics=[
                DecisionHeuristic(
                    name=cfg["heuristic"][0],
                    principle=cfg["heuristic"][1],
                    application=f"Strictly apply in daily {role.title} operations."
                )
            ]
        )
        _register(entry)


_generate_ladder_dossiers()


# =============================================================================
# ENCYCLOPEDIC SEARCH & LOOKUP ENGINE
# =============================================================================

def get_role_encyclopedia(role_id: str) -> Optional[EncyclopediaEntry]:
    """Returns the comprehensive encyclopedic dossier for a specific role."""
    return ENCYCLOPEDIA.get(role_id.lower())


def get_all_encyclopedias() -> Dict[str, EncyclopediaEntry]:
    """Returns all 48 encyclopedic dossiers."""
    return ENCYCLOPEDIA


def search_encyclopedia(query: str, role_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Performs full-text relevance search across encyclopedic entries, cases, failure modes, and glossaries."""
    q = query.lower().strip()
    if not q:
        return []

    tokens = q.split()
    results = []

    search_pool = [ENCYCLOPEDIA[role_id.lower()]] if (role_id and role_id.lower() in ENCYCLOPEDIA) else ENCYCLOPEDIA.values()

    for entry in search_pool:
        score = 0.0
        matches = []

        # 1. Match role title & department
        if q in entry.role_title.lower() or q in entry.role_id.lower():
            score += 15.0
            matches.append(f"Role title match: {entry.role_title}")
        if q in entry.department.lower():
            score += 8.0
            matches.append(f"Department: {entry.department}")

        # 2. Match canonical definition
        def_lower = entry.canonical_definition.lower()
        if q in def_lower:
            score += 10.0
            matches.append("Canonical definition contains exact query")
        else:
            token_hits = sum(1 for t in tokens if t in def_lower)
            if token_hits > 0:
                score += token_hits * 2.0
                matches.append(f"Definition matches {token_hits} query term(s)")

        # 3. Match historical case studies
        for cs in entry.historical_case_studies:
            cs_text = f"{cs.title} {cs.organization} {cs.incident_summary} {cs.root_cause} {cs.lessons_learned}".lower()
            if q in cs_text:
                score += 12.0
                matches.append(f"Case study: '{cs.title}' ({cs.organization})")
            else:
                hits = sum(1 for t in tokens if t in cs_text)
                if hits > 0:
                    score += hits * 1.5

        # 4. Match failure modes
        for fm in entry.failure_modes:
            fm_text = f"{fm.name} {' '.join(fm.symptoms)} {fm.root_cause} {fm.mitigation_protocol}".lower()
            if q in fm_text:
                score += 12.0
                matches.append(f"Failure mode: '{fm.name}'")
            else:
                hits = sum(1 for t in tokens if t in fm_text)
                if hits > 0:
                    score += hits * 1.5

        # 5. Match glossary
        for term in entry.key_glossary:
            term_text = f"{term.term} {term.definition}".lower()
            if q in term_text:
                score += 14.0
                matches.append(f"Glossary term: '{term.term}'")
            else:
                hits = sum(1 for t in tokens if t in term_text)
                if hits > 0:
                    score += hits * 2.0

        # 6. Match training resources and books (Version 2.0)
        for res in entry.training_resources:
            res_text = f"{res.title} {res.description} {res.track}".lower()
            if q in res_text:
                score += 15.0
                matches.append(f"Training Resource: '{res.title}'")
        for bk in entry.book_references:
            bk_text = f"{bk.title} {bk.publisher} {bk.description}".lower()
            if q in bk_text:
                score += 15.0
                matches.append(f"Reference Book: '{bk.title}'")

        if score > 0.0:
            results.append({
                "role_id": entry.role_id,
                "role_title": entry.role_title,
                "department": entry.department,
                "level": entry.level,
                "score": round(score, 2),
                "matches": matches[:4],
                "canonical_definition_snippet": entry.canonical_definition[:160] + "...",
                "case_studies_count": len(entry.historical_case_studies),
                "failure_modes_count": len(entry.failure_modes),
                "training_resources_count": len(entry.training_resources),
                "book_references_count": len(entry.book_references),
            })

    results.sort(key=lambda x: -x["score"])
    return results[:limit]


# -----------------------------------------------------------------------------
# Hydrate all 48 Encyclopedia Entries with Version 2.0 Learning Maps
# -----------------------------------------------------------------------------
for _role_id, _entry in ENCYCLOPEDIA.items():
    _lm = get_role_learning_map(_role_id)
    if _lm:
        _entry.core_capability_profile = _lm.core_capability_profile
        _entry.role_focus_summary = _lm.role_focus_summary
        _entry.training_resources = _lm.training_resources
        _entry.book_references = _lm.book_references
