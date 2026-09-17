document.addEventListener('DOMContentLoaded', async () => {
    let summaryData = null;

    try {
        const response = await fetch('clustering_summary.json');
        summaryData = await response.json();
        console.log('Clustering summary loaded:', summaryData);

        initElbowChart(summaryData.elbow_curve);
        initPCAScatterChart(summaryData.scatter_sample, 'Persona');
        initAttritionPersonaChart(summaryData.cluster_stats);
        populateTable(summaryData.scatter_sample);
        setupEventListeners(summaryData);

    } catch (err) {
        console.error('Error loading clustering_summary.json:', err);
    }
});

// Chart 1: Elbow Method Curve (WCSS vs k)
function initElbowChart(elbowData) {
    const ctx = document.getElementById('elbowChart').getContext('2d');

    const labels = elbowData.map(item => `k=${item.k}`);
    const values = elbowData.map(item => item.wcss);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'WCSS (Inertia)',
                data: values,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.15)',
                borderWidth: 3,
                fill: true,
                tension: 0.3,
                pointRadius: 6,
                pointBackgroundColor: elbowData.map(item => item.k === 3 ? '#ef4444' : '#6366f1'),
                pointBorderColor: '#ffffff',
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` WCSS: ${ctx.raw.toLocaleString()}`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                }
            }
        }
    });
}

// Chart 2: 2D PCA Cluster Scatter Plot
let pcaChartInstance = null;
function initPCAScatterChart(sampleData, colorBy = 'Persona') {
    const ctx = document.getElementById('pcaScatterChart').getContext('2d');

    if (pcaChartInstance) {
        pcaChartInstance.destroy();
    }

    let datasets = [];

    if (colorBy === 'Persona') {
        const personas = ['Junior Core', 'Mid-Level Professionals', 'Senior Leadership'];
        const colors = {
            'Junior Core': '#ef4444',
            'Mid-Level Professionals': '#3b82f6',
            'Senior Leadership': '#10b981'
        };

        datasets = personas.map(persona => {
            const points = sampleData.filter(d => d.Persona === persona).map(d => ({
                x: d.PCA1,
                y: d.PCA2,
                meta: d
            }));

            return {
                label: persona,
                data: points,
                backgroundColor: colors[persona],
                pointRadius: 5,
                pointHoverRadius: 7
            };
        });
    } else {
        const statuses = ['Yes', 'No'];
        const colors = { 'Yes': '#ef4444', 'No': '#10b981' };

        datasets = statuses.map(status => {
            const points = sampleData.filter(d => d.Attrition === status).map(d => ({
                x: d.PCA1,
                y: d.PCA2,
                meta: d
            }));

            return {
                label: status === 'Yes' ? 'Departed (Yes)' : 'Retained (No)',
                data: points,
                backgroundColor: colors[status],
                pointRadius: 5,
                pointHoverRadius: 7
            };
        });
    }

    pcaChartInstance = new Chart(ctx, {
        type: 'scatter',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#f3f4f6', usePointStyle: true }
                },
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const d = ctx.raw.meta;
                            return ` ${d.Persona} | ${d.JobRole} (Income: $${d.MonthlyIncome.toLocaleString()}, Exp: ${d.TotalWorkingYears} yrs)`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'PCA Component 1', color: '#9ca3af' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                },
                y: {
                    title: { display: true, text: 'PCA Component 2', color: '#9ca3af' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                }
            }
        }
    });
}

// Chart 3: Attrition Rate by Persona Bar Chart
function initAttritionPersonaChart(clusterStats) {
    const ctx = document.getElementById('attritionPersonaChart').getContext('2d');

    const labels = Object.values(clusterStats).map(c => c.persona);
    const attritionRates = Object.values(clusterStats).map(c => c.attrition_rate);
    const colors = ['#ef4444', '#3b82f6', '#10b981'];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attrition Rate (%)',
                data: attritionRates,
                backgroundColor: colors,
                borderRadius: 8,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` Attrition: ${ctx.raw}%`
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#9ca3af' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af', callback: val => `${val}%` }
                }
            }
        }
    });
}

// Populate Clustered Directory Table
function populateTable(data) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    data.slice(0, 100).forEach(row => {
        const tr = document.createElement('tr');

        const personaBadgeClass = 
            row.Persona === 'Junior Core' ? 'tag-red' :
            row.Persona === 'Mid-Level Professionals' ? 'tag-blue' : 'tag-green';

        const attritionBadgeClass = row.Attrition === 'Yes' ? 'alert-red' : 'alert-green';

        tr.innerHTML = `
            <td><span class="persona-pill ${personaBadgeClass}">${row.Persona}</span></td>
            <td>${row.Age}</td>
            <td>${row.Department}</td>
            <td>${row.JobRole}</td>
            <td><strong>$${row.MonthlyIncome.toLocaleString()}</strong></td>
            <td>${row.TotalWorkingYears} yrs</td>
            <td>${row.YearsAtCompany} yrs</td>
            <td><span class="kpi-badge ${attritionBadgeClass}">${row.Attrition}</span></td>
        `;

        tbody.appendChild(tr);
    });
}

// Setup Event Listeners for Dynamic Filtering
function setupEventListeners(summaryData) {
    const pcaHueSelect = document.getElementById('pcaHueSelect');
    const personaFilter = document.getElementById('personaFilter');
    const attritionFilter = document.getElementById('attritionFilter');
    const searchInput = document.getElementById('searchInput');

    pcaHueSelect.addEventListener('change', (e) => {
        initPCAScatterChart(summaryData.scatter_sample, e.target.value);
    });

    const filterTable = () => {
        const personaVal = personaFilter.value;
        const attritionVal = attritionFilter.value;
        const searchVal = searchInput.value.toLowerCase();

        const filtered = summaryData.scatter_sample.filter(row => {
            const matchPersona = personaVal === 'ALL' || row.Persona === personaVal;
            const matchAttrition = attritionVal === 'ALL' || row.Attrition === attritionVal;
            const matchSearch = row.JobRole.toLowerCase().includes(searchVal) || 
                                row.Department.toLowerCase().includes(searchVal);

            return matchPersona && matchAttrition && matchSearch;
        });

        populateTable(filtered);
    };

    personaFilter.addEventListener('change', filterTable);
    attritionFilter.addEventListener('change', filterTable);
    searchInput.addEventListener('input', filterTable);
}
