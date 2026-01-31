# Multi-Source E-Commerce ETL Pipeline

A fully containerized data engineering project utilizing **Apache Airflow** for orchestration and **dbt** for transformations. This pipeline extracts data from a PostgreSQL source, S3 (MinIO), and a paginated Mock API, loading it into a PostgreSQL Data Warehouse.

## 🚀 Project Overview

This repository demonstrates a robust ETL (Extract, Transform, Load) architecture:

* **Extraction**: Multi-source data ingestion (API, SQL, S3).
* **Staging**: Raw data storage in a dedicated `staging` schema.
* **Transformation**: dbt models for dimension and fact table creation.
* **Testing**: Automated data quality checks using `dbt test`.

---

## 🛠️ Tech Stack

* **Orchestration**: Apache Airflow 2.7.1
* **Transformation**: dbt (Data Build Tool) with `dbt-postgres`
* **Storage**: PostgreSQL (Source & Warehouse), MinIO (S3-compatible)
* **Containerization**: Docker & Docker Compose

---

## 📂 Project Structure

```text
├── dags/                       # Airflow DAG definitions
├── dbt_project/                # dbt models and configurations
├── seeds/                      # SQL and CSV files for initial DB/S3 seeding
├── .env.example                # Template for environment variables
└── docker-compose.yml          # Infrastructure definition

```
---

## 📋 Prerequisites

* Docker and Docker Compose installed.
* At least 4GB of RAM allocated to Docker.

---

## ⚙️ Setup & Installation

1. **Clone the Repository**:
```bash
git clone <your-repo-link>
cd Multi-Source-E-commerce-ETL-Pipeline-with-Apache-Airflow-and-dbt

```


2. **Environment Configuration**:
Copy the example environment file and update if necessary:
```bash
cp .env.example .env

```


3. **Launch the Environment**:
```bash
docker-compose up -d

```


*Note: The first run may take a few minutes as it installs `dbt-postgres` and initializes the databases.*

---

## 📊 Pipeline Structure

### 1. Airflow DAG: `ecommerce_etl_pipeline`

The DAG is scheduled `@daily` and performs the following tasks:

* `extract_api`: Fetches paginated order data.
* `extract_s3`: Loads `inventory.csv` from MinIO.
* `extract_db`: Pulls `users` and `products` from the source DB.
* `dbt_run`: Executes transformations to build `dim_users`, `dim_products`, and `fct_orders`.
* `dbt_test`: Runs schema and data quality tests.

### 2. dbt Models

* **`dim_users`**: Cleaned user dimension.
* **`dim_products`**: Product details enriched with stock levels from inventory.
* **`fct_orders`**: Incremental fact table tracking sales performance.

---

## ✅ Verification
To confirm the pipeline has successfully isolated and transformed the data:

1. **Check Staging Schema:**
   
```bash
docker exec -it data_warehouse psql -U user -d dwh -c "\dt staging.*"
```

2. **Check Final Fact Table:**
   
```bash
docker exec -it data_warehouse psql -U user -d dwh -c "SELECT * FROM public.fct_orders LIMIT 5;"
```

**Expected Result:** A successful run should return a count (e.g., `25` records).

---

## 🧪 Testing

Data quality is enforced through dbt tests:

* **Uniqueness**: Ensured for `user_id` and `product_id`.
* **Null Checks**: Critical ID columns are verified to be non-null.

To run tests manually:

```bash
docker exec -it airflow_web dbt test --project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_project
```
