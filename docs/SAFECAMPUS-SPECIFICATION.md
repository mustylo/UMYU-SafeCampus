UMYU SafeCampus

One Platform for a Safer, Smarter and More Secure Campus

Project Type: Campus Safety, Service Management, Communication and Cybersecurity Platform
Target Environment: Umaru Musa Yar'adua University (UMYU)
Primary Users: Students, Staff, Department Officers, Department Heads, Super Administrators and Authorized Field Workers
Technology Direction: Python + Flask + PostgreSQL + SQLAlchemy + HTML/CSS/JavaScript
Development Environment: Termux/Linux during development, with the ability to continue on Windows/PC
Project Repository: UMYU-SafeCampus
Specification Status: Official baseline specification for development

---

1. PROJECT OVERVIEW

1.1 What is UMYU SafeCampus?

UMYU SafeCampus is a centralized digital platform designed to help students and university staff report, manage, track and resolve campus-related problems through a structured workflow.

Instead of a student having to search for the correct officer, department, technician, security personnel, health worker or administrator, SafeCampus allows the user to submit a case through one platform.

The system then helps route the case to the appropriate department and authorized personnel.

The core workflow is:

REPORT
   ↓
ROUTE
   ↓
REVIEW
   ↓
ASSIGN
   ↓
COMMUNICATE
   ↓
ACT
   ↓
VERIFY
   ↓
RESOLVE
   ↓
CLOSE
   ↓
AUDIT

SafeCampus is therefore not simply a reporting website.

It is a campus case-management and coordination platform.

---

2. THE PROBLEM

Universities contain many different services and departments.

A student may experience:

- a security incident
- a medical emergency
- a broken electrical cable
- a damaged hostel door
- a Wi-Fi problem
- a university portal problem
- a lost item
- a phishing message
- an academic issue
- a complaint
- a maintenance problem
- an unsafe environment
- or another campus-related problem.

In many situations, the user may not know:

- which department is responsible
- which officer to contact
- which staff member should handle the issue
- whether the report has been received
- whether somebody has been assigned
- what the current status is
- whether the problem has been investigated
- whether the problem has actually been fixed
- how to provide additional evidence
- how to follow up.

Communication may become fragmented between different channels.

SafeCampus aims to create a structured digital workflow where a case can be submitted once and then routed, assigned, communicated, investigated, acted upon, verified and closed.

---

3. PROJECT OBJECTIVES

The main objectives of SafeCampus are:

1. Provide a central platform for campus-related reporting and service requests.
2. Automatically route cases to the appropriate department where possible.
3. Allow authorized officers to review and assign cases.
4. Allow field workers and staff to receive and manage assigned tasks.
5. Allow students and staff to track their cases.
6. Provide secure case-based communication.
7. Support evidence uploads.
8. Support cybersecurity awareness and threat reporting.
9. Provide Lost & Found coordination.
10. Provide safety alerts.
11. Provide department dashboards.
12. Track response and resolution performance.
13. Maintain an auditable history of important actions.
14. Apply security and privacy controls.
15. Reduce unnecessary confusion about who should handle a problem.
16. Provide a practical demonstration of how technology can improve campus services and safety.

---

4. CORE DESIGN PRINCIPLE

SafeCampus follows this principle:

«The user should describe the problem. The system should help determine who should handle it.»

The student should not normally need to know the name of a particular officer or technician.

For example:

Student
   ↓
"Electrical problem in Hostel A"
   ↓
Category: Electrical
Location: Hostel A
   ↓
Routing Engine
   ↓
Maintenance Department
   ↓
Maintenance Officer
   ↓
Electrician
   ↓
Repair
   ↓
Verification
   ↓
Closure

The same location can produce different routing depending on the problem.

For example, Hostel A can contain:

Theft
   → Security

Medical Emergency
   → Health Services

Broken Light
   → Maintenance

Wi-Fi Problem
   → ICT

Room Allocation
   → Hostel Management

Therefore:

«Location does not determine the responsible department by itself.
Case type and category help determine responsibility.»

---

5. USERS AND ACCESS LEVELS

SafeCampus uses Role-Based Access Control (RBAC).

A role determines what a user is allowed to do.

Department determines organizational scope.

Position describes the person's job/function.

These concepts must not be confused.

Example:

Role:
STAFF

Department:
HEALTH SERVICES

Position:
NURSE

Another example:

Role:
STAFF

Department:
ICT

Position:
NETWORK TECHNICIAN

---

6. USER TYPES

6.1 Student

Students can:

- register
- login
- maintain their profile
- create cases
- submit reports
- submit service requests
- submit complaints
- submit emergency reports
- submit feedback
- submit Lost & Found cases
- submit cybersecurity reports
- submit academic requests
- upload evidence
- communicate through case messages
- track case status
- receive notifications
- view safety alerts
- use the phishing/scam analyzer
- complete cybersecurity awareness lessons
- take cybersecurity quizzes
- receive Lost & Found match notifications.

Students cannot create privileged accounts such as Department Head or Super Admin.

---

7. STUDENT REGISTRATION

Student registration should collect information such as:

