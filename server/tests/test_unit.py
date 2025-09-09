import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from app.worker import tasks
from app.services import jobs


@pytest.mark.asyncio
@patch("app.worker.tasks.AsyncSessionLocal")
@patch("app.worker.tasks.RequestLog")
@patch("app.worker.tasks.User")
@patch("app.worker.tasks.Broker")
async def test_get_request_info(
    mock_broker, mock_user, mock_requestlog, mock_sessionlocal
):
    # Setup mocks
    mock_session = AsyncMock()
    mock_sessionlocal.return_value.__aenter__.return_value = mock_session
    mock_req = MagicMock()
    mock_user_obj = MagicMock()
    mock_broker_obj = MagicMock()
    mock_session.get.side_effect = [mock_req, mock_user_obj, mock_broker_obj]
    req, user, broker = await tasks.get_request_info(1)
    assert req == mock_req
    assert user == mock_user_obj
    assert broker == mock_broker_obj


@pytest.mark.asyncio
@patch("app.worker.tasks.AsyncSessionLocal")
@patch("app.worker.tasks.RequestLog")
@patch("app.worker.tasks.User")
@patch("app.worker.tasks.Broker")
async def test_get_request_info_db_error(
    mock_broker, mock_user, mock_requestlog, mock_sessionlocal
):
    # Simulate DB error
    mock_session = AsyncMock()
    mock_sessionlocal.return_value.__aenter__.return_value = mock_session
    mock_session.get.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        await tasks.get_request_info(1)


@pytest.mark.asyncio
@patch("app.worker.tasks.get_request_info", new_callable=AsyncMock)
@patch("app.worker.tasks.SMTP")
async def test_send_email_task(mock_smtp, mock_get_request_info):
    req = MagicMock()
    user = MagicMock(
        full_name="Test", email="test@example.com", phone="123", address="Addr"
    )
    broker = MagicMock(name="Broker", url="broker@example.com")
    mock_get_request_info.return_value = (req, user, broker)
    smtp_instance = AsyncMock()
    mock_smtp.return_value = smtp_instance
    await tasks.send_email_task(1)
    smtp_instance.sendmail.assert_awaited()
    assert req.status in ["Completed", "Failed"]


@pytest.mark.asyncio
@patch("app.worker.tasks.get_request_info", new_callable=AsyncMock)
@patch("app.worker.tasks.SMTP")
async def test_send_email_task_exception(mock_smtp, mock_get_request_info):
    req = MagicMock()
    user = MagicMock(
        full_name="Test", email="test@example.com", phone="123", address="Addr"
    )
    broker = MagicMock(name="Broker", url="broker@example.com")
    mock_get_request_info.return_value = (req, user, broker)
    smtp_instance = AsyncMock()
    smtp_instance.sendmail.side_effect = Exception("SMTP error")
    mock_smtp.return_value = smtp_instance
    await tasks.send_email_task(1)
    assert req.status == "Failed"


@pytest.mark.asyncio
@patch("app.worker.tasks.get_request_info", new_callable=AsyncMock)
@patch("app.worker.tasks.async_playwright")
async def test_submit_form_task(mock_playwright, mock_get_request_info):
    req = MagicMock()
    user = MagicMock(full_name="Test", email="test@example.com", phone="123")
    broker = MagicMock(url="http://example.com")
    mock_get_request_info.return_value = (req, user, broker)
    browser = AsyncMock()
    page = AsyncMock()
    browser.new_page.return_value = page
    context = AsyncMock()
    context.chromium.launch.return_value = browser
    mock_playwright.return_value.__aenter__.return_value = context
    await tasks.submit_form_task(1)
    page.goto.assert_awaited_with(broker.url)
    assert req.status in ["Completed", "Failed"]


@pytest.mark.asyncio
@patch("app.worker.tasks.get_request_info", new_callable=AsyncMock)
@patch("app.worker.tasks.async_playwright")
async def test_submit_form_task_exception(mock_playwright, mock_get_request_info):
    req = MagicMock()
    user = MagicMock(full_name="Test", email="test@example.com", phone="123")
    broker = MagicMock(url="http://example.com")
    mock_get_request_info.return_value = (req, user, broker)
    browser = AsyncMock()
    page = AsyncMock()
    browser.new_page.return_value = page
    context = AsyncMock()
    context.chromium.launch.return_value = browser
    mock_playwright.return_value.__aenter__.return_value = context
    page.goto.side_effect = Exception("Playwright error")
    await tasks.submit_form_task(1)
    assert req.status == "Failed"


@patch("app.worker.tasks.get_request_info")
@patch("app.worker.tasks.HTML")
@patch("app.worker.tasks.asyncio.run")
def test_generate_pdf_task(mock_asyncio_run, mock_html, mock_get_request_info):
    req = MagicMock()
    user = MagicMock(
        full_name="Test", email="test@example.com", phone="123", address="Addr"
    )
    broker = MagicMock(name="Broker")
    mock_get_request_info.return_value = (req, user, broker)
    html_instance = MagicMock()
    mock_html.return_value = html_instance
    tasks.generate_pdf_task(1)
    html_instance.write_pdf.assert_called()
    assert req.status in ["Completed", "Failed"]


@patch("app.worker.tasks.get_request_info")
@patch("app.worker.tasks.HTML")
@patch("app.worker.tasks.asyncio.run")
def test_generate_pdf_task_exception(
    mock_asyncio_run, mock_html, mock_get_request_info
):
    req = MagicMock()
    user = MagicMock(
        full_name="Test", email="test@example.com", phone="123", address="Addr"
    )
    broker = MagicMock(name="Broker")
    mock_get_request_info.return_value = (req, user, broker)
    html_instance = MagicMock()
    mock_html.return_value = html_instance
    html_instance.write_pdf.side_effect = Exception("PDF error")
    tasks.generate_pdf_task(1)
    assert req.status == "Failed"


def test_process_dead_letter_queue_logs_and_requeues(monkeypatch):
    job1 = MagicMock(id="1", exc_info="fail1")
    job2 = MagicMock(id="2", exc_info="fail2")
    jobs.dead_letter_queue.get_jobs = MagicMock(return_value=[job1, job2])
    job1.requeue = MagicMock()
    job2.requeue = MagicMock()
    # Log only
    jobs.process_dead_letter_queue(log_failed=True, requeue=False)
    # Log and requeue
    jobs.process_dead_letter_queue(log_failed=True, requeue=True)
    job1.requeue.assert_called_with(jobs.queue)
    job2.requeue.assert_called_with(jobs.queue)


@patch("app.services.jobs.queue")
@patch("app.services.jobs.Retry")
def test_enqueue_request(mock_retry, mock_queue):
    mock_job = MagicMock()
    mock_queue.enqueue.return_value = mock_job
    jobs.enqueue_request(123)
    mock_queue.enqueue.assert_called()
