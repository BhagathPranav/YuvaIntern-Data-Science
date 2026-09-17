let allData = [];
let filteredData = [];
let charts = {};

document.addEventListener("DOMContentLoaded", () => {
  fetch('hr_data.json')
    .then(res => res.json())
    .then(data => {
      allData = data;
      filteredData = [...allData];
      populateFilterOptions();
      updateDashboard();
      setupEventListeners();
    })
    .catch(err => console.error("Error loading HR data:", err));
});

function populateFilterOptions() {
  const deptSelect = document.getElementById("filterDept");
  const roleSelect = document.getElementById("filterRole");
  const eduSelect = document.getElementById("filterEdu");

  const depts = [...new Set(allData.map(d => d.Department))].sort();
  const roles = [...new Set(allData.map(d => d.JobRole))].sort();
  const edus = [...new Set(allData.map(d => d.EducationField))].sort();

  depts.forEach(d => deptSelect.add(new Option(d, d)));
  roles.forEach(r => roleSelect.add(new Option(r, r)));
  edus.forEach(e => eduSelect.add(new Option(e, e)));
}

function filterDataset() {
  const dept = document.getElementById("filterDept").value;
  const role = document.getElementById("filterRole").value;
  const edu = document.getElementById("filterEdu").value;
  const gender = document.getElementById("filterGender").value;
  const ot = document.getElementById("filterOT").value;

  filteredData = allData.filter(item => {
    return (dept === "all" || item.Department === dept) &&
           (role === "all" || item.JobRole === role) &&
           (edu === "all" || item.EducationField === edu) &&
           (gender === "all" || item.Gender === gender) &&
           (ot === "all" || item.OverTime === ot);
  });

  updateDashboard();
}

function resetFilters() {
  document.getElementById("filterDept").value = "all";
  document.getElementById("filterRole").value = "all";
  document.getElementById("filterEdu").value = "all";
  document.getElementById("filterGender").value = "all";
  document.getElementById("filterOT").value = "all";
  filteredData = [...allData];
  updateDashboard();
}

function updateDashboard() {
  renderKPIs();
  renderCharts();
  renderTable();
}

function renderKPIs() {
  const total = filteredData.length;
  const attritionCount = filteredData.reduce((acc, curr) => acc + curr.Attrition_Numeric, 0);
  const attritionRate = total > 0 ? ((attritionCount / total) * 100).toFixed(1) : 0;
  
  const avgIncome = total > 0 ? (filteredData.reduce((acc, curr) => acc + curr.MonthlyIncome, 0) / total).toFixed(0) : 0;
  const avgAge = total > 0 ? (filteredData.reduce((acc, curr) => acc + curr.Age, 0) / total).toFixed(1) : 0;
  const avgTenure = total > 0 ? (filteredData.reduce((acc, curr) => acc + curr.YearsAtCompany, 0) / total).toFixed(1) : 0;

  const otEmployees = filteredData.filter(d => d.OverTime === 'Yes');
  const otAttrition = otEmployees.length > 0 ? ((otEmployees.filter(d => d.Attrition_Numeric === 1).length / otEmployees.length) * 100).toFixed(1) : 0;

  document.getElementById("kpiTotal").textContent = total.toLocaleString();
  document.getElementById("kpiAttritionRate").textContent = `${attritionRate}%`;
  document.getElementById("kpiAttritionSub").textContent = `${attritionCount} Employees Departed`;
  document.getElementById("kpiAvgSalary").textContent = `$${parseInt(avgIncome).toLocaleString()}`;
  document.getElementById("kpiAvgAge").textContent = `${avgAge} Yrs`;
  document.getElementById("kpiAvgTenure").textContent = `${avgTenure} Yrs`;
  document.getElementById("kpiOTRisk").textContent = `${otAttrition}%`;
}

function renderCharts() {
  renderChartDeptRole();
  renderChartEduPie();
  renderChartOvertime();
  renderChartMaritalPie();
  renderChartTravelPie();
  renderChartIncome();
  renderChartAgeBar();
  renderChartTenureBar();
  renderChartSatisfaction();
}

