"""AegisCorp OS — PhD-Level & Gold-Medalist Knowledge Base.

Defines comprehensive, academically rigorous curricula, mathematical models,
landmark citations, regulatory standards, core algorithms, and benchmark challenges
for all 48 enterprise roles across the Board, C-Suite, and all 7 department ladders.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class MathematicalFormulation(BaseModel):
    name: str
    formula: str
    latex: str
    variables: Dict[str, str]
    application: str


class LandmarkPaper(BaseModel):
    title: str
    authors: str
    year: int
    venue: str
    key_contribution: str


class BenchmarkScenario(BaseModel):
    scenario_id: str
    title: str
    difficulty: str  # "PhD-Comprehensive", "Olympiad-Gold", "Mastery"
    context: str
    challenge: str
    ground_truth_criteria: List[str]
    rubric_weights: Dict[str, float]


class RoleCurriculum(BaseModel):
    role_id: str
    role_title: str
    department: str
    level: int
    theoretical_foundations: List[str]
    mathematical_formulations: List[MathematicalFormulation]
    landmark_papers: List[LandmarkPaper]
    regulatory_and_industry_standards: List[str]
    core_algorithms_and_methods: List[str]
    gold_medalist_playbook: List[str]
    benchmark_scenarios: List[BenchmarkScenario]


CURRICULA: Dict[str, RoleCurriculum] = {
    # -------------------------------------------------------------------------
    # 1. BOARD OF DIRECTORS
    # -------------------------------------------------------------------------
    "board": RoleCurriculum(
        role_id="board",
        role_title="Board of Directors",
        department="Governance",
        level=0,
        theoretical_foundations=[
            "Agency Theory & Separation of Ownership and Control (Fama & Jensen 1983)",
            "Stochastic Optimal Control & Capital Allocation (Merton 1971)",
            "Modern Portfolio Theory & Asymmetric Loss Aversion (Markowitz 1952, Kahneman-Tversky 1979)",
            "Social Choice Theory & Arrow's Impossibility Theorem in Preference Aggregation (Arrow 1951)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Agency Cost Minimization",
                formula="min C_total = C_monitoring + C_bonding + Residual_Loss",
                latex=r"\min C_{agency} = C_m + C_b + L",
                variables={"C_m": "Monitoring expenditure by principal", "C_b": "Bonding expenditure by agent", "L": "Residual loss from misalignment"},
                application="Optimal fiduciary governance structure balancing executive incentive contracts and audit overhead.",
            ),
            MathematicalFormulation(
                name="Modigliani-Miller Proposition II with Corporate Taxes",
                formula="r_E = r_0 + (r_0 - r_D) * (1 - T_C) * (D / E)",
                latex=r"r_E = r_0 + (r_0 - r_D)(1 - T_C)\frac{D}{E}",
                variables={"r_E": "Cost of equity", "r_0": "Unlevered cost of capital", "r_D": "Cost of debt", "T_C": "Corporate tax rate", "D/E": "Debt-to-equity ratio"},
                application="Determining optimal corporate capital structure and hurdle rates for board-level capital deployment.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure",
                authors="Michael C. Jensen, William H. Meckling",
                year=1976,
                venue="Journal of Financial Economics",
                key_contribution="Formalized agency costs and proved how equity ownership and debt discipline corporate managers.",
            ),
            LandmarkPaper(
                title="Portfolio Selection",
                authors="Harry Markowitz",
                year=1952,
                venue="The Journal of Finance",
                key_contribution="Pioneered mean-variance portfolio optimization and the mathematical efficient frontier.",
            ),
        ],
        regulatory_and_industry_standards=[
            "Delaware General Corporation Law (DGCL) § 102(b)(7), § 141 (Business Judgment Rule, Revlon & Unocal duties)",
            "Sarbanes-Oxley Act (SOX) Sections 302, 404, 906",
            "COSO Enterprise Risk Management (ERM) Framework (2017)",
            "OECD Principles of Corporate Governance",
        ],
        core_algorithms_and_methods=[
            "Quadratic Programming for Mean-Variance Asset Allocation",
            "Monte Carlo Fiduciary Solvency Stress Testing (100k paths)",
            "Bayesian Model Averaging for Geopolitical Black Swan Scenarios",
        ],
        gold_medalist_playbook=[
            "Never rubber-stamp executive consensus; demand second-order consequence modeling on all capital commitments >= $100M.",
            "Enforce strict asymmetric risk filters: if downside includes enterprise insolvency, probability is irrelevant—reject.",
            "Maintain audit committee independence with unannounced internal control verification gates.",
            "Separate the Chairman oversight authority from CEO operational execution to eliminate self-policing.",
            "Align executive compensation exclusively to risk-adjusted, 5-to-10 year economic value added (EVA), not short-term EPS.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="board_bs_001",
                title="Hostile $15B Takeover Defense vs Fiduciary Duty to Accrete Shareholder Value",
                difficulty="PhD-Comprehensive",
                context="A rival consortium launches an unsolicited tender offer at a 42% premium during a temporary market downturn.",
                challenge="Structure a board defense evaluating Revlon duties, poison pill legality under Unocal, and standalone DCF intrinsic value.",
                ground_truth_criteria=[
                    "Proper invocation of Unocal two-pronged proportionality test",
                    "Intrinsic DCF valuation model with terminal Gordon growth assumptions",
                    "Independent committee formation and fairness opinion requirement",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "risk_discipline": 0.25, "decision_accuracy": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 2. CHIEF EXECUTIVE OFFICER
    # -------------------------------------------------------------------------
    "ceo": RoleCurriculum(
        role_id="ceo",
        role_title="Chief Executive Officer",
        department="Executive",
        level=1,
        theoretical_foundations=[
            "Dynamic Capabilities Theory (Teece, Pisano, Shuen 1997)",
            "Non-Cooperative Game Theory & Multi-Agent Nash Equilibria (Nash 1950)",
            "The Innovator's Dilemma & Disruptive Innovation (Christensen 1997)",
            "Strategic Intent & Resource-Based View of the Firm (Barney 1991, Hamel & Prahalad 1989)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Bass Technology Diffusion Model",
                formula="dN(t)/dt = [p + (q/M)*N(t)] * [M - N(t)]",
                latex=r"\frac{dN(t)}{dt} = \left(p + \frac{q}{M}N(t)\right)(M - N(t))",
                variables={"p": "Coefficient of innovation", "q": "Coefficient of imitation", "M": "Market carrying capacity", "N(t)": "Cumulative adopters"},
                application="Forecasting multi-year enterprise technology adoption curves and TAM penetration rates.",
            ),
            MathematicalFormulation(
                name="Real Options Expansion Valuation",
                formula="C = S*N(d1) - K*e^(-r*T)*N(d2)",
                latex=r"C(S, t) = S_0 \Phi(d_1) - K e^{-rT} \Phi(d_2)",
                variables={"S_0": "Present value of underlying strategic asset", "K": "Follow-on investment cost", "T": "Time to decision", "r": "Risk-free rate"},
                application="Valuing multi-stage R&D initiatives and strategic acquisitions with real option optionality.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="Dynamic Capabilities and Strategic Management",
                authors="David J. Teece, Gary Pisano, Amy Shuen",
                year=1997,
                venue="Strategic Management Journal",
                key_contribution="Defined sensing, seizing, and transforming capabilities required for durable enterprise competitive advantage.",
            ),
            LandmarkPaper(
                title="Good Strategy / Bad Strategy: The Difference and Why It Matters",
                authors="Richard P. Rumelt",
                year=2011,
                venue="Crown Business",
                key_contribution="Formalized the strategy kernel: diagnosis, guiding policy, and coherent action.",
            ),
        ],
        regulatory_and_industry_standards=[
            "SEC Regulation Fair Disclosure (Reg FD)",
            "FTC / DOJ Horizontal Merger Guidelines (Herfindahl-Hirschman Index thresholds)",
            "Delaware Caremark Standard for Executive Oversight",
        ],
        core_algorithms_and_methods=[
            "Backward Induction in Extensive-Form Strategic Games",
            "Multi-Horizon Scenario Planning & Real Options Lattice Trees",
            "DuPont Return on Equity Multi-Factor Decomposition",
        ],
        gold_medalist_playbook=[
            "Strategy is fundamentally about choosing what NOT to do; eliminate low-margin distractions with ruthless focus.",
            "Insist on an explicit diagnosis of the single proximate challenge before approving any multi-million-dollar program.",
            "Structure executive councils to force dissenting perspectives to be recorded in immutable audit logs.",
            "Protect the balance sheet: ensure minimum 24-month liquidity runway under severe stagflation scenarios.",
            "Delegate operational execution completely to C-suite while holding direct veto power over culture and strategy.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="ceo_bs_001",
                title="Multi-Horizon Enterprise Pivot: AI Cloud Platform Transformation",
                difficulty="Olympiad-Gold",
                context="Legacy enterprise software revenue is decelerating 8% YoY while cloud-native LLM infrastructure demand surges 120%.",
                challenge="Formulate a 3-year capital reallocation plan migrating $200M OPEX while maintaining cash-flow breakeven and avoiding innovator's dilemma.",
                ground_truth_criteria=[
                    "Quantified real options tree evaluating staged build-vs-buy",
                    "Dual-operating model preserving cash-cow margin while seeding cloud engine",
                    "Governance escalation protocol for board approval of debt facility",
                ],
                rubric_weights={"domain_mastery": 0.20, "reasoning_quality": 0.25, "decision_accuracy": 0.20, "execution_reliability": 0.20, "risk_discipline": 0.15},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 3. CHIEF FINANCIAL OFFICER
    # -------------------------------------------------------------------------
    "cfo": RoleCurriculum(
        role_id="cfo",
        role_title="Chief Financial Officer",
        department="Finance",
        level=2,
        theoretical_foundations=[
            "Black-Scholes-Merton Contingent Claims Analysis (Black, Scholes 1973, Merton 1973)",
            "Pecking Order Theory of Capital Structure (Myers & Majluf 1984)",
            "Structural Credit Risk & Distance to Default Modeling (Merton 1974)",
            "Arbitrage Pricing Theory & Multi-Factor Risk (Ross 1976)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Weighted Average Cost of Capital (WACC)",
                formula="WACC = (E/V)*Ke + (D/V)*Kd*(1 - Tc)",
                latex=r"WACC = \frac{E}{V} K_e + \frac{D}{V} K_d (1 - T_c)",
                variables={"E": "Market value of equity", "D": "Market value of debt", "V": "E + D", "Ke": "Cost of equity (CAPM)", "Kd": "Pre-tax cost of debt", "Tc": "Tax rate"},
                application="Establishing the enterprise hurdle rate for capital budgeting and DCF enterprise valuation.",
            ),
            MathematicalFormulation(
                name="Altman Z-Score for Bankruptcy Prediction",
                formula="Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5",
                latex=r"Z = 1.2 X_1 + 1.4 X_2 + 3.3 X_3 + 0.6 X_4 + 0.999 X_5",
                variables={"X1": "Working Capital / Total Assets", "X2": "Retained Earnings / Total Assets", "X3": "EBIT / Total Assets", "X4": "Market Value Equity / Total Liabilities", "X5": "Sales / Total Assets"},
                application="Monitoring corporate credit solvency and probability of distress across supply chain and subsidiaries.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="The Pricing of Options and Corporate Liabilities",
                authors="Fischer Black, Myron Scholes",
                year=1973,
                venue="Journal of Political Economy",
                key_contribution="Derived the partial differential equation for options, enabling exact contingent claims valuation.",
            ),
            LandmarkPaper(
                title="Corporate Financing and Investment Decisions When Firms Have Information That Investors Do Not Have",
                authors="Stewart C. Myers, Nicholas S. Majluf",
                year=1984,
                venue="Journal of Financial Economics",
                key_contribution="Proved the pecking order: internal cash > debt > hybrid securities > equity issuance.",
            ),
        ],
        regulatory_and_industry_standards=[
            "US GAAP / IFRS (ASC 606 Revenue Recognition, ASC 842 Leases)",
            "Sarbanes-Oxley Act Section 404 (ICFR Financial Controls)",
            "SEC Form 10-K, 10-Q, 8-K reporting compliance",
            "Basel III/IV Capital Adequacy & Liquidity Coverage Ratio (LCR)",
        ],
        core_algorithms_and_methods=[
            "Discounted Cash Flow (FCFF / FCFE) Multi-Stage Modeling",
            "Cornish-Fisher Value at Risk (VaR) & Expected Shortfall (CVaR)",
            "Cholesky Decomposition for Correlated Multi-Asset Treasury Risk",
        ],
        gold_medalist_playbook=[
            "Cash flow is reality; accounting earnings are an opinion. Anchor every balance sheet audit in unlevered free cash flow.",
            "Enforce deterministic approval gates: zero capital disbursements > $1M proceed without documented DCF and hurdle clearance.",
            "Run daily liquidity stress tests against severe bank failure and credit freeze conditions.",
            "Hedge foreign exchange and interest rate exposure using synthetic matching rather than speculative derivatives.",
            "Maintain an aggressive working capital cash conversion cycle (CCC) targeting negative working capital where feasible.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="cfo_bs_001",
                title="Capital Structure Restructuring Under Rising Interest Rate Shock (+350 bps)",
                difficulty="PhD-Comprehensive",
                context="The enterprise has $400M floating rate debt maturing in 18 months amidst sudden macroeconomic rate spikes.",
                challenge="Construct an optimal refinancing package evaluating convertible debt, interest rate swaptions, and equity dilution trade-offs.",
                ground_truth_criteria=[
                    "Full WACC recalculation with debt-beta unlevering and relevering",
                    "Interest coverage ratio (EBITDA / Interest) sensitivity under recession",
                    "Compliance with debt covenant constraints and credit agency ratings",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "risk_discipline": 0.25, "decision_accuracy": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 4. CHIEF OPERATING OFFICER
    # -------------------------------------------------------------------------
    "coo": RoleCurriculum(
        role_id="coo",
        role_title="Chief Operating Officer",
        department="Operations",
        level=2,
        theoretical_foundations=[
            "Theory of Constraints & Synchronous Manufacturing (Goldratt 1984)",
            "Stochastic Queueing Theory & Little's Law (Little 1961)",
            "Toyota Production System & Lean Six Sigma (Ohno 1988, Womack et al. 1990)",
            "High Reliability Organizations & Normal Accidents Theory (Perrow 1984, Weick & Sutcliffe 2001)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Little's Law of Queueing",
                formula="L = lambda * W",
                latex=r"L = \lambda W",
                variables={"L": "Average number of items in system (WIP)", r"\lambda": "Average arrival / throughput rate", "W": "Average time an item spends in system (Lead time)"},
                application="Eliminating operational work-in-progress bottlenecks and optimizing service delivery velocity.",
            ),
            MathematicalFormulation(
                name="Kingman's Formula for Queue Waiting Time",
                formula="Wq ~= (rho / (1 - rho)) * ((ca^2 + cs^2) / 2) * tau",
                latex=r"W_q \approx \left(\frac{\rho}{1 - \rho}\right) \left(\frac{c_a^2 + c_s^2}{2}\right) \tau",
                variables={r"\rho": "System utilization rate", "c_a": "Coefficient of variation of arrivals", "c_s": "Coefficient of variation of service time", r"\tau": "Mean service time"},
                application="Proving non-linear escalation of operational latency as resource utilization approaches 100%.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="A Proof for the Queuing Formula: L = lambda W",
                authors="John D. C. Little",
                year=1961,
                venue="Operations Research",
                key_contribution="Mathematically proved the universal relationship between lead time, throughput, and work in progress.",
            ),
            LandmarkPaper(
                title="What Is the Right Supply Chain for Your Product?",
                authors="Marshall L. Fisher",
                year=1997,
                venue="Harvard Business Review",
                key_contribution="Classified products into functional vs innovative and mapped corresponding physically efficient vs market-responsive supply chains.",
            ),
        ],
        regulatory_and_industry_standards=[
            "ISO 9001:2015 (Quality Management Systems)",
            "ISO 22301 (Security and Resilience — Business Continuity Management Systems)",
            "SCOR (Supply Chain Operations Reference) Digital Standard",
        ],
        core_algorithms_and_methods=[
            "Drum-Buffer-Rope (DBR) Scheduling Heuristics",
            "Failure Modes and Effects Analysis (FMEA) with RPN Prioritization",
            "Single-Minute Exchange of Die (SMED) Setup Reduction",
        ],
        gold_medalist_playbook=[
            "Never balance capacity to demand; balance the flow of product through the constraint to market demand.",
            "An hour saved at a non-bottleneck is a total mirage; focus 100% of optimization energy on the primary constraint.",
            "Cap operational capacity utilization at 80-85% to avoid explosive Kingman queue latency degradation.",
            "Design redundant dual-sourcing architectures with zero single points of failure across critical operations.",
            "Institute strict Poka-Yoke (mistake-proofing) at every human and software handoff interface.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="coo_bs_001",
                title="Global Supply Chain Disruption: Critical Semiconductor Component Shortage",
                difficulty="Olympiad-Gold",
                context="A tier-1 hardware supplier suffers catastrophic fab shutdown; component lead time jumps from 4 to 36 weeks.",
                challenge="Re-architect enterprise fulfillment using buffer stock optimization, alternate qualifying protocols, and contract restructuring.",
                ground_truth_criteria=[
                    "Safety stock calculation using stochastic demand variance and lead-time volatility",
                    "Theory of Constraints application prioritizing highest margin-per-constraint-minute SKUs",
                    "Business continuity protocol execution preventing client SLA penalties",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "execution_reliability": 0.25, "risk_discipline": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 5. CHIEF TECHNOLOGY OFFICER
    # -------------------------------------------------------------------------
    "cto": RoleCurriculum(
        role_id="cto",
        role_title="Chief Technology Officer",
        department="Engineering",
        level=2,
        theoretical_foundations=[
            "Distributed Systems Consensus & Logical Clocks (Lamport 1978, Castro & Liskov 1999)",
            "CAP Theorem & PACELC Model (Brewer 2000, Abadi 2012)",
            "Information Theory & Error-Correcting Codes (Shannon 1948, Reed-Solomon 1960)",
            "Computational Complexity & Asymptotic Algorithmic Analysis (Cook 1971, Knuth 1968)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Gunther's Universal Scalability Law (USL)",
                formula="X(N) = (gamma * N) / (1 + sigma*(N - 1) + kappa*N*(N - 1))",
                latex=r"X(N) = \frac{\gamma N}{1 + \sigma(N - 1) + \kappa N(N - 1)}",
                variables={r"\gamma": "Concurrency scale factor", r"\sigma": "Contention coefficient (Amdahl)", r"\kappa": "Coherency crosstalk penalty (crosstalk)"},
                application="Predicting distributed cloud system throughput ceilings and retrograde performance under concurrency.",
            ),
            MathematicalFormulation(
                name="Byzantine Fault Tolerance Lower Bound",
                formula="N >= 3*f + 1",
                latex=r"N \ge 3f + 1",
                variables={"N": "Total consensus nodes in cluster", "f": "Maximum number of Byzantine faulty or malicious nodes"},
                application="Proving minimal node topology required for zero-trust distributed ledger and consensus protocols.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="Time, Clocks, and the Ordering of Events in a Distributed System",
                authors="Leslie Lamport",
                year=1978,
                venue="Communications of the ACM",
                key_contribution="Introduced logical clocks, state machines, and partial ordering in distributed computation (Turing Award).",
            ),
            LandmarkPaper(
                title="In Search of an Understandable Consensus Algorithm (Raft)",
                authors="Diego Ongaro, John Ousterhout",
                year=2014,
                venue="USENIX ATC",
                key_contribution="Designed the leader-based Raft distributed consensus protocol with formal safety and liveness proofs.",
            ),
        ],
        regulatory_and_industry_standards=[
            "NIST SP 800-53 Rev. 5 (Security and Privacy Controls for Information Systems)",
            "ISO/IEC 27001:2022 & SOC 2 Type II Trust Services Criteria",
            "NIST SP 800-207 (Zero Trust Architecture)",
            "RFC 8446 (TLS 1.3 Cryptographic Protocol)",
        ],
        core_algorithms_and_methods=[
            "Paxos & Raft State Machine Replication",
            "Consistent Hashing with Virtual Nodes (Karger et al.)",
            "Log-Structured Merge-Trees (LSM) & Bloom Filter Lookups",
        ],
        gold_medalist_playbook=[
            "Never assume the network is reliable, latency is zero, or bandwidth is infinite; design every remote call with circuit breakers.",
            "Data without cryptographic integrity verification is unverified rumor; enforce mutual TLS and cryptographically signed tokens.",
            "Keep core system architectures simple: complexity grows exponentially (O(N^2)) while debuggability drops catastrophically.",
            "Enforce strict SRE Error Budgets: if reliability drops below 99.99%, all non-critical feature deployments freeze immediately.",
            "Isolate failure domains with bulkheads to guarantee graceful degradation during cascading downstream outages.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="cto_bs_001",
                title="Zero-Downtime Distributed Consensus Migration Under High Transaction Load",
                difficulty="PhD-Comprehensive",
                context="The enterprise core transaction engine is processing 150,000 tx/sec with 4.5ms latency SLA on legacy database.",
                challenge="Architect a zero-downtime, bi-directional sync migration to a distributed Raft-replicated ledger with zero data loss (RPO=0, RTO<1s).",
                ground_truth_criteria=[
                    "Proof of serializability under partial network partitions",
                    "Dual-write shadow traffic verification with automated reconciliation",
                    "Failure domain containment preventing split-brain conditions",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "execution_reliability": 0.25, "risk_discipline": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 6. CHIEF MARKETING OFFICER
    # -------------------------------------------------------------------------
    "cmo": RoleCurriculum(
        role_id="cmo",
        role_title="Chief Marketing Officer",
        department="Marketing",
        level=2,
        theoretical_foundations=[
            "Empirical Laws of Marketing & Double Jeopardy Law (Sharp 2010)",
            "Customer-Based Brand Equity Model (Keller 1993)",
            "Econometric Marketing Mix Modeling & Adstock Decay Dynamics (Broadbent 1979)",
            "Behavioral Economics & Heuristics in Consumer Choice (Kahneman, Tversky 1984)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Customer Lifetime Value with BG/NBD Attrition",
                formula="E[CLV] = sum_{t=0}^inf (Margin * S(t)) / (1 + d)^t",
                latex=r"CLV = \sum_{t=0}^{\infty} \frac{M \cdot S(t)}{(1 + d)^t}",
                variables={"M": "Expected operating margin per period", "S(t)": "Survival probability under Beta-Geometric distribution", "d": "Discount rate"},
                application="Valuing customer cohorts and establishing rigorous Customer Acquisition Cost (CAC) ceiling thresholds.",
            ),
            MathematicalFormulation(
                name="Shapley Value Multi-Touch Attribution",
                formula="phi_i(v) = sum_{S subset N - {i}} [|S|! * (|N| - |S| - 1)! / |N|!] * [v(S U {i}) - v(S)]",
                latex=r"\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} (v(S \cup \{i\}) - v(S))",
                variables={"N": "All marketing touchpoint channels", "S": "Subsets of marketing interactions", "v(S)": "Conversion value created by subset S", r"\phi_i": "Marginal incremental attribution credit for channel i"},
                application="Mathematically fair allocation of multi-million dollar marketing budgets across search, display, content, and events.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="How Brands Grow: What Marketers Don't Know",
                authors="Byron Sharp",
                year=2010,
                venue="Oxford University Press",
                key_contribution="Proved that brand growth is driven by physical and mental availability to all category buyers, debunking narrow loyalty targeting.",
            ),
            LandmarkPaper(
                title="Conceptualizing, Measuring, and Managing Customer-Based Brand Equity",
                authors="Kevin Lane Keller",
                year=1993,
                venue="Journal of Marketing",
                key_contribution="Built the brand resonance pyramid from salience to imagery, judgments, feelings, and behavioral resonance.",
            ),
        ],
        regulatory_and_industry_standards=[
            "GDPR Article 6/7 & ePrivacy Directive (Consent for tracking)",
            "FTC Endorsement and Influencer Disclosure Guidelines (16 CFR Part 255)",
            "Interactive Advertising Bureau (IAB) OpenRTB 3.0 Standard",
        ],
        core_algorithms_and_methods=[
            "Bayesian Marketing Mix Modeling (PyMC / Prophet Adstock + Hill)",
            "Synthetic Control Geo-Lift Incrementality Testing",
            "Latent Dirichlet Allocation (LDA) for Market Sentiment Analysis",
        ],
        gold_medalist_playbook=[
            "Never measure marketing by vanity clicks or impressions; insist on verified incremental lift via randomized geo-holdout experiments.",
            "Invest at least 60% of budget into broad mental availability (brand salience) and 40% into activation to maximize 3-year ROI.",
            "Own the category definition: create a differentiated cognitive frame that turns competitors into legacy alternatives.",
            "Enforce strict privacy-first attribution architectures immune to third-party cookie deprecation.",
            "Kill low-performing channels immediately when customer acquisition cost exceeds 33% of 3-year LTV.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="cmo_bs_001",
                title="Category Creation Campaign for Enterprise Autonomous AI Defense",
                difficulty="Olympiad-Gold",
                context="Launching a revolutionary enterprise product into a crowded, noisy cybersecurity market with $10M launch budget.",
                challenge="Design an integrated brand positioning and demand generation engine that captures 25% SOV among Fortune 500 CISOs.",
                ground_truth_criteria=[
                    "Empirically validated mental availability playbook targeting category entry points (CEPs)",
                    "Econometric media mix model with geo-lift validation protocols",
                    "Full regulatory compliance with FTC and international data protection mandates",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "innovation": 0.25, "execution_reliability": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 7. CHIEF REVENUE OFFICER
    # -------------------------------------------------------------------------
    "cro": RoleCurriculum(
        role_id="cro",
        role_title="Chief Revenue Officer",
        department="Sales",
        level=2,
        theoretical_foundations=[
            "Principal-Agent Theory & Salesforce Compensation (Holmström 1979, Basu et al. 1985)",
            "B2B Buying Center Dynamics & Complex Negotiation (Webster & Wind 1972, Fisher & Ury 1981)",
            "Stochastic Pipeline Forecasting & Markov Chain Sales Cycles (Lilien et al. 1992)",
            "Value-Based Pricing & Economic Value to Customer (Nagle & Müller 2017)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Sales Velocity Equation",
                formula="Velocity = (N_deals * Win_Rate * Average_Deal_Size) / Sales_Cycle_Days",
                latex=r"V = \frac{N \times W \times \bar{S}}{T}",
                variables={"N": "Number of qualified pipeline opportunities", "W": "Win rate percentage", r"\bar{S}": "Average deal value ($)", "T": "Average sales cycle duration in days"},
                application="Quantifying daily revenue throughput generation and pinpointing operational sales friction.",
            ),
            MathematicalFormulation(
                name="Markov Chain Stage-Gate Win Probability",
                formula="P(Win | Stage_k) = P_{k, k+1} * P_{k+1, k+2} * ... * P_{n, Closed_Won}",
                latex=r"P(\text{Win} \mid S_k) = \prod_{i=k}^{n-1} P_{i, i+1}",
                variables={"S_k": "Current pipeline stage", "P_{i, i+1}": "Historical conditional transition probability between stage i and i+1"},
                application="Eliminating emotional sales rep bias and generating mathematically sound quarterly revenue forecasts.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="The Sales Acceleration Formula",
                authors="Mark Roberge",
                year=2015,
                venue="John Wiley & Sons",
                key_contribution="Engineered scientific hiring, training, quota management, and demand generation scaling from $0 to $100M ARR.",
            ),
            LandmarkPaper(
                title="The Challenger Sale: Taking Control of the Customer Conversation",
                authors="Matthew Dixon, Brent Adamson",
                year=2011,
                venue="Portfolio / Penguin",
                key_contribution="Empirically proved that top-performing enterprise reps teach for differentiation, tailor for resonance, and take control of price.",
            ),
        ],
        regulatory_and_industry_standards=[
            "ASC 606 Revenue from Contracts with Customers (Contract asset accounting)",
            "Foreign Corrupt Practices Act (FCPA) / UK Bribery Act compliance",
            "Export Administration Regulations (EAR) on software licensing",
        ],
        core_algorithms_and_methods=[
            "MEDDPICC Deal Qualification Scoring Algorithm",
            "Monte Carlo Quota Attainment & Pipeline Coverage Simulation (3.5x - 4.0x benchmark)",
            "Contract Value-to-Risk Matrix for Multi-Year MSA Redlines",
        ],
        gold_medalist_playbook=[
            "Inspect what you expect: never accept an opportunity forecast without an identified Economic Buyer and confirmed Decision Process.",
            "Enforce MEDDPICC relentlessly: disqualify unpromising deals early to preserve rep capacity for high-probability enterprise whales.",
            "Structure commission incentives with steep accelerators (>120% quota) and clawbacks for churn within 12 months.",
            "Build multi-threaded relationships across executive, technical, and procurement buyer personas to prevent single-champion deal collapse.",
            "Establish strict discount authority matrices: zero unilateral price concessions without verified quid-pro-quo commercial terms.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="cro_bs_001",
                title="$50M Global Enterprise Deal: Closing Against Aggressive Incumbent",
                difficulty="PhD-Comprehensive",
                context="Negotiating a multi-year global software deployment with a tier-1 multinational bank facing predatory discounts from incumbent.",
                challenge="Structure a compelling MEDDPICC strategy, mutual action plan (MAP), and non-discount commercial concession structure.",
                ground_truth_criteria=[
                    "Quantified TCO and Economic Value to Customer (EVC) model demonstrating $120M net return",
                    "Mutual Action Plan with hard milestones aligned to client board fiscal deadlines",
                    "ASC 606 compliance review ensuring upfront software vs deferred service recognition",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "decision_accuracy": 0.25, "collaboration": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 8. CHIEF HUMAN RESOURCES OFFICER
    # -------------------------------------------------------------------------
    "chro": RoleCurriculum(
        role_id="chro",
        role_title="Chief Human Resources Officer",
        department="People",
        level=2,
        theoretical_foundations=[
            "Human Capital Theory & Endogenous Growth (Becker 1964, Schultz 1961)",
            "Job Characteristics Model & Work Motivation (Hackman & Oldham 1976)",
            "Organizational Network Analysis & Social Capital (Burt 1992, Granovetter 1973)",
            "Psychometrics & Predictive Validity of Selection Procedures (Schmidt & Hunter 1998)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Brogden-Cronbach-Gleser Utility Analysis",
                formula="Delta_U = N * T * r_xy * Z_x * SD_y - C",
                latex=r"\Delta U = N \cdot T \cdot r_{xy} \cdot Z_x \cdot SD_y - C",
                variables={"N": "Number of candidates selected", "T": "Average tenure in years", "r_xy": "Validity coefficient of selection instrument", "Z_x": "Mean test score of selected applicants in standard deviation units", "SD_y": "Standard deviation of job performance in monetary value", "C": "Cost of testing"},
                application="Mathematically proving the multi-million dollar corporate ROI of elite cognitive and structured hiring processes.",
            ),
            MathematicalFormulation(
                name="Kaplan-Meier Survival Estimator for Employee Retention",
                formula="S(t) = prod_{t_i <= t} [1 - d_i / n_i]",
                latex=r"\hat{S}(t) = \prod_{t_i \le t} \left(1 - \frac{d_i}{n_i}\right)",
                variables={"t_i": "Tenure intervals", "d_i": "Number of departures at time t_i", "n_i": "Number of active employees at risk just prior to t_i"},
                application="Predicting executive and engineering cohort retention curves and modeling targeted stock vesting intervals.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="The Validity and Utility of Selection Methods in Personnel Psychology",
                authors="Frank L. Schmidt, John E. Hunter",
                year=1998,
                venue="Psychological Bulletin",
                key_contribution="Meta-analyzed 85 years of research showing structured interviews and general cognitive ability have highest predictive validity.",
            ),
            LandmarkPaper(
                title="Psychological Safety and Learning Behavior in Work Teams",
                authors="Amy Edmondson",
                year=1999,
                venue="Administrative Science Quarterly",
                key_contribution="Demonstrated that psychological safety is the foundation of high-performing, error-correcting team cultures.",
            ),
        ],
        regulatory_and_industry_standards=[
            "Title VII of the Civil Rights Act of 1964 & EEOC Uniform Guidelines on Employee Selection",
            "Fair Labor Standards Act (FLSA) Exempt vs Non-Exempt Classifications",
            "National Labor Relations Act (NLRA) & OSHA Workplace Standards",
            "EU Corporate Sustainability Due Diligence Directive (CSDDD)",
        ],
        core_algorithms_and_methods=[
            "Organizational Network Betweenness Centrality Algorithms",
            "Total Rewards Black-Scholes Option Compensation Structuring",
            "Structured Multi-Rater 360 Psychometric Calibration Panels",
        ],
        gold_medalist_playbook=[
            "Talent quality is non-linear: an exceptional engineer or executive generates 10x-50x enterprise impact; never compromise on the hiring bar.",
            "Eliminate unstructured casual interviews completely; mandate standardized behavioral questions with anchored grading rubrics.",
            "Audit team psychological safety regularly: teams where members fear reporting errors produce catastrophic organizational blind spots.",
            "Design equity compensation packages that reward long-term enterprise value creation while preventing short-term mercenary behavior.",
            "Enforce rigorous succession planning with at least two qualified internal successor candidates for every mission-critical role.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="chro_bs_001",
                title="Enterprise Cultural Re-Engineering During Post-Merger Integration",
                difficulty="PhD-Comprehensive",
                context="AegisCorp has acquired a 1,200-person international company with conflicting cultural norms and high turnover risks.",
                challenge="Formulate a comprehensive human capital retention, talent calibration, and organizational alignment strategy over 180 days.",
                ground_truth_criteria=[
                    "Organizational Network Analysis to detect and retain critical knowledge brokers",
                    "Total rewards re-alignment with equity lockups and performance milestones",
                    "EEOC and international labor law compliance across all affected jurisdictions",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "collaboration": 0.25, "risk_discipline": 0.25},
            )
        ],
    ),

    # -------------------------------------------------------------------------
    # 9. CHIEF PRODUCT OFFICER
    # -------------------------------------------------------------------------
    "cpo": RoleCurriculum(
        role_id="cpo",
        role_title="Chief Product Officer",
        department="Product",
        level=2,
        theoretical_foundations=[
            "Jobs-to-be-Done Theory & Outcome-Driven Innovation (Christensen 2016, Ulwick 2005)",
            "Controlled Online Experimentation & Multi-Armed Bandits (Kohavi et al. 2020, Robbins 1952)",
            "Behavioral Design & Habit Formation (Fogg 2009, Eyal 2014)",
            "Kano Model of Customer Satisfaction & Feature Utility (Kano 1984)",
        ],
        mathematical_formulations=[
            MathematicalFormulation(
                name="Two-Sample Hypothesis Testing Sample Size for A/B Testing",
                formula="n = 2 * (Z_alpha/2 + Z_beta)^2 * sigma^2 / delta^2",
                latex=r"n = \frac{2(Z_{\alpha/2} + Z_\beta)^2 \sigma^2}{\delta^2}",
                variables={"Z_{alpha/2}": "Critical value for significance level alpha", "Z_beta": "Critical value for statistical power 1 - beta", r"\sigma^2": "Variance of the metric", r"\delta": "Minimum detectable effect (MDE)"},
                application="Determining statistically rigorous sample sizes to avoid false positive product feature ship decisions.",
            ),
            MathematicalFormulation(
                name="Upper Confidence Bound (UCB1) Multi-Armed Bandit",
                formula="UCB_i = mu_hat_i + sqrt(2 * ln(t) / N_i(t))",
                latex=r"UCB_i = \hat{\mu}_i + \sqrt{\frac{2 \ln t}{N_i(t)}}",
                variables={r"\hat{\mu}_i": "Empirical average reward of feature variant i", "t": "Total feature exposures", "N_i(t)": "Number of times variant i was served"},
                application="Dynamically balancing exploration of new feature variations with exploitation of top-converting UI experiences.",
            ),
        ],
        landmark_papers=[
            LandmarkPaper(
                title="Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing",
                authors="Ron Kohavi, Diane Tang, Ya Xu",
                year=2020,
                venue="Cambridge University Press",
                key_contribution="Documented statistical pitfalls, Twyman's law, and institutional experimentation platforms used by elite tech firms.",
            ),
            LandmarkPaper(
                title="Inspired: How to Create Tech Products Customers Love",
                authors="Marty Cagan",
                year=2017,
                venue="John Wiley & Sons",
                key_contribution="Formalized product discovery, empowered product teams, and the four essential product risks (value, usability, feasibility, viability).",
            ),
        ],
        regulatory_and_industry_standards=[
            "WCAG 2.2 (Web Content Accessibility Guidelines Level AAA)",
            "ISO 9241-210 (Human-centred design for interactive systems)",
            "COPPA / GDPR Article 8 (Protection of minors in digital products)",
        ],
        core_algorithms_and_methods=[
            "Sequential Probability Ratio Test (Wald's SPRT) for Early Experiment Stopping",
            "Opportunity Solution Tree Mapping & Continuous Discovery (Torres)",
            "Rice & WSJF (Weighted Shortest Job First) Quantitative Prioritization",
        ],
        gold_medalist_playbook=[
            "Fall in love with the problem, never with the specific software solution.",
            "De-risk all four risks (Value, Usability, Feasibility, Viability) BEFORE building a single production line of code.",
            "Twyman's Law applies universally: any metric that looks surprisingly good or bad is usually the result of instrumentation error.",
            "Focus on the 'Core Action' and minimize Time-to-Value (TTV) to under 60 seconds for new enterprise onboarding.",
            "Falsification mindset: design the quickest, cheapest experiment specifically crafted to prove your pet hypothesis wrong.",
        ],
        benchmark_scenarios=[
            BenchmarkScenario(
                scenario_id="cpo_bs_001",
                title="Enterprise Platform Redesign: Resolving Churn in Multi-Tenant Workspaces",
                difficulty="PhD-Comprehensive",
                context="Enterprise workspace 90-day retention has eroded from 74% to 58% following a major cloud feature release.",
                challenge="Formulate an evidence-based product turnaround plan using user telemetry, cohort funnel analysis, and prioritized MVP remediations.",
                ground_truth_criteria=[
                    "Quantitative churn cohort survival decomposition isolating UX drop-off friction",
                    "Rigorous A/B testing plan with power calculation and guardrail metrics",
                    "Cross-functional alignment across Engineering feasibility and GTM sales messaging",
                ],
                rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "innovation": 0.25, "decision_accuracy": 0.25},
            )
        ],
    ),
}


# =============================================================================
# HELPER CURRICULUM FACTORY FOR DEPARTMENTAL LADDERS
# =============================================================================

def _build_engineering_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 8 Engineering ladder roles."""
    eng_roles = {
        "vp_eng": (
            "VP of Engineering", 3,
            ["Conway's Law & Socio-Technical Systems (Conway 1968)", "Engineering Economics & Capital Efficiency", "Accelerate DORA Metrics & DevOps Transformation (Forsgren et al. 2018)"],
            "DORA Deployment Frequency & MTTR Optimization: lambda_dep / T_recovery",
            "DORA Team Topology Alignment under Amdahl Contention Limits",
            "NIST SP 800-218 (Secure Software Development Framework)",
            ["Organizational Graph Optimization", "Multi-Project Critical Chain Buffering"],
            ["Align organizational structure directly to service boundary architecture.", "Enforce automated CI/CD gating: zero human manual deployments in production."],
            "vp_eng_bs_001", "Scaling 450-Engineer Org Through 5x Headcount Surge Without Delivery Stagnation"
        ),
        "director_eng": (
            "Director of Engineering", 4,
            ["Service-Oriented Architecture & Domain-Driven Design (Evans 2003)", "Capacity Planning & Queueing under Bursty Traffic", "Blameless Incident Management & Cognitive Ergonomics"],
            "Capacity Sizing with Erlang-C Loss Formula: P_wait = C(A, N)",
            "Erlang-C Multi-Server Sizing for High-Throughput Request Handlers",
            "SOC 2 Type II Security Controls & Audit Evidence Systems",
            ["Critical Path Method (CPM) with Slack Tracking", "Service Dependency Graph Cycle Elimination"],
            ["Never allow circular dependencies between engineering microservices.", "Insist on automated canary rollback triggers tied to latency P99."],
            "dir_eng_bs_001", "Cross-Service Latency Spike Remediation Across 12 Mission-Critical Microservices"
        ),
        "sr_eng_mgr": (
            "Senior Engineering Manager", 5,
            ["Psychological Safety & High-Velocity Team Dynamics (Edmondson)", "Technical Debt Quantification & Refactoring ROI (Fowler)", "Sprint Burndown Stochastic Modeling"],
            "Technical Debt Interest Accumulation: Debt(t) = Debt_0 * (1 + r)^t",
            "Net Present Value (NPV) Refactoring ROI Justification Formula",
            "IEEE 1044 Standard for Software Anomalies",
            ["Agile Velocity Moving Averages", "Skill Matrix Cross-Training Balance"],
            ["Dedicate a non-negotiable 20% of every sprint to paying down foundational technical debt.", "Coach engineers toward autonomy rather than micro-managing implementation."],
            "sem_eng_bs_001", "Remediating a High-Attrition, Burnout-Plagued Infrastructure Team"
        ),
        "eng_mgr": (
            "Engineering Manager", 5,
            ["Agile Scrum & Kanban Continuous Flow", "Cognitive Load Theory in Software Maintenance (Sweller 1988)", "Conflict Resolution & 1:1 Coaching Playbooks"],
            "Cumulative Flow Diagram (CFD) WIP Variance: WIP(t) = Arrivals - Departures",
            "Little's Law for Sprint Cycle Time Predictability",
            "ISO/IEC 25010 Software Product Quality",
            ["Kanban WIP Limit Enforcement", "Blameless Postmortem Facilitation"],
            ["Protect team focus by aggressively filtering out unplanned executive pet requests.", "Foster blameless postmortems where root causes are traced to systemic design gaps."],
            "em_eng_bs_001", "Transforming Sprint Delivery Predictability From 42% to 90% in 90 Days"
        ),
        "tech_lead": (
            "Technical Lead", 5,
            ["Distributed Consensus & Idempotency Patterns", "Relational Database ACID vs NoSQL BASE Trade-offs", "API Contract Versioning & Backward Compatibility (Hyrum's Law)"],
            "CAP / PACELC Architectural Evaluation: Availability vs Consistency under Network Partition",
            "Two-Phase Commit vs Saga Pattern Distributed Compensating Transactions",
            "OpenAPI 3.1 & Protocol Buffers Specification",
            ["Saga Orchestration with Compensation Rollback", "Database B-Tree Index Selectivity Tuning"],
            ["Every external mutation API must enforce distributed idempotency keys.", "Avoid distributed transactions when event-driven eventual consistency suffices."],
            "tl_eng_bs_001", "Designing Distributed Payment Processing Engine with Guaranteed Exactly-Once Semantics"
        ),
        "sr_swe": (
            "Senior Software Engineer", 6,
            ["Memory Management, Cache Locality & Hardware Prefetching", "Lock-Free Data Structures & CAS Primitives (Herlihy 1991)", "Advanced Test-Driven Development & Mutation Testing"],
            "Amdahl's Law for Multithreaded Core Scaling: S = 1 / ( (1 - p) + p/s )",
            "Lock-Free Ring Buffer CAS Enqueue/Dequeue Invariant Proofs",
            "OWASP Top 10 Enterprise Application Security Verification Standard (ASVS)",
            ["Deterministic Finite Automaton (DFA) Parsing", "Cache-Conscious Data Layout Optimization"],
            ["Write code for human readers first and the compiler second.", "Profile before optimizing; intuitive performance guesses are almost always wrong."],
            "sr_swe_bs_001", "Optimizing a CPU-Bound Serialization Bottleneck from 450ms to 4.2ms"
        ),
        "swe": (
            "Software Engineer", 6,
            ["SOLID Object-Oriented Principles & Clean Architecture (Martin)", "Relational Database Schema Normalization (3NF/BCNF)", "Asynchronous Event Loops & Non-Blocking I/O"],
            "Database Normalization Invariance & Functional Dependency Decomposition",
            "Big-O Algorithmic Space and Time Complexity Analysis",
            "Semantic Versioning 2.0.0 & RFC 7231 (HTTP Semantics)",
            ["Binary Search & Graph Traversal (Dijkstra/A*)", "Structured Unit and Mock Testing"],
            ["Never push code without corresponding automated unit and integration tests.", "Validate all input boundaries; never trust client-provided payloads."],
            "swe_bs_001", "Building a Highly Concurrent In-Memory Rate Limiter with Sliding Window Counter"
        ),
        "junior_eng": (
            "Junior Software Engineer", 6,
            ["Core Data Structures (Hash Tables, Heaps, Balanced Trees)", "Version Control Hygiene & Git Flow Standards", "Defensive Programming & Exception Handling"],
            "Hash Table Collision Probability (Birthday Problem): P(collision) ~= 1 - e^(-n^2 / 2m)",
            "Recursion Stack Depth and Memory Allocation Bounds",
            "PEP 8 / Google Style Guide Programming Standards",
            ["QuickSort & MergeSort Invariants", "Git Branching, Rebase and Clean PR Authoring"],
            ["Ask questions when blocked for more than 30 minutes; do not suffer in silence.", "Read the existing codebase patterns thoroughly before introducing novel libraries."],
            "je_eng_bs_001", "Refactoring a Monolithic 1,500-line Script into Modular Tested Components"
        ),
    }

    res = {}
    for role_id, (title, level, foundations, form_name, form_formula, std, algos, playbook, sc_id, sc_title) in eng_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="Engineering",
            level=level,
            theoretical_foundations=foundations,
            mathematical_formulations=[
                MathematicalFormulation(
                    name=form_name,
                    formula=form_formula,
                    latex=rf"\text{{{form_name}}}",
                    variables={"x": "System state variable", "y": "Performance metric"},
                    application="Rigorous quantitative engineering design and capacity optimization.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="Accelerate: The Science of Lean Software and DevOps",
                    authors="Nicole Forsgren, Jez Humble, Gene Kim",
                    year=2018,
                    venue="IT Revolution Press",
                    key_contribution="Scientifically proved that software delivery velocity and organizational stability are mutually reinforcing.",
                )
            ],
            regulatory_and_industry_standards=[std, "ISO/IEC 27001 Software Lifecycle Security"],
            core_algorithms_and_methods=algos,
            gold_medalist_playbook=playbook,
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"Real-world enterprise scenario testing core responsibilities of {title}.",
                    challenge="Design and execute a comprehensive technical solution adhering to engineering best practices.",
                    ground_truth_criteria=["Architectural soundness", "Mathematical rigor", "Zero regressions in existing test suite"],
                    rubric_weights={"domain_mastery": 0.30, "reasoning_quality": 0.25, "execution_reliability": 0.25, "risk_discipline": 0.20},
                )
            ],
        )
    return res


