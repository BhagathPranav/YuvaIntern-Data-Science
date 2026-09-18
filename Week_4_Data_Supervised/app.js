document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    setupSimulatorListeners();
});

let summaryData = null;

async function fetchData() {
    try {
        const response = await fetch('supervised_summary.json');
        summaryData = await response.json();
        
        updateKPIs(summaryData);
        updateConfusionMatrices(summaryData);
        renderROCChart(summaryData.roc_curves, summaryData.logistic_regression.test_roc_auc, summaryData.random_forest.test_roc_auc);
        renderDriversChart(summaryData.logistic_regression.top_drivers);
        renderEmployeeTable(summaryData.sample_employees);
        
        // Initial simulation calculate
        calculateSimulatedRisk();
    } catch (error) {
        console.error('Error loading supervised summary JSON:', error);
    }
}

function updateKPIs(data) {
    const lrMetrics = data.logistic_regression.metrics;
    const lr = data.logistic_regression;
    const rf = data.random_forest;
    const riskCounts = data.risk_category_counts;

    document.getElementById('kpi-recall').textContent = `${(lrMetrics.recall * 100).toFixed(2)}%`;
    document.getElementById('kpi-lr-auc').textContent = lr.test_roc_auc.toFixed(4);
    document.getElementById('kpi-rf-auc').textContent = rf.test_roc_auc.toFixed(4);
    document.getElementById('kpi-high-risk').textContent = riskCounts['High Risk'] || 416;
}

function updateConfusionMatrices(data) {
    const lrCM = data.logistic_regression.confusion_matrix;
    const rfCM = data.random_forest.confusion_matrix;

    document.getElementById('cm-lr-tn').textContent = lrCM.true_negatives;
    document.getElementById('cm-lr-fp').textContent = lrCM.false_positives;
    document.getElementById('cm-lr-fn').textContent = lrCM.false_negatives;
    document.getElementById('cm-lr-tp').textContent = lrCM.true_positives;

    document.getElementById('cm-rf-tn').textContent = rfCM.true_negatives;
    document.getElementById('cm-rf-fp').textContent = rfCM.false_positives;
    document.getElementById('cm-rf-fn').textContent = rfCM.false_negatives;
    document.getElementById('cm-rf-tp').textContent = rfCM.true_positives;
}

function renderROCChart(rocData, lrAUC, rfAUC) {
    const ctx = document.getElementById('rocChart').getContext('2d');
    
    const lrPoints = rocData.logistic_regression.map(p => ({ x: p.fpr, y: p.tpr }));
    const rfPoints = rocData.random_forest.map(p => ({ x: p.fpr, y: p.tpr }));

    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: `Logistic Regression (AUC = ${lrAUC.toFixed(4)})`,
                    data: lrPoints,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    tension: 0.2,
                    fill: false
                },
                {
                    label: `Random Forest (AUC = ${rfAUC.toFixed(4)})`,
                    data: rfPoints,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    tension: 0.2,
                    fill: false
                },
                {
                    label: 'Random Baseline (AUC = 0.5000)',
                    data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
                    borderColor: '#64748b',
                    borderDash: [5, 5],
                    borderWidth: 1.5,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    title: { display: true, text: 'False Positive Rate (1 - Specificity)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' },
                    min: 0,
                    max: 1
                },
                y: {
                    title: { display: true, text: 'True Positive Rate (Recall)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' },
                    min: 0,
                    max: 1
                }
            },
            plugins: {
                legend: { labels: { color: '#f8fafc', font: { family: 'Plus Jakarta Sans' } } }
            }
        }
    });
}

function renderDriversChart(drivers) {
    const ctx = document.getElementById('driversChart').getContext('2d');
    
    const labels = drivers.map(d => d.feature.replace('_', ' '));
    const coefs = drivers.map(d => d.coefficient);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Log-Odds Coefficient',
                data: coefs,
                backgroundColor: 'rgba(239, 68, 68, 0.75)',
                borderColor: '#ef4444',
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#f8fafc', font: { size: 11, family: 'Plus Jakarta Sans' } }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function setupSimulatorListeners() {
    const inputs = ['sim-overtime', 'sim-travel', 'sim-dept', 'sim-income', 'sim-tenure', 'sim-satisfaction'];
    inputs.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) {
            elem.addEventListener('change', calculateSimulatedRisk);
            elem.addEventListener('input', calculateSimulatedRisk);
        }
    });
}

