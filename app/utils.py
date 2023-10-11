from passlib.context import CryptContext
from . import models
from . import schemas
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from .database import get_db
from fastapi import Depends, HTTPException
from weasyprint import HTML
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi.responses import JSONResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import random
import uuid
import string


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password: str):
    return pwd_context.hash(password)


def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)

def generate_invoice_report(invoice):
    # Create a dictionary with the details you want to include in the report
    report = {
        "order_number": invoice.order_number,
        "title": invoice.title,
        "cost_per_page": invoice.cost_per_page,
        "pages_done": invoice.pages_done,
        "total_amount_per_job": invoice.total_amount_per_job,
        "total_amount_for_all_jobs": invoice.total_amount_for_all_jobs,
        "paid_amount": invoice.paid_amount,
        "advance_amount": invoice.advance_amount,
        "remaining": invoice.remaining,
        "due_date": invoice.due_date,
        "job_status": invoice.job_status,
        "order_status": invoice.order_status,
    }
    return report


def generate_pdf_report(invoice):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create data for the table
    data = [
        ["Order Number", invoice.order_number],
        ["Title", invoice.title],
        ["Cost per Page", str(invoice.cost_per_page)],
        ["Pages", str(invoice.pages_done)],
        ["Amount", str(invoice.total_amount_per_job)],
        ["Total", str(invoice.total_amount_for_all_jobs)],
        ["Paid", str(invoice.paid_amount)],
        ["Advance", str(invoice.advance_amount)],
        ["Pending", str(invoice.remaining)],
    ]

    # Create the table
    table = Table(data, colWidths=[100, 200])

    # Style the table
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, 5), colors.beige),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(style)

    # Build the PDF document
    elements = [table]
    doc.build(elements)

    buffer.seek(0)
    return buffer

def generate_short_code(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