- Full Name
- Registration Number
- Email
- Phone Number
- Faculty
- Academic Department
- Level
- Password
- Confirm Password

The system should validate the information.

Passwords must never be stored as plaintext.

Use a secure password hashing mechanism such as Argon2.

---

8. STUDENT ACADEMIC PROFILE

The student's academic profile is important for automatic academic routing.

Example:

Name:
Mustapha Umar

Registration Number:
UMYU/CSC/XXXX

Faculty:
Computing

Department:
Computer Science

Level:
300

The system stores the student's default academic department.

---

9. AUTOMATIC ACADEMIC DEPARTMENT ROUTING

When a student creates an academic request, the system should normally know the student's academic department automatically.

The student should not repeatedly enter their department.

Example:

Student Profile
      ↓
Department = Computer Science
      ↓
Academic Request
      ↓
Request Type = Course Registration Issue
      ↓
Routing Engine
      ↓
Computer Science Department

However, not every academic/system issue should automatically go to the student's academic department.

For example:

Course/Department Academic Issue
      ↓
Student's Academic Department

But:

University Portal Problem
      ↓
ICT / Relevant Central Service

Therefore the routing engine must consider both:

1. Student's profile
2. Case category/type

The student's academic department is the default academic context, not an unconditional destination.

---

10. PRIVILEGED USERS

Privileged users must not have public self-registration.

Examples:

- Super Admin
- Department Head
- Officer
- Supervisor
- Staff
- Field Worker

These accounts should be created, invited or activated through authorized administrative workflows.

Nobody should be able to simply select:

Role = ADMIN

during public registration.

---

11. USER HIERARCHY

The general hierarchy is:

SUPER ADMIN
     ↓
DEPARTMENT HEAD
     ↓
OFFICER / SUPERVISOR
     ↓
STAFF / FIELD WORKER

Not every department must use every level.

For example, a small department may only require:

Department Head
     ↓
Staff

The system should therefore support configurable organizational structures.

---

12. DEPARTMENTS

Initial departments include:

1. Security
2. Health Services
3. ICT / IT Services
4. Cybersecurity
5. Maintenance
6. Hostel Management
7. Lost & Found
8. Academic / Departmental Services
9. Student / Administrative Services

The system must be configurable.

A Super Admin should be able to create additional departments without changing application source code.

A department may have:

- Name
- Code
- Description
- Status
- Head
- Officers
- Staff
- Units
- Categories
- Permissions

---

13. DEPARTMENT VS UNIT VS LOCATION

These concepts must remain separate.

Department

The organizational owner or handler.

Example:

Maintenance

Unit

A subdivision or operational area.

Example:

Electrical Unit

Location

The physical location related to a case.

Example:

Hostel A

A case may therefore contain:

Owner Department:
Hostel Management

Supporting Department:
Maintenance

Unit:
Electrical

Location:
Hostel A

This allows multiple departments to cooperate on one case.

---

14. CASE TYPES

SafeCampus should support multiple case types.

14.1 Incident

Something happened.

Examples:

- theft
- damaged property
- security incident
- cyber incident

14.2 Service Request

The user is requesting a service.

Examples:

- repair
- account support
- room allocation
- IT support

14.3 Complaint

A user wants to report dissatisfaction or concern about a service, person or process.

A complaint must not automatically be treated as proof of wrongdoing.

14.4 Emergency

An urgent situation requiring immediate attention.

Examples:

- medical emergency
- serious security incident
- immediate safety hazard

14.5 Feedback

Suggestions or general feedback.

14.6 Lost & Found

Used for lost or found property.

14.7 Cybersecurity Report

Used for suspicious cyber activity.

Examples:

- phishing
- scam
- suspicious link
- fake scholarship
- fake job offer
- impersonation
- account compromise concern.

---

15. GENERAL CASE CREATION

A case should contain information such as:

- Reporter
- Case type
- Category
- Description
- Location
- Priority
- Owner Department
- Supporting Departments
- Assigned Officer
- Assigned Staff
- Status
- Evidence
- Messages
- Resolution
- Audit History
- Created time
- Updated time
- SLA target
- SLA status

---

16. CASE PRIORITY

The system should support:

LOW
MEDIUM
HIGH
CRITICAL

Priority affects handling and visibility.

Emergency cases can receive high or critical priority.

The system must not claim that it automatically contacts police, ambulance or other emergency responders unless an actual integration exists.

For immediate danger, the interface can display configured emergency contact information.

---

17. CASE STATUS

Example case lifecycle:

SUBMITTED
    ↓
UNDER_REVIEW
    ↓
ASSIGNED
    ↓
ACCEPTED
    ↓
IN_PROGRESS
    ↓
COMPLETED
    ↓
VERIFIED
    ↓
RESOLVED
    ↓
CLOSED

Other states such as:

ESCALATED
REJECTED
CANCELLED
REOPENED

may be supported where appropriate.

---

18. ROUTING ENGINE

The Routing Engine is one of the central components of SafeCampus.

Its responsibility is to help determine the appropriate department.

Example rules:

Medical Emergency
→ Health Services