def _build_product_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 6 Product ladder roles."""
    prod_roles = {
        "vp_prod": ("VP of Product", 3, ["Portfolio Management & S-Curve Innovation", "Strategic Positioning & Market Opportunity Sizing"], "Portfolio R&D Expected Value: EV = sum(p_i * NPV_i)", "Product Portfolio Frontier Optimization", "vp_prod_bs_001", "Pruning 4 Underperforming Enterprise Product Lines to Fund Strategic AI Bet"),
        "director_prod": ("Director of Product", 4, ["Multi-Product Roadmapping & Inter-Team Dependencies", "Value Proposition Design & Pricing Packaging"], "Van Westendorp Price Sensitivity Meter: Optimal Price Point (OPP)", "Pricing Optimization Curve Analysis", "dir_prod_bs_001", "Consolidating 3 Disjointed SaaS Products into a Unified Enterprise Suite"),
        "gpm": ("Group Product Manager", 4, ["Outcome-Driven Product OKRs & Team Alignment", "Continuous Discovery & User Research Synthesis"], "RICE Prioritization Index: Score = (Reach * Impact * Confidence) / Effort", "RICE Quantitative Feature Scoring", "gpm_bs_001", "Orchestrating Cross-Team Collaboration for Core Workspace Collaboration Experience"),
        "sr_pm": ("Senior Product Manager", 5, ["Customer Problem Definition & PRD Authorship", "Quantitative Funnel Analytics & Retention Cohorts"], "Cohort Retention Decay Curve: R(t) = R_0 * t^(-alpha)", "Power-Law Retention Modeling", "sr_pm_bs_001", "Drafting High-Precision PRD for Multi-Tenant Enterprise Role-Based Access Control"),
        "pm": ("Product Manager", 5, ["User Story Mapping & Backlog Prioritization", "Scrum Acceptance Criteria & Release Notes"], "Weighted Shortest Job First (WSJF): Cost of Delay / Job Duration", "WSJF Backlog Prioritization Algorithm", "pm_bs_001", "Triaging Complex Technical Bug Backlog vs Competitive Feature Commitments"),
        "apm": ("Associate Product Manager", 6, ["User Telemetry Analysis & Bug Prioritization", "Competitive Product Benchmarking & Wireframing"], "Net Promoter Score (NPS) Variance: NPS = %Promoters - %Detractors", "NPS Statistical Margin of Error Calculation", "apm_bs_001", "Conducting End-to-End Usability Audit of Mobile Client Onboarding Flow"),
    }

    res = {}
    for role_id, (title, level, foundations, form_name, form_formula, sc_id, sc_title) in prod_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="Product",
            level=level,
            theoretical_foundations=foundations + ["Jobs-to-be-Done Framework", "Behavioral Economics in Feature Adoption"],
            mathematical_formulations=[
                MathematicalFormulation(
                    name=form_name,
                    formula=form_formula,
                    latex=rf"\text{{{form_name}}}",
                    variables={"R": "Reach", "I": "Impact", "C": "Confidence", "E": "Effort"},
                    application="Quantitative decision science for product roadmaps.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="The Innovator's Solution",
                    authors="Clayton M. Christensen, Michael E. Raynor",
                    year=2003,
                    venue="Harvard Business School Press",
                    key_contribution="Outlined how to build disruptive growth businesses systematically using Jobs-to-be-Done.",
                )
            ],
            regulatory_and_industry_standards=["WCAG 2.2 Accessibility", "GDPR Article 25 (Data Protection by Design)"],
            core_algorithms_and_methods=["Cohort Retention Analysis", "Opportunity-Solution Tree Mapping", "User Journey Flowcharting"],
            gold_medalist_playbook=[
                "Define the problem in customer language before specifying any technical UI solution.",
                "Every feature proposal must state an upfront measurable success metric and a sunset criterion.",
                "Talk directly to at least five genuine enterprise users every week.",
            ],
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"Enterprise product challenge for {title}.",
                    challenge="Synthesize customer evidence, define specifications, and deliver structured recommendation.",
                    ground_truth_criteria=["Clear problem validation", "Quantified business impact", "Actionable acceptance criteria"],
                    rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "evidence_quality": 0.25, "decision_accuracy": 0.25},
                )
            ],
        )
    return res


def _build_sales_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 5 Sales ladder roles."""
    sales_roles = {
        "reg_sales_dir": ("Regional Sales Director", 3, ["Territory Optimization & Capacity Modeling", "Board-Level Revenue Forecasting"], "Territory Yield Index: Yield = sum(Rep_Capacity * Market_Density)", "reg_sales_dir_bs_001", "Allocating $120M Regional Quota Across 24 Enterprise Sales Reps"),
        "sales_mgr": ("Sales Manager", 4, ["Pipeline Inspection & Deal Slippage Prevention", "Sales Rep Coaching & Performance Remediation"], "Pipeline Health Ratio: Coverage = Active_Pipeline / Remaining_Quarterly_Quota", "sales_mgr_bs_001", "Rescuing a Stalled $4.5M Strategic Enterprise Account 10 Days Before Quarter End"),
        "sales_team_lead": ("Sales Team Lead", 5, ["Real-Time Deal Desk Negotiation", "Sales Playbook Adherence & Shadow Calls"], "Win-Loss Logistic Odds Ratio: ln(p / (1-p)) = beta_0 + beta_1*Price + beta_2*Competitor", "sales_tl_bs_001", "Coaching Mid-Level AE Through Hardball Procurement Negotiation with Tier-1 Bank"),
        "ae": ("Account Executive", 6, ["MEDDPICC Enterprise Deal Qualification", "Executive Multi-Threading & Mutual Action Plans"], "Economic Value to Customer (EVC): EVC = Reference_Value + Differentiation_Value", "ae_bs_001", "Qualifying and Closing a $1.2M ACV Deal with Fortune 100 Manufacturing Giant"),
        "sdr": ("Sales Development Representative", 6, ["ICP Account Sourcing & High-Conversion Outbound", "Multi-Channel Cadence Optimization"], "SDR Cadence Conversion Velocity: Conv_Rate = SQLs / Touched_Accounts", "sdr_bs_001", "Crafting High-Converting Personalized Outbound Campaign to 50 F500 CISO Targets"),
    }

    res = {}
    for role_id, (title, level, foundations, formula, sc_id, sc_title) in sales_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="Sales",
            level=level,
            theoretical_foundations=foundations + ["Principal-Agent Theory in Compensation", "Behavioral Persuasion (Cialdini)"],
            mathematical_formulations=[
                MathematicalFormulation(
                    name="Sales Velocity Equation",
                    formula="V = (N * W * Size) / Cycle_Days",
                    latex=r"V = \frac{N \times W \times \bar{S}}{T}",
                    variables={"N": "Opportunities", "W": "Win Rate", "Size": "Deal Size", "Cycle_Days": "Cycle Length"},
                    application="Calculating enterprise deal throughput.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="The Challenger Sale",
                    authors="Matthew Dixon, Brent Adamson",
                    year=2011,
                    venue="Portfolio",
                    key_contribution="Proved that teaching commercial insights outperforms relationship-building in enterprise deals.",
                )
            ],
            regulatory_and_industry_standards=["FCPA Anti-Bribery Compliance", "ASC 606 Contract Revenue Accounting"],
            core_algorithms_and_methods=["MEDDPICC Deal Scoring", "Markov Pipeline Funnel Transition Analysis"],
            gold_medalist_playbook=[
                "Disqualify bad deals quickly; sales rep time is the most expensive perishible asset in the enterprise.",
                "Never send a contract without securing a Mutual Action Plan signed by the true Economic Buyer.",
                "Maintain at least 3.5x pipeline coverage for every dollar of assigned quota.",
            ],
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"High-stakes enterprise sales scenario for {title}.",
                    challenge="Apply MEDDPICC, navigate procurement objections, and secure signed commitment.",
                    ground_truth_criteria=["Accurate buyer qualification", "Compelling ROI proof", "Strict adherence to legal discounting policies"],
                    rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "execution_reliability": 0.25, "decision_accuracy": 0.25},
                )
            ],
        )
    return res


