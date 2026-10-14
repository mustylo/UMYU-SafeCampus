# Requirements traceability

| Requirement | Implementation | Status / limitation |
|---|---|---|
| Student registration, login, logout, sessions | `app/auth/routes.py`, `User` | Implemented; password-reset email workflow remains future work. |
| Roles and department scope | `User.role`, `Department`, `can_access_case` | Implemented core roles; granular permission administration remains future work. |
| Case routing, updates, audit, notification | `CampusCase`, catalog seeder and `main/routes.py` | Implemented department-owned categories, status history, comments, assignment and in-app notifications. Evidence uploads, SLA and field tasks remain deferred. |
| Health privacy | `is_health_sensitive` and access guard | Implemented department isolation; dedicated retention controls remain future work. |
| Phishing analyzer | `services/phishing.py` | Implemented local heuristics; no external reputation API. |
| Lost & Found | `LostFoundItem`, `/lost-found` | Implemented controlled public listing; matching workflow remains future work. |
| Safety alerts | `SafetyAlert`, `/alerts`, `/alerts/new` | Display and restricted officer/head/admin publishing implemented. |
| Evidence uploads, field tasks, SLA, quizzes, full analytics | — | Not yet implemented; planned extension work. |