Electrical Problem
→ Maintenance

Phishing
→ Cybersecurity

Theft
→ Security

Portal Problem
→ ICT

Hostel Allocation
→ Hostel Management

Academic Request
→ Student's Academic Department

Routing should be configurable.

Authorized administrators should be able to modify categories and routing rules without rewriting the entire application.

---

19. DEPARTMENT ASSIGNMENT

A case may have:

- Owner Department
- Supporting Department
- Assigned Officer
- Assigned Staff

Example:

Case:
Broken electrical cable in Hostel A

Owner:
Hostel Management

Supporting:
Maintenance

Officer:
Maintenance Officer

Staff:
Electrician

Another example:

Case:
Theft in Hostel A

Owner:
Security

Supporting:
Hostel Management

Assigned:
Security Officer

This allows multi-department coordination.

---

20. SECURITY DEPARTMENT

Security handles cases such as:

- theft
- threats
- suspicious activity
- unauthorized entry
- forced entry
- safety incidents
- dangerous situations
- security concerns.

Security officers can:

- review cases
- investigate
- assign tasks
- communicate
- record investigation notes
- request additional information
- escalate
- verify resolution
- close authorized cases.

---

21. HEALTH SERVICES

Health Services handles:

- illness
- injury
- medical assistance
- medical emergency
- health-related reports.

Example:

Student
   ↓
Medical Request
   ↓
Health Officer
   ↓
Nurse / Doctor / Medical Staff
   ↓
Physical Response
   ↓
Case Update
   ↓
Resolution

Health information must receive strict privacy protection.

Users outside Health Services should only see information necessary for their authorized role.

SafeCampus is not a replacement for a hospital or emergency medical service.

---

22. ICT / IT SERVICES

ICT handles:

- account problems
- password/account support
- university portal problems
- course registration system issues
- network problems
- Wi-Fi
- computer laboratory problems
- university email
- printers
- hardware
- software
- applications
- other IT services.

Example:

Student
   ↓
Portal Problem
   ↓
ICT Department
   ↓
ICT Officer
   ↓
IT Staff
   ↓
Diagnosis
   ↓
Fix
   ↓
Verification
   ↓
Close

---

23. MAINTENANCE

Maintenance handles:

- electrical problems
- plumbing
- furniture
- building damage
- structural issues
- lights
- fans
- water systems
- doors
- locks
- other repair work.

Example:

Student
   ↓
Broken Light
   ↓
Maintenance
   ↓
Electrical Unit
   ↓
Electrician
   ↓
Repair
   ↓
Evidence
   ↓
Officer Verification
   ↓
Close

---

24. HOSTEL MANAGEMENT

Hostel is a service/organizational unit and should not simply be treated as a Security or Maintenance category.

Possible structure:

HOSTEL MANAGEMENT
       ↓
HOSTEL OFFICER / MANAGER
       ↓
SUPERVISORS
       ↓
WARDENS / STAFF

Hostel units may include:

- Hostel A
- Hostel B
- Hostel C
- Male Hostel
- Female Hostel
- Postgraduate Hostel

The exact structure should be configurable.

---

25. HOSTEL CASE CATEGORIES

Accommodation

- room allocation
- bed allocation
- room transfer
- space issue

Maintenance

- broken door
- electrical issue
- water
- toilet
- light
- fan
- furniture
- building damage

Security

- theft
- suspicious person
- threat
- forced entry
- lost key

Health

- illness
- injury
- unsafe health condition
- medical emergency

Environment

- waste
- dirty environment
- pests
- flooding
- drainage

Conduct

- excessive noise
- fighting
- harassment
- property damage
- other conduct concerns

The hostel is the context/location.

The responsible department depends on the case.

---

26. ACADEMIC SERVICES

Students should be able to report or request:

- course registration issue
- examination issue
- result issue
- lecturer/class issue
- academic inquiry
- departmental request
- other academic complaint.

The system should use the student's registered academic department automatically when appropriate.

Example:

Student:
Computer Science

Request:
Course Registration Issue

Routing:
Computer Science Department

But:

Student:
Computer Science

Request:
University Portal Failure

Routing:
ICT

---

27. STAFF REPORTING

Staff members should also be able to create cases.

Examples:

- IT problems
- office equipment
- maintenance
- security
- health
- administrative services
- workplace concerns
- other campus problems.

Lecturers/staff may also submit authorized student conduct reports where permitted.

Students may submit complaints or concerns involving lecturers/staff.

Such reports must go through proper review and investigation.

A complaint is not automatically proof of guilt.

---

28. COMMUNICATION SYSTEM

Communication is a core feature.

Communication should be attached to cases.

Example:

CASE
│
├── Messages
├── Evidence
├── Assignment
├── Status
├── Activity
└── Resolution

Possible communication:

Student ↔ Officer
Student ↔ Assigned Staff
Staff ↔ Officer

Access must be controlled by authorization rules.

The platform should reduce the need for users to move the entire conversation to external messaging applications.

Physical interaction may still be required for:

- medical care
- security response
- maintenance
- inspections
- other physical operations.

---

29. EVIDENCE

