/**
 * app.js — application entry point.
 * Wires the API and UI modules together. No fetch or DOM logic here.
 */

const POLL_INTERVAL_MS = 10_000;

// ── Actions ────────────────────────────────────────────────────────────────

async function loadRecords() {
  try {
    const records = await RecordsAPI.list();
    RecordsTable.render(records);
    StatusIndicator.setConnected(true);
  } catch {
    StatusIndicator.setConnected(false);
    RecordsTable.setError('http://localhost:8000');
  }
}

async function handleSubmit() {
  const data = RecordForm.read();
  if (!data) return;

  RecordForm.setSubmitting(true);

  try {
    const created = await RecordsAPI.create(data);
    RecordForm.clear();
    Toast.show(`Record added for ${cap(created.firstname)} ${cap(created.lastname)}`);
    await loadRecords();
  } catch (err) {
    Toast.show(err.message, true);
  } finally {
    RecordForm.setSubmitting(false);
  }
}

async function handleDelete(id) {
  RecordsTable.setRowPending(id);

  try {
    await RecordsAPI.remove(id);
    Toast.show('Record deleted');
    await loadRecords();
  } catch (err) {
    Toast.show(err.message, true);
    RecordsTable.restoreRow(id);
  }
}

// ── Event delegation for table delete buttons ──────────────────────────────

document.getElementById('recordsBody').addEventListener('click', (e) => {
  const btn = e.target.closest('[data-action="delete"]');
  if (btn) {
    handleDelete(Number(btn.dataset.id));
  }
});

// ── Initialise ─────────────────────────────────────────────────────────────

(async function init() {
  RecordsTable.setLoading();
  RecordForm.onSubmit(handleSubmit);

  const online = await RecordsAPI.ping();
  StatusIndicator.setConnected(online);

  await loadRecords();

  setInterval(loadRecords, POLL_INTERVAL_MS);
})();