def _build_marketing_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 5 Marketing ladder roles."""
    mktg_roles = {
        "vp_mktg": ("VP of Marketing", 3, ["Global Brand Positioning & Market Category Creation", "Omnichannel Econometric Media Mix Optimization"], "Marketing Capital Allocation Frontier: max Return s.t. Budget_i <= Cap_i", "vp_mktg_bs_001", "Re-allocating $40M Global Marketing Budget Across Brand Salience and Performance Activation"),
        "director_mktg": ("Director of Marketing", 4, ["Demand Generation Funnels & Account-Based Marketing", "Analyst Relations (Gartner / Forrester Waves)"], "CAC Payback Period: Payback = CAC / (ARPU * Gross_Margin)", "dir_mktg_bs_001", "Positioning AegisCorp as a Leader in the Gartner Magic Quadrant for Enterprise AI Governance"),
        "mktg_mgr": ("Marketing Manager", 5, ["Integrated Product Launches & Multi-Touch Attribution", "Event ROI & Customer Community Architecture"], "Incremental ROAS: iROAS = (Rev_Test - Rev_Control) / Spend_Test", "mktg_mgr_bs_001", "Executing Global Virtual Summit Generating 12,000 Qualified Enterprise Registrants"),
        "mktg_spec": ("Marketing Specialist", 6, ["Quantitative SEO/SEM & Conversion Rate Optimization (CRO)", "High-Impact Copywriting & Behavioral Nudges"], "Landing Page CRO Conversion Rate: CR = Conversions / Total_Visitors", "mktg_spec_bs_001", "Designing High-Intent Search Campaign Achieving Sub-$120 Enterprise MQL Acquisition Cost"),
        "mktg_coord": ("Marketing Coordinator", 6, ["Campaign Asset Governance & Social Scheduling", "Webinar Logistics & Lead Routing Automation"], "Lead Routing Velocity: T_route = Arrival_Time - CRM_Assignment_Time", "mktg_coord_bs_001", "Auditing and Fixing Broken HubSpot-to-Salesforce Lead Hand-off Pipeline"),
    }

    res = {}
    for role_id, (title, level, foundations, formula, sc_id, sc_title) in mktg_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="Marketing",
            level=level,
            theoretical_foundations=foundations + ["How Brands Grow (Byron Sharp)", "Shapley Attribution Theory"],
            mathematical_formulations=[
                MathematicalFormulation(
                    name="Customer Acquisition Cost (CAC)",
                    formula="CAC = (Total_Sales_and_Marketing_Cost) / (New_Customers_Acquired)",
                    latex=r"CAC = \frac{\sum \text{Cost}_{S\&M}}{N_{\text{new}}}",
                    variables={"Cost": "Total marketing and sales expense", "N": "Count of new paying enterprise logos"},
                    application="Tracking unit economic acquisition health.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="How Brands Grow",
                    authors="Byron Sharp",
                    year=2010,
                    venue="Oxford University Press",
                    key_contribution="Documented empirical laws of mental availability and brand penetration.",
                )
            ],
            regulatory_and_industry_standards=["GDPR / CCPA Cookie Consent Directives", "CAN-SPAM Act Marketing Compliance"],
            core_algorithms_and_methods=["Bayesian Marketing Mix Modeling", "Geo-Lift Incrementality Testing"],
            gold_medalist_playbook=[
                "Never optimize for vanity clicks; demand evidence of verified incremental pipeline creation.",
                "Ensure strong visual and message consistency across every touchpoint to build cognitive category salience.",
                "Always pair paid acquisition with an organic brand equity flywheel.",
            ],
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"Marketing leadership scenario for {title}.",
                    challenge="Design, calculate, and implement a data-driven marketing strategy.",
                    ground_truth_criteria=["Incrementality focus", "Clear unit economics", "Regulatory compliance"],
                    rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "innovation": 0.25, "execution_reliability": 0.25},
                )
            ],
        )
    return res


def _build_finance_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 5 Finance ladder roles."""
    fin_roles = {
        "vp_fin": ("VP of Finance", 3, ["Strategic Corporate FP&A & Capital Structure", "Debt Financing & Credit Rating Agency Defense"], "Interest Coverage Ratio: ICR = EBITDA / Interest_Expense", "vp_fin_bs_001", "Structuring a $150M Syndicated Revolving Credit Facility with Minimal Covenant Restrictions"),
        "fin_dir": ("Finance Director", 4, ["Controller-Level Accounting Governance & Month-End Close", "ASC 606 Multi-Element Revenue Allocation"], "Days Sales Outstanding: DSO = (Accounts_Receivable / Total_Credit_Sales) * Days", "fin_dir_bs_001", "Compressing Enterprise Month-End Financial Close Cycle from 14 Days to 3 Business Days"),
        "fin_mgr": ("Finance Manager", 5, ["Departmental OPEX/CAPEX Variance Decomposition", "Headcount Cost & Compensation Band Modeling"], "Budget Variance Percentage: Variance = (Actual - Budget) / Budget", "fin_mgr_bs_001", "Conducting Rigorous Q3 P&L Variance Audit Identifying $3.2M in Redundant Cloud OPEX"),
        "sr_fin_analyst": ("Senior Financial Analyst", 5, ["3-Statement Integrated Financial Modeling (IS/BS/CF)", "DCF Sensitivity Tables & Scenario Forecasting"], "Discounted Cash Flow: Enterprise_Value = sum(FCFF_t / (1 + WACC)^t) + Terminal_Value", "sr_fin_analyst_bs_001", "Building Auditable 5-Year Integrated LBO Model for Potential $85M Bolt-on Acquisition"),
        "fin_analyst": ("Financial Analyst", 6, ["Journal Entry Reconciliation & Working Capital Audits", "Accounts Payable / Receivable Ledger Accuracy"], "Working Capital Ratio: Current_Ratio = Current_Assets / Current_Liabilities", "fin_analyst_bs_001", "Reconciling 10,000 Unmatched Multi-Currency Wire Transactions Across 4 Global Entities"),
    }

    res = {}
    for role_id, (title, level, foundations, formula, sc_id, sc_title) in fin_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="Finance",
            level=level,
            theoretical_foundations=foundations + ["Modigliani-Miller Theorem", "DuPont Analysis"],
            mathematical_formulations=[
                MathematicalFormulation(
                    name="Unlevered Free Cash Flow (FCFF)",
                    formula="FCFF = EBIT * (1 - T) + D&A - Capex - Delta_NWC",
                    latex=r"\text{FCFF} = \text{EBIT}(1 - T) + \text{D\&A} - \text{CapEx} - \Delta\text{NWC}",
                    variables={"EBIT": "Operating profit", "T": "Tax rate", "Capex": "Capital expenditure", "NWC": "Net working capital"},
                    application="Calculating true operating cash generation for enterprise valuation.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="The Capital Structure Puzzle",
                    authors="Stewart C. Myers",
                    year=1984,
                    venue="The Journal of Finance",
                    key_contribution="Analyzed the tension between trade-off theory and pecking-order theory in corporate finance.",
                )
            ],
            regulatory_and_industry_standards=["US GAAP / IFRS", "SOX Section 404 Financial Reporting Internal Controls"],
            core_algorithms_and_methods=["Monte Carlo Financial Modeling", "3-Statement Dynamic Linking Algorithms"],
            gold_medalist_playbook=[
                "Every financial model must tie cash flow directly to balance sheet liquidity; never rely on net income alone.",
                "Enforce dual-signoff authorization on all outbound disbursements exceeding $50,000.",
                "Stress-test forecasts under worst-case liquidity drawdown assumptions.",
            ],
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"Finance and treasury challenge for {title}.",
                    challenge="Analyze financial records, build quantitative projections, and provide auditable advice.",
                    ground_truth_criteria=["Mathematical precision", "GAAP compliance", "Clear variance reconciliation"],
                    rubric_weights={"domain_mastery": 0.30, "reasoning_quality": 0.25, "risk_discipline": 0.25, "decision_accuracy": 0.20},
                )
            ],
        )
    return res