Users may upload appropriate evidence such as:

- photographs
- documents
- screenshots
- other supported files.

File uploads must be secured.

Security requirements include:

- file type validation
- size limits
- safe filenames
- authorization checks
- secure storage
- protection against executable uploads
- access control
- malware scanning architecture where available.

---

30. FIELD OPERATIONS

Some cases require physical action.

An officer can assign a case/task to a staff member.

Staff dashboard:

MY TASKS

Task lifecycle:

ASSIGNED
   ↓
ACCEPTED
   ↓
ON_SITE
   ↓
WORKING
   ↓
COMPLETED

The staff member can submit:

- action notes
- evidence
- completion information.

The officer then reviews the work.

COMPLETED
   ↓
OFFICER REVIEW
   ↓
VERIFIED
   ↓
CLOSED

---

31. ESCALATION

A staff member may escalate a problem to an officer.

An officer may escalate to a Department Head.

Example:

Staff
 ↓
ESCALATE
 ↓
Officer
 ↓
Department Head

Escalation must record:

- who escalated
- when
- reason
- previous state
- new responsible person/department
- action taken.

---

32. NOTIFICATIONS

The system should notify users when important events happen.

Examples:

- case submitted
- case assigned
- officer sends message
- staff assigned
- status changed
- case resolved
- case closed
- case escalated
- Lost & Found possible match
- safety alert
- action required
- SLA approaching/breached.

Notifications may initially be implemented as in-app notifications.

Email/SMS/push notification integrations can be added when appropriate.

---

33. SAFETY ALERTS

Authorized officers/admins can publish campus safety alerts.

An alert may contain:

- Title
- Location
- Severity
- Message
- Issued By
- Time
- Status

Example:

SAFETY ALERT

Title:
Electrical Hazard

Location:
Near ICT Building

Severity:
HIGH

Message:
Students should avoid the affected area until
maintenance work is completed.

Students should receive the alert through the platform.

---

34. LOST & FOUND

SafeCampus should provide a controlled Lost & Found workflow.

Example:

Student A
   ↓
Reports Lost Phone
   ↓
Location + Date + Description

Another student:

Student B
   ↓
Reports Found Phone
   ↓
Location + Date + Description

The system can identify possible matches using:

- category
- location
- date
- description
- relevant attributes.

A possible match is not proof that the item belongs to the claimant.

Controlled verification must happen before handover.

---

35. LOST & FOUND COMMUNICATION

Users should communicate through the platform.

The system should not expose personal phone numbers unnecessarily.

An authorized officer can coordinate:

Lost Item
   ↓
Possible Match
   ↓
Verification
   ↓
Handover
   ↓
Confirmation
   ↓
Close

---

36. CYBERSECURITY MODULE

Cybersecurity is a major component of SafeCampus.

The module should include:

1. Cyber threat reporting
2. Phishing/scam analyzer
3. Suspicious URL analysis
4. Cybersecurity awareness lessons
5. Security tips
6. Cybersecurity quiz
7. Fake scholarship/job scam awareness
8. Cyber incident workflow.

---

37. CYBERSECURITY REPORTING

Students and staff can report:

- phishing
- scam
- suspicious links
- fake scholarship
- fake job offer
- impersonation
- suspicious account activity
- possible account compromise
- other cyber threats.

Reports should route to:

Cybersecurity Department

where appropriate.

---

38. PHISHING / SCAM ANALYZER

The analyzer accepts:

- pasted suspicious message
- optional URL

The system analyzes indicators such as:

- urgency
- credential requests
- suspicious URL structure
- suspicious domain
- payment request
- prize/reward claims
- unknown sender
- impersonation indicators.

Example:

Input:
"URGENT! Your university account will be closed.
Click this link immediately and enter your password..."

Possible output:

Potential Phishing / High Risk

Indicators:
✓ Urgency
✓ Credential request
✓ Suspicious link
✓ Account threat

Recommendation:
Do not enter your password.
Verify the message through an official channel.

The analyzer must clearly state that its result is an indicator/risk assessment.

It must not claim:

100% phishing

unless there is verified evidence.

A risk score is an indicator, not a probability or certainty.

---

39. SAFE URL ANALYSIS

The MVP should primarily analyze the URL string and domain structure.

The application must not blindly fetch arbitrary user-supplied URLs from the server.

This is important because unrestricted URL fetching can create SSRF vulnerabilities.

If external reputation checking is introduced later, it must use a secure architecture with:

- allow/deny controls
- network restrictions
- timeout
- safe DNS handling
- private IP protection
- redirect controls
- logging
- rate limiting.

---

40. CYBERSECURITY EDUCATION

The platform should provide educational content such as:

- phishing awareness
- password security
- MFA
- social engineering
- safe browsing
- account protection
- scam detection
- device security
- privacy
- cyber hygiene.

Users can complete quizzes to test understanding.

---

41. AUDIT LOGGING

Important actions must be recorded.

Examples:

Case Created
Case Assigned
Message Sent
Evidence Added
Status Changed
Task Accepted
Investigation Started
Task Completed
Case Verified
Case Closed
Case Escalated

