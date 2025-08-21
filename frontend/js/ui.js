function toast(msg, type = 'info') {
    const wrap = document.getElementById('toasts');
    const node = document.createElement('div');
    node.className = `px-4 py-2 rounded-xl shadow text-sm ${
      type === 'error'
        ? 'bg-red-100 text-red-800'
        : type === 'success'
        ? 'bg-green-100 text-green-800'
        : 'bg-zinc-100 text-zinc-800'
    }`;
    node.innerText = msg;
    wrap.appendChild(node);
    setTimeout(() => node.remove(), 3500);
  }
  
  function badgeClass(status) {
    const s = String(status || '').toUpperCase();
    if (s === 'APPROVED') return 'bg-green-100 text-green-800';
    if (s === 'REJECTED') return 'bg-red-100 text-red-800';
    if (s === 'PENDING')  return 'bg-amber-100 text-amber-800';
    return 'bg-zinc-100 text-zinc-700';
  }
  
  function renderSummary(s) {
    if (!s) return;
    const el = document.getElementById('summaryCards');
    el.innerHTML = '';
    const cards = [
      { label: 'Total',     value: s.total },
      { label: 'Approved',  value: s.approved },
      { label: 'Rejected',  value: s.rejected },
      { label: 'Pending',   value: s.pending },
      { label: 'Unassessed',     value: s.unassessed },
    ];
    for (const c of cards) {
      const node = document.createElement('div');
      node.className = 'p-4 rounded-2xl shadow bg-white border';
      node.innerHTML = `
        <div class="text-sm text-zinc-500">${c.label}</div>
        <div class="text-2xl font-semibold">${c.value ?? 0}</div>`;
      el.appendChild(node);
    }
  }
  
  function renderContractors(rows) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    for (const r of (rows || [])) {
      const tr = document.createElement('tr');
      tr.className = 'border-b last:border-0';
      const status = r.prequalificationStatus || r.status || r.prequalification || 'UNASSESSED';
      tr.innerHTML = `
        <td class="px-3 py-2 font-mono text-xs">${r.id || r.contractorId || '—'}</td>
        <td class="px-3 py-2">${r.business_name || r.name || '—'}</td>
        <td class="px-3 py-2">${r.tax_id || '—'}</td>
        <td class="px-3 py-2">${(r.certifications || []).join(', ')}</td>
        <td class="px-3 py-2">${r.years_of_experience ?? '—'}</td>
        <td class="px-3 py-2">
          <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${badgeClass(status)}">${status}</span>
        </td>
        <td class="px-3 py-2 text-right">
          <button class="px-3 py-1.5 rounded-xl border hover:bg-zinc-50" data-quick-prequal="${r.id || r.contractorId || ''}">
            Prequalify
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    }
  
    tbody.querySelectorAll('[data-quick-prequal]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-quick-prequal');
        if (!id) return;
        try {
          await api(ENDPOINTS.prequalify(id), {
            method: 'POST',
            body: JSON.stringify({ contractorId: id })
          });
          toast(`Prequalification requested for ${id}`, 'success');
          await Promise.all([loadContractors(), loadSummary()]);
        } catch (e) { toast(e.message, 'error'); }
      });
    });
  }
  
  async function loadContractors() {
    try {
      const list = await api(ENDPOINTS.list);
      renderContractors(list || []);
    } catch (e) { toast(e.message, 'error'); }
  }
  
  async function loadSummary() {
    try {
      const summary = await api(ENDPOINTS.summary);
      renderSummary(summary);
    } catch (e) {
      toast(e.message, 'error');
    }
  }
  
    async function createContractor() {
    const form = document.getElementById('createForm');
    

    const businessName = form.businessName.value || '';
    const taxId = form.taxId.value || '';
    const mainContact = form.primaryContact.value || '';
    const yearsOfExperience = Number(form.yearsOfExperience.value) || 0;
    
    const errors = [];
    if (!businessName.trim()) errors.push('Business name is required');
    if (!taxId.trim()) errors.push('Tax ID is required');
    if (!mainContact.trim()) errors.push('Primary contact is required');
    if (yearsOfExperience < 0) errors.push('Years of experience must be 0 or greater');
    
    if (errors.length > 0) {
      toast(`Validation errors: ${errors.join(', ')}`, 'error');
      return;
    }
    
    const payload = {
      business_name: businessName || '',
      tax_id: taxId || '',
      main_contact: mainContact || '',
      certifications: (form.certifications.value || '')
        .split(',')
        .map(s => s.trim())
        .filter(Boolean),
      years_of_experience: yearsOfExperience
    };

    try {
      const c = await api(ENDPOINTS.create, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      toast('Contractor created', 'success');
      form.reset();
      const id = c && (c.id || c.contractorId);
      if (id) document.getElementById('prequalifyId').value = id;
      await Promise.all([loadContractors(), loadSummary()]);
    } catch (e) { toast(e.message, 'error'); }
  }
  
  async function prequalifyById() {
    const id = document.getElementById('prequalifyId').value;
    try {
      await api(ENDPOINTS.prequalify(id), {
        method: 'POST',
        body: JSON.stringify({ contractorId: id })
      });
      toast(`Prequalification requested for ${id}`, 'success');
      await Promise.all([loadContractors(), loadSummary()]);
    } catch (e) { toast(e.message, 'error'); }
  }
  
  window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btnCreate').addEventListener('click', createContractor);
    document.getElementById('btnPrequal').addEventListener('click', prequalifyById);
    document.getElementById('btnRefresh').addEventListener('click', loadContractors);
  
    loadContractors();
    loadSummary();
  });
  