// Chart 1: Department & Job Role Bar Chart
function renderChartDeptRole() {
  const ctx = document.getElementById("chartDeptRole").getContext("2d");
  
  const rolesMap = {};
  filteredData.forEach(d => {
    if (!rolesMap[d.JobRole]) rolesMap[d.JobRole] = { Yes: 0, No: 0 };
    if (d.Attrition === 'Yes') rolesMap[d.JobRole].Yes++;
    else rolesMap[d.JobRole].No++;
  });

  const labels = Object.keys(rolesMap);
  const dataYes = labels.map(l => rolesMap[l].Yes);
  const dataNo = labels.map(l => rolesMap[l].No);

  if (charts.deptRole) charts.deptRole.destroy();

  charts.deptRole = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { label: 'Attrition (Left)', data: dataYes, backgroundColor: '#f43f5e', borderRadius: 4 },
        { label: 'Retained', data: dataNo, backgroundColor: '#38bdf8', borderRadius: 4 }
      ]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
        y: { stacked: true, grid: { display: false }, ticks: { color: '#cbd5e1' } }
      },
      plugins: {
        legend: { labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 2: Education Field Pie Chart
function renderChartEduPie() {
  const ctx = document.getElementById("chartEduPie").getContext("2d");

  const eduMap = {};
  filteredData.forEach(d => {
    if (!eduMap[d.EducationField]) eduMap[d.EducationField] = 0;
    if (d.Attrition_Numeric === 1) eduMap[d.EducationField]++;
  });

  const labels = Object.keys(eduMap);
  const values = labels.map(l => eduMap[l]);
  const palette = ['#38bdf8', '#818cf8', '#f43f5e', '#34d399', '#fbbf24', '#a855f7'];

  if (charts.eduPie) charts.eduPie.destroy();

  charts.eduPie = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: palette.slice(0, labels.length),
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#f8fafc', font: { size: 11 } } }
      }
    }
  });
}

