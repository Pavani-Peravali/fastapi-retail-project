from data_loader import load_data


from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"message": "FastAPI is working successfully"}

from fastapi import HTTPException
customers = {}

@app.post("/customers")
def create_customer(customer: dict):
    customer_id = customer.get("customer_id")
    customer_id = int(customer_id)
    if customer_id in customers:
        raise HTTPException(status_code=400, detail="Customer already exists")
    customers[customer_id] = customer
    return {"message": "Customer created successfully", "data": customer}

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="customer not found")
    return customers[customer_id]


invoices = {}

retail_df = load_data()

@app.post("/customers/{customer_id}/invoice")
def create_invoice(customer_id: int, invoice: dict):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    invoice_no = invoice.get("invoice_no")

    if invoice_no is None:
        raise HTTPException(status_code=400, detail="invoice_no is required")

    if invoice_no in invoices:
        raise HTTPException(status_code=400, detail="Invoice already exists")

    invoices[invoice_no] = {
        "customer_id": customer_id,
        "description": invoice.get("description"),
        "items": []
    }

    return {
        "message": "Invoice created successfully",
        "invoice_no": invoice_no
    }

@app.get("/customers/{customer_id}/invoice")
def read_invoice(customer_id:int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    result = []
    for invoice_no, invoice_data in invoices.items():
        if invoice_data["customer_id"] == customer_id:
            result.append({
                "invoice_no": invoice_no,
                **invoice_data
            })
    return result

@app.get("/invoice/{invoice_no}")
def read_invoice(invoice_no: str):
    if invoice_no not in invoices:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        "invoice_no": invoice_no,
        **invoices[invoice_no]
    }
@app.post("/invoice/{invoice_no}/{stockcode}")
def add_item(invoice_no: str, stockcode: str, item: dict):
    if invoice_no not in invoices:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if item.get("stockcode") != stockcode:
        raise HTTPException(status_code=400, detail="Stockcode mismatch")
    invoices[invoice_no]["items"].append(item)
    return{
        "message": "Item added successfully",
        "invoice_no": invoice_no,
        "item": item
    }

@app.get("/invoice/{invoice_no}/{stockcode}")
def read_item(invoice_no: str, stockcode: str):
    if invoice_no not in invoices:
        raise HTTPException(status_code=404, detail="Invoice not found")
    for item in invoices[invoice_no]["items"]:
        if item["stockcode"] == stockcode:
            return item
    raise HTTPException(status_code=404, detail="Invoice not found")

@app.get("/dataset/summary")
def dataset_summary():
    if retail_df.empty:
        return {"message": "No dataset loaded"}
    return {
        "rows": len(retail_df),
        "columns": retail_df.columns.tolist(),
        "sample_data": retail_df.head(5).fillna("").to_dict(orient="records")
    }

@app.get("/dataset/invoice/{invoice_no}")
def dataset_invoice(invoice_no: str):
    if retail_df.empty:
        return {"message": "No dataset loaded"}
    # handle both possible column names
    if "invoiceno" in retail_df.columns:
        filtered = retail_df[retail_df["invoiceno"].astype(str) == str(invoice_no)]
    elif "invoice_no" in retail_df.columns:
        filtered = retail_df[retail_df["invoice_no"].astype(str) == str(invoice_no)]
    else:
        return {"message": "Invoice column not found"}
    if filtered.empty:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return filtered.head(20).fillna("").to_dict(orient="records")

@app.get("/dataset/customer/{customer_id}")
def dataset_customer(customer_id: int):
    if retail_df.empty:
        return {"message": "No dataset loaded"}
    # check column name
    if "customerid" not in retail_df.columns:
        return {"message": "customerid column not found"}
    
    filtered = retail_df[retail_df["customerid"] == customer_id]

    if filtered.empty:
        raise HTTPException(status_code=404, detail="Customer not found in dataset")
    
    return {
        "customer_id": customer_id,
        "records": filtered.head(20).fillna("").to_dict(orient="records")
    }
    