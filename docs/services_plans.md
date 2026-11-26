Build Plan by Service

--Population Service--

-Step 0: branch + scope-

- branch: feature/population-service

scope for v1:

- 1 main model (Population or RegionPopulation)

- read-only public endpoints (GET x2)

- one internal init endpoint (POST /population) wired into province creation

-Step 1: Model + migration-

- Files:
game_app/core/population/models.py
game_app/core/__init__.py (ensure model import if needed)


- Model Population fields:
    id – PK
    province_id – FK → Province
    region_name – string (name of city/region)
    population_size – int
    growth_rate – float, constrained 0 < x < 1
    happiness – int (0–99)

- Actions:
define the model
generate migration: flask db migrate -m "add population model"
apply: flask db upgrade

Verify:
check DB / migration logs: population table exists with all fields

Commit:
feat(population): add population model and migration


-Step 2: Blueprint skeleton-

- Files:
game_app/core/population/routes.py (or population_routes.py)
game_app/core/__init__.py (register blueprint, prefix /population)

Endpoints (empty handlers for now):
- GET /population/<int:province_id>
- GET /population/<int:province_id>/<int:region_id>
- POST /population (internal init)
(optional stub) PATCH /population/<int:province_id> (end-turn)

All routes should use the same JWT auth decorator as provinces.

Verify:
flask routes shows all four endpoints under /population

Commit:
feat(population): add population blueprint skeleton


-Step 3: Public read endpoints-

- Files:
game_app/core/population/routes.py

Behavior:
GET /population/<province_id>:

auth: user/admin JWT
check province ownership (current user or admin) using your existing pattern from provinces
query all Population rows for that province_id

return list: region_name, population_size, growth_rate, happiness

- GET /population/<province_id>/<region_id>:
same auth + ownership
fetch single row by id + province_id
404 if not found with error shape like:
{"code":"Not Found","message":"Population Not Found"}

Verify via curl:
401 without token
200 with token + valid province
404 for non-existent region/province combo

Commit:
feat(population): implement public read endpoints with ownership checks

-Step 4: Internal init- (POST /population) and wiring into province create

- Files:
game_app/core/population/routes.py
game_app/core/provinces/routes.py (POST /province/create)

Behavior:
POST /population:
for now, auth: admin-only (role check) or 
TODO token check:
e.g. allow only when g.role == "admin" and leave a comment for INTERNAL_SERVICE_TOKEN_SECRET

request body:
province_id
maybe regions array or use a default region template
create one or more Population rows for that province with default:
population_size (e.g. 10_000)
growth_rate (e.g. 0.02)
happiness (e.g. 50)

integrate with POST /province/create:
after province record is created:
call internal helper that triggers /population init (direct function call is fine for now)

Verify:
create province via POST /province/create
GET /population/<province_id> returns default population set

Commit:
feat(population): add internal init and hook into province creation


-Step 5: Error/response shape + docs-

- Files:
game_app/core/population/routes.py
README + /docs/province-security-review.md

Actions:
ensure population errors match existing style:
401 Unauthorized – same code/message as provinces
404 Not Found – "Population Not Found"
400 Bad Request – for invalid growth_rate or happiness range

update README:
move population routes from “design-only” to “implemented” once they’re actually done

update security docs:
add 1–2 curl examples for population GETs

Commit:
chore(population): align error shapes and update docs
Step 6 – Optional: basic end-turn stub

- Files:
game_app/core/population/routes.py

Behavior:
PATCH /population/<province_id> (internal/admin only):
pseudo-logic: population_size = population_size * (1 + growth_rate)
maybe nudge happiness based on a simple rule

Verify:
call endpoint and confirm rows update as expected

Commit:
feat(population): add basic end-turn update stub



--Tax Service--


-Step 0: Branch + Scope-

- branch: feature/tax-service

-Step 1: Model + migration-

