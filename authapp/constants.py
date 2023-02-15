
USER_TYPES = [
    ('PUBLIC USER', 'PUBLIC USER'),
    ('INTERNAL STAFF', 'INTERNAL STAFF'),
    ('ORGANIZATION', 'ORGANIZATION'),
    ('PROFESSIONAL', 'PROFESSSIONAL')
]

ROLES = [
    ("BOOKING MANAGER", "BOOKING MANAGER"),
    ("FINANCE OFFICER", "FINANCE OFFICER"),
    ("CUSTOMER CARE", "CUSTOMER CARE"),
    ("ICT OFFICER", "ICT OFFICER"),
    ("BOOKING OFFICER", "BOOKING OFFICER"),
    ("GENERAL MANAGER", "GENERAL MANAGER"),
    ("DIRECTOR", "DIRECTOR"),
    ("GENERAL STAFF", "GENERAL STAFF"),
    ("CEO", "CEO")
]

PROFESSIONAL_ACCOUNTS = [
    ("DRIVER", "DRIVER"),
    ("TRANSLATOR", "TRANSLATOR"),
    ("TOUR GUIDE", "TOUR GUIDE"),
    ("CONSULTANT", "CONSULTANT")
]

INDUSTRY_TYPES = [
    ("HOSPITALITY", "HOSPITALITY"),
    ("TRAVEL AND TOURS", "TRAVEL AND TOURS"),
    ("TRANSPORTATION", "TRANSPORTATION")
]

ALL_ROLES = [
    "ICT OFFICER",
    "DIRECTOR",
    "DATA CLERK",
    "TOUR GUIDE"
]

DEPARTMENT_HEADS_ROLES = [
    "CHIEF ICT OFFICER",
    "GENERAL MANAGER",
    "CHIEF CUSTOMER CARE OFFICER",
    "CEO"
]

SYSTEM_ADMINS_ROLES = [
    "ICT OFFICER"
]

DATA_ENTRY_ROLES = [
    "DATA CLERK"
]


DEPARTMENTS_ROLES_DATA = [
    {
        "department":"ICT",
        "department_head":"CHIEF ICT OFFICER",
        "department_roles":[
            "ICT OFFICER",
            "DATA CLERK",
            "DEVELOPER"
        ]
    },
    {
        "department":"CUSTOMER CARE",
        "department_head":"CHIEF CUSTOMER CARE OFFICER",
        "department_roles":[
            "CHIEF CUSTOMER CARE OFFICER"
            "CUSTOMER CARE",
            "CALL CENTER OFFICERS"
        ]
    },
    {
        "department":"EXECUTIVE",
        "department_head":"GENERAL MANAGER",
        "department_roles":[
            "CEO",
            "FINANCE OFFICER",
            "DIRECTOR",
            "CHIEF CUSTOMER CARE OFFICER",
            "BOOKING MANAGER",
            "CHIEF ICT OFFICER"
        ]
    },
    {
        "department":"BOOKING",
        "department_head":"BOOKING MANAGER",
        "department_roles":[
            "BOOKING MANAGER",
            "BOOKING OFFICER",
            "BOOKING ASSISTANT"
        ]
    },
    {
        "department":"BUSINESS AND MARKETING",
        "department_head":"CEO",
        "department_roles":[
            "MARKETING OFFICER",
            "FIELD OFFICER",
            "CASUAL"
        ]
    }
]