Example timeline:

09:31  Case created
09:34  Officer assigned
09:38  Officer sent message
09:45  Investigation started
10:20  Staff completed task
10:30  Officer verified
10:35  Case closed

Audit records should not be casually deleted.

Audit logs are important for accountability, troubleshooting and security investigations.

---

42. SLA / RESPONSE TRACKING

SafeCampus should support configurable Service Level Agreement (SLA) targets.

The system should not invent official university response times.

Instead, an authorized administrator can configure targets.

Example:

LOW       → configurable target
MEDIUM    → configurable target
HIGH      → configurable target
CRITICAL  → configurable target

The system can display:

- target response time
- target resolution time
- current elapsed time
- overdue status
- SLA breached status.

Example:

Case:
Broken Electrical Cable

Target:
2 hours

Elapsed:
3 hours

Status:
SLA BREACHED

---

43. ANALYTICS DASHBOARD

Authorized users should have dashboards appropriate to their roles.

Possible statistics:

- open cases
- resolved cases
- closed cases
- cases by department
- cases by category
- emergency cases
- hostel cases
- IT requests
- security incidents
- cyber reports
- overdue cases
- SLA breaches
- response time
- resolution time.

Department staff should only see data they are authorized to see.

Super Admin may have broader system-level analytics.

---

44. ROLE-BASED DASHBOARDS

Student Dashboard

Possible sections:

My Cases
Create Case
Messages
Notifications
Safety Alerts
Lost & Found
Cybersecurity
Profile

Staff Dashboard

My Tasks
Assigned Cases
Messages
Evidence
Escalation
Notifications

Officer Dashboard

Department Cases
Unassigned Cases
Assigned Cases
Escalations
Staff
SLA
Analytics

Department Head Dashboard

Department Overview
Cases
Staff
Performance
Escalations
Analytics
Reports

Super Admin Dashboard

Users
Departments
Units
Roles
Permissions
Categories
Routing Rules
SLA Configuration
System Analytics
Audit Logs
Safety Alerts
System Settings

---

45. AUTHORIZATION

Authorization must be enforced on the server.

Hiding a button in HTML is not security.

For example, even if a normal student cannot see:

Delete Department

the backend must still reject a direct unauthorized request.

The system should check:

WHO is the user?
WHAT role do they have?
WHICH department do they belong to?
WHAT permission do they have?
WHAT resource are they trying to access?

---

46. SECURITY REQUIREMENTS

SafeCampus must use secure development practices.

Required controls include:

- Argon2 or equivalent secure password hashing
- no plaintext passwords
- Role-Based Access Control
- department-scoped authorization
- server-side authorization
- CSRF protection
- rate limiting
- input validation
- secure session handling
- secure cookies
- file upload security
- audit logging
- privacy controls
- least privilege
- HTTPS-ready deployment
- secure database access
- protection against SQL injection through ORM/parameterized queries
- output escaping where appropriate
- protection against XSS
- SSRF protection for URL analysis
- secure error handling
- appropriate logging
- secret management through environment variables.

---

47. PRIVACY

Different users should not see all information.

For example:

A student's private medical information should not automatically be visible to:

- Security
- Maintenance
- General staff
- Other students.

A department should only access the information required for its authorized work.

Sensitive cases require additional privacy controls.

---

48. DATABASE DESIGN

The application will use PostgreSQL.

SQLAlchemy will be used as the ORM.

Alembic will be used for database migrations.

Possible core entities include:

User
Role
Permission
Department
DepartmentUnit
Faculty
AcademicDepartment
StudentProfile
StaffProfile
Position
Location
Hostel
Case
CaseCategory
CaseAssignment
CaseSupportingDepartment
CaseMessage
CaseEvidence
CaseStatusHistory
Task
TaskUpdate
Escalation
Notification
SafetyAlert
LostFoundItem
LostFoundMatch
CyberReport
CyberAnalysis
Quiz
QuizQuestion
AuditLog
SLAConfiguration
RoutingRule

The final database schema must be designed carefully before implementation.

---

49. CASE RELATIONSHIP MODEL

Conceptually:

USER
 │
 ├──────── creates ──────── CASE
 │                            │
 │                            ├── TYPE
 │                            ├── CATEGORY
 │                            ├── LOCATION
 │                            ├── PRIORITY
 │                            ├── OWNER DEPARTMENT
 │                            ├── SUPPORTING DEPARTMENTS
 │                            ├── OFFICER
 │                            ├── STAFF
 │                            ├── MESSAGES
 │                            ├── EVIDENCE
 │                            ├── TASKS
 │                            ├── ESCALATIONS
 │                            ├── STATUS HISTORY
 │                            ├── RESOLUTION
 │                            └── AUDIT LOG

---

50. ARCHITECTURE

The high-level architecture is:

                USERS
                  │
                  ▼
          HTML / CSS / JavaScript
                  │
                  ▼
             Flask Backend
                  │
       ┌──────────┼──────────┐
       │          │          │
       ▼          ▼          ▼
 Authentication  Case     Cybersecurity
 Authorization   System      Module
       │          │          │
       └──────────┼──────────┘
                  ▼
              SQLAlchemy
                  │
                  ▼
              PostgreSQL
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
  Audit Logs  Notifications Analytics

