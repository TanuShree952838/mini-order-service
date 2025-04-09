# Mini Order Processing Service

**Problem Statement**  
Develop a mini service for a small online retailer that processes customer orders. The system must:

- Validate input
- Apply bulk discount rules
- Calculate a shipping fee if the order subtotal is below a defined threshold
- Update product inventories accordingly

---

## - Technical Requirements

### Core Logic:
- [x] Use Pydantic for JSON input validation
- [x] Calculate bulk discounts when product quantities exceed a set limit
- [x] Add a flat shipping fee if the order subtotal is under a certain amount

### Database Interaction:
- [x] Use SQLAlchemy to model products and orders
- [x] Ensure atomic updates to inventory during order processing

### REST API:
- [x] POST /orders — order submission
- [x] GET /products — product retrieval
- [x] Proper error handling

### Testing:
- [x] Unit tests for transformation logic
- [x] FastAPI TestClient for endpoint testing

---
### Approach  
Break the solution into 6 simple components:

1. **Models**  
   - SQLAlchemy models for `Product`, `Order`, and `OrderItem`  
   - Define table structure, relationships, and constraints  

2. **Schemas**  
   - Pydantic models for request and response validation  
   - Ensure only valid, structured data is accepted and returned  

3. **Repositories**  
   - Database operations are abstracted here  
   - Handle DB queries, inserts, updates, and transactions cleanly
   - Keeps business logic separate from DB logic  

4. **Services**  
   - Core business logic:  
     - Apply bulk discounts  
     - Add shipping fee if subtotal is low  
     - Ensure stock is available and update inventory  
   - Central place for reusable logic  

5. **API (main.py)**  
   - FastAPI endpoints  
     - `GET /products` – Fetch product list  
     - `POST /orders` – Place new orders  
   - Connects frontend callers to services and DB  

6. **Testing**  
   - Use `pytest` for testing logic  
   - Use `TestClient` from FastAPI to test API endpoints  
   - Covers edge cases like empty products, bulk discounts, insufficient stock

---

## - How to Run the App

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## - How to Run the Tests

```bash
PYTHONPATH=. pytest -v tests/
