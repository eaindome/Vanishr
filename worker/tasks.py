import asyncio
from playwright.async_api import async_playwright
from aiosmtplib import SMTP
from weasyprint import HTML
from app.data.db import AsyncSessionLocal
from app.data.models import RequestLog, Broker, User

# ---------------------------
# Helper to get DB session
# ---------------------------
async def get_request_info(request_id: int):
    async with AsyncSessionLocal() as session:
        req = await session.get(RequestLog, request_id)
        user = await session.get(User, req.user_id)
        broker = await session.get(Broker, req.broker_id)
        return req, user, broker

# ---------------------------
# Email Task
# ---------------------------
async def send_email_task(request_id: int):
    req, user, broker = await get_request_info(request_id)

    message = f"""Subject: Privacy Opt-Out Request

Dear {broker.name},

Please remove my personal information from your database.

Name: {user.full_name}
Email: {user.email}
Phone: {user.phone}
Address: {user.address}

Thank you.
"""
    smtp_host = "smtp.example.com"  # replace with real SMTP server
    smtp_port = 587
    smtp_user = "your_email@example.com"
    smtp_pass = "your_password"

    try:
        smtp = SMTP(hostname=smtp_host, port=smtp_port)
        await smtp.connect()
        await smtp.starttls()
        await smtp.login(smtp_user, smtp_pass)
        await smtp.sendmail(smtp_user, broker.url, message)  # assuming broker.url is email
        await smtp.quit()
        req.status = "Completed"
    except Exception as e:
        print(f"Email task failed: {e}")
        req.status = "Failed"

    async with AsyncSessionLocal() as session:
        session.add(req)
        await session.commit()

# ---------------------------
# Form Submission Task
# ---------------------------
async def submit_form_task(request_id: int):
    req, user, broker = await get_request_info(request_id)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(broker.url)
            # Example: fill form fields (adjust selectors)
            await page.fill("input[name='full_name']", user.full_name)
            await page.fill("input[name='email']", user.email)
            if user.phone:
                await page.fill("input[name='phone']", user.phone)
            await page.click("button[type='submit']")
            await browser.close()
        req.status = "Completed"
    except Exception as e:
        print(f"Form task failed: {e}")
        req.status = "Failed"

    async with AsyncSessionLocal() as session:
        session.add(req)
        await session.commit()

# ---------------------------
# PDF Letter Generation Task
# ---------------------------
def generate_pdf_task(request_id: int):
    import asyncio
    req, user, broker = asyncio.run(get_request_info(request_id))

    html_content = f"""
    <html>
    <body>
        <p>Dear {broker.name},</p>
        <p>Please remove my personal information from your database:</p>
        <ul>
            <li>Name: {user.full_name}</li>
            <li>Email: {user.email}</li>
            <li>Phone: {user.phone}</li>
            <li>Address: {user.address}</li>
        </ul>
        <p>Thank you.</p>
    </body>
    </html>
    """

    pdf_file = f"/tmp/request_{request_id}.pdf"
    HTML(string=html_content).write_pdf(pdf_file)

    req.status = "Completed"
    asyncio.run(_commit_status(req))

async def _commit_status(req):
    async with AsyncSessionLocal() as session:
        session.add(req)
        await session.commit()

# ---------------------------
# Main processing function
# ---------------------------
def process_request(request_id: int):
    """
    Decide which task to run based on broker opt_out_method
    """
    import asyncio
    from app.db import AsyncSessionLocal
    from app.models import RequestLog, Broker

    async def main():
        async with AsyncSessionLocal() as session:
            req = await session.get(RequestLog, request_id)
            broker = await session.get(Broker, req.broker_id)

            if broker.opt_out_method == "email":
                await send_email_task(request_id)
            elif broker.opt_out_method == "form":
                await submit_form_task(request_id)
            elif broker.opt_out_method == "letter":
                generate_pdf_task(request_id)
            else:
                req.status = "Failed"
                session.add(req)
                await session.commit()

    asyncio.run(main())
