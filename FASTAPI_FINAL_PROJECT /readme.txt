# Gym Management System

A fully functional FastAPI backend system designed for managing the "IronFit Gym". This project implements all Day 1 – Day 6 concepts required for the FastAPI Final Assignment, covering CRUD operations, Pydantic validations, dynamic computations, filtering, searching, sorting, and pagination.

## Features Implemented
* **Day 1: REST APIs**: Developed pure GET endpoints retrieving plan records, membership lists, summaries of gym plans, and dynamic counts.
* **Day 2: POST & Validation**: Implemented creating memberships with `Pydantic` `EnrollRequest` enforcing constraints like name length and dynamic defaults.
* **Day 3: Helpers & Filters**: Modularized logic into standard python functions such as `calculate_membership_fee` (with discounts based on duration and referral) and `filter_plans_logic`. 
* **Day 4: CRUD Operations**: Add new plans handling potential duplicate names, update plans handling partial edits optionally, and block deleting plans that are linked to active members safely.
* **Day 5: Multi-Step Workflow**: An interconnected process where users can Book Classes only if their active membership allows it, and functionalities to freeze and reactivate active memberships seamlessly.
* **Day 6: Advanced APIs**: Robust `keyword` searching (case-insensitive checking in both string and boolean configurations), result sorting natively through queries, mathematics-driven list slicing for Pagination, and an all-in-one browsing super-endpoint.

## Complete Project Structure
- `main.py` - Core application file with all API routes properly partitioned (fixed routes before variable ones).
- `requirements.txt` - Required project dependencies.
- `README.md` - Complete markdown documentation.
- `screenshots/` - Mandatory directory for saving Swagger UI outputs.

## Setup Instructions
1. Install dependencies locally:
   ```bash
   pip install -r requirements.txt
   ```
2. Start up the backend server properly:
   ```bash
   uvicorn main:app --reload
   ```
3. Test your 20 task APIs:
   Navigate to `http://127.0.0.1:8000/docs` in your browser where Swagger UI interacts with the app natively.

## Mandatory Next Actions For Grading
- [x] Create project structure
- [x] Implement all **20 tasks** locally inside `main.py`
- [ ] Thoroughly click through the endpoints in **Swagger** and save testing screenshots to the included `/screenshots/` empty directory
- [ ] Push contents to your unique generic Github Repository
- [ ] Publish an engaging **LinkedIn Post** explicitly showing this system tagging **Innomatics Research Labs**
- [ ] **Submit the official Google Form.**
