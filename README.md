# Basic ETL Pipeline – Sales Data Processing  

## 📌 Project Overview  
This project demonstrates a simple **Extract, Transform, Load (ETL)** process using **Python**, **Pandas**, and **PostgreSQL** (with Adminer for database management).  
It processes raw sales order data from a CSV file, cleans and transforms it, and loads it into a PostgreSQL database.  

---

## 🗂 Data Source  
The input dataset (`main_data.csv`) contains fictional customer purchase records:  

| date       | time  | location    | customer          | price | payment_method | masked_card_number |
|------------|-------|-------------|------------------|-------|----------------|--------------------|
| 09/05/2023 | 10:17 | Manchester  | Mikasa Ackerman  | 3.20  | CASH           |                    |
| 09/05/2023 | 10:19 | Birmingham  | Light Yagami     | 3.00  | CARD           | XXXXXXXXXXXXXX22   |
| ...        | ...   | ...         | ...              | ...   | ...            | ...                |

---

## ⚙️ ETL Steps  

### 1️⃣ Extract  
- Reads the **raw CSV file** into a Pandas DataFrame.  

### 2️⃣ Transform  
- **Renames columns** for clarity.  
- **Splits** combined datetime into separate `date` and `time` fields.  
- **Cleans customer names** by removing unwanted characters.  
- **Splits multiple orders** into separate columns (`order_1`, `order_2`, etc.) with corresponding prices.  
- **Masks card numbers** (keeping only last 4 digits).  
- **Removes duplicates** and checks for missing values.  

### 3️⃣ Load  
- Creates an **`orders`** table in PostgreSQL (if it doesn't already exist).  
- Inserts cleaned data into the database using **`psycopg2`**.  

---

## 🛠 Tech Stack  
- **Python 3**  
- **Pandas** – Data manipulation  
- **Psycopg2** – PostgreSQL database connection  
- **PostgreSQL** – Data storage  
- **Docker** – Database containerization  
- **Adminer** – Database management UI  
- **dotenv** – Environment variable management  

---

## 📦 Project Setup  

### 1️⃣ Clone Repository  
```bash
git clone https://github.com/yourusername/basic-etl-pipeline.git
cd basic-etl-pipeline
