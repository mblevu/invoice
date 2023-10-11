from fastapi import APIRouter, Depends, HTTPException, Body, Response, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from weasyprint import HTML
from ..models import Invoice
from ..database import SessionLocal
from .. import database, schemas, oauth2
from typing import List
from .. import models
import uuid
from ..utils import generate_invoice_report, generate_pdf_report, generate_short_code
router = APIRouter(
    prefix='/invoice',
    tags=['Invoices']
)


@router.post("/", response_model=schemas.CreateInvoice)

def create_invoice(invoice: schemas.CreateInvoice,
                   db: Session = Depends(database.get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    short_code = generate_short_code(5)
    order_number = f"{short_code}-{uuid.uuid4().hex[:10]}"
    # Set the user_id based on the authenticated user
    db_invoice = models.Invoice(
        order_number=order_number,
        title=invoice.title,
        cost_per_page=invoice.cost_per_page,
        pages_done=invoice.pages_done,
        total_amount_per_job=invoice.total_amount_per_job,
        total_amount_for_all_jobs=invoice.total_amount_for_all_jobs,
        paid_amount=invoice.paid_amount,
        advance_amount=invoice.advance_amount,
        remaining=invoice.remaining,
        due_date=invoice.due_date,
        job_status=invoice.job_status,
        order_status=invoice.order_status,
        user_id=current_user.id
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return db_invoice



@router.get("/all", response_model=List[schemas.InvoiceResponse])

def list_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    invoice = db.query(Invoice).offset(skip).limit(limit).all()
    return invoice

@router.get("/{invoice_id}", response_model=schemas.InvoiceResponse)

def get_invoice_by_id(invoice_id: int, db: Session = Depends(database.get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.get("/{invoice_id}/report", response_model=dict)

def get_invoice_report(invoice_id: int, db: Session = Depends(database.get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    report = generate_invoice_report(invoice)
    return report

@router.get("/{invoice_id}/report-pdf", response_class=Response)
def download_invoice_pdf_report(invoice_id: int, db: Session = Depends(database.get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    pdf_buffer = generate_pdf_report(invoice)

    # Create a FastAPI Response with the PDF content
    response = Response(content=pdf_buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=invoice_report.pdf"

    return response

@router.put("/{invoice_id}", response_model=schemas.InvoiceResponse)

def edit_invoice(invoice_id: int, updated_invoice: schemas.InvoiceResponse, db: Session = Depends(database.get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    db.commit()
    db.refresh(invoice)
    return invoice


@router.delete("/{invoice_id}", response_model=schemas.InvoiceResponse)
def delete_invoice(invoice_id: int, db: Session = Depends(database.get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    return invoice
