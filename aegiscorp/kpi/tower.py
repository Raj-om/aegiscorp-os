from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class KPIDomain(str, Enum):
    FINANCE = "Finance"
    PRODUCT = "Product"
    ENGINEERING = "Engineering"
    SALES = "Sales"
    MARKETING = "Marketing"
    PEOPLE = "People"
    OPERATIONS = "Operations"
    ENTERPRISE = "Enterprise"

class KPIMetric(BaseModel):
    id: str
    name: str
    domain: KPIDomain
    current_value: float
    target_value: float
    unit: str
    owner_role_id: str
    status: str = "GREEN"  # GREEN, AMBER, RED
    trend: str = "UP"      # UP, FLAT, DOWN

class KPIControlTower:
    """Manages the corporate KPI control tower across all 8 functional domains specified in Section 16."""

    def __init__(self):
        self.metrics: Dict[str, KPIMetric] = {}
        self._seed_default_metrics()

    def _seed_default_metrics(self):
        defaults = [
            # Finance
            KPIMetric(id="kpi_fin_arr", name="Annual Recurring Revenue (ARR)", domain=KPIDomain.FINANCE, current_value=120.0, target_value=250.0, unit="$M", owner_role_id="cfo"),
            KPIMetric(id="kpi_fin_margin", name="Gross Margin", domain=KPIDomain.FINANCE, current_value=78.5, target_value=82.0, unit="%", owner_role_id="cfo"),
            KPIMetric(id="kpi_fin_runway", name="Cash Runway", domain=KPIDomain.FINANCE, current_value=30.3, target_value=24.0, unit="mo", owner_role_id="cfo"),
            
            # Product
            KPIMetric(id="kpi_prod_act", name="User Activation Rate", domain=KPIDomain.PRODUCT, current_value=64.2, target_value=70.0, unit="%", owner_role_id="cpo"),
            KPIMetric(id="kpi_prod_ret", name="Net Retention Rate (D90)", domain=KPIDomain.PRODUCT, current_value=128.0, target_value=130.0, unit="%", owner_role_id="cpo"),
            KPIMetric(id="kpi_prod_road", name="Roadmap Delivery Index", domain=KPIDomain.PRODUCT, current_value=94.0, target_value=95.0, unit="%", owner_role_id="cpo"),

            # Engineering
            KPIMetric(id="kpi_eng_avail", name="Platform Availability", domain=KPIDomain.ENGINEERING, current_value=99.98, target_value=99.99, unit="%", owner_role_id="cto"),
            KPIMetric(id="kpi_eng_lead", name="Change Lead Time", domain=KPIDomain.ENGINEERING, current_value=14.5, target_value=8.0, unit="hrs", owner_role_id="cto"),
            KPIMetric(id="kpi_eng_fail", name="Change Failure Rate", domain=KPIDomain.ENGINEERING, current_value=1.2, target_value=1.0, unit="%", owner_role_id="cto"),

            # Sales
            KPIMetric(id="kpi_sales_pipe", name="Total Weighted Pipeline", domain=KPIDomain.SALES, current_value=26.2, target_value=35.0, unit="$M", owner_role_id="cro"),
            KPIMetric(id="kpi_sales_win", name="Opportunity Win Rate", domain=KPIDomain.SALES, current_value=32.4, target_value=35.0, unit="%", owner_role_id="cro"),
            KPIMetric(id="kpi_sales_cycle", name="Sales Cycle Length", domain=KPIDomain.SALES, current_value=42.0, target_value=35.0, unit="days", owner_role_id="cro"),

            # Marketing
            KPIMetric(id="kpi_mktg_cac", name="Customer Acquisition Cost (CAC)", domain=KPIDomain.MARKETING, current_value=12400.0, target_value=10000.0, unit="$", owner_role_id="cmo"),
            KPIMetric(id="kpi_mktg_roi", name="Marketing Campaign ROI", domain=KPIDomain.MARKETING, current_value=4.8, target_value=5.0, unit="x", owner_role_id="cmo"),

            # People
            KPIMetric(id="kpi_peo_ret", name="Annualized Talent Retention", domain=KPIDomain.PEOPLE, current_value=93.8, target_value=92.0, unit="%", owner_role_id="chro"),
            KPIMetric(id="kpi_peo_skill", name="Critical Skill Coverage", domain=KPIDomain.PEOPLE, current_value=91.5, target_value=95.0, unit="%", owner_role_id="chro"),

            # Operations
            KPIMetric(id="kpi_ops_sla", name="Cross-Functional SLA Attainment", domain=KPIDomain.OPERATIONS, current_value=98.2, target_value=99.0, unit="%", owner_role_id="coo"),
            KPIMetric(id="kpi_ops_util", name="Core Capacity Utilization", domain=KPIDomain.OPERATIONS, current_value=84.0, target_value=85.0, unit="%", owner_role_id="coo"),

            # Enterprise
            KPIMetric(id="kpi_ent_risk", name="Composite Enterprise Risk Score", domain=KPIDomain.ENTERPRISE, current_value=24.5, target_value=20.0, unit="/100", owner_role_id="ceo"),
            KPIMetric(id="kpi_ent_val", name="Estimated Enterprise Valuation", domain=KPIDomain.ENTERPRISE, current_value=1850.0, target_value=1000000.0, unit="$M", owner_role_id="ceo"),
        ]
        for m in defaults:
            self.metrics[m.id] = m

    def get_all_metrics(self) -> List[KPIMetric]:
        return list(self.metrics.values())

    def get_metrics_by_domain(self, domain: KPIDomain) -> List[KPIMetric]:
        return [m for m in self.metrics.values() if m.domain == domain]

    def update_metric(self, metric_id: str, new_value: float) -> Optional[KPIMetric]:
        m = self.metrics.get(metric_id)
        if not m:
            return None
        m.trend = "UP" if new_value >= m.current_value else "DOWN"
        m.current_value = new_value
        
        # Calculate status
        if m.id == "kpi_ent_risk" or "fail" in m.id:
            m.status = "GREEN" if new_value <= m.target_value else "RED"
        else:
            pct = new_value / m.target_value if m.target_value > 0 else 1.0
            if pct >= 0.95:
                m.status = "GREEN"
            elif pct >= 0.80:
                m.status = "AMBER"
            else:
                m.status = "RED"
        return m
