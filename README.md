BACKEND PROJECT - ROMAN PROVINCE SIMULATOR - 

--Project overview--

- This project implements the backend for a turn-based resource management game, the Roman Province Simulator.

- The player takes the role of a Roman provincial governor managing the basic resources and population of a single province.

- The backend will provide structured data services for core concepts such as provinces, regions, populations, projects, taxes, and events.

- It will expose a clear set of API endpoints that an eventual frontend can use to run the game loop through a single public gateway.

--Running Locally (v0.4)--

When a user spins up the app they get an authenticated Flask API that provides User + Province (Game Session) management alongside a simple Admin Route for checking total User base.

Prerequisites:
- Docker /Docker Compose 

To run this backend locally:

1. Build and start services:
    docker compose up --build
    --URL/PORT: http://localhost:5001/

2. In a Separate Terminal - run migrations in container:
    docker exec -it backend-project-web-1 sh

    export FLASK_APP="game_app:create_app()"

    flask db upgrade

-Environment Variables-

Copy .env.example -> .env 

Currently In Usage:
APP_ENV - Configuration Setting For App; Expected Values ['development', 'testing', 'production']
DATABASE_URL - Path for sql database; example -  `postgresql+psycopg://ADMIN1:Secular4Cheesecake@db:5432/provincial_db`

JWT_SECRET - secret key for issuing and reading JWTs; Keep Secret

Designed For Future:
INTERNAL_SERVICE_TOKEN_SECRET - Will be used for internal-only access routes used during game loop. 

-- Do not commit .env, it should be added to .gitignore upon creation. 

-Confirmation Sequence- 
- register user http://0.0.0.0:5001/user/register
- login to get JWT http://0.0.0.0:5001/user/login
- create province http://0.0.0.0:5001/province/create
- list provinces http://0.0.0.0:5001/province/list

-Persistence Verification-
    docker compose down
    docker compose up
    GET /province/list

-Shut Down- 
    docker compose down

--Architecture-- 
NOTE: This section describes design targets for a future MVP v1.0 build.  
As of v0.4, the implemented services are:
-- User services (including Admin routes)
-- Province services

Other services (population, tax, infrastructure, events) are not yet implemented; their routes below are design-only for now.


- This backend is structured around six logical services, separated by data ownership and responsibility.

- They may be deployed together in a single application, but are designed as clear domains:

    - user-service – manages user profiles and, if needed, basic authentication.

    - province-service – manages game sessions, including provinces and their regions and core resource fields.

    - population-service – manages population data per region (size, growth, happiness/unrest) and updates it each turn.

    - tax-service – manages regional tax records and province/region tax policy, and computes tax outcomes each turn.

    - infrastructure-service – manages the master project catalog and active projects per province, including their progress and effects.

    - events-service – manages the master event catalog and scheduled events that affect a province on future turns.

---Implemented Routes---

- Users Services
-- POST /user/register - auth:public - create a new user with username/email/password
-- POST /user/login - auth:public - return a JWT on valid credentials
-- GET /user/me - auth:JWT - return current user's profile
-- PATCH /user/me -auth:JWT - update current user's display_name or email

- Admin Services
-- GET /admin/system-check - auth:JWT (role == 'admin' only) - return full list of registered users

- Province Services
-- POST /province/create - auth:JWT - creates a province with name and difficulty; ownership on user_id from JWT
-- GET /province/list - auth:JWT - Returns a paginated list of current user's provinces
-- GET /province/<int:id> - auth:JWT - returns a province profile if authenticated owner in JWT
-- PATCH /province/<int:id> - auth:JWT - updates name and difficulty if authenticated owner from JWT or admin; Admin may also update current_turn
-- DELETE /province/<int:id> -auth:JWT - deletes province if authenticated owner or admin


---END OF IMPLEMENTED ROUTES---

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


--Security & HTTP Walkthrough Docs--

These documents provide example request/response flows and security behavior for the current API:

- User & Admin routes review – see /docs/security-test-19-11.md
- Province routes review – (planned) /docs/province_tests_25-11.md
- Additional services – reserved for future security reviews as more services are implemented.