---

51. TECHNOLOGY STACK

The initial technology stack should remain beginner-friendly.

Frontend

- HTML
- CSS
- JavaScript

Backend

- Python
- Flask

Database

- PostgreSQL

ORM

- SQLAlchemy
- Flask-SQLAlchemy where appropriate

Database Migration

- Alembic / Flask-Migrate if selected

Security

- Argon2
- CSRF protection
- rate limiting
- RBAC
- secure sessions
- audit logs

Version Control

- Git
- GitHub

The project should avoid unnecessary complexity such as microservices, React, Node.js or Docker unless a real requirement appears.

---

52. DEVELOPMENT PRINCIPLE

The project should be built incrementally.

Do not build the entire application in one uncontrolled step.

Development should follow:

SPECIFICATION
      ↓
PROJECT STRUCTURE
      ↓
DATABASE DESIGN
      ↓
AUTHENTICATION
      ↓
USER PROFILES
      ↓
DEPARTMENTS / ROLES
      ↓
CASE SYSTEM
      ↓
ROUTING
      ↓
ASSIGNMENT
      ↓
COMMUNICATION
      ↓
FIELD OPERATIONS
      ↓
NOTIFICATIONS
      ↓
CYBERSECURITY
      ↓
LOST & FOUND
      ↓
ANALYTICS
      ↓
SECURITY HARDENING
      ↓
TESTING
      ↓
DEMO

---

53. GIT AND GITHUB

Git is used to track project changes.

GitHub is used as the remote repository and collaboration/backup location.

The GitHub repository should become the source of truth once connected.

Development from Termux and Windows should work with the same repository.

Conceptually:

Termux
   │
   ├── Git commit
   │
   └── Git push
          ↓
       GitHub
          ↓
      Git pull
          ↓
       Windows

The same process can work in the opposite direction.

Before changing the project on another machine, synchronize with GitHub.

---

54. AI DEVELOPMENT WORKFLOW

AI tools may assist development, but they must not replace understanding or verification.

Preferred workflow:

PROJECT REQUIREMENT
        ↓
CHATGPT
Architecture / Teaching / Review
        ↓
MANUS or OTHER CODING AGENT
Implementation
        ↓
USER
Runs and tests
        ↓
CHATGPT
Explains / Reviews / Debugs / Security checks
        ↓
GIT
Version control
        ↓
GITHUB
Source of truth

Different AI agents should not edit the same repository simultaneously without coordination.

---

55. RULES FOR AI CODING AGENTS

Any AI coding agent working on SafeCampus must follow these rules:

1. Read the existing repository before modifying it.
2. Do not create an unrelated project.
3. Do not blindly rewrite existing files.
4. Preserve working functionality.
5. Follow the official specification.
6. Implement one defined task at a time.
7. Explain what was changed.
8. Explain which files were modified.
9. Run tests after changes.
10. Report test results.
11. Do not silently remove functionality.
12. Do not invent external integrations.
13. Do not claim a feature works if it has not been tested.
14. Do not store secrets in source code.
15. Follow security requirements.
16. Keep changes reviewable.
17. Use Git commits for meaningful milestones.

---

56. DEMO SCENARIO

The hackathon demo should demonstrate a real end-to-end workflow.

Demo 1: Maintenance Case

Login as a student.

Student creates:

Type:
Service Request

Category:
Electrical

Location:
ICT Centre

Description:
Damaged electrical cable / unsafe electrical condition

Priority:
High

Student submits evidence/photo if appropriate.

Then:

Student
   ↓
SafeCampus
   ↓
Routing Engine
   ↓
Maintenance
   ↓
Officer
   ↓
Electrician

The electrician:

ACCEPTED
   ↓
ON_SITE
   ↓
WORKING
   ↓
COMPLETED

Officer verifies:

COMPLETED
   ↓
VERIFIED
   ↓
CLOSED

The student sees the status updates.

---

57. DEMO 2: CYBERSECURITY

Open the Cybersecurity Analyzer.

Paste a suspicious message.

Example:

URGENT! Your university account will be suspended.
Click the link below and enter your password immediately.

The analyzer identifies indicators such as:

Urgency
Credential request
Account threat
Suspicious link

The result should explain:

Potential phishing / high risk indicator.

Then demonstrate that the user can report the incident.

The report routes to:

Cybersecurity Department

---

58. DEMO 3: LOST & FOUND

Student A reports:

Lost item:
Phone

Location:
Hostel A

Date:
Selected date

Description:
Specific description

Student B reports:

Found item:
Phone

Location:
Hostel A

Date:
Similar date

The system identifies a possible match.

It should not automatically declare ownership.

Instead:

Possible Match
      ↓
Verification
      ↓
Controlled Communication
      ↓
Handover
      ↓
Confirmation
      ↓
Closed

---

59. DEMO 4: ACADEMIC ROUTING

Use a student whose profile contains:

Faculty:
Computing