- Files:
game_app/core/tax/models.py
maybe game_app/core/__init__.py for imports

Models:
- TaxRecord:
    id (PK)
    province_id (FK → Province)
    region_name or region_id
    turn_number (int)
    tax_collected (int)
    tax_rate (float, e.g. 0–1)
    maybe population_size_snapshot (int) for audit

- TaxPolicy (optional for v1; can also be v1.1):
    id
    province_id
    base_tax_rate (float)
    created_at

Actions:
define TaxRecord (and TaxPolicy if you want it now)
flask db migrate -m "add tax models"
flask db upgrade

Verify:
both tables exist with expected columns

Commit:
feat(tax): add tax models and migration

-Step 2: Blueprint skeleton-

- Files:
game_app/core/tax/routes.py
game_app/core/__init__.py (register blueprint with prefix /tax)

Endpoints to stub:

public:
- GET /tax/<int:province_id>/tax-records
- GET /tax/<int:province_id>/tax-records/<int:region_id>
- GET /tax/<int:province_id>/tax-policy (if you add TaxPolicy)
internal:
- POST /tax (init data for new province)
- PATCH /tax/<int:province_id> (end-turn tax computation)

All guarded by JWT; internal ones additionally restricted (admin now, token later).

Verify:
flask routes shows all 5 endpoints

Commit:
feat(tax): add tax blueprint skeleton

-Step 3: Public read endpoints (analytics view)-

- Files:
game_app/core/tax/routes.py

Behavior:

GET /tax/<province_id>/tax-records:
auth: user/admin JWT
enforce province ownership like provinces/population
return list of TaxRecord for that province (can paginate later)

GET /tax/<province_id>/tax-records/<region_id>:
same auth + ownership
404 when no record, with {"code":"Not Found","message":"Tax Record Not Found"}

GET /tax/<province_id>/tax-policy (if implemented):
returns current tax policy for that province, or 404 if not set

Verify via curl:
401 without JWT
200 for valid owner
404 for missing records/policy

Commit:
feat(tax): implement read endpoints with ownership checks

-Step 4: Internal init (POST /tax)-

- Files:
game_app/core/tax/routes.py
game_app/core/provinces/routes.py (POST /province/create)

Behavior:

POST /tax:
auth: admin-only for now (same pattern as population internal)
body: province_id + optionally default tax_rate
create:
default TaxPolicy for the province (if you’ve added it)
zeroed or initial TaxRecord entries for each region (or leave records to end-turn)
integrate:
after province + population are created, call internal tax init helper

Verify:
create a new province, check DB:
there’s a TaxPolicy row and/or baseline tax data tied to that province

Commit:
feat(tax): add internal init and hook into province creation

-Step 5: End-turn computation stub (PATCH /tax/<province_id>)-

- Files:
game_app/core/tax/routes.py

Behavior (v1 stub, simple rule):
auth: internal/admin only
for a given province_id:
query population data (read-only) – even if this starts as a simple join/query
compute tax_collected = population_size_snapshot * tax_rate per region

insert a new TaxRecord per region with:
turn_number
tax_collected
tax_rate
optional population snapshot


Verify:
seed or reuse existing population for a province
call PATCH /tax/<province_id>
confirm new TaxRecord rows appear with expected values

Commit:
feat(tax): add basic end-turn tax computation

-Step 6: Error/response shape + docs-

- Files:
game_app/core/tax/routes.py
README / docs

Actions:
align tax errors with existing pattern:
401 → {"code":"Unauthorized", ...}
403 for forbidden internal/admin routes if you add that distinction
404 → "Tax Record Not Found" or "Tax Policy Not Found"
400 for invalid rate inputs (e.g., tax_rate outside 0–1)

update README:
once implemented, move tax routes from “design-only” to “implemented”
add a short section in a tax-security-review.md or extend the existing province/security docs with a “tax” section

Commit:
chore(tax): align error shapes and update docs