// Chart 3: Overtime Work Donut Chart
function renderChartOvertime() {
  const ctx = document.getElementById("chartOvertime").getContext("2d");

  const otYesAttr = filteredData.filter(d => d.OverTime === 'Yes' && d.Attrition_Numeric === 1).length;
  const otNoAttr = filteredData.filter(d => d.OverTime === 'No' && d.Attrition_Numeric === 1).length;

  if (charts.overtime) charts.overtime.destroy();

  charts.overtime = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['OverTime Required (High Risk)', 'No Overtime'],
      datasets: [{
        data: [otYesAttr, otNoAttr],
        backgroundColor: ['#f43f5e', '#38bdf8'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 4: Marital Status Pie Chart
function renderChartMaritalPie() {
  const ctx = document.getElementById("chartMaritalPie").getContext("2d");

  const maritalMap = {};
  filteredData.forEach(d => {
    if (!maritalMap[d.MaritalStatus]) maritalMap[d.MaritalStatus] = 0;
    if (d.Attrition_Numeric === 1) maritalMap[d.MaritalStatus]++;
  });

  const labels = Object.keys(maritalMap);
  const values = labels.map(l => maritalMap[l]);
  const palette = ['#f43f5e', '#fbbf24', '#38bdf8'];

  if (charts.maritalPie) charts.maritalPie.destroy();

  charts.maritalPie = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: palette.slice(0, labels.length),
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 5: Business Travel Risk Pie Chart
function renderChartTravelPie() {
  const ctx = document.getElementById("chartTravelPie").getContext("2d");

  const travelMap = {};
  filteredData.forEach(d => {
    if (!travelMap[d.BusinessTravel]) travelMap[d.BusinessTravel] = 0;
    if (d.Attrition_Numeric === 1) travelMap[d.BusinessTravel]++;
  });

  const labels = Object.keys(travelMap);
  const values = labels.map(l => travelMap[l]);
  const palette = ['#818cf8', '#38bdf8', '#f43f5e'];

  if (charts.travelPie) charts.travelPie.destroy();

  charts.travelPie = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: palette.slice(0, labels.length),
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 6: Income Slabs Bar Chart
function renderChartIncome() {
  const ctx = document.getElementById("chartIncome").getContext("2d");
  
  const slabMap = {};
  filteredData.forEach(d => {
    const slab = d.SalarySlab || 'Other';
    if (!slabMap[slab]) slabMap[slab] = { total: 0, attrition: 0 };
    slabMap[slab].total++;
    if (d.Attrition_Numeric === 1) slabMap[slab].attrition++;
  });

  const labels = Object.keys(slabMap);
  const rates = labels.map(l => ((slabMap[l].attrition / slabMap[l].total) * 100).toFixed(1));

  if (charts.income) charts.income.destroy();

  charts.income = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Attrition Rate (%)',
        data: rates,
        backgroundColor: 'rgba(129, 140, 248, 0.75)',
        borderColor: '#818cf8',
        borderWidth: 1,
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
      plugins: {
        legend: { labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 7: Age Group Distribution Bar Chart
function renderChartAgeBar() {
  const ctx = document.getElementById("chartAgeBar").getContext("2d");

  const ageMap = {};
  filteredData.forEach(d => {
    const grp = d.Age_Group || 'Unknown';
    if (!ageMap[grp]) ageMap[grp] = { total: 0, attrition: 0 };
    ageMap[grp].total++;
    if (d.Attrition_Numeric === 1) ageMap[grp].attrition++;
  });

  const labels = Object.keys(ageMap).sort();
  const rates = labels.map(l => ((ageMap[l].attrition / ageMap[l].total) * 100).toFixed(1));

  if (charts.ageBar) charts.ageBar.destroy();

  charts.ageBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Attrition Rate (%)',
        data: rates,
        backgroundColor: '#38bdf8',
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
      plugins: {
        legend: { labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 8: Company Tenure Group Bar Chart
function renderChartTenureBar() {
  const ctx = document.getElementById("chartTenureBar").getContext("2d");

  const tenureMap = {};
  filteredData.forEach(d => {
    const grp = d.Tenure_Group || 'Unknown';
    if (!tenureMap[grp]) tenureMap[grp] = { total: 0, attrition: 0 };
    tenureMap[grp].total++;
    if (d.Attrition_Numeric === 1) tenureMap[grp].attrition++;
  });

  const labels = Object.keys(tenureMap);
  const rates = labels.map(l => ((tenureMap[l].attrition / tenureMap[l].total) * 100).toFixed(1));

  if (charts.tenureBar) charts.tenureBar.destroy();

  charts.tenureBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Attrition Rate (%)',
        data: rates,
        backgroundColor: '#fbbf24',
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
      plugins: {
        legend: { labels: { color: '#f8fafc' } }
      }
    }
  });
}

// Chart 9: Satisfaction Radar Chart
function renderChartSatisfaction() {
  const ctx = document.getElementById("chartSatisfaction").getContext("2d");

  const envMap = [1, 2, 3, 4].map(score => {
    const subset = filteredData.filter(d => d.EnvironmentSatisfaction === score);
    const rate = subset.length > 0 ? (subset.filter(d => d.Attrition_Numeric === 1).length / subset.length * 100).toFixed(1) : 0;
    return rate;
  });

  const wlbMap = [1, 2, 3, 4].map(score => {
    const subset = filteredData.filter(d => d.WorkLifeBalance === score);
    const rate = subset.length > 0 ? (subset.filter(d => d.Attrition_Numeric === 1).length / subset.length * 100).toFixed(1) : 0;
    return rate;
  });

  if (charts.satisfaction) charts.satisfaction.destroy();

  charts.satisfaction = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['1-Low', '2-Medium', '3-High', '4-Very High'],
      datasets: [
        { label: 'Env Satisfaction Attrition %', data: envMap, borderColor: '#f43f5e', backgroundColor: 'rgba(244, 63, 94, 0.2)' },
        { label: 'Work-Life Balance Attrition %', data: wlbMap, borderColor: '#34d399', backgroundColor: 'rgba(52, 211, 153, 0.2)' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          grid: { color: 'rgba(255,255,255,0.1)' },
          pointLabels: { color: '#cbd5e1' },
          ticks: { color: '#94a3b8', backdropColor: 'transparent' }
        }
      },
      plugins: {
        legend: { labels: { color: '#f8fafc' } }
      }
    }
  });
}

function renderTable() {
  const tbody = document.getElementById("employeeTableBody");
  const search = document.getElementById("searchTable").value.toLowerCase();

  const searchFiltered = filteredData.filter(d => {
    return d.JobRole.toLowerCase().includes(search) ||
           d.Department.toLowerCase().includes(search) ||
           (d.EducationField && d.EducationField.toLowerCase().includes(search)) ||
           d.Gender.toLowerCase().includes(search);
  });

  const displayData = searchFiltered.slice(0, 10);
  tbody.innerHTML = displayData.map(d => `
    <tr>
      <td>${d.JobRole}</td>
      <td>${d.Department}</td>
      <td>${d.EducationField || 'N/A'}</td>
      <td>${d.Age}</td>
      <td>${d.Gender}</td>
      <td>$${d.MonthlyIncome.toLocaleString()}</td>
      <td>${d.YearsAtCompany} Yrs</td>
      <td>${d.OverTime}</td>
      <td>
        <span class="badge ${d.Attrition === 'Yes' ? 'badge-attrition-yes' : 'badge-attrition-no'}">
          ${d.Attrition}
        </span>
      </td>
    </tr>
  `).join("");

  document.getElementById("tableCount").textContent = `Showing 1-10 of ${searchFiltered.length} records`;
}

function setupEventListeners() {
  document.getElementById("filterDept").addEventListener("change", filterDataset);
  document.getElementById("filterRole").addEventListener("change", filterDataset);
  document.getElementById("filterEdu").addEventListener("change", filterDataset);
  document.getElementById("filterGender").addEventListener("change", filterDataset);
  document.getElementById("filterOT").addEventListener("change", filterDataset);
  document.getElementById("btnReset").addEventListener("click", resetFilters);
  document.getElementById("searchTable").addEventListener("input", renderTable);
}
