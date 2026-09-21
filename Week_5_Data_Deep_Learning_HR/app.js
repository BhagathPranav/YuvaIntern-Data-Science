document.addEventListener('DOMContentLoaded', () => {
  // Load deep learning summary data
  fetch('deep_learning_summary.json')
    .then(response => response.json())
    .then(data => {
      initKPIs(data);
      initLossChart(data);
    })
    .catch(err => {
      console.warn('Could not load deep_learning_summary.json, using fallback metrics', err);
      initLossChart(null);
    });

  initSimulator();
});

function initKPIs(data) {
  if (!data) return;
  const metrics = data.test_metrics;
  const traj = data.training_trajectory;

  document.getElementById('kpi-auc').textContent = metrics.roc_auc.toFixed(4);
  document.getElementById('kpi-recall').textContent = (metrics.recall * 100).toFixed(2) + '%';
  document.getElementById('kpi-precision').textContent = (metrics.precision * 100).toFixed(2) + '%';
  document.getElementById('kpi-epoch').textContent = `Epoch ${traj.best_epoch}`;
}

function initLossChart(data) {
  const ctx = document.getElementById('lossChart').getContext('2d');
  
  let epochs = Array.from({length: 23}, (_, i) => i + 1);
  let trainLoss = [1.157, 1.115, 1.067, 0.959, 0.878, 0.805, 0.761, 0.673, 0.676, 0.653, 0.666, 0.569, 0.572, 0.574, 0.524, 0.495, 0.488, 0.460, 0.414, 0.420, 0.410, 0.396, 0.415];
  let valLoss = [1.124, 1.060, 0.982, 0.878, 0.808, 0.757, 0.743, 0.737, 0.765, 0.756, 0.752, 0.794, 0.805, 0.809, 0.821, 0.847, 0.887, 0.882, 0.960, 0.951, 1.031, 1.038, 0.998];
  
  if (data && data.training_trajectory) {
    epochs = data.training_trajectory.history.epoch;
    trainLoss = data.training_trajectory.history.train_loss;
    valLoss = data.training_trajectory.history.val_loss;
  }

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: epochs,
      datasets: [
        {
          label: 'Training Loss (BCE)',
          data: trainLoss,
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          fill: true,
          tension: 0.3
        },
        {
          label: 'Validation Loss (BCE)',
          data: valLoss,
          borderColor: '#ec4899',
          borderDash: [5, 5],
          backgroundColor: 'transparent',
          fill: false,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: '#94a3b8', font: { family: 'Inter' } }
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          title: { display: true, text: 'Training Epoch', color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#94a3b8' }
        },
        y: {
          title: { display: true, text: 'Binary Cross-Entropy Loss', color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#94a3b8' }
        }
      }
    }
  });
}

function initSimulator() {
  const overTime = document.getElementById('sim-overtime');
  const income = document.getElementById('sim-income');
  const distance = document.getElementById('sim-distance');
  const satisfaction = document.getElementById('sim-satisfaction');
  const years = document.getElementById('sim-years');

  const valIncome = document.getElementById('val-income');
  const valDistance = document.getElementById('val-distance');
  const valSatisfaction = document.getElementById('val-satisfaction');
  const valYears = document.getElementById('val-years');

  const riskScoreEl = document.getElementById('risk-score');
  const riskLabelEl = document.getElementById('risk-label');
  const riskFillEl = document.getElementById('risk-fill');
  const recEl = document.getElementById('sim-recommendation');

  function calculateRisk() {
    valIncome.textContent = parseInt(income.value).toLocaleString();
    valDistance.textContent = distance.value;
    valSatisfaction.textContent = satisfaction.value;
    valYears.textContent = years.value;

    // Simulated ANN Forward Pass Logit Calculation
    // Base logit
    let z = -0.5;

    // Overtime impact (+1.4 logit if OverTime = Yes)
    z += (parseInt(overTime.value) === 1) ? 1.4 : -0.4;

    // Income impact (-0.00015 per dollar above 3000)
    z -= (parseInt(income.value) - 3000) * 0.00015;

    // Distance impact (+0.04 per mile)
    z += (parseInt(distance.value) - 5) * 0.04;

    // Environment satisfaction (-0.4 per point above 1)
    z -= (parseInt(satisfaction.value) - 1) * 0.45;

    // Years at company (-0.08 per year)
    z -= (parseInt(years.value)) * 0.08;

    // Sigmoid activation
    const prob = 1 / (1 + Math.exp(-z));
    const riskPercent = Math.min(Math.max(Math.round(prob * 100), 2), 98);

    riskScoreEl.textContent = `${riskPercent}%`;
    riskFillEl.style.width = `${riskPercent}%`;

    if (riskPercent < 35) {
      riskScoreEl.style.color = '#34d399';
      riskLabelEl.textContent = 'Low Flight Risk';
      recEl.textContent = 'Standard engagement. Employee shows stable compensation and satisfaction indicators.';
    } else if (riskPercent < 65) {
      riskScoreEl.style.color = '#fbbf24';
      riskLabelEl.textContent = 'Moderate Flight Risk';
      recEl.textContent = 'Proactive monitoring advised. Review work-life balance, overtime load, and growth opportunities.';
    } else {
      riskScoreEl.style.color = '#f43f5e';
      riskLabelEl.textContent = 'High Flight Risk (Retention Alert)';
      recEl.textContent = 'Immediate HR intervention recommended! High overtime combined with commute or compensation gaps indicates critical flight risk.';
    }
  }

  [overTime, income, distance, satisfaction, years].forEach(el => {
    el.addEventListener('input', calculateRisk);
    el.addEventListener('change', calculateRisk);
  });

  calculateRisk();
}