Department:
Computer Science

Level:
300

The student creates:

Academic Request

The system automatically uses:

Computer Science

as the default academic department.

The student does not need to manually type/select the department again.

Then demonstrate an exception:

Problem:
University Portal Not Working

The routing engine can route it to:

ICT

This demonstrates that SafeCampus uses both:

- student profile
- case category

for intelligent routing.

---

60. DEMO 5: AUDIT TRAIL

After completing a case, show the activity timeline:

09:31  Case created
09:34  Routed to Maintenance
09:38  Officer assigned
09:45  Staff accepted
10:00  Staff marked ON_SITE
10:20  Task completed
10:30  Officer verified
10:35  Case closed

This demonstrates accountability.

---

61. HACKATHON PITCH STRUCTURE

The presentation should not begin by simply saying:

«"We built a website."»

Instead, begin with the problem.

Suggested structure:

1. Problem
2. Why the problem matters
3. SafeCampus solution
4. How the platform works
5. Key features
6. Security
7. Live demo
8. Impact
9. Future scalability
10. Questions

---

62. SIMPLE PITCH EXPLANATION

A simple explanation of the project:

«UMYU SafeCampus is a centralized campus safety and service management platform that allows students and staff to report problems through one secure platform. Instead of forcing users to search for the right officer or department, SafeCampus uses case information, location and user context to help route the issue to the appropriate department. Officers can review and assign cases, field workers can perform tasks, users can communicate and track progress, and the system maintains an audit trail from reporting to resolution.»

---

63. WHY THE PROJECT IS DIFFERENT

SafeCampus combines multiple campus workflows into one structured platform.

It connects:

Campus Safety
      +
Health
      +
ICT
      +
Maintenance
      +
Hostel
      +
Academic Services
      +
Cybersecurity
      +
Lost & Found
      +
Communication
      +
Case Management
      +
Analytics

The platform is therefore designed around the lifecycle of a campus problem rather than a single isolated feature.

---

64. SECURITY-FIRST APPROACH

Security is not an optional feature.

The platform handles potentially sensitive information.

Therefore security must exist at multiple levels:

Authentication
     ↓
Authorization
     ↓
Department Scope
     ↓
Input Validation
     ↓
Secure Files
     ↓
Privacy Controls
     ↓
Audit Logging
     ↓
Secure Sessions
     ↓
Rate Limiting
     ↓
HTTPS

---

65. WHAT SAFECAMPUS DOES NOT CLAIM

The project must be honest about its capabilities.

SafeCampus does not claim:

- 100% phishing detection
- automatic police response
- automatic ambulance dispatch
- guaranteed crime prevention
- guaranteed medical treatment
- guaranteed resolution of every case
- replacement of university emergency services
- replacement of hospitals
- replacement of security personnel.

SafeCampus is a coordination, reporting, tracking, communication and management platform.

---

66. FUTURE EXTENSIONS

Future versions may include:

- mobile application
- push notifications
- SMS integration
- email integration
- university identity integration
- official emergency service integrations
- advanced analytics
- GIS/map integration
- secure reputation APIs for URLs
- QR-based asset reporting
- multilingual support
- accessibility improvements
- advanced AI-assisted classification
- document intelligence
- institutional integrations.

These should only be implemented when there is a real requirement and a secure architecture.

---

67. MVP PRIORITY

The initial working version should prioritize the features necessary to demonstrate the core concept.

The MVP should include:

1. Student registration/login
2. Secure authentication
3. Student profile
4. Departments
5. Roles
6. Case creation
7. Case categories
8. Automatic routing
9. Officer dashboard
10. Staff assignment
11. Case status tracking
12. Case communication
13. Evidence upload
14. Audit trail
15. Cybersecurity analyzer
16. Lost & Found
17. Safety alerts
18. Basic analytics
19. Security controls
20. End-to-end demo.

The MVP should be functional rather than visually overloaded.

---

68. QUALITY REQUIREMENTS

The project should prioritize:

- correctness
- security
- usability
- maintainability
- clear architecture
- understandable code
- testability
- responsive interface
- accessibility where possible
- reliable database design
- clear documentation.

---

69. TESTING

Testing should cover:

Authentication

- valid login
- invalid login
- password hashing
- rate limiting
- unauthorized access

Authorization

- student cannot access admin functions
- staff cannot access unrelated department data
- officer cannot access unauthorized departments
- Super Admin has appropriate administrative permissions.

Case Management

- case creation
- routing
- assignment
- status transitions
- messaging
- evidence
- closure
- reopening where supported.

Cybersecurity

- phishing indicators
- suspicious URLs
- safe input handling
- SSRF protection.

Lost & Found

- item creation
- matching
- verification
- communication.

Audit

- important actions create audit records.

---

70. ERROR HANDLING

The application should provide controlled error handling.

Examples:

400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
429 Too Many Requests
500 Internal Server Error

Sensitive internal error information should not be exposed to normal users.

---

71. CONFIGURATION

Sensitive configuration must not be hard-coded.

Use environment variables for values such as:

SECRET_KEY
DATABASE_URL
EMAIL_CONFIGURATION
API_KEYS
OTHER_SECRETS

