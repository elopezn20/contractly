# Contractly – README

MVP para gestión de subcontratistas con precalificación y un BFF de resumen.

---

## Cómo correr la solución

### Requisitos

* Python 3.11+
* pip y venv

### Setup

```bash
# 1) Crear entorno
python3 -m venv .venv
source .venv/bin/activate 

# 2) Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt  # (o pip install fastapi uvicorn pydantic[dotenv] pytest httpx)

# 3) Correr API
uvicorn main:app --reload  # o: uvicorn app.entrypoints.api:app --reload

# 4) Probar
open http://127.0.0.1:8000/docs
```

### Tests

```bash
PYTHONPATH=. pytest -v
```

### Frontend

Se puede navegar una interfaz de usuario muy simple abriendo el archivo en frontend/index.html

## Decisiones de Arquitectura

### 1) Clean + Hexagonal Architecture

**Objetivo:** separar el núcleo de negocio (dominio) de frameworks y detalles de infraestructura.

**Capas:**

* **Domain (Core):** entidades (Contractor), value objects, reglas; puertos (interfaces) que expresan lo que el dominio necesita: `ContractorRepository`, `PrequalificationService`.
* **Application (Use Cases):** orquesta casos de uso: `CreateContractor`, `ListContractors`, `RunPrequalification`, `GetSummary`.
* **BFF (Backend for Frontend):** endpoint específico `/bff/summary` que agrega métricas para el front.


### 2) DIP + Repositorios (Inversión de Dependencias)

* Los casos de uso dependen de interfaces del repositorio y del servicio de precalificación, no de implementaciones concretas.

### 3) Modelado del Dominio

* Entidad `Contractor`: `id`, `business_name`, `tax_id`, `main_contact`, `certifications: list[str]`, `years_of_experience: int`, `prequalification_status`.
* Estados de precalificación: `UNASSESSED` (por defecto), `PENDING`, `APPROVED`, `REJECTED`.


---

## Endpoints

### 1) Crear contratista

`POST /contractors`

**Request**

```bash
curl -X POST http://localhost:8000/contractors \
  -H "Content-Type: application/json" \
  -d '{
    "businessName": "Company 1",
    "taxId": "111",
    "mainContact": "john@company.com,
    "certifications": ["ISO9001","OSHA"],
    "yearsOfExperience": 5
  }'
```

**201 Response**

```json
{
  "id": "c_01J0WQ8H42X6A6C3R4",
  "businessName": "Company 1",
  "taxId": "111",
  "mainContact": "john@company.com",
  "certifications": ["ISO9001","OSHA"],
  "yearsOfExperience": 5,
  "prequalificationStatus": "UNASSESSED"
}
```
---

### 2) Listar contratistas

`GET /contractors`

**Request**

```bash
curl http://localhost:8000/contractors
```

**200 Response**

```json
[
  {
    "id": "c_01J0WQ8H42X6A6C3R4",
    "businessName": "Company 1",
    "taxId": "111",
    "mainContact": "john@company.com",
    "certifications": ["ISO9001","OSHA"],
    "yearsOfExperience": 5,
    "prequalificationStatus": "PENDING"
  }
]
```

---

### 3) Lanzar precalificación (usa el mock externo)

`POST /contractors/{contractorId}/prequalify`

**Request**

```bash
curl -X POST http://localhost:8000/contractors/c_01J0W…/prequalify
```

**200 Response**

```json
{
  "contractorId": "c_01J0W…",
  "status": "APPROVED"
}
```

**404** si el `contractorId` no existe.



### 4) Resumen BFF

`GET /bff/summary`

**Request**

```bash
curl http://localhost:8000/bff/summary
```

**200 Response**

```json
{
  "total": 12,
  "approved": 5,
  "rejected": 2,
  "pending": 3,
  "unassessed": 2
}
```

---
