
"""Authoritative MVP service categories and owning departments."""

DEPARTMENTS = {
    "SEC": ("Security", "Campus security, safety incidents and threats."),
    "ICT": ("ICT Services", "University technology, portal and connectivity support."),
    "MNT": ("Maintenance", "Facilities, electrical, plumbing and repair work."),
    "HST": ("Hostel Management", "Accommodation and hostel administration."),
    "HLT": ("Health Services", "Privacy-sensitive health support requests."),
    "CYB": ("Cybersecurity", "Phishing, scams and cyber incident reports."),
    "ADM": ("Student & Administrative Services", "Student services and administrative requests."),
    "LAF": ("Lost & Found", "Controlled lost property coordination."),
}

# (name, slug, department code, sensitive)
CATEGORIES = [
    # Security
    ("Theft, threat or suspicious activity", "security-incident", "SEC", False),
    ("Unauthorized entry or safety hazard", "security-hazard", "SEC", False),
    ("Harassment, intimidation or physical assault", "security-harassment-assault", "SEC", True),
    ("Missing property or security-related loss", "security-property-loss", "SEC", False),

    # ICT and cybersecurity
    ("Wi-Fi, university portal or email problem", "ict-support", "ICT", False),
    ("Computer, printer or software support", "ict-equipment", "ICT", False),
    ("Account compromise or unauthorized account access", "ict-account-security", "CYB", True),
    ("Phishing, scam, impersonation or suspicious link", "cybersecurity-report", "CYB", False),

    # Maintenance
    ("Electrical, lighting or power problem", "maintenance-electrical", "MNT", False),
    ("Water, plumbing, door, furniture or building repair", "maintenance-facility", "MNT", False),
    ("Toilet, sanitation, waste or environmental cleanliness", "maintenance-sanitation", "MNT", False),
    ("Damaged classroom, lecture hall or laboratory facility", "maintenance-academic-facility", "MNT", False),

    # Hostel
    ("Hostel allocation, transfer or accommodation concern", "hostel-accommodation", "HST", False),
    ("Hostel environment, noise or conduct concern", "hostel-welfare", "HST", False),

    # Health
    ("Health support or medical assistance", "health-request", "HLT", True),
    ("Public health, unsafe water or sanitation concern", "health-environment", "HLT", True),

    # Academic and administration
    ("Course registration, result or academic department request", "academic-request", "ADM", False),
    ("Timetable, examination or lecture-related administrative issue", "academic-administration", "ADM", False),
    ("General student service or administrative complaint", "administrative-request", "ADM", False),
    ("Accessibility or campus facility access concern", "accessibility-concern", "ADM", False),

    # Lost and found
    ("Lost or found student property", "lost-found-property", "LAF", False),
]