A ".env" file may be used locally but must not be committed to GitHub if it contains secrets.

A safe ".env.example" file can document required variables without exposing real secrets.

---

72. PROJECT STRUCTURE

The final structure may evolve, but a conceptual structure can look like:

UMYU-SafeCampus/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   ├── auth/
│   ├── users/
│   ├── departments/
│   ├── cases/
│   ├── routing/
│   ├── notifications/
│   ├── cybersecurity/
│   ├── lost_found/
│   ├── alerts/
│   ├── analytics/
│   ├── audit/
│   ├── templates/
│   └── static/
│
├── migrations/
│
├── tests/
│
├── docs/
│   └── SAFECAMPUS-SPECIFICATION.md
│
├── scripts/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py

This structure is a conceptual starting point.

The implementation agent must inspect the actual repository before making changes.

---

73. DEVELOPMENT PHASES

Phase 0 — Specification

Create and verify this document.

Phase 1 — Project Setup

Set up:

- Python environment
- Flask
- project structure
- Git
- configuration
- environment variables.

Phase 2 — Database

Design and implement:

- users
- roles
- departments
- profiles
- core case entities.

Phase 3 — Authentication

Implement:

- registration
- login
- logout
- password hashing
- sessions
- rate limiting.

Phase 4 — Authorization

Implement:

- RBAC
- permissions
- department scope
- server-side authorization.

Phase 5 — Case Management

Implement:

- case creation
- categories
- types
- priority
- status
- location
- evidence.

Phase 6 — Routing

Implement:

- routing rules
- automatic academic department routing
- category-based routing
- department assignment
- override/reassignment.

Phase 7 — Assignment and Field Operations

Implement:

- officer assignment
- staff assignment
- My Tasks
- task status
- evidence
- verification
- escalation.

Phase 8 — Communication and Notifications

Implement:

- case messages
- notifications
- status updates.

Phase 9 — Cybersecurity

Implement:

- cyber reports
- phishing analyzer
- URL analysis
- awareness
- quiz.

Phase 10 — Lost & Found

Implement:

- lost items
- found items
- matching
- verification
- controlled communication.

Phase 11 — Safety Alerts

Implement:

- alerts
- severity
- location
- notifications.

Phase 12 — Analytics

Implement:

- dashboard
- department statistics
- SLA
- response/resolution metrics.

Phase 13 — Security Hardening

Review:

- authorization
- CSRF
- XSS
- SQL injection
- file uploads
- SSRF
- rate limiting
- sessions
- privacy
- audit logging.

Phase 14 — Testing

Run:

- unit tests
- integration tests
- security tests
- workflow tests.

Phase 15 — Demo Preparation

Prepare:

- student account
- staff account
- officer account
- sample departments
- sample cases
- phishing demo
- Lost & Found demo
- academic routing demo
- analytics
- audit timeline.

---

74. SUCCESS CRITERIA

The project is considered successfully demonstrated when a judge can see the following complete workflow:

Student
  ↓
Creates Case
  ↓
System Understands Category
  ↓
Routing Engine
  ↓
Correct Department
  ↓
Officer
  ↓
Staff
  ↓
Action
  ↓
Communication
  ↓
Evidence
  ↓
Verification
  ↓
Resolution
  ↓
Audit Trail

And when the project can demonstrate at least:

✓ Secure authentication
✓ Role-based access
✓ Department routing
✓ Academic automatic routing
✓ Case management
✓ Staff assignment
✓ Communication
✓ Cybersecurity analyzer
✓ Lost & Found
✓ Safety alerts
✓ Analytics
✓ Audit trail

---

75. FINAL PROJECT VISION

UMYU SafeCampus aims to provide a single structured digital environment through which students and staff can report problems, request services, communicate with authorized personnel, track progress and receive updates.

The system connects campus departments through a common workflow while respecting departmental responsibilities, privacy and security.

The long-term vision is:

ONE CAMPUS
     ↓
ONE SECURE PLATFORM
     ↓
MULTIPLE SERVICES
     ↓
INTELLIGENT ROUTING
     ↓
ACCOUNTABLE ACTION
     ↓
VERIFIABLE RESOLUTION

The fundamental idea is:

«Report once. Route correctly. Act responsibly. Track transparently. Resolve securely.»

---

76. OFFICIAL IMPLEMENTATION RULE

This document is the baseline specification for UMYU SafeCampus.

Any developer or AI agent working on the project must:

1. Read this specification first.
2. Inspect the existing repository.
3. Understand the current implementation.
4. Compare implementation against this specification.
5. Identify implemented, partially implemented and missing features.
6. Implement only the requested phase/task.
7. Preserve existing working functionality.
8. Avoid unnecessary rewrites.
9. Test every significant change.
10. Report what was changed and tested.
11. Follow the security and privacy requirements.
12. Keep Git history understandable.
13. Never expose secrets.
14. Never claim an untested feature is complete.

The repository and this specification together define the development context of UMYU SafeCampus.

---

END OF UMYU SAFECAMPUS SPECIFICATION
