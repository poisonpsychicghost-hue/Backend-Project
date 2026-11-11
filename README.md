BACKEND PROJECT - ROMAN PROVINCE SIMULATOR - 

--Project overview--

- This project implements the backend for a turn-based resource management game, the Roman Province Simulator.

- The player takes the role of a Roman provincial governor managing the basic resources and population of a single province.

- The backend will provide structured data services for core concepts such as provinces, regions, populations, projects, taxes, and events.

- It will expose a clear set of API endpoints that an eventual frontend can use to run the game loop through a single public gateway.

--Running Locally (Unit 1 Skeleton)--

To run this backend locally:

1. Clone this repository to your machine.
2. Open a terminal **in the project root directory** (the folder that contains `README.md` and `requirements.txt`), then run:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    flask run

Note: This starts the **Unit 1 skeleton** only. The game endpoints listed below are design targets and are not implemented yet.

--Environment Variables--

-Used-
APP_ENV - Sets the App's Config Environment
DATABASE_URL - Main Database Path

-Unused-
JWT_SECRET - Read to Issue/Validate JWT's
INTERNAL_SERVICE_TOKEN_SECRET - Read to Protect Internal Routes

--Migrations--

Migration tooling is installed and wired (Flask-Migrate)
V0.01 - No Models Designed -> No Migration Scripts

Once models exist, migrations will be run with flask db migrate / flask db upgrade

--Game concept & learning focus--

- The Roman Province Simulator is a semi-historical game where the player governs one Roman province.

- To progress, the player must balance limited resources against population needs, infrastructure projects, and turn-by-turn events.

- The goal is not strict historical or economic realism.

- Instead, the game focuses on teaching basic resource-management skills (especially planning under constraints and trade-offs) and sparking interest in Roman logistics and governance, in a simple, interactive way.

--Architecture-- 

- This backend is structured around six logical services, separated by data ownership and responsibility.

- They may be deployed together in a single application, but are designed as clear domains:

    - user-service – manages user profiles and, if needed, basic authentication.

    - province-service – manages game sessions, including provinces and their regions and core resource fields.

    - population-service – manages population data per region (size, growth, happiness/unrest) and updates it each turn.

    - tax-service – manages regional tax records and province/region tax policy, and computes tax outcomes each turn.

    - infrastructure-service – manages the master project catalog and active projects per province, including their progress and effects.

    - events-service – manages the master event catalog and scheduled events that affect a province on future turns.

--Public routes – user-service--

    - POST /users – create a new user profile (registration: username, email, password, etc.).

    - GET /users/{userId}/provinces – list the user’s saved game sessions (province ids + basic metadata).

    - PATCH /users/{userId} – update user profile fields (email, password, display name).

    - DELETE /users/{userId} (optional) – delete a user account and all related game sessions.

--Public routes – province-service--

    - POST /provinces – create a new province (game session) for a given user; initializes base province and region data.

    - GET /provinces/{provinceId} – load high-level game state for a province (turn number, region list, basic resource summary).

    - PATCH /provinces/{provinceId} – update province metadata (e.g. name, difficulty, maybe last-accessed time) or apply a “save” operation.

    - DELETE /provinces/{provinceId} – delete a game session and trigger cleanup of related data in other services.

--Public routes – population-service--

    - GET /population/{provinceId} – list population and unrest data for all regions in a province.

    - GET /population/{provinceId}/{regionId} – get population and unrest data for a single region.

*Internal-only*

    - POST /population – initialize population data for a new game (called during new province creation).

    - PATCH /population/{provinceId} – apply end-turn population updates for a province (part of end-turn processing).

--Public routes – tax-service--

    - GET /tax/{provinceId}/tax-records – list tax records for all regions in a province (for analytics/history).

    - GET /tax/{provinceId}/tax-records/{regionId} – get tax records for a specific region.

    - GET /tax/{provinceId}/tax-policy – get the current tax policy for a province (and/or its regions).

*Internal-only*

    - POST /tax – initialize tax-related data for a new game (called during new province creation).

    - PATCH /tax/{provinceId} – apply end-turn tax computations and persist new tax records.

--Public routes – infrastructure-service--

    - GET /projects – list all project templates in the master catalog.

    - GET /projects/{projectId} – get details for a specific project template.

    - GET /provinces/{provinceId}/projects – list all active projects for a province.

    - GET /provinces/{provinceId}/projects/{projectId} – get details for a specific active project in a province.

*Internal-only*

    - POST /provinces/{provinceId}/projects – create a new active project for a province (when a player starts a project).

    - PATCH /provinces/{provinceId}/projects/apply-end-turn – apply end-turn progress and status updates for all active projects in a province.

--Public routes – events-service--

    - GET /events – list all event templates in the master catalog.

    - GET /events/{eventId} – get details for a specific event template.

*Internal-only*

    - GET /provinces/{provinceId}/events/next-turn – get scheduled events for the next turn for a province.

    - POST /provinces/{provinceId}/events/schedule – schedule events for a future turn based on current state (used during end-turn processing).

--Branching Strategy--

Branching should be done when implementing new features. 