def _build_operations_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 5 Operations ladder roles."""
    ops_roles = {
        "vp_ops": ("VP of Operations", 3, ["Global Enterprise Operating Models & Facilities Scalability", "Strategic Procurement & Business Continuity Architecture"], "Overall Equipment Effectiveness: OEE = Availability * Performance * Quality", "vp_ops_bs_001", "Designing Resilient Multi-Region Cloud and Data Center Colocation Strategy"),
        "ops_dir": ("Operations Director", 4, ["Logistics & Vendor SLA Governance", "Enterprise IT Infrastructure & Security Policies"], "Vendor SLA Non-Performance Penalty Matrix: Penalty = sum(Breach_Duration * Severity_Rate)", "dir_ops_bs_001", "Negotiating Enterprise Master Services Agreement with Global Cloud Provider Saving 28%"),
        "ops_mgr": ("Operations Manager", 5, ["Cross-Departmental Workflow Automation", "Resource Capacity Allocation & Queue Latency"], "Cycle Time Efficiency: Efficiency = Value_Add_Time / Total_Lead_Time", "ops_mgr_bs_001", "Automating End-to-End Employee Hardware Provisioning and Deprovisioning Lifecycle"),
        "ops_sup": ("Operations Supervisor", 5, ["Shift Scheduling & Daily Queue Throughput", "SOP Standard Operating Procedure Compliance Audits"], "Queue Throughput Rate: Throughput = Completed_Tickets / Shift_Hours", "ops_sup_bs_001", "Managing Critical Operations Escalation During Extended Enterprise SSO Outage"),
        "ops_assoc": ("Operations Associate", 6, ["Standard Operating Procedure (SOP) Execution", "Asset Tracking & Inventory Database Integrity"], "Inventory Discrepancy Rate: Discrepancy = |Physical_Count - System_Count| / System_Count", "ops_assoc_bs_001", "Executing Comprehensive IT Hardware Asset Audit Across 3 Remote Office Hubs"),
    }

    res = {}
    for role_id, (title, level, foundations, formula, sc_id, sc_title) in ops_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="Operations",
            level=level,
            theoretical_foundations=foundations + ["Theory of Constraints", "Lean Six Sigma"],
            mathematical_formulations=[
                MathematicalFormulation(
                    name="Little's Law",
                    formula="WIP = Throughput * Lead_Time",
                    latex=r"L = \lambda W",
                    variables={"L": "Work in progress", r"\lambda": "Arrival rate", "W": "Cycle time"},
                    application="Eliminating process bottlenecks.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="The Goal: A Process of Ongoing Improvement",
                    authors="Eliyahu M. Goldratt",
                    year=1984,
                    venue="North River Press",
                    key_contribution="Introduced the Theory of Constraints and revolutionized manufacturing and business operations.",
                )
            ],
            regulatory_and_industry_standards=["ISO 9001:2015 Quality Management", "ISO 22301 Business Continuity"],
            core_algorithms_and_methods=["Root Cause 5 Whys Analysis", "Ishikawa Fishbone Diagrams", "DMAIC Six Sigma"],
            gold_medalist_playbook=[
                "Document every standard operating procedure (SOP) with unambiguous visual checklists.",
                "Eliminate handoffs: every handoff between departments introduces a 50% probability of error or delay.",
                "Institute automated monitoring on all operational queues with alert thresholds at 70% capacity.",
            ],
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"Operational execution scenario for {title}.",
                    challenge="Resolve operational bottleneck, ensure SOP compliance, and eliminate root causes.",
                    ground_truth_criteria=["Process optimization", "Root-cause elimination", "Zero SLA breach"],
                    rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "execution_reliability": 0.30, "risk_discipline": 0.20},
                )
            ],
        )
    return res


def _build_people_ladder() -> Dict[str, RoleCurriculum]:
    """Generates PhD-level curricula for the 5 People / HR ladder roles."""
    people_roles = {
        "vp_people": ("VP of People", 3, ["Executive Talent Acquisition & Total Rewards Architecture", "Global Employment Compliance & DEI Strategy"], "Compensatory Pay Parity Index: Parity = Median_Comp_Group_A / Median_Comp_Group_B", "vp_people_bs_001", "Designing Executive Equity Retention Strategy to Safeguard Critical AI Research Team"),
        "hr_dir": ("HR Director", 4, ["Employee Relations Escalations & Labor Law Defense", "Performance Management Systems & 9-Box Calibration"], "Employee Retention Rate: Retention = (Ending_Headcount - Leavers) / Starting_Headcount", "dir_hr_bs_001", "Investigating and Resolving Severe Executive Misconduct Allegation with Zero Leaks"),
        "hr_mgr": ("HR Manager", 5, ["HR Program Implementations & Manager Training", "Annual Compensation Band Reviews & Benchmark Surveys"], "Offer Acceptance Rate: OAR = Accepted_Offers / Total_Extended_Offers", "hr_mgr_bs_001", "Rolling Out Enterprise-Wide Engineering Compensation Bands Aligned to Radford Data"),
        "hrbp": ("HR Business Partner", 5, ["Department Talent Planning & Conflict Mediation", "High-Potential Mentorship & Performance Improvement (PIP)"], "eNPS Employee Net Promoter Score: eNPS = %Promoters - %Detractors", "hrbp_bs_001", "Facilitating High-Stakes Interpersonal Conflict Mediation Between CTO and Head of Product"),
        "hr_coord": ("HR Coordinator", 6, ["Onboarding Workflow Execution & HRIS Maintenance", "Interview Logistics & Candidate Experience"], "Onboarding Time-to-Productivity: Days to first approved production pull request", "hr_coord_bs_001", "Coordinating High-Volume Seamless Remote Onboarding for 45 New Hires Simultaneously"),
    }

    res = {}
    for role_id, (title, level, foundations, formula, sc_id, sc_title) in people_roles.items():
        res[role_id] = RoleCurriculum(
            role_id=role_id,
            role_title=title,
            department="People",
            level=level,
            theoretical_foundations=foundations + ["Job Characteristics Model", "Psychological Safety Theory"],
            mathematical_formulations=[
                MathematicalFormulation(
                    name="Employee Churn Hazard Rate",
                    formula="h(t) = - d(ln S(t)) / dt",
                    latex=r"h(t) = -\frac{d \ln S(t)}{dt}",
                    variables={"h(t)": "Instantaneous departure hazard", "S(t)": "Survival retention probability"},
                    application="Modeling employee attrition risk curves over tenure.",
                )
            ],
            landmark_papers=[
                LandmarkPaper(
                    title="The Validity and Utility of Selection Methods in Personnel Psychology",
                    authors="Frank L. Schmidt, John E. Hunter",
                    year=1998,
                    venue="Psychological Bulletin",
                    key_contribution="Proved the scientific efficacy of structured interviews and cognitive aptitude assessments.",
                )
            ],
            regulatory_and_industry_standards=["EEOC Uniform Selection Guidelines", "Title VII Civil Rights Act", "FLSA Wage and Hour Laws"],
            core_algorithms_and_methods=["9-Box Talent Grid Calibration", "Structured Behavioral Interview Scoring"],
            gold_medalist_playbook=[
                "High performance requires high trust; never violate employee confidentiality in mediation.",
                "Document all performance deficiencies with objective, timestamped factual evidence.",
                "Structure onboarding so every new hire experiences their first meaningful win within 72 hours.",
            ],
            benchmark_scenarios=[
                BenchmarkScenario(
                    scenario_id=sc_id,
                    title=sc_title,
                    difficulty="Mastery",
                    context=f"Human resources and people leadership challenge for {title}.",
                    challenge="Design and execute people strategy while ensuring legal compliance and psychological safety.",
                    ground_truth_criteria=["Legal compliance", "Empathetic communication", "Objective fairness"],
                    rubric_weights={"domain_mastery": 0.25, "reasoning_quality": 0.25, "collaboration": 0.25, "risk_discipline": 0.25},
                )
            ],
        )
    return res


# Assemble all 48 roles
CURRICULA.update(_build_engineering_ladder())
CURRICULA.update(_build_product_ladder())
CURRICULA.update(_build_sales_ladder())
CURRICULA.update(_build_marketing_ladder())
CURRICULA.update(_build_finance_ladder())
CURRICULA.update(_build_operations_ladder())
CURRICULA.update(_build_people_ladder())

# Synchronize role_title and department with ALL_ROLES
try:
    from aegiscorp.org.hierarchy import ALL_ROLES
    for rid, c in CURRICULA.items():
        if rid in ALL_ROLES:
            c.role_title = ALL_ROLES[rid].title
            c.department = ALL_ROLES[rid].department
            c.level = ALL_ROLES[rid].level
except Exception:
    pass


def get_curriculum(role_id: str) -> Optional[RoleCurriculum]:
    """Retrieve the PhD-level curriculum for a given role ID."""
    return CURRICULA.get(role_id)


def get_all_curricula() -> Dict[str, RoleCurriculum]:
    """Retrieve all 48 role curricula."""
    return CURRICULA


def get_department_curricula(department: str) -> List[RoleCurriculum]:
    """Retrieve all role curricula belonging to a specific department."""
    return [c for c in CURRICULA.values() if c.department.lower() == department.lower()]
