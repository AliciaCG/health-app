/**
 * ui.js — all DOM reads/writes.
 * No fetch calls here; receives data and renders it.
 */

// ── Utility helpers ────────────────────────────────────────────────────────

/** Capitalise first letter of a string. */
const cap = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : '');

/** Escape HTML special characters to prevent XSS. */
const esc = (s) =>
  String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

/** Format an ISO timestamp to a readable date string. */
const formatDate = (iso) =>
  new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  });


// ── Toast ──────────────────────────────────────────────────────────────────

const Toast = (() => {
  const el = document.getElementById('toast');
  let timer = null;

  return {
    show(message, isError = false) {
      el.textContent = message;
      el.className = `toast--visible${isError ? ' toast--error' : ''}`;
      clearTimeout(timer);
      timer = setTimeout(() => { el.className = ''; }, 3000);
    },
  };
})();


// ── API status indicator ───────────────────────────────────────────────────

const StatusIndicator = (() => {
  const el     = document.getElementById('apiStatus');
  const label  = el.querySelector('.api-status__label');

  return {
    setConnected(connected) {
      if (connected) {
        el.classList.add('api-status--connected');
        label.textContent = 'api connected';
      } else {
        el.classList.remove('api-status--connected');
        label.textContent = 'api offline';
      }
    },
  };
})();


// ── Records table ──────────────────────────────────────────────────────────

const RecordsTable = (() => {
  const tbody     = document.getElementById('recordsBody');
  const countEl   = document.getElementById('recordCount');

  /**
   * Build a health badge element.
   * @param {string} health
   * @returns {string} HTML string
   */
  function buildBadge(health) {
    return `<span class="health-badge health-badge--${esc(health)}">${esc(cap(health))}</span>`;
  }

  /**
   * Build a single table row.
   * @param {object} record
   * @returns {string} HTML string
   */
  function buildRow(record) {
    const fullName = `${cap(record.firstname)} ${cap(record.lastname)}`;
    return `
      <tr data-id="${record.id}">
        <td class="cell--id">${esc(record.id)}</td>
        <td class="cell--name">${esc(fullName)}</td>
        <td>${esc(record.age)}</td>
        <td>${esc(cap(record.sex))}</td>
        <td>${buildBadge(record.health)}</td>
        <td>${esc(formatDate(record.created_at))}</td>
        <td>
          <button
            class="btn btn--action"
            data-action="delete"
            data-id="${record.id}"
            aria-label="Delete record for ${esc(fullName)}"
          >delete</button>
        </td>
      </tr>`;
  }

  return {
    setLoading() {
      tbody.innerHTML = '<tr class="row--loading"><td colspan="7">loading records...</td></tr>';
    },

    setError(apiBase) {
      tbody.innerHTML = `
        <tr class="row--error">
          <td colspan="7">Could not reach API at ${esc(apiBase)}</td>
        </tr>`;
    },

    render(records) {
      countEl.textContent = records.length;

      if (records.length === 0) {
        tbody.innerHTML = `
          <tr><td colspan="7">
            <div class="empty-state">
              <div class="empty-state__icon" aria-hidden="true">◈</div>
              <p class="empty-state__text">No records yet — add one above</p>
            </div>
          </td></tr>`;
        return;
      }

      tbody.innerHTML = records.map(buildRow).join('');
    },

    /** Mark a specific row as pending deletion. */
    setRowPending(id) {
      const btn = tbody.querySelector(`[data-action="delete"][data-id="${id}"]`);
      if (btn) {
        btn.textContent = '...';
        btn.disabled = true;
      }
    },

    /** Restore a row's delete button (on error). */
    restoreRow(id) {
      const btn = tbody.querySelector(`[data-action="delete"][data-id="${id}"]`);
      if (btn) {
        btn.textContent = 'delete';
        btn.disabled = false;
      }
    },
  };
})();


// ── Record form ────────────────────────────────────────────────────────────

const RecordForm = (() => {
  const fields = {
    firstname: document.getElementById('firstname'),
    lastname:  document.getElementById('lastname'),
    age:       document.getElementById('age'),
    sex:       document.getElementById('sex'),
    health:    document.getElementById('health'),
  };
  const submitBtn = document.getElementById('submitBtn');

  return {
    /** Read and validate all field values. Returns data or null on error. */
    read() {
      const data = {
        firstname: fields.firstname.value.trim(),
        lastname:  fields.lastname.value.trim(),
        age:       fields.age.value,
        sex:       fields.sex.value,
        health:    fields.health.value,
      };

      if (Object.values(data).some((v) => !v)) {
        Toast.show('Please fill in all fields', true);
        return null;
      }

      return { ...data, age: parseInt(data.age, 10) };
    },

    clear() {
      fields.firstname.value = '';
      fields.lastname.value  = '';
      fields.age.value       = '';
      fields.sex.selectedIndex    = 0;
      fields.health.selectedIndex = 0;
    },

    setSubmitting(submitting) {
      submitBtn.disabled    = submitting;
      submitBtn.textContent = submitting ? 'Adding...' : '+ Add Record';
    },

    /** Attach a submit handler; also fires on Enter from any input/select. */
    onSubmit(handler) {
      submitBtn.addEventListener('click', handler);
      Object.values(fields).forEach((el) => {
        el.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') handler();
        });
      });
    },
  };
})();
