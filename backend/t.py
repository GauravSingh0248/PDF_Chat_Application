from app.services.faq_service import generate_pdf_faqs


result = generate_pdf_faqs(
    "5c6a191d-0597-47e8-b693-5c0e956f2c91"
)

print(result)