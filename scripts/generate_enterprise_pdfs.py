"""
scripts/generate_enterprise_pdfs.py

Generates authentic, high-density 3-to-4 page enterprise PDF documents for RAG benchmarking
under the "HR & Enterprise Management" corpus. Each document simulates a real internal policy
manual: dense corporate prose, multi-column reference tables, worked numerical formulas,
escalation/SLA matrices, and realistic clause language — with no debug/metadata banners
printed inside the PDF text itself.

Document set (10 total):
  policies/employee_handbook_2026.pdf
  policies/performance_and_grievance_policy.pdf
  policies/code_of_conduct_and_ethics_policy.pdf
  payroll/salary_structure_bands_2026.pdf
  payroll/bonus_payout_matrix_2026.pdf
  benefits/health_insurance_plan_2026.pdf
  benefits/pf_and_gratuity_policy.pdf
  legal_labour/maternity_and_paternity_leave_policy.pdf
  talent/recruitment_and_onboarding_policy.pdf
  talent/learning_and_development_policy.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def get_custom_styles():
    styles = getSampleStyleSheet()

    doc_title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        alignment=0,
        spaceAfter=4,
    )

    doc_subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=body_style,
        leftIndent=12,
        spaceAfter=4,
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
    )

    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
    )

    cell_header_style = ParagraphStyle(
        "TableHeaderCell",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.white,
    )

    return {
        "title": doc_title_style,
        "subtitle": doc_subtitle_style,
        "h1": h1_style,
        "h2": h2_style,
        "body": body_style,
        "bullet": bullet_style,
        "callout": callout_style,
        "cell": cell_style,
        "cell_header": cell_header_style,
    }


def make_callout(text, styles, bg_color="#F1F5F9", border_color="#CBD5E1"):
    t_data = [[Paragraph(text, styles["callout"])]]
    t = Table(t_data, colWidths=[7.0 * inch])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg_color)),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor(border_color)),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    return t


def make_table(header_row, data_rows, col_widths, header_bg="#1E3A8A"):
    styles = get_custom_styles()
    header = [Paragraph(h, styles["cell_header"]) for h in header_row]
    body_rows = [[Paragraph(str(c), styles["cell"]) for c in row] for row in data_rows]
    t = Table([header] + body_rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def build_pdf(filepath, title, subtitle, story_content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    styles = get_custom_styles()

    story = [
        Paragraph(title, styles["title"]),
        Paragraph(subtitle, styles["subtitle"]),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=12),
    ]
    story.extend(story_content)

    doc.build(story)
    print(f"Generated: {filepath}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. POLICIES — Employee Handbook
# ─────────────────────────────────────────────────────────────────────────────
def generate_employee_handbook():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Corporate Governance & Purpose of This Handbook", styles["h1"]))
    s.append(Paragraph(
        "This Employee Handbook is the authoritative operating reference for every person employed by the Enterprise "
        "Organization, regardless of function, seniority, or contract type. It sets out the administrative processes, "
        "employment classifications, professional conduct standards, leave accrual mechanics, travel and expense rules, "
        "remote-work security obligations, and the code of conduct that governs day-to-day work across every regional "
        "office. Managers are expected to apply these policies consistently; deviations require written sign-off from "
        "the Human Resources Business Partner (HRBP) assigned to that function.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Where local statutory requirements are more generous to the employee than the baseline described in this "
        "handbook (for example, a jurisdiction that mandates a longer notice period or a higher minimum leave "
        "entitlement), the local statutory requirement takes precedence. The People Operations team maintains a "
        "country-specific addendum register that supplements — but never narrows — the protections described here.",
        styles["body"]
    ))
    s.append(Paragraph(
        "This handbook is reviewed annually by the Executive People Committee and republished each January. Employees "
        "are notified of material changes at least 30 days before they take effect, and continued employment after "
        "that notice period constitutes acknowledgement of the revised terms.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Employment Classifications & Work Schedule", styles["h1"]))
    s.append(Paragraph(
        "Employees are assigned to specific job classifications that determine compensation structure, overtime "
        "eligibility, and benefit allocation at the point of hire and re-confirmed at every promotion or transfer:",
        styles["body"]
    ))
    s.append(Paragraph("• <b>Full-Time Exempt Staff:</b> Professional, technical, or managerial employees working a minimum of 40 hours per week, exempt from statutory overtime pay under their local employment code.", styles["bullet"]))
    s.append(Paragraph("• <b>Full-Time Non-Exempt Staff:</b> Hourly operational staff entitled to overtime pay at 1.5x the standard hourly rate for hours worked beyond 40 per week, and 2.0x for hours worked on a designated public holiday.", styles["bullet"]))
    s.append(Paragraph("• <b>Part-Time Employees:</b> Staff scheduled for fewer than 30 hours per week, eligible for prorated leave accrual and prorated participation in the group benefits plan.", styles["bullet"]))
    s.append(Paragraph("• <b>Fixed-Term Contractors:</b> Engaged for a defined project duration not exceeding 24 months, renewable once, with statutory leave entitlements but no eligibility for the variable bonus pool.", styles["bullet"]))
    s.append(Paragraph(
        "Standard business operating hours are Monday through Friday, 8:00 AM to 6:00 PM local time. Mandatory core "
        "collaboration hours — during which all staff must be reachable regardless of flexible scheduling — run from "
        "10:00 AM to 4:00 PM. Flexible arrival between 8:00 AM and 10:00 AM is permitted subject to the direct "
        "supervisor's approval and does not require a formal exception request.",
        styles["body"]
    ))

    s.append(Paragraph("Section 3: Remote & Hybrid Work Arrangements", styles["h1"]))
    s.append(Paragraph(
        "Employees in eligible roles may work under a hybrid arrangement (minimum 2 in-office days per week, set by "
        "the department lead) or a fully remote arrangement approved by the VP of the function. Eligibility is "
        "reassessed at each performance cycle and is not a permanent entitlement.",
        styles["body"]
    ))
    s.append(Paragraph("• <b>Equipment:</b> The company issues a standard laptop, monitor, and peripheral kit; additional ergonomic equipment is reimbursable up to $300 USD per employee every 3 years under expense code EXP-ERG-210.", styles["bullet"]))
    s.append(Paragraph("• <b>Home Office Stipend:</b> $75.00 USD per month for verified remote employees, disbursed with monthly payroll under expense code EXP-4401.", styles["bullet"]))
    s.append(Paragraph("• <b>Security Requirements:</b> Mandatory VPN connection for any access to internal systems, disk encryption on all company devices, and a strict prohibition on conducting company business over unsecured public Wi-Fi.", styles["bullet"]))
    s.append(Paragraph("• <b>Core Presence Days:</b> Hybrid staff must be on-site on the department's designated anchor days, published quarterly by the workplace operations team.", styles["bullet"]))

    s.append(Paragraph("Section 4: Probationary Evaluation & Performance Appraisals", styles["h1"]))
    s.append(Paragraph(
        "All newly hired employees undergo a mandatory 90-day introductory probationary period beginning on the "
        "official date of hire. Direct managers conduct formal milestone evaluations on Day 30, Day 60, and Day 85, "
        "each recorded in the performance management system. Successful completion of probation activates full group "
        "medical insurance and retirement benefit allocations retroactive to the date of hire.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Subsequent performance appraisals occur biannually, on June 15 (Mid-Year Review) and December 15 (Annual "
        "Performance Appraisal). Ratings from the Annual Appraisal directly determine merit increase eligibility and "
        "the variable bonus multiplier described in the Bonus Payout Matrix.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Paid Time Off (PTO) & Leave Accrual Schedule", styles["h1"]))
    s.append(Paragraph("Paid vacation, sick leave, and personal casual days accrue monthly based on completed years of continuous service:", styles["body"]))
    s.append(make_table(
        ["Completed Tenure", "Vacation Days / Yr", "Sick Days / Yr", "Casual Days / Yr", "Max Annual Carryover"],
        [
            ["0 - 2 Years", "15 Days", "10 Days", "5 Days", "5 Days"],
            ["2 - 5 Years", "20 Days", "12 Days", "5 Days", "7 Days"],
            ["5 - 10 Years", "25 Days", "15 Days", "7 Days", "10 Days"],
            ["10+ Years", "30 Days", "18 Days", "10 Days", "15 Days"],
        ],
        [1.4*inch, 1.4*inch, 1.3*inch, 1.3*inch, 1.6*inch],
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "Unused vacation days beyond the maximum carryover threshold are forfeited on December 31 unless the "
        "employee's manager approves a documented business-need extension into Q1 of the following year. Sick leave "
        "does not carry over and resets on January 1.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Business Travel & Daily Per Diem Expense Policy", styles["h1"]))
    s.append(Paragraph(
        "Employees traveling on official company business are entitled to expense reimbursements and per diem "
        "allowances. All business travel must receive pre-authorization from the Department Head via Travel "
        "Authorization Form (TAF-101) at least 7 days prior to departure.",
        styles["body"]
    ))
    s.append(Paragraph("• <b>Air Travel:</b> Standard Economy class required for all domestic flights. Business Class permitted only for international flights exceeding 8 consecutive hours.", styles["bullet"]))
    s.append(Paragraph("• <b>Lodging / Hotel Caps:</b> Tier 1 Metropolitan Cities capped at $250.00 USD/night; Tier 2 Cities capped at $175.00 USD/night.", styles["bullet"]))
    s.append(Paragraph("• <b>Daily Meal Per Diem:</b> Fixed daily allowance of $75.00 USD/day ($15 Breakfast, $25 Lunch, $35 Dinner) with no itemized receipts required for food.", styles["bullet"]))
    s.append(Paragraph("• <b>Ground Transport:</b> Rideshare or taxi reimbursed at actuals; personal vehicle mileage reimbursed at $0.67 USD/mile.", styles["bullet"]))
    s.append(make_callout(
        "<b>Submission Deadline & Expense Code:</b> Expense claims with receipts for lodging and transport must be "
        "submitted in the finance portal under expense category code <b>EXP-TRV-802</b> within <b>15 calendar days</b> "
        "of trip completion. Claims submitted after 30 days require CFO-office approval.",
        styles, bg_color="#EFF6FF", border_color="#93C5FD"
    ))

    s.append(Paragraph("Section 7: Code of Conduct & Intellectual Property (Summary)", styles["h1"]))
    s.append(Paragraph(
        "Employees must adhere to strict ethical standards; conflicts of interest, bribery, or unauthorized "
        "disclosure of trade secrets are grounds for immediate termination. All software, patent filings, processes, "
        "and documentation produced during employment remain the sole intellectual property of the organization. A "
        "full statement of expected conduct, gift and hospitality limits, and the whistleblower reporting channel is "
        "published separately in the Code of Conduct & Ethics Policy.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Health, Safety & Workplace Incident Reporting", styles["h1"]))
    s.append(Paragraph(
        "All office locations maintain a documented emergency evacuation plan, a first-aid trained floor warden per "
        "40 employees, and quarterly fire-drill exercises. Any workplace injury, near-miss, or safety hazard must be "
        "reported to the Workplace Safety Officer within 24 hours using Incident Form WS-14. Repeat safety violations "
        "by a facility trigger a mandatory review by the Global Real Estate & Workplace Safety Committee.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Dress Code, Facilities & Visitor Access", styles["h1"]))
    s.append(Paragraph(
        "Business-casual attire is the standard expectation for office-based roles; client-facing meetings and "
        "formal events call for business formal attire unless the client environment indicates otherwise. Denim "
        "and closed-toe casual footwear are acceptable on non-client days. Employees hosting external visitors must "
        "register them at reception at least 2 hours in advance and remain with the visitor at all times while they "
        "are inside secured areas of the office.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Shared facilities — meeting rooms, phone booths, and collaboration spaces — are bookable through the "
        "workplace scheduling system. Rooms held but unused for more than 10 minutes past the scheduled start are "
        "automatically released for other bookings.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Acceptable Use of Company Systems & Social Media", styles["h1"]))
    s.append(Paragraph(
        "Company-issued email, messaging, and file-storage systems are provided for business use; limited incidental "
        "personal use is permitted provided it does not interfere with productivity, consume disproportionate "
        "bandwidth, or violate the Code of Conduct. All activity on company systems may be monitored for security "
        "and compliance purposes, consistent with applicable local privacy law and with notice provided to "
        "employees at the time of hire.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Employees who identify themselves as company staff on public social media must include a standard "
        "disclaimer that views expressed are their own, must not disclose confidential or unreleased company "
        "information, and must not speak on the company's behalf without authorization from Corporate "
        "Communications.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Equal Opportunity, Accommodation & Anti-Discrimination Statement", styles["h1"]))
    s.append(Paragraph(
        "The Enterprise Organization is an equal opportunity employer and makes employment decisions — hiring, "
        "promotion, compensation, and termination — based on merit, qualifications, and business need, without "
        "regard to race, color, religion, sex, national origin, age, disability, or any other legally protected "
        "characteristic. Employees requiring a reasonable accommodation for a disability or religious observance "
        "should submit a request to HR via the Accommodation Request Form (ACM-05); requests are acknowledged "
        "within 5 business days and an interactive dialogue to identify a workable accommodation begins within 10 "
        "business days.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Separation Protocol & Offboarding Deadlines", styles["h1"]))
    s.append(Paragraph(
        "Resigning staff must provide formal written notice: 30 calendar days for individual contributors and 60 "
        "calendar days for managers and executives. On the final working day, all corporate assets — encrypted "
        "laptops, physical badges, security tokens, and corporate cards — must be returned to IT and HR. Final "
        "settlement of dues, including any pro-rated bonus and encashment of unused leave, is processed within 45 "
        "calendar days of the last working day.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Exiting employees complete a mandatory exit interview with HR and a knowledge-transfer plan signed off by "
        "their manager. Access to all company systems is revoked at 11:59 PM on the last working day unless a "
        "documented, time-boxed transition extension has been approved by the CISO's office.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "policies", "employee_handbook_2026.pdf")
    build_pdf(
        filepath,
        "Enterprise Employee Handbook & Administrative Guidelines",
        "Version 2026.1 | Authoritative Reference for Governance, Leave, Travel, Remote Work & Operating Rules",
        s
    )


def generate_performance_grievance_policy():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Annual Appraisal Framework & Rating Distribution", styles["h1"]))
    s.append(Paragraph(
        "The enterprise performance management framework establishes transparent, measurable performance criteria "
        "evaluated biannually on June 15 and December 15. Appraisals combine objective KPI achievement (weighted "
        "60%), technical execution and craft quality (weighted 25%), and leadership or cultural-values alignment "
        "(weighted 15%). Managers submit draft ratings two weeks before the review date; ratings are then calibrated "
        "in cross-functional panels to reduce individual manager bias before being finalized.",
        styles["body"]
    ))
    s.append(Paragraph("Performance ratings follow a standardized 5-point evaluation scale:", styles["body"]))
    s.append(Paragraph("• <b>Rating 5.0 (Outstanding):</b> Top 10% of workforce. Consistently exceeds targets. Qualifies for 1.50x bonus multiplier and priority merit increase.", styles["bullet"]))
    s.append(Paragraph("• <b>Rating 4.0 (Exceeds Expectations):</b> Exceeds core goals in major impact areas. Qualifies for 1.25x bonus multiplier.", styles["bullet"]))
    s.append(Paragraph("• <b>Rating 3.0 (Meets Expectations):</b> Consistently meets established standards. Qualifies for 1.00x bonus multiplier.", styles["bullet"]))
    s.append(Paragraph("• <b>Rating 2.0 (Needs Improvement):</b> Fails to meet expectations in 1-2 core duties. Requires a mandatory 60-day Performance Improvement Plan (PIP).", styles["bullet"]))
    s.append(Paragraph("• <b>Rating 1.0 (Unsatisfactory):</b> Persistent failure across primary responsibilities. Triggers formal disciplinary review or contract termination.", styles["bullet"]))
    s.append(Paragraph(
        "Calibration panels apply a soft guideline — not a forced curve — targeting roughly 10% of a function at "
        "Rating 5.0 and no more than 5% combined at Ratings 1.0-2.0, reviewed each cycle by the Executive People "
        "Committee to confirm the distribution reflects genuine performance rather than quota pressure.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Performance Improvement Plan (PIP) Execution Roadmap", styles["h1"]))
    s.append(Paragraph(
        "Employees assigned a Rating 2.0 enter a structured 60-day Performance Improvement Plan. The PIP details "
        "clear, measurable objectives, weekly milestone check-ins with the direct manager and HRBP, and access to "
        "technical or managerial coaching resources funded by the Learning & Development budget.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Bi-weekly progress audits are conducted on Day 15, Day 30, Day 45, and Day 60. If acceptable performance "
        "standards are achieved by Day 60, the PIP is closed and the employee returns to standard review cadence. "
        "Failure to meet targets results in contract termination, subject to the progressive discipline safeguards "
        "described in Section 4.",
        styles["body"]
    ))

    s.append(Paragraph("Section 3: Workplace Grievance Escalation Architecture & SLA Matrix", styles["h1"]))
    s.append(Paragraph(
        "Employees have the right to seek fair resolution for workplace disputes, unfair treatment, or policy "
        "misapplication (harassment and discrimination complaints follow the separate, confidential process managed "
        "by the Internal Complaints Committee). General grievances are managed through a three-tier escalation "
        "hierarchy:",
        styles["body"]
    ))
    s.append(make_table(
        ["Escalation Tier", "Authority Officer", "Initial Acknowledgement", "Max Investigation SLA"],
        [
            ["Level 1 (Initial)", "Direct Reporting Manager", "24 Hours", "5 Business Days"],
            ["Level 2 (Departmental)", "HR Business Partner (HRBP)", "48 Hours", "10 Business Days"],
            ["Level 3 (Executive)", "Chief Human Resources Officer (CHRO)", "72 Hours", "14 Business Days"],
        ],
        [1.6*inch, 2.0*inch, 1.7*inch, 1.7*inch],
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "Grievances that remain unresolved after Level 3 investigation may be referred, at the employee's request, "
        "to an external ombudsperson retained by the company, whose recommendation is advisory but is reviewed "
        "directly by the CEO's office.",
        styles["body"]
    ))

    s.append(Paragraph("Section 4: Progressive Disciplinary Policy Framework", styles["h1"]))
    s.append(Paragraph(
        "Uncorrected misconduct or policy breaches warrant progressive discipline in the following order: "
        "(1) Verbal Counseling, documented in the employee file; (2) Written Warning; (3) Final Written Warning "
        "combined with a 5-day unpaid suspension; (4) Involuntary termination of employment. Serious misconduct — "
        "including theft, violence, or data exfiltration — bypasses progressive steps and may result in immediate "
        "termination following a documented investigation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Whistleblower Safeguards & Anti-Retaliation Protections", styles["h1"]))
    s.append(Paragraph(
        "The organization strictly prohibits retaliation of any kind against an employee who reports a grievance, "
        "safety concern, or compliance violation in good faith, whether the report is made to a manager, HR, legal, "
        "or the anonymous ethics hotline. Any confirmed retaliatory conduct results in immediate termination of the "
        "offending party, regardless of seniority.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Goal Setting, OKRs & Mid-Cycle Check-Ins", styles["h1"]))
    s.append(Paragraph(
        "Every employee sets quarterly objectives and key results (OKRs) in the performance system within the first "
        "2 weeks of each quarter, aligned to team and company priorities cascaded from the annual strategic plan. "
        "Managers and direct reports hold a documented 1:1 check-in at least every 2 weeks, and a formal mid-quarter "
        "progress review at the midpoint of each quarter to surface risks before they affect the biannual rating.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Objectives that become obsolete mid-quarter due to shifting business priorities may be revised with "
        "manager sign-off; unexplained objective changes after the quarter's final two weeks are flagged during "
        "calibration as a possible sign of goal-setting weakness rather than genuine business change.",
        styles["body"]
    ))

    s.append(Paragraph("Section 7: 360-Degree Feedback for People Managers", styles["h1"]))
    s.append(Paragraph(
        "All people-managers (anyone with 1 or more direct reports) undergo an anonymous 360-degree feedback survey "
        "once per year, gathering input from direct reports, peers, and the manager's own manager. Aggregated "
        "results (minimum 3 respondents required to preserve anonymity) are shared with the manager and factored "
        "qualitatively into the leadership-competency component of their own annual rating; raw individual comments "
        "are never shared with the manager or with anyone outside the People Analytics team.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Appeals Process for Disputed Ratings", styles["h1"]))
    s.append(Paragraph(
        "An employee who disagrees with their finalized performance rating may file a written appeal within 10 "
        "business days of the rating being communicated. The appeal is reviewed by a panel consisting of the "
        "HRBP, a skip-level manager, and one calibration-committee representative who was not involved in the "
        "original rating decision. The panel issues a decision within 15 business days; the appeal decision is "
        "final and is not subject to further internal escalation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Documentation Standards for Managers", styles["h1"]))
    s.append(Paragraph(
        "Managers are required to log specific, dated examples of performance in the system throughout the review "
        "period rather than reconstructing feedback from memory at cycle-end. A rating of 2.0 or below must be "
        "supported by at least 3 documented, dated instances shared with the employee before the formal review "
        "meeting; ratings lacking this documentation are returned to the manager by the calibration panel for "
        "revision before they can be finalized.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Grievance Categories & Illustrative Examples", styles["h1"]))
    s.append(make_table(
        ["Grievance Category", "Illustrative Example", "Typical Handling Track"],
        [
            ["Compensation dispute", "Incorrect band applied at promotion", "Level 1 -> Level 2 (HRBP + Payroll)"],
            ["Unfair treatment", "Inconsistent application of leave policy", "Level 1 -> Level 2"],
            ["Manager conduct", "Repeated dismissive behavior in meetings", "Level 2 direct (bypass manager)"],
            ["Harassment / discrimination", "Any protected-characteristic based conduct", "Internal Complaints Committee (separate process)"],
        ],
        [1.9*inch, 2.7*inch, 1.9*inch],
        header_bg="#1E3A8A",
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "Grievances that a Level 1 manager cannot handle impartially — such as complaints about the manager "
        "themselves — are routed directly to Level 2 without requiring the employee to raise the matter with the "
        "person the complaint concerns.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "policies", "performance_and_grievance_policy.pdf")
    build_pdf(
        filepath,
        "Performance Management & Grievance Policy Guidelines",
        "Version 2026.1 | Standard Operating Procedures for Appraisals, PIPs, and Dispute Resolutions",
        s
    )


def generate_code_of_conduct_policy():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Purpose & Applicability", styles["h1"]))
    s.append(Paragraph(
        "This Code of Conduct & Ethics Policy defines the minimum standard of professional and ethical behavior "
        "expected of every employee, contractor, officer, and director of the Enterprise Organization. It applies "
        "on company premises, at company-sponsored events, while traveling on company business, and in any online "
        "activity that identifies the individual as a representative of the company.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Violations of this policy are addressed through the Progressive Disciplinary Policy Framework described in "
        "the Performance Management & Grievance Policy. Certain violations — bribery, fraud, or falsification of "
        "company records — are grounds for immediate termination and may be referred to law enforcement or "
        "regulators where required by law.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Conflicts of Interest", styles["h1"]))
    s.append(Paragraph(
        "Employees must avoid situations where personal interests could reasonably be seen to conflict with the "
        "interests of the company. Common examples requiring mandatory disclosure via the Conflicts of Interest "
        "Register include:",
        styles["body"]
    ))
    s.append(Paragraph("• Holding a financial stake exceeding 5% in a supplier, vendor, or competitor.", styles["bullet"]))
    s.append(Paragraph("• Directly managing a family member or someone with whom the employee has a close personal relationship.", styles["bullet"]))
    s.append(Paragraph("• Accepting outside board seats, advisory roles, or paid consulting engagements related to the company's industry.", styles["bullet"]))
    s.append(Paragraph(
        "Disclosures must be filed within 10 business days of the conflict arising and are reviewed by the Ethics & "
        "Compliance Office, which may require recusal from specific decisions rather than prohibiting the "
        "relationship outright.",
        styles["body"]
    ))

    s.append(Paragraph("Section 3: Gifts, Hospitality & Anti-Bribery Limits", styles["h1"]))
    s.append(make_table(
        ["Category", "Threshold Requiring Disclosure", "Absolute Prohibition Threshold"],
        [
            ["Gifts from vendors/partners", "$75 USD per instance", "$250 USD annual aggregate per counterparty"],
            ["Business meals & hospitality", "$150 USD per instance", "Any hospitality tied to an active procurement decision"],
            ["Cash or cash-equivalent gifts", "N/A", "Prohibited in all cases, any amount"],
            ["Gifts to government officials", "Any amount", "Prohibited unless pre-cleared by Legal"],
        ],
        [2.0*inch, 2.6*inch, 2.4*inch],
        header_bg="#4C1D95",
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "The company maintains a zero-tolerance stance on bribery and facilitation payments consistent with "
        "applicable anti-corruption law. Any request for, or offer of, an improper payment must be reported "
        "immediately to the Ethics & Compliance Office.",
        styles["body"]
    ))

    s.append(Paragraph("Section 4: Confidentiality, Data Handling & Insider Information", styles["h1"]))
    s.append(Paragraph(
        "Employees with access to confidential business information, unreleased financials, or material non-public "
        "information must not disclose it outside authorized channels and must not trade in company securities "
        "while in possession of such information, consistent with the company's separate Insider Trading Policy. "
        "Confidentiality obligations survive termination of employment.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Workplace Respect, Anti-Harassment & Anti-Discrimination", styles["h1"]))
    s.append(Paragraph(
        "The company prohibits harassment or discrimination on the basis of race, color, religion, sex, national "
        "origin, age, disability, veteran status, or any other legally protected characteristic. Complaints of "
        "sexual harassment or discrimination are handled under the confidential Internal Complaints Committee "
        "process, not the general grievance process, and carry statutory investigation timelines that take "
        "precedence over the standard SLA matrix.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Ethics Hotline & Reporting Channels", styles["h1"]))
    s.append(make_callout(
        "<b>Anonymous Ethics Hotline:</b> Available 24/7 via web portal or toll-free number, operated by an "
        "independent third party. Reports may be filed anonymously where permitted by local law. Every report "
        "receives an acknowledgement within 48 hours and a documented resolution or escalation decision within "
        "30 calendar days.",
        styles, bg_color="#F5F3FF", border_color="#C4B5FD"
    ))

    s.append(Paragraph("Section 7: Acknowledgement Requirement", styles["h1"]))
    s.append(Paragraph(
        "All employees must electronically acknowledge this Code of Conduct at the time of hire and annually "
        "thereafter during the January compliance attestation cycle. Failure to complete the attestation within 15 "
        "days of the deadline is escalated to the employee's manager and recorded as a compliance exception.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Use of Company Assets & Expense Integrity", styles["h1"]))
    s.append(Paragraph(
        "Company assets — funds, equipment, facilities, and information — must be used only for legitimate business "
        "purposes. Deliberate misstatement of an expense claim, inflation of mileage, or submission of a personal "
        "expense as a business expense is treated as financial misconduct regardless of the dollar amount involved, "
        "and is investigated by Internal Audit rather than the standard grievance process.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Third-Party & Supplier Conduct Expectations", styles["h1"]))
    s.append(Paragraph(
        "Employees who manage vendor or supplier relationships must ensure those third parties are held to "
        "equivalent standards of ethical conduct, including prohibitions on child labor, forced labor, and unsafe "
        "working conditions, as set out in the Supplier Code of Conduct incorporated into every procurement "
        "contract above $10,000 USD. Suspected violations by a third party must be reported to Procurement and the "
        "Ethics & Compliance Office within 5 business days of discovery.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Environmental, Social & Governance (ESG) Conduct", styles["h1"]))
    s.append(Paragraph(
        "Employees are expected to support the company's published ESG commitments in their day-to-day decisions, "
        "including responsible resource use, accurate ESG data reporting, and escalation of any practice that could "
        "misrepresent the company's environmental or social performance to regulators, investors, or the public. "
        "Knowingly submitting false ESG or sustainability data is treated with the same severity as financial "
        "misstatement.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Political Activity & Lobbying", styles["h1"]))
    s.append(Paragraph(
        "Employees may participate in political activity on their own time using personal resources, but must not "
        "represent personal political views as those of the company, use company funds, email systems, or letterhead "
        "for political contributions or campaigning, or pressure colleagues to support a particular candidate or "
        "cause. Any company-level political contribution or lobbying activity is coordinated exclusively through "
        "the Government Affairs function under Board-approved guidelines.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Investigation Standards & Employee Rights During Review", styles["h1"]))
    s.append(Paragraph(
        "Employees under investigation for a suspected Code of Conduct violation are informed of the general nature "
        "of the allegation (unless doing so would compromise the investigation), may be accompanied by an HR "
        "representative during formal interviews, and receive the outcome of the investigation in writing. "
        "Investigations are conducted by Ethics & Compliance or Internal Audit as appropriate to the allegation and "
        "are targeted for completion within 30 calendar days, extendable once for complex matters with notice to "
        "the employee.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "policies", "code_of_conduct_and_ethics_policy.pdf")
    build_pdf(
        filepath,
        "Code of Conduct & Ethics Policy",
        "Version 2026.1 | Standards of Professional Conduct, Conflicts of Interest, and Reporting Channels",
        s
    )


# ─────────────────────────────────────────────────────────────────────────────
# 2. PAYROLL
# ─────────────────────────────────────────────────────────────────────────────
def generate_salary_structure_bands():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Enterprise Compensation Governance & Principles", styles["h1"]))
    s.append(Paragraph(
        "The corporate compensation framework ensures competitive, transparent, and equitable remuneration "
        "benchmarked annually against third-party market survey data (Radford and Mercer benchmarks) across every "
        "operational hub. Salary grade ranges are reviewed each January by the Executive Compensation Committee, "
        "and a formal pay-equity audit is conducted every 12 months to identify and remediate unexplained pay gaps "
        "by gender, ethnicity, and tenure cohort.",
        styles["body"]
    ))
    s.append(Paragraph(
        "New hire offers are targeted between the 25th and 60th percentile of the relevant band based on the "
        "candidate's assessed experience and internal parity with existing team members in comparable roles. Offers "
        "above the 60th percentile require VP-level approval.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Job Grade Salary Bands & Base Pay Range", styles["h1"]))
    s.append(Paragraph("The enterprise compensation framework is categorized across 7 job grades (L1 to L7), effective January 1, 2026:", styles["body"]))
    s.append(make_table(
        ["Grade", "Role Designation", "Min Base Pay ($)", "Midpoint ($)", "Max Base Pay ($)"],
        [
            ["L1", "Junior Associate / Assistant", "$45,000", "$55,000", "$65,000"],
            ["L2", "Associate Specialist / Engineer", "$65,000", "$80,000", "$95,000"],
            ["L3", "Senior Specialist / Senior Eng", "$95,000", "$115,000", "$135,000"],
            ["L4", "Lead Engineer / Project Manager", "$135,000", "$160,000", "$185,000"],
            ["L5", "Senior Manager / Principal Eng", "$185,000", "$215,000", "$245,000"],
            ["L6", "Director / Vice President", "$245,000", "$295,000", "$345,000"],
            ["L7", "Executive C-Suite (CXO)", "$350,000", "$425,000", "$500,000+"],
        ],
        [0.8*inch, 2.4*inch, 1.3*inch, 1.2*inch, 1.3*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 3: Salary Components & Percentage Formulas", styles["h1"]))
    s.append(Paragraph("Total Cost to Company (CTC) is allocated across fixed allowances and statutory components using the following formulas:", styles["body"]))
    s.append(Paragraph("• <b>Basic Salary:</b> Calculated as exactly <b>50% of Total Annual CTC</b>.", styles["bullet"]))
    s.append(Paragraph("• <b>House Rent Allowance (HRA):</b> <b>40% of Basic Salary</b> for Tier 1 Metro cities or <b>30% of Basic Salary</b> for Non-Metro locations.", styles["bullet"]))
    s.append(Paragraph("• <b>Provident Fund (PF) Contribution:</b> Mandatory <b>12% of Basic Salary</b>, matched by the employer.", styles["bullet"]))
    s.append(Paragraph("• <b>Special Allowance:</b> Residual balancing component, typically approximately 30% of CTC.", styles["bullet"]))
    s.append(Paragraph("• <b>Overtime (Non-Exempt Only):</b> 1.5x the hourly base rate, where hourly rate = Annual Basic Salary / 2,080 working hours.", styles["bullet"]))

    s.append(Paragraph("Section 4: Income Tax Deductions & Statutory Withholding Slabs", styles["h1"]))
    s.append(Paragraph(
        "Payrolls are subject to statutory income tax withholding based on annual taxable income slabs: 0% up to "
        "$15,000; 10% between $15,001-$45,000; 20% between $45,001-$90,000; 30% for earnings above $90,000 USD. "
        "Employees may declare eligible investment and insurance deductions each April to reduce taxable income "
        "under the standard exemption schedule.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Merit Increases & Promotion Adjustments", styles["h1"]))
    s.append(Paragraph(
        "Annual merit increases are budgeted as a percentage pool of total payroll, distributed according to "
        "performance rating: 6-8% for Rating 5.0, 4-5% for Rating 4.0, 2-3% for Rating 3.0, and 0% for Ratings below "
        "3.0. Promotion adjustments are calculated separately and typically bring base pay to at least the 25th "
        "percentile of the new grade's band, applied on the promotion effective date rather than the annual cycle.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Relocation & Location-Based Pay Adjustment", styles["h1"]))
    s.append(Paragraph(
        "Employees relocating between cost-of-living zones at company request receive a one-time relocation "
        "allowance (capped at $8,000 USD domestic / $15,000 USD international) and have their base salary "
        "re-benchmarked to the destination location's band within one payroll cycle.",
        styles["body"]
    ))

    s.append(Paragraph("Section 7: Payroll Disbursements & Direct Deposit Schedule", styles["h1"]))
    s.append(Paragraph(
        "Salaries are credited via direct electronic bank transfer on the 25th day of each calendar month. If the "
        "25th falls on a weekend or bank holiday, payments are executed on the preceding business day. Payslips are "
        "published to the self-service portal no later than 2 business days before disbursement.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Allowance Schedule Beyond Basic & HRA", styles["h1"]))
    s.append(make_table(
        ["Allowance", "Eligibility", "Monthly Amount / Basis", "Taxable?"],
        [
            ["Conveyance Allowance", "All grades", "$150 flat", "Partially exempt up to statutory limit"],
            ["Meal Card Allowance", "All grades", "$200 flat", "Exempt up to statutory limit"],
            ["Shift Allowance", "Non-exempt, night shift", "15% of Basic for shift days", "Fully taxable"],
            ["Car Lease / Fuel Allowance", "Grade L4+", "Up to $600, per lease agreement", "Partially taxable"],
        ],
        [2.0*inch, 1.7*inch, 2.0*inch, 1.3*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 9: Deductions Beyond Statutory Tax", styles["h1"]))
    s.append(Paragraph(
        "Beyond income tax and PF, monthly payroll deductions may include: Professional Tax (where applicable by "
        "jurisdiction, typically $20-$30/month), Labour Welfare Fund contribution (nominal, jurisdiction-dependent), "
        "the employee's share of health-plan premium for coverage tiers above the standard Tier 1 default, and any "
        "court-ordered wage garnishment processed strictly in the order and priority required by law.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Off-Cycle Pay Corrections & Recovery of Overpayment", styles["h1"]))
    s.append(Paragraph(
        "Payroll errors identified after disbursement are corrected in the next available off-cycle run, targeted "
        "within 5 business days of the error being confirmed. Where an employee has been overpaid, Payroll notifies "
        "the employee in writing before recovery begins and recovers the amount over a period no shorter than the "
        "number of pay cycles over which the overpayment accrued, unless the employee elects to repay it faster.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Location-Based Cost-of-Living Zones", styles["h1"]))
    s.append(make_table(
        ["Zone", "Representative Cities", "Band Adjustment Factor"],
        [
            ["Zone A (Tier 1 Metro)", "New York, San Francisco, London", "1.00x (baseline band)"],
            ["Zone B (Tier 2 Metro)", "Austin, Manchester, Toronto", "0.90x of baseline band"],
            ["Zone C (Tier 3 / Remote-First)", "Secondary cities, fully remote hires", "0.80x of baseline band"],
        ],
        [2.2*inch, 2.4*inch, 2.0*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "An employee who relocates from a higher-factor zone to a lower-factor zone retains their current base "
        "salary (no reduction), but future merit increases are calculated against the destination zone's band until "
        "pay converges naturally with the new zone's range.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Confidentiality of Compensation Information", styles["h1"]))
    s.append(Paragraph(
        "Individual compensation details are confidential between the employee, their manager, HR, and Payroll. "
        "Employees are, however, permitted under company policy and applicable pay-transparency law to discuss "
        "their own compensation with colleagues if they choose; no employee may be disciplined or retaliated "
        "against for doing so. Managers and HR staff who improperly disclose another employee's compensation "
        "details outside authorized business need are subject to disciplinary action.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "payroll", "salary_structure_bands_2026.pdf")
    build_pdf(
        filepath,
        "Enterprise Salary Band Structure & Salary Components",
        "FY 2026 Compensation Framework, Grade Distribution, and Pay Adjustment Guide",
        s
    )


def generate_bonus_payout_matrix():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Variable Compensation Program Governance", styles["h1"]))
    s.append(Paragraph(
        "The variable incentive plan rewards performance by sharing corporate success across three programs: the "
        "Quarterly Bonus Pool (all eligible employees), the Sales Incentive Plan (quota-carrying roles), and the "
        "Spot Recognition Award (manager-nominated, any time of year). Incentive pools are funded based on audited "
        "financial performance verified by external auditors following quarterly close.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Quarterly Bonus Disbursement Schedule", styles["h1"]))
    s.append(Paragraph("Incentive bonuses are calculated and paid out on strict quarterly schedules:", styles["body"]))
    s.append(Paragraph("• <b>Q1 Bonus (Jan 1 - Mar 31):</b> Disbursed May 15", styles["bullet"]))
    s.append(Paragraph("• <b>Q2 Bonus (Apr 1 - Jun 30):</b> Disbursed August 15", styles["bullet"]))
    s.append(Paragraph("• <b>Q3 Bonus (Jul 1 - Sep 30):</b> Disbursed November 15", styles["bullet"]))
    s.append(Paragraph("• <b>Q4 Bonus (Oct 1 - Dec 31):</b> Disbursed February 15 of the following year", styles["bullet"]))

    s.append(Paragraph("Section 3: Corporate EBITDA & Rating Multipliers", styles["h1"]))
    s.append(Paragraph("Final bonus payout is calculated using the formula: <code>Final Payout = Target Bonus x Corporate EBITDA Multiplier x Performance Multiplier</code>.", styles["body"]))
    s.append(make_table(
        ["Corporate EBITDA Achievement", "EBITDA Multiplier", "Individual Performance Rating", "Rating Multiplier"],
        [
            ["< 85% of Target", "0.0x (No Pool)", "Rating 1.0 - 2.0", "0.0x (Zero Payout)"],
            ["85% - 99% of Target", "0.8x", "Rating 3.0 (Meets Standards)", "1.0x"],
            ["100% - 110% of Target", "1.0x", "Rating 4.0 (Exceeds Standards)", "1.25x"],
            ["> 110% of Target", "1.3x (Cap)", "Rating 5.0 (Outstanding)", "1.50x"],
        ],
        [1.8*inch, 1.5*inch, 2.2*inch, 1.5*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 4: Numerical Worked Case Study", styles["h1"]))
    s.append(make_callout(
        "<b>Case Study Example:</b> Senior Specialist (Grade L3) with a base target bonus of $10,000 USD.<br/>"
        "If Corporate EBITDA reaches 105% (1.0x multiplier) and the employee achieves a Rating 4.0 (1.25x multiplier):<br/>"
        "<code>Payout = $10,000 x 1.0 x 1.25 = $12,500 USD gross</code>.",
        styles, bg_color="#F8FAFC", border_color="#CBD5E1"
    ))

    s.append(Paragraph("Section 5: Sales Incentive Plan (Quota-Carrying Roles)", styles["h1"]))
    s.append(Paragraph(
        "Sales roles are excluded from the standard quarterly bonus pool and instead earn commission under the "
        "Sales Incentive Plan: a base commission rate of 8% of closed net-new revenue up to 100% of quota, "
        "accelerating to 12% for revenue between 100-150% of quota, and 15% for revenue above 150% of quota. "
        "Commission is paid the month following invoice collection, not at deal signature.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Spot Recognition Awards & Referral Bonuses", styles["h1"]))
    s.append(Paragraph("• <b>Spot Award:</b> Any manager may nominate an employee for exceptional, time-bound contribution; awards of $250-$1,000 USD are approved by the manager's own manager and paid within 30 days.", styles["bullet"]))
    s.append(Paragraph("• <b>Employee Referral Bonus:</b> $2,000 USD for a successful referral hired into a standard role, $4,000 USD for a hard-to-fill technical or executive role, paid 50% at the new hire's 90-day mark and 50% at the 6-month mark.", styles["bullet"]))

    s.append(Paragraph("Section 7: Proration Rules for Mid-Cycle Joiners & Leavers", styles["h1"]))
    s.append(Paragraph(
        "Employees who join mid-quarter are eligible for a prorated bonus based on the number of complete calendar "
        "days employed during the quarter, provided they were active on the payroll for at least 30 days of that "
        "quarter. Employees who resign before the disbursement date forfeit any unpaid bonus for completed quarters "
        "unless local law requires otherwise; employees terminated without cause remain eligible for bonus earned "
        "through their last working day, paid on the standard quarterly schedule.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Bonus Clawback Conditions", styles["h1"]))
    s.append(Paragraph(
        "The company reserves the right to claw back a paid bonus, in whole or in part, in cases of confirmed "
        "financial restatement caused by employee misconduct, a finding of fraud connected to the metrics used to "
        "calculate the payout, or termination for cause within 90 days of disbursement where the cause relates "
        "directly to the performance being rewarded. Clawback determinations are made by the Executive Compensation "
        "Committee and communicated in writing with the specific basis for the decision.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Long-Term Incentive (Equity) Overview", styles["h1"]))
    s.append(Paragraph(
        "Grade L4 and above employees may additionally receive Restricted Stock Units (RSUs) as part of total "
        "compensation, vesting over 4 years with a 1-year cliff (25% at month 12, then ratably monthly thereafter). "
        "Equity grants are approved by the Board Compensation Committee annually and are governed by the separate "
        "Equity Incentive Plan document, not by this bonus matrix.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Department Funding Pool Allocation", styles["h1"]))
    s.append(Paragraph(
        "The company-wide bonus pool, once set by the EBITDA multiplier, is allocated to departments in proportion "
        "to each department's contribution to the achieved EBITDA and headcount-weighted target bonus exposure. "
        "Department heads may not reallocate more than 10% of their pool across sub-teams without Finance Business "
        "Partner sign-off, ensuring the individual performance-rating multipliers remain the primary driver of "
        "individual payout rather than manager discretion.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Tax Withholding on Bonus Payments", styles["h1"]))
    s.append(Paragraph(
        "Bonus payments are subject to statutory withholding at the applicable marginal tax rate for supplemental "
        "wages in the employee's jurisdiction, which may differ from the withholding rate applied to regular salary. "
        "Employees anticipating a large bonus payout are encouraged to review their annual withholding elections "
        "with Payroll ahead of the disbursement date to avoid under- or over-withholding at year-end.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Communication of Individual Payout Details", styles["h1"]))
    s.append(Paragraph(
        "Individual bonus statements, including the target bonus, applied EBITDA multiplier, applied rating "
        "multiplier, and resulting gross payout, are published to each employee's payslip portal at least 5 "
        "business days before the disbursement date so that questions can be routed to the HRBP before the payment "
        "is processed rather than after. Managers are briefed on their team's aggregate payout the week prior so "
        "they can field questions from direct reports with full context.",
        styles["body"]
    ))

    s.append(Paragraph("Section 13: Leave-of-Absence & Disability Impact on Bonus Eligibility", styles["h1"]))
    s.append(Paragraph(
        "Employees on approved paid leave (including maternity, paternity, or short-term disability) remain fully "
        "eligible for the quarterly bonus pool at their full target amount, unaffected by the leave; the leave "
        "period is treated as active service for bonus-eligibility purposes. Employees on approved unpaid leave "
        "exceeding 30 consecutive days in a quarter have that quarter's bonus prorated based on active days worked, "
        "consistent with the mid-cycle joiner/leaver proration described in Section 7.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Disputes about proration calculations are resolved by Payroll in consultation with the HRBP, with a "
        "written explanation of the calculation provided to the employee within 10 business days of the dispute "
        "being raised.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "payroll", "bonus_payout_matrix_2026.pdf")
    build_pdf(
        filepath,
        "Variable Compensation & Quarterly Bonus Matrix",
        "FY 2026 Guidelines for EBITDA Funding Pools, Sales Incentives, and Individual Performance Multipliers",
        s
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. BENEFITS
# ─────────────────────────────────────────────────────────────────────────────
def generate_health_insurance_plan():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Group Health Insurance Program (Policy #GHI-99201)", styles["h1"]))
    s.append(Paragraph(
        "The organization provides comprehensive group health insurance coverage underwritten by BlueShield "
        "Corporate Health. Coverage begins on the employee's official date of hire, with options to extend benefits "
        "to legal spouses, domestic partners, and dependent children under age 26 during the annual open enrollment "
        "window or within 30 days of a qualifying life event (marriage, birth, adoption, loss of other coverage).",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Coverage Tiers & Benefit Sub-Limits Matrix", styles["h1"]))
    s.append(Paragraph("Insurance benefits are structured into three distinct plan tiers based on employment category and grade:", styles["body"]))
    s.append(make_table(
        ["Coverage Tier", "Sum Insured Cap", "Maternity Sub-Limit", "Network Co-Pay %", "Room Rent Cap"],
        [
            ["Tier 1 (Individual)", "$10,000 / Year", "$3,500", "10%", "$250 / Day"],
            ["Tier 2 (Family Floater)", "$25,000 / Year", "$5,000", "10%", "$500 / Day"],
            ["Tier 3 (Executive Plan)", "$50,000 / Year", "$8,000", "0% (Nil)", "Suite / Actuals"],
        ],
        [1.4*inch, 1.4*inch, 1.4*inch, 1.4*inch, 1.4*inch],
        header_bg="#065F46",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 3: Waiting Periods, Co-Pay Rules & Exclusions", styles["h1"]))
    s.append(Paragraph("• <b>Pre-existing Conditions:</b> Covered after a mandatory waiting period of 24 months of continuous coverage.", styles["bullet"]))
    s.append(Paragraph("• <b>Non-Network Admissions:</b> Subject to a mandatory 20% co-payment by the insured employee.", styles["bullet"]))
    s.append(Paragraph("• <b>Pre/Post Hospitalization:</b> Expenses covered for 30 days prior to admission and 60 days post-discharge.", styles["bullet"]))
    s.append(Paragraph("• <b>Standard Exclusions:</b> Cosmetic procedures not medically necessary, self-inflicted injury, and treatment obtained outside the plan's recognized provider network without prior authorization.", styles["bullet"]))

    s.append(Paragraph("Section 4: Claim Settlement & Cashless Authorization Procedures", styles["h1"]))
    s.append(Paragraph(
        "For planned hospitalizations at network facilities, pre-authorization must be submitted at least 72 hours "
        "prior to admission. For emergency admissions, notification must reach the Third-Party Administrator (TPA) "
        "helpdesk within 24 hours of hospitalization. Reimbursement claims for non-network treatment must be filed "
        "within 30 days of discharge with original itemized bills.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Dental, Vision & Employee Assistance Program (EAP)", styles["h1"]))
    s.append(Paragraph("• <b>Dental:</b> Annual coverage up to $1,500 USD for preventive and basic restorative care; orthodontic coverage capped at $1,000 USD lifetime for dependents under 18.", styles["bullet"]))
    s.append(Paragraph("• <b>Vision:</b> Annual allowance of $250 USD toward eye exams, lenses, or frames.", styles["bullet"]))
    s.append(Paragraph("• <b>EAP:</b> Confidential access to up to 6 counseling sessions per issue per year, covering mental health, financial planning, and legal consultation, at no cost to the employee and not visible to the employer.", styles["bullet"]))

    s.append(Paragraph("Section 6: Wellness Program & Preventive Care Incentives", styles["h1"]))
    s.append(make_callout(
        "<b>Annual Wellness Incentive:</b> Employees who complete an annual preventive health screening and the "
        "wellness portal risk assessment qualify for a $200 USD reduction in their annual health-plan contribution, "
        "credited each January following the prior year's completion.",
        styles, bg_color="#ECFDF5", border_color="#A7F3D0"
    ))

    s.append(Paragraph("Section 7: Life & Accidental Death Insurance", styles["h1"]))
    s.append(Paragraph(
        "Every full-time employee is automatically enrolled in Group Term Life Insurance at 3x annual base salary "
        "(minimum $50,000 USD) at no cost to the employee, alongside Accidental Death & Dismemberment (AD&D) "
        "coverage at an equivalent sum insured. Employees may purchase Voluntary Supplemental Life Insurance for "
        "themselves or dependents at group rates through the annual open enrollment portal, up to 5x annual salary "
        "subject to evidence-of-insurability approval above 2x salary.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Continuation of Coverage After Separation (COBRA-Equivalent)", styles["h1"]))
    s.append(Paragraph(
        "Employees who separate from the company, and their covered dependents, may elect to continue group health "
        "coverage at their own cost for up to 18 months following the last day of active coverage, or up to 36 "
        "months for dependents losing eligibility due to divorce or the employee's death. Election must be made "
        "within 60 days of the qualifying event using the continuation election form provided by HR at separation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Annual Open Enrollment & Mid-Year Plan Changes", styles["h1"]))
    s.append(Paragraph(
        "Open enrollment runs each year from November 1 to November 20, with elections effective January 1. "
        "Outside this window, plan changes (adding a dependent, switching coverage tier, or dropping coverage) are "
        "permitted only within 30 days of a qualifying life event such as marriage, birth or adoption, divorce, or "
        "involuntary loss of other coverage, and must be filed with supporting documentation via the benefits "
        "portal.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Network Providers & Second Opinion Access", styles["h1"]))
    s.append(Paragraph(
        "The plan's network includes over 8,000 hospitals and clinics nationally through the BlueShield Corporate "
        "Health directory, searchable via the benefits portal. For any diagnosis involving a major surgical "
        "procedure or a critical illness, employees may request a fully covered second medical opinion from a "
        "network specialist without a new referral, in addition to their treating physician's recommendation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Grievance & Appeal of a Denied Claim", styles["h1"]))
    s.append(Paragraph(
        "An employee whose claim is denied, in part or in full, may file a written appeal with the TPA within 30 "
        "days of the denial notice, supported by any additional medical documentation. The TPA must issue a "
        "decision on the appeal within 15 business days for standard claims and within 72 hours for urgent claims "
        "involving ongoing treatment. If the appeal is denied, the employee may request a final independent medical "
        "review at no cost, coordinated by the People Benefits team.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: International Travel & Expatriate Medical Coverage", styles["h1"]))
    s.append(Paragraph(
        "Employees traveling internationally on company business are automatically covered under the Global Travel "
        "Medical Insurance rider for the duration of the trip, including emergency evacuation and repatriation "
        "coverage up to $250,000 USD, at no cost to the employee and with no interaction required with the base "
        "group health plan. Expatriate employees on a long-term international assignment (90+ days) are instead "
        "moved onto the dedicated Expatriate Health Plan, coordinated by Global Mobility, which mirrors the "
        "Executive Plan tier described in Section 2 regardless of the employee's home-country grade.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Employees should carry their digital insurance card, accessible via the benefits mobile app, whenever "
        "traveling, and should contact the 24/7 international assistance line before seeking treatment where "
        "medically feasible so that cashless arrangements can be made with the local provider.",
        styles["body"]
    ))

    s.append(Paragraph("Section 13: Dependent Eligibility Verification & Fraud Prevention", styles["h1"]))
    s.append(Paragraph(
        "During open enrollment and at the time a dependent is first added, the benefits team may request "
        "supporting documentation (marriage certificate, birth certificate, or adoption papers) to verify dependent "
        "eligibility. Employees are required to remove a dependent from coverage within 30 days of the dependent "
        "losing eligibility — for example, a spouse following divorce or a child aging out at 26 — and failure to "
        "do so may result in retroactive premium recovery and, in cases of deliberate misrepresentation, "
        "disciplinary action under the Code of Conduct.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Periodic dependent audits are conducted every 2 years across the full plan population, coordinated by the "
        "TPA, to keep the group risk pool accurate and to keep premium costs, which are partly borne by employees "
        "at higher coverage tiers, as low as possible for the whole workforce.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "benefits", "health_insurance_plan_2026.pdf")
    build_pdf(
        filepath,
        "Group Health Insurance Plan & Benefits Guide",
        "Policy Period 2026 | Coverage Limits, Co-Pay Terms, Ancillary Benefits, and Claim Guidelines",
        s
    )


def generate_pf_gratuity_policy():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Provident Fund (PF) Statutory Framework", styles["h1"]))
    s.append(Paragraph(
        "Employees contribute 12% of their Monthly Basic Salary toward the Employees' Provident Fund (EPF). The "
        "employer provides a matching contribution of 12%, divided as: 3.67% to EPF and 8.33% to the Employees' "
        "Pension Scheme (EPS), capped at $175 USD monthly. Employees may additionally opt into the Voluntary "
        "Provident Fund (VPF) at any contribution rate above the statutory 12%, up to 100% of Basic Salary.",
        styles["body"]
    ))
    s.append(Paragraph(
        "PF balances earn interest declared annually by the trustee board and are fully vested from day one — there "
        "is no service-based vesting schedule on the employee's own contribution. Employer contributions vest "
        "immediately as well, consistent with the statutory framework.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: National Pension Scheme (NPS) & Superannuation", styles["h1"]))
    s.append(Paragraph(
        "Grade L4 and above employees may additionally opt into the employer-co-funded National Pension Scheme, "
        "with the company matching up to 10% of Basic Salary annually, subject to the applicable tax-exemption "
        "ceiling. Superannuation fund contributions for L6 and above are handled separately under the executive "
        "retirement benefits addendum.",
        styles["body"]
    ))

    s.append(Paragraph("Section 3: Statutory Gratuity Formula & Numerical Case Study", styles["h1"]))
    s.append(Paragraph(
        "Gratuity is payable to an employee upon separation after rendering continuous service for a minimum of 4.8 "
        "years (5 years statutory threshold), except in cases of death or permanent disability, where the minimum "
        "service requirement is waived entirely.",
        styles["body"]
    ))
    s.append(make_callout(
        "<b>Statutory Calculation Formula:</b><br/>"
        "<code>Gratuity Amount = (15 x Last Drawn Monthly Basic Salary x Completed Years of Service) / 26</code>",
        styles, bg_color="#ECFDF5", border_color="#A7F3D0"
    ))
    s.append(Spacer(1, 8))
    s.append(Paragraph(
        "<b>Numerical Worked Example:</b><br/>"
        "For an employee with a last drawn basic salary of $6,000/month and 10 years of service:<br/>"
        "<code>Gratuity = (15 x $6,000 x 10) / 26 = $900,000 / 26 = $34,615.38 USD</code>.<br/>"
        "The maximum statutory tax-free gratuity ceiling is capped at $240,000 USD per employee.",
        styles["body"]
    ))

    s.append(Paragraph("Section 4: Nomination, Withdrawal & Settlement Timelines", styles["h1"]))
    s.append(Paragraph(
        "Every employee must file a PF and Gratuity nomination (Form NOM-1) within 30 days of joining, naming a "
        "family member as beneficiary. Full and final PF settlement is processed within 30 days of the claim being "
        "filed post-separation; gratuity is disbursed within 30 days of the employee's last working day, with "
        "interest accruing on any delay beyond that window as required by statute.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Partial Withdrawal & Advance Rules", styles["h1"]))
    s.append(Paragraph("Employees may apply for a partial, non-repayable PF advance under specific, documented circumstances:", styles["body"]))
    s.append(make_table(
        ["Purpose", "Minimum Service Required", "Maximum Withdrawable"],
        [
            ["Medical treatment (self/dependent)", "No minimum", "Up to 6x monthly wages or full employee share"],
            ["Home purchase / construction", "5 years", "Up to 90% of accumulated PF balance"],
            ["Higher education (self/child)", "7 years", "Up to 50% of employee share"],
            ["Marriage (self/sibling/child)", "7 years", "Up to 50% of employee share"],
        ],
        [2.4*inch, 2.0*inch, 2.6*inch],
        header_bg="#065F46",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 6: Tax Treatment of PF, NPS & Gratuity", styles["h1"]))
    s.append(Paragraph(
        "PF withdrawals after 5 years of continuous service are fully tax-exempt; withdrawals before 5 years are "
        "taxable as income in the year of withdrawal, with the exception of withdrawals due to permanent disability "
        "or company closure. NPS contributions up to the statutory ceiling qualify for an additional tax deduction "
        "beyond the standard PF deduction limit. Gratuity is tax-exempt up to the statutory ceiling described in "
        "Section 3; any amount above the ceiling is taxed as regular income.",
        styles["body"]
    ))

    s.append(Paragraph("Section 7: Forfeiture Conditions", styles["h1"]))
    s.append(Paragraph(
        "Gratuity may be wholly or partially forfeited only where an employee's service is terminated for "
        "proven acts of willful misconduct, riotous behavior, or an offense involving moral turpitude committed "
        "during the course of employment, and only after the employee has been given a documented opportunity to "
        "respond. PF balances, by contrast, are never forfeited regardless of the reason for separation, as they "
        "represent the employee's own vested savings.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Transfer of PF Account on Change of Employer", styles["h1"]))
    s.append(Paragraph(
        "Employees joining from a previous employer's PF scheme may transfer their existing balance into the "
        "company's PF trust within 6 months of joining using the standard inter-trust transfer form, preserving "
        "continuity of service for the 5-year tax-exemption threshold. The People Operations payroll team "
        "coordinates directly with the previous employer's trust administrator once the transfer request is filed.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Death-in-Service Benefit Coordination", styles["h1"]))
    s.append(Paragraph(
        "In the event of death while in service, the nominated beneficiary receives the full accumulated PF "
        "balance, the EPS pension benefit, gratuity calculated without regard to the 5-year minimum service "
        "threshold, and the Group Term Life Insurance payout described in the Health Insurance Plan, coordinated "
        "as a single settlement package by a dedicated HR case owner assigned within 3 business days of "
        "notification.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Annual Statement & Self-Service Access", styles["h1"]))
    s.append(Paragraph(
        "Every employee can view a real-time PF and NPS balance, contribution history, and nominee details through "
        "the retirement benefits self-service portal, refreshed monthly following payroll close. An annual "
        "consolidated statement — covering PF contributions, interest credited, NPS contributions and fund "
        "performance, and projected gratuity accrual to date — is issued each April for the preceding financial "
        "year, and employees are encouraged to review nominee details whenever a major life event (marriage, birth, "
        "divorce) occurs rather than waiting for the annual cycle.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Employer Compliance & Audit Obligations", styles["h1"]))
    s.append(Paragraph(
        "The company remits its own and the employee's PF contribution to the statutory trust by the 15th of the "
        "following month without exception, and any late remittance triggers a statutory penal interest charge "
        "borne entirely by the company, never passed on to the employee. An independent actuarial audit of the PF "
        "and gratuity trust is conducted annually, and the audited report is made available to the works council or "
        "employee representative body upon request, consistent with statutory transparency requirements.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Any employee who believes their PF or gratuity contribution has been miscalculated may request a "
        "line-item reconciliation from Payroll, which must be provided within 10 business days showing the exact "
        "basic-salary figure, contribution rate, and running balance used in the calculation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Frequently Encountered Calculation Scenarios", styles["h1"]))
    s.append(make_table(
        ["Scenario", "How It Is Handled"],
        [
            ["Employee served 4 years 9 months, then resigns", "Rounded up to 5 years under the 4.8-year rule; full gratuity applies"],
            ["Basic salary changed mid-final-year via promotion", "Last drawn basic salary at separation date is used, not an average"],
            ["Employee moves from contractor to full-time mid-career", "Gratuity service count starts from full-time conversion date unless offer letter states otherwise"],
            ["Employee dies in service after 2 years", "5-year minimum waived; full gratuity paid to nominee"],
        ],
        [3.0*inch, 3.6*inch],
        header_bg="#065F46",
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "Any scenario not captured above is escalated to the Total Rewards team for a documented ruling, which is "
        "then added to this internal scenario library to keep future calculations consistent across the "
        "organization.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "benefits", "pf_and_gratuity_policy.pdf")
    build_pdf(
        filepath,
        "Provident Fund (PF), NPS & Statutory Gratuity Rules",
        "Statutory Calculation Formulas, Eligibility Cutoffs, and Tax Exemption Limits",
        s
    )


# ─────────────────────────────────────────────────────────────────────────────
# 4. LEGAL & LABOUR
# ─────────────────────────────────────────────────────────────────────────────
def generate_maternity_paternity_policy():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Paid Maternity Leave Schedule", styles["h1"]))
    s.append(Paragraph(
        "Female employees who have completed at least 80 days of service in the preceding 12 months are entitled to "
        "26 weeks (182 calendar days) of fully paid maternity leave.",
        styles["body"]
    ))
    s.append(Paragraph("• A maximum of 8 weeks can be taken prior to the expected delivery date; the remaining 18 weeks are taken post-delivery.", styles["bullet"]))
    s.append(Paragraph("• For employees having 2 or more surviving children, paid maternity leave entitlement is 12 weeks, with a maximum of 6 weeks pre-delivery.", styles["bullet"]))
    s.append(Paragraph("• Employees experiencing a miscarriage or medical termination of pregnancy are entitled to 6 weeks of paid leave immediately following the event.", styles["bullet"]))

    s.append(Paragraph("Section 2: Adoption & Commissioning (Surrogacy) Leave", styles["h1"]))
    s.append(Paragraph(
        "A commissioning mother (through surrogacy) or an employee legally adopting a child below the age of 3 "
        "months is entitled to 12 weeks of fully paid leave from the date the child is handed over to the employee.",
        styles["body"]
    ))

    s.append(Paragraph("Section 3: Paternity Leave Policy", styles["h1"]))
    s.append(Paragraph(
        "Eligible male employees receive 2 weeks (10 business days) of fully paid paternity leave, which must be "
        "utilized within 6 months of the child's birth or adoption date. Leave may be split into two blocks with "
        "manager approval.",
        styles["body"]
    ))

    s.append(Paragraph("Section 4: Post-Maternity Support & Return-to-Work Provisions", styles["h1"]))
    s.append(Paragraph("• <b>Creche Benefit:</b> Employees with children under age 6 may access the company-empanelled creche facility, or a monthly reimbursement of $150 USD where no facility is available locally.", styles["bullet"]))
    s.append(Paragraph("• <b>Nursing Breaks:</b> Two paid 30-minute nursing breaks per workday for 12 months following the return-to-work date.", styles["bullet"]))
    s.append(Paragraph("• <b>Phased Return:</b> Returning employees may request up to 8 weeks of remote or reduced-hours work, subject to role eligibility, without loss of grade or pay.", styles["bullet"]))
    s.append(Paragraph("• <b>Written Intimation:</b> The employer must communicate available benefits in writing at the time the employee proceeds on maternity leave, per statutory requirement.", styles["bullet"]))

    s.append(Paragraph("Section 5: Job Protection & Prohibition on Dismissal", styles["h1"]))
    s.append(Paragraph(
        "It is unlawful to dismiss or vary the terms of employment of a woman to her disadvantage on account of "
        "pregnancy, maternity leave, or related medical absence. Any termination during the protected period "
        "requires documented, non-pregnancy-related cause and mandatory review by the CHRO's office before it can "
        "take effect.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Medical Bonus & Prenatal Care Support", styles["h1"]))
    s.append(Paragraph(
        "Employees who do not receive free prenatal and postnatal care through the group health plan's maternity "
        "sub-limit are entitled to a one-time medical bonus of $500 USD, disbursed with the first maternity-leave "
        "payroll cycle. Employees are additionally granted paid time off for a minimum of 6 antenatal medical "
        "appointments during the pregnancy without deduction from standard sick or casual leave balances.",
        styles["body"]
    ))

    s.append(Paragraph("Section 7: Notification & Documentation Requirements", styles["h1"]))
    s.append(Paragraph(
        "Employees intending to take maternity leave must notify their manager and HR in writing at least 8 weeks "
        "before the expected leave start date, accompanied by a physician's certificate confirming the expected "
        "delivery date. Paternity and adoption leave requests require at least 2 weeks' notice along with the "
        "relevant birth, adoption, or surrogacy documentation. Late notice arising from a medical emergency is "
        "accommodated retroactively upon submission of supporting medical documentation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Interaction With Other Leave Types", styles["h1"]))
    s.append(Paragraph(
        "Maternity and paternity leave run concurrently with, not in addition to, any applicable statutory family "
        "and medical leave entitlement in the employee's jurisdiction, with the employee receiving whichever "
        "combination of pay and duration is more generous. Accrued vacation and sick leave continue to accrue "
        "during paid maternity and paternity leave and may be used to extend the leave period once statutory paid "
        "leave is exhausted, subject to manager approval.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Crèche Reimbursement & Extended Family Care Leave", styles["h1"]))
    s.append(make_table(
        ["Benefit", "Eligibility", "Value / Duration"],
        [
            ["Crèche reimbursement", "Employees with children under 6", "$150 USD/month, up to 36 months"],
            ["Extended unpaid family leave", "1+ year of continuous service", "Up to 90 additional unpaid days"],
            ["Elder / dependent care leave", "All employees", "5 paid days per calendar year"],
        ],
        [2.2*inch, 2.4*inch, 2.4*inch],
        header_bg="#7C2D12",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 10: Manager Obligations & Confidentiality", styles["h1"]))
    s.append(Paragraph(
        "Managers receiving notice of an employee's pregnancy or intended parental leave must keep the information "
        "confidential outside the immediate need-to-know group (HR and, where relevant, the employee's designated "
        "backup), must not factor the leave into performance ratings or project staffing decisions in a way that "
        "disadvantages the employee, and are required to complete a documented transition plan with the employee "
        "at least 4 weeks before the leave start date.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Statutory Basis & Employer Record-Keeping Obligations", styles["h1"]))
    s.append(Paragraph(
        "This policy is administered consistently with applicable maternity benefit and family leave statute in "
        "each jurisdiction where the company operates, and the more generous of the statutory or company-policy "
        "entitlement always applies. HR maintains a leave register for every maternity, paternity, and adoption "
        "leave case, recording notice date, leave start and end dates, pay disbursed, and return-to-work "
        "confirmation, retained for the statutory record-keeping period applicable in that jurisdiction (typically "
        "not less than 3 years).",
        styles["body"]
    ))
    s.append(Paragraph(
        "Managers found to have discouraged an employee from taking their full statutory entitlement, whether "
        "explicitly or through informal pressure, are subject to disciplinary action under the Progressive "
        "Disciplinary Policy Framework, and the matter is reported to the CHRO's office regardless of whether the "
        "affected employee files a formal grievance.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Frequently Encountered Scenarios", styles["h1"]))
    s.append(make_table(
        ["Scenario", "Applicable Provision"],
        [
            ["Employee's due date shifts and she wants to start leave later", "Permitted with updated physician certificate; total entitlement unchanged"],
            ["Second child born within 2 years of first", "12-week entitlement applies (2+ surviving children rule)"],
            ["Same-sex couple, one partner gives birth", "Birthing partner receives maternity leave; other partner receives paternity leave"],
            ["Contractor becomes pregnant mid-contract", "Statutory minimum applies per local law; company policy applies only after conversion to employee"],
        ],
        [2.8*inch, 3.8*inch],
        header_bg="#7C2D12",
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "Scenarios not explicitly covered above are escalated to the HRBP for a documented determination, referencing "
        "both this policy and the statutory framework applicable in the employee's work location, and the "
        "determination is logged for consistency in future similar cases.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "legal_labour", "maternity_and_paternity_leave_policy.pdf")
    build_pdf(
        filepath,
        "Maternity & Paternity Benefit Policy Guidelines",
        "Statutory Entitlements, Adoption & Surrogacy Leave, and Return-to-Work Provisions",
        s
    )


# ─────────────────────────────────────────────────────────────────────────────
# 5. TALENT — Recruitment & Learning
# ─────────────────────────────────────────────────────────────────────────────
def generate_recruitment_onboarding_policy():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Requisition Approval & Sourcing Governance", styles["h1"]))
    s.append(Paragraph(
        "Every open role requires an approved headcount requisition (Form REQ-200) signed by the hiring manager and "
        "the relevant VP before Talent Acquisition begins sourcing. Requisitions above Grade L5 additionally require "
        "CFO sign-off given the compensation impact. Roles are posted internally for a minimum of 5 business days "
        "before external sourcing begins, consistent with the internal mobility priority policy.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Interview Process & Structured Evaluation", styles["h1"]))
    s.append(Paragraph(
        "All candidates progress through a structured interview loop calibrated by role family: a recruiter "
        "screen, a hiring-manager screen, a skills or technical assessment, and a panel loop of 3-4 interviewers "
        "scoring independently against a shared rubric before any group discussion. Interviewers submit scorecards "
        "within 24 hours of the interview to reduce recall bias.",
        styles["body"]
    ))
    s.append(make_table(
        ["Stage", "Typical Duration", "Owner", "Pass Criteria"],
        [
            ["Recruiter Screen", "30 minutes", "Talent Acquisition Partner", "Role fit, compensation alignment, logistics"],
            ["Hiring Manager Screen", "45 minutes", "Hiring Manager", "Motivation, experience depth"],
            ["Skills Assessment", "60-90 minutes", "Subject-matter panel", "Threshold score per role rubric"],
            ["Panel / Onsite Loop", "3-4 hours", "Cross-functional panel", "Majority recommend-to-hire"],
            ["Final / Bar-Raiser", "45 minutes", "Senior leader outside team", "Independent go/no-go"],
        ],
        [1.5*inch, 1.3*inch, 1.8*inch, 2.4*inch],
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 3: Offer Approval, Background Screening & Pre-Boarding", styles["h1"]))
    s.append(Paragraph(
        "Compensation offers are generated from the approved salary band (see Salary Structure Bands) and require "
        "Compensation Committee approval for any offer above the band midpoint. Offers are contingent on successful "
        "completion of background screening, covering identity verification, prior employment confirmation, and "
        "education verification; criminal background checks are conducted only where legally permitted and role-relevant.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Pre-boarding begins immediately upon offer acceptance: IT provisions accounts and equipment, HR issues "
        "statutory new-hire paperwork, and the assigned onboarding buddy is notified, all completed at least 3 "
        "business days before the new hire's start date.",
        styles["body"]
    ))

    s.append(Paragraph("Section 4: The 30-60-90 Day Onboarding Framework", styles["h1"]))
    s.append(Paragraph("New hires and their managers jointly track integration against a structured 30-60-90 day plan:", styles["body"]))
    s.append(Paragraph("• <b>Day 1-30 (Learn):</b> Complete mandatory compliance training, meet key stakeholders, understand team processes and tooling, and complete the first 1:1 with the HRBP.", styles["bullet"]))
    s.append(Paragraph("• <b>Day 31-60 (Contribute):</b> Take ownership of first assigned deliverables, participate fully in team rituals, and complete the 30-day check-in survey.", styles["bullet"]))
    s.append(Paragraph("• <b>Day 61-90 (Deliver):</b> Operate independently on core responsibilities, set goals for the next two quarters with the manager, and complete the probation-closing review.", styles["bullet"]))
    s.append(make_callout(
        "<b>Onboarding Buddy Program:</b> Every new hire is paired with a peer buddy (minimum 6 months' tenure, not "
        "their manager) for the first 90 days to accelerate social and cultural integration.",
        styles, bg_color="#EFF6FF", border_color="#93C5FD"
    ))

    s.append(Paragraph("Section 5: Probation Confirmation & Early Attrition Review", styles["h1"]))
    s.append(Paragraph(
        "Probation confirmation follows the milestone evaluations described in the Employee Handbook (Day 30, 60, "
        "85). Any voluntary or involuntary exit within the first 6 months triggers a mandatory early-attrition "
        "review by Talent Acquisition to identify sourcing, interview, or expectation-setting gaps.",
        styles["body"]
    ))

    s.append(Paragraph("Section 6: Internal Referral & Employee Value Proposition", styles["h1"]))
    s.append(Paragraph(
        "Employees are encouraged to refer qualified candidates through the internal referral portal; referral "
        "eligibility and payout amounts are governed by the Bonus Payout Matrix. Recruiters are expected to present "
        "candidates with a consistent Employee Value Proposition covering compensation philosophy, benefits, "
        "learning investment, and flexible-work options, avoiding verbal commitments that are not reflected in the "
        "written offer letter.",
        styles["body"]
    ))

    s.append(Paragraph("Section 7: Diversity Sourcing & Fair Hiring Commitments", styles["h1"]))
    s.append(Paragraph(
        "For every open requisition, Talent Acquisition maintains a documented sourcing plan that includes at least "
        "one diverse slate channel appropriate to the role and location. Interview panels for Grade L4 and above "
        "roles must include at least one panelist from outside the hiring manager's immediate function to reduce "
        "in-group bias. Compensation offers are benchmarked strictly against the approved salary band and the "
        "candidate's assessed level, never against a candidate's prior salary alone, to avoid perpetuating "
        "historical pay disparities.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Contractor-to-Employee Conversion", styles["h1"]))
    s.append(Paragraph(
        "Fixed-term contractors converting to full-time employment undergo an abbreviated interview loop (hiring "
        "manager screen and a single panel round) rather than the full external process, and their prior contract "
        "tenure is not counted toward full-time service-length calculations for leave accrual or gratuity purposes "
        "unless explicitly stated in the conversion offer letter.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: Candidate Data Privacy & Retention", styles["h1"]))
    s.append(Paragraph(
        "Candidate resumes, interview scorecards, and assessment results are retained for 24 months following the "
        "close of a requisition to support future re-engagement and to defend against potential hiring disputes, "
        "after which they are automatically purged from the applicant tracking system. Candidates may request "
        "earlier deletion of their data by emailing the privacy inbox, and such requests are honored within 30 days "
        "except where retention is required by an active legal matter.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Rejection Communication & Candidate Experience Standards", styles["h1"]))
    s.append(Paragraph(
        "Every candidate who reaches the panel-interview stage receives a personalized rejection communication "
        "within 5 business days of the final hiring decision, including where feasible one constructive area of "
        "feedback. Candidates rejected at the resume-screen stage receive an automated but professionally worded "
        "notification within 10 business days. Recruiters track time-to-first-response and time-to-decision "
        "metrics, reviewed monthly to identify bottlenecks in the pipeline.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Roles & Responsibilities Summary", styles["h1"]))
    s.append(make_table(
        ["Stakeholder", "Primary Responsibility"],
        [
            ["Hiring Manager", "Define role, participate in interviews, make final hire decision"],
            ["Talent Acquisition Partner", "Source candidates, manage pipeline, coordinate offer"],
            ["HRBP", "Compensation guidance, statutory paperwork, probation tracking"],
            ["IT / Workplace Ops", "Equipment provisioning, system access, desk setup"],
            ["Onboarding Buddy", "Peer support and cultural integration for first 90 days"],
        ],
        [2.4*inch, 4.2*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))

    filepath = os.path.join(DATA_DIR, "talent", "recruitment_and_onboarding_policy.pdf")
    build_pdf(
        filepath,
        "Recruitment, Interviewing & New Hire Onboarding Policy",
        "Version 2026.1 | Requisition Governance, Structured Interviewing, and the 30-60-90 Day Framework",
        s
    )


def generate_learning_development_policy():
    styles = get_custom_styles()
    s = []

    s.append(Paragraph("Section 1: Learning & Development Philosophy", styles["h1"]))
    s.append(Paragraph(
        "The company invests in continuous employee growth through a blended model of formal training, on-the-job "
        "stretch assignments, mentorship, and external certification support. The People Development team publishes "
        "a refreshed catalog of internal courses each quarter, mapped to the competency framework used in the "
        "annual performance appraisal.",
        styles["body"]
    ))

    s.append(Paragraph("Section 2: Individual Learning Budget & Reimbursement", styles["h1"]))
    s.append(make_table(
        ["Grade Band", "Annual Learning Budget", "Conference / Certification Cap", "Approval Required"],
        [
            ["L1 - L2", "$1,000 USD", "$500 USD per item", "Manager"],
            ["L3 - L4", "$2,000 USD", "$1,200 USD per item", "Manager"],
            ["L5 - L6", "$3,500 USD", "$2,500 USD per item", "Department VP"],
            ["L7", "$5,000 USD", "No per-item cap", "CEO office"],
        ],
        [1.4*inch, 1.8*inch, 2.0*inch, 1.8*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))
    s.append(Paragraph(
        "Unused learning budget does not carry over to the following calendar year. Reimbursement claims must be "
        "filed under expense code EXP-LND-330 within 30 days of course or exam completion, accompanied by a "
        "certificate or attendance confirmation.",
        styles["body"]
    ))

    s.append(Paragraph("Section 3: Mandatory Compliance Training", styles["h1"]))
    s.append(Paragraph(
        "All employees must complete the following training within 30 days of hire and annually thereafter: "
        "Code of Conduct & Ethics, Anti-Harassment & Anti-Discrimination, Information Security Awareness, and "
        "Data Privacy Fundamentals. People-managers additionally complete Manager Essentials training within their "
        "first 90 days of assuming direct reports. Completion rates are reported to the Executive People Committee "
        "quarterly, and overdue training is escalated to the employee's manager after a 15-day grace period.",
        styles["body"]
    ))

    s.append(Paragraph("Section 4: Tuition Assistance for Degree & Certification Programs", styles["h1"]))
    s.append(Paragraph(
        "Employees with at least 1 year of continuous service may apply for tuition assistance toward a "
        "job-relevant degree or professional certification, reimbursed up to $5,250 USD per calendar year upon "
        "successful completion (grade C or above, or pass/fail equivalent). Employees who resign within 12 months "
        "of receiving tuition assistance repay a prorated portion under the standard training-bond schedule.",
        styles["body"]
    ))

    s.append(Paragraph("Section 5: Internal Mobility, Mentorship & Leadership Development", styles["h1"]))
    s.append(Paragraph("• <b>Internal Mobility:</b> Employees in their current role for 12+ months may apply to internal postings without requiring current-manager pre-approval to apply, though a transition conversation is expected before offer.", styles["bullet"]))
    s.append(Paragraph("• <b>Mentorship Program:</b> Voluntary pairing of employees with senior mentors outside their reporting line, running in structured 6-month cohorts twice a year.", styles["bullet"]))
    s.append(Paragraph("• <b>Leadership Development Track:</b> Grade L4+ employees identified in succession planning attend a structured 9-month leadership program combining coaching, 360-degree feedback, and a capstone business project reviewed by the executive team.", styles["bullet"]))

    s.append(Paragraph("Section 6: Skills Framework & Learning Paths by Function", styles["h1"]))
    s.append(make_table(
        ["Function", "Core Competencies Assessed", "Recommended Learning Path"],
        [
            ["Engineering", "System design, code quality, incident response", "Technical Ladder Track (self-paced + quarterly workshop)"],
            ["Sales & Customer Success", "Consultative selling, negotiation, account planning", "Sales Excellence Certification (external, company-funded)"],
            ["People Management", "Coaching, delegation, difficult conversations", "Manager Essentials + ongoing Manager Forum"],
            ["Finance & Operations", "Financial modeling, process excellence, risk controls", "FP&A Bootcamp + Lean Six Sigma Green Belt"],
        ],
        [1.6*inch, 2.6*inch, 2.6*inch],
        header_bg="#0F172A",
    ))
    s.append(Spacer(1, 10))

    s.append(Paragraph("Section 7: Manager Responsibilities in Employee Development", styles["h1"]))
    s.append(Paragraph(
        "Every manager is expected to hold at least one dedicated career-development conversation with each direct "
        "report per quarter, separate from routine work status check-ins, and to document agreed development actions "
        "in the performance system. Managers approving learning-budget spend are responsible for confirming the "
        "activity is role-relevant; approvals for clearly non-role-relevant spend may be reversed by Finance during "
        "quarterly expense audits.",
        styles["body"]
    ))

    s.append(Paragraph("Section 8: Measuring Learning & Development Effectiveness", styles["h1"]))
    s.append(Paragraph(
        "The People Development team tracks four core metrics each quarter: learning-budget utilization rate by "
        "function, completion rate for mandatory compliance training, internal-mobility fill rate (percentage of "
        "open roles filled by internal candidates), and post-training satisfaction scores collected via a "
        "standardized survey within 2 weeks of course completion. Results are reviewed with the Executive People "
        "Committee each quarter and inform the following year's catalog and budget planning.",
        styles["body"]
    ))

    s.append(Paragraph("Section 9: External Conference & Speaking Engagement Policy", styles["h1"]))
    s.append(Paragraph(
        "Employees invited to speak at an external industry conference on company-related work may request "
        "sponsorship of travel and registration costs in addition to their standard learning budget, subject to "
        "Corporate Communications review of any public-facing materials at least 10 business days before the event. "
        "Attendance as a non-speaking delegate draws from the employee's standard annual learning budget described "
        "in Section 2.",
        styles["body"]
    ))

    s.append(Paragraph("Section 10: Succession Planning & High-Potential Identification", styles["h1"]))
    s.append(Paragraph(
        "Each function conducts an annual talent review identifying high-potential employees and at least one "
        "identified successor for every Grade L5+ role. High-potential designation is communicated to the employee "
        "along with a tailored development plan, and is reassessed annually rather than treated as a permanent "
        "label; the designation itself carries no automatic compensation change but is a key input into promotion "
        "and stretch-assignment decisions.",
        styles["body"]
    ))

    s.append(Paragraph("Section 11: Learning Technology Platform & Access", styles["h1"]))
    s.append(Paragraph(
        "All employees have unlimited access to the enterprise learning platform, which hosts self-paced technical "
        "courses, leadership content, and compliance modules from a mix of internal subject-matter experts and "
        "licensed third-party providers. Course completions sync automatically to the employee's learning record "
        "and are visible to the employee's manager to support development-conversation planning; they are not "
        "visible to other employees or used in performance calibration beyond the mandatory compliance completion "
        "metric described in Section 3.",
        styles["body"]
    ))

    s.append(Paragraph("Section 12: Cross-Functional Rotation & Stretch Assignments", styles["h1"]))
    s.append(Paragraph(
        "Employees with 18+ months of tenure in their current function may apply for a structured 3-to-6-month "
        "cross-functional rotation, subject to both the sending and receiving manager's agreement and business "
        "continuity coverage for the sending team. Rotations are documented with clear success criteria agreed "
        "upfront, and the employee's grade and base compensation are unaffected during the rotation regardless of "
        "the receiving team's typical band for that type of work.",
        styles["body"]
    ))
    s.append(Paragraph(
        "Stretch assignments — temporary expanded scope without a formal rotation or role change — are the most "
        "commonly used development lever and are logged in the performance system so they are visible during "
        "promotion and calibration discussions, ensuring employees receive credit for expanded contribution even "
        "before a formal title change.",
        styles["body"]
    ))

    filepath = os.path.join(DATA_DIR, "talent", "learning_and_development_policy.pdf")
    build_pdf(
        filepath,
        "Learning & Development and Tuition Assistance Policy",
        "Version 2026.1 | Learning Budgets, Mandatory Compliance Training, and Career Growth Pathways",
        s
    )


def generate_all_pdfs():
    print("Starting Enterprise HR & Management PDF Generation...")
    generate_employee_handbook()
    generate_performance_grievance_policy()
    generate_code_of_conduct_policy()
    generate_salary_structure_bands()
    generate_bonus_payout_matrix()
    generate_health_insurance_plan()
    generate_pf_gratuity_policy()
    generate_maternity_paternity_policy()
    generate_recruitment_onboarding_policy()
    generate_learning_development_policy()
    print("All 10 HR & Enterprise Management PDFs successfully generated!")


if __name__ == "__main__":
    generate_all_pdfs()