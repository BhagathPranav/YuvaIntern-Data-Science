let edaData = {};
let charts = {};

document.addEventListener("DOMContentLoaded", () => {
  fetch('eda_summary.json')
    .then(res => res.json())
    .then(data => {
      edaData = data;
      populateRoleFilter();
      updateDashboard();
      setupEventListeners();
    })
    .catch(err => console.error("Error loading EDA summary:", err));
});

function populateRoleFilter() {
  const roleSelect = document.getElementById("filterRole");
  if (edaData.sample_records) {
    const roles = [...new Set(edaData.sample_records.map(r => r.JobRole))].sort();
    roles.forEach(r => roleSelect.add(new Option(r, r)));
  }
}

function filterData() {
  updateDashboard();
}

function resetFilters() {
  document.getElementById("filterDept").value = "all";
  document.getElementById("filterRole").value = "all";
  document.getElementById("filterOT").value = "all";
  updateDashboard();
}

function updateDashboard() {
  renderKPIs();
  renderScatter();
  renderDonut();
  renderHeatmap();
  renderIncomeBox();
  renderDeptBar();
}

function getFilteredRecords() {
  const dept = document.getElementById("filterDept").value;
  const role = document.getElementById("filterRole").value;
  const ot = document.getElementById("filterOT").value;

  if (!edaData.sample_records) return [];

  return edaData.sample_records.filter(r => {
    return (dept === "all" || r.Department === dept) &&
           (role === "all" || r.JobRole === role) &&
           (ot === "all" || r.OverTime === ot);
  });
}

function renderKPIs() {
  if (!edaData.metrics) return;
  const m = edaData.metrics;

  document.getElementById("kpiClassImbalance").textContent = `${m.attrition_rate}%`;
  document.getElementById("kpiLoyaltyGap").textContent = `+${m.loyalty_penalty_gap}`;
  document.getElementById("kpiSalaryGap").textContent = `$${m.income_gap.toLocaleString()}`;
}

// Chart 1: Loyalty Penalty Scatter Plot
function renderScatter() {
  const ctx = document.getElementById("chartLoyaltyScatter").getContext("2d");
  const records = getFilteredRecords();

  const dataPoints = records.map(r => ({
    x: r.TotalWorkingYears,
    y: r.MonthlyIncome,
    r: Math.max(4, r.YearsAtCompany * 0.8),
    attrition: r.Attrition
  }));

  const dataYes = dataPoints.filter(d => d.attrition === 'Yes');
  const dataNo = dataPoints.filter(d => d.attrition === 'No');

  if (charts.scatter) charts.scatter.destroy();

  charts.scatter = new Chart(ctx, {
    type: 'bubble',
    data: {
      datasets: [
        { label: 'Attrition (Left)', data: dataYes, backgroundColor: 'rgba(244, 63, 94, 0.7)', borderColor: '#f43f5e' },
        { label: 'Retained', data: dataNo, backgroundColor: 'rgba(56, 189, 248, 0.5)', borderColor: '#38bdf8' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { title: { display: true, text: 'Total Working Years (Industry Experience)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#cbd5e1' } },
        y: { title: { display: true, text: 'Monthly Income ($)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#cbd5e1' } }
      },
      plugins: {
        legend: { labels: { color: '#f8fafc' } },
        tooltip: {
          callbacks: {
            label: ctx => `Total Yrs: ${ctx.raw.x}, Salary: $${ctx.raw.y.toLocaleString()}, Co. Tenure: ${Math.round(ctx.raw.r/0.8)} Yrs`
          }
        }
      }
    }
  });
}

// Chart 2: Class Imbalance Donut
function renderDonut() {
  const ctx = document.getElementById("chartClassImbalance").getContext("2d");
  const m = edaData.metrics || { attrition_count: 237, retained_count: 1236 };

  if (charts.donut) charts.donut.destroy();

  charts.donut = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Attrition (Departed)', 'Retained Workforce'],
      datasets: [{
        data: [m.attrition_count, m.retained_count],
        backgroundColor: ['#f43f5e', '#38bdf8'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { color: '#f8fafc' } } }
    }
  });
}

// Heatmap Grid
function renderHeatmap() {
  const container = document.getElementById("heatmapGrid");
  container.innerHTML = "";

  const featureCols = ['MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'Age', 'Attrition_Numeric'];
  const labels = ['Income', 'Total Yrs', 'Co. Yrs', 'Role Yrs', 'Promo Yrs', 'Age', 'Attrition'];

  if (!edaData.correlations) return;
  const corrs = edaData.correlations;

  // Header row
  container.appendChild(createHeatmapCell("", "rgba(255,255,255,0.05)"));
  labels.forEach(l => container.appendChild(createHeatmapCell(l, "rgba(255,255,255,0.05)")));

  featureCols.forEach((rowKey, i) => {
    container.appendChild(createHeatmapCell(labels[i], "rgba(255,255,255,0.05)"));
    featureCols.forEach(colKey => {
      const val = corrs[rowKey] ? corrs[rowKey][colKey] : 0;
      const bg = getCorrColor(val);
      const text = val !== undefined ? val.toFixed(2) : "0.00";
      container.appendChild(createHeatmapCell(text, bg));
    });
  });
}

function createHeatmapCell(text, bg) {
  const div = document.createElement("div");
  div.className = "heatmap-cell";
  div.style.backgroundColor = bg;
  div.textContent = text;
  return div;
}

function getCorrColor(val) {
  if (val === 1) return "rgba(56, 189, 248, 0.6)";
  if (val > 0.5) return "rgba(56, 189, 248, 0.4)";
  if (val > 0.2) return "rgba(129, 140, 248, 0.3)";
  if (val < -0.1) return "rgba(244, 63, 94, 0.5)";
  return "rgba(255, 255, 255, 0.04)";
}

// Chart 4: Bivariate Income Box
function renderIncomeBox() {
  const ctx = document.getElementById("chartIncomeBox").getContext("2d");

  if (charts.incomeBox) charts.incomeBox.destroy();

  charts.incomeBox = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Retained (Median)', 'Departed (Median)'],
      datasets: [{
        label: 'Median Monthly Income ($)',
        data: [6700, 4570],
        backgroundColor: ['#34d399', '#f43f5e'],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { display: false }, ticks: { color: '#cbd5e1' } },
        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', callback: v => '$' + v.toLocaleString() } }
      },
      plugins: { legend: { labels: { color: '#f8fafc' } } }
    }
  });
}

// Chart 5: Dept Bar Chart
function renderDeptBar() {
  const ctx = document.getElementById("chartDeptBar").getContext("2d");
  const stats = edaData.department_stats || [];

  const labels = stats.map(s => s.department);
  const rates = stats.map(s => s.rate);

  if (charts.deptBar) charts.deptBar.destroy();

  charts.deptBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Attrition Rate (%)',
        data: rates,
        backgroundColor: ['#fbbf24', '#38bdf8', '#f43f5e'],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { display: false }, ticks: { color: '#cbd5e1' } },
        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', callback: v => v + '%' } }
      },
      plugins: { legend: { labels: { color: '#f8fafc' } } }
    }
  });
}

function setupEventListeners() {
  document.getElementById("filterDept").addEventListener("change", filterData);
  document.getElementById("filterRole").addEventListener("change", filterData);
  document.getElementById("filterOT").addEventListener("change", filterData);
  document.getElementById("btnReset").addEventListener("click", resetFilters);
}