function calculateSimulatedRisk() {
    const overtime = document.getElementById('sim-overtime').value;
    const travel = document.getElementById('sim-travel').value;
    const dept = document.getElementById('sim-dept').value;
    const income = parseFloat(document.getElementById('sim-income').value) || 3200;
    const tenure = parseFloat(document.getElementById('sim-tenure').value) || 2;
    const satisfaction = parseInt(document.getElementById('sim-satisfaction').value) || 2;

    // Logistic Regression Sigmoid formula approximation based on coefficients
    let logOdds = -1.2; // Baseline intercept
    
    if (overtime === 'Yes') logOdds += 0.787;
    if (travel === 'Travel_Frequently') logOdds += 0.650;
    if (travel === 'Travel_Rarely') logOdds += 0.443;
    if (dept === 'Sales') logOdds += 0.585;
    if (dept === 'Research & Development') logOdds += 0.379;
    
    // Income effect (lower income increases risk)
    if (income < 3500) logOdds += 0.45;
    else if (income < 6000) logOdds += 0.15;
    else logOdds -= 0.35;

    // Tenure effect
    if (tenure <= 3) logOdds += 0.40;
    
    // Job satisfaction effect
    if (satisfaction === 1) logOdds += 0.60;
    else if (satisfaction === 2) logOdds += 0.25;
    else if (satisfaction >= 3) logOdds -= 0.40;

    const prob = 1 / (1 + Math.exp(-logOdds));
    const scorePct = (prob * 100).toFixed(1);

    const scoreDisplay = document.getElementById('risk-score-display');
    const badgeDisplay = document.getElementById('risk-badge-display');
    const actionDisplay = document.getElementById('risk-action-display');

    scoreDisplay.textContent = `${scorePct}%`;

    if (prob >= 0.65) {
        scoreDisplay.style.color = '#ef4444';
        badgeDisplay.className = 'risk-badge badge-red';
        badgeDisplay.textContent = 'HIGH FLIGHT RISK';
        actionDisplay.innerHTML = '<strong>HR Action:</strong> Schedule urgent Stay Interview &amp; cap weekly overtime within 14 days.';
    } else if (prob >= 0.35) {
        scoreDisplay.style.color = '#f59e0b';
        badgeDisplay.className = 'risk-badge badge-amber';
        badgeDisplay.textContent = 'MEDIUM FLIGHT RISK';
        actionDisplay.innerHTML = '<strong>HR Action:</strong> Conduct career progression review &amp; assess compensation parity.';
    } else {
        scoreDisplay.style.color = '#10b981';
        badgeDisplay.className = 'risk-badge badge-emerald';
        badgeDisplay.textContent = 'LOW FLIGHT RISK';
        actionDisplay.innerHTML = '<strong>HR Action:</strong> Routine annual performance review; no immediate intervention needed.';
    }
}

function renderEmployeeTable(sampleData) {
    const tbody = document.getElementById('table-body');
    if (!tbody || !sampleData) return;

    tbody.innerHTML = '';
    sampleData.forEach(emp => {
        const tr = document.createElement('tr');
        
        let badgeClass = 'badge-emerald';
        if (emp.Risk_Category === 'High Risk') badgeClass = 'badge-red';
        else if (emp.Risk_Category === 'Medium Risk') badgeClass = 'badge-amber';

        tr.innerHTML = `
            <td>${emp.Age}</td>
            <td>${emp.Department}</td>
            <td>${emp.JobRole}</td>
            <td>$${emp.MonthlyIncome.toLocaleString()}</td>
            <td>${emp.OverTime}</td>
            <td>${emp.YearsAtCompany} yrs</td>
            <td style="font-weight: 700;">${(emp.FlightRiskScore_LR * 100).toFixed(1)}%</td>
            <td><span class="badge ${badgeClass}">${emp.Risk_Category}</span></td>
        `;
        tbody.appendChild(tr);
    });
}
