/**
 * Interactive Academic Visualizations using Chart.js
 * Automatically synchronizes with Dark/Light theme switching
 */

const chartInstances = {};

function getChartColors() {
  const isDark = document.documentElement.classList.contains('dark');
  return {
    isDark,
    textColor: isDark ? '#94a3b8' : '#475569',
    gridColor: isDark ? '#334155' : '#e2e8f0',
    tooltipBg: isDark ? '#1e293b' : '#ffffff',
    tooltipText: isDark ? '#f8fafc' : '#0f172a',
    primary: '#2563eb',
    primaryAlpha: 'rgba(37, 99, 235, 0.7)',
    secondary: '#059669',
    secondaryAlpha: 'rgba(5, 150, 105, 0.7)',
    accent: '#d97706',
    danger: '#dc2626',
    purple: '#7c3aed'
  };
}

// Update all initialized charts when theme toggles
window.addEventListener('themeChanged', () => {
  const c = getChartColors();
  Object.values(chartInstances).forEach(chart => {
    if (chart && chart.options && chart.options.scales) {
      if (chart.options.scales.x) {
        if (chart.options.scales.x.ticks) chart.options.scales.x.ticks.color = c.textColor;
        if (chart.options.scales.x.grid) chart.options.scales.x.grid.color = c.gridColor;
      }
      if (chart.options.scales.y) {
        if (chart.options.scales.y.ticks) chart.options.scales.y.ticks.color = c.textColor;
        if (chart.options.scales.y.grid) chart.options.scales.y.grid.color = c.gridColor;
      }
      if (chart.options.plugins && chart.options.plugins.legend) {
        chart.options.plugins.legend.labels.color = c.textColor;
      }
      chart.update();
    }
  });
});

/**
 * 1. TABULAR ANALYSIS CHARTS
 */
function initTabularCharts() {
  const c = getChartColors();

  // Feature Importance Horizontal Bar Chart
  const featCtx = document.getElementById('chart-tabular-feature-importance');
  if (featCtx) {
    chartInstances.tabularFeature = new Chart(featCtx, {
      type: 'bar',
      data: {
        labels: [
          'Monthly_Income',
          'Debt_to_Income_Ratio',
          'Credit_History_Length',
          'Num_Open_Accounts',
          'Payment_Delinquency_Score',
          'Employment_Duration',
          'Recent_Inquiries_Count',
          'Revolving_Utilization'
        ],
        datasets: [{
          label: 'SHAP / Feature Importance Weight',
          data: [0.284, 0.231, 0.165, 0.112, 0.089, 0.054, 0.041, 0.024],
          backgroundColor: c.primaryAlpha,
          borderColor: c.primary,
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: c.tooltipBg,
            titleColor: c.tooltipText,
            bodyColor: c.tooltipText,
            borderColor: c.gridColor,
            borderWidth: 1
          }
        },
        scales: {
          x: {
            ticks: { color: c.textColor },
            grid: { color: c.gridColor }
          },
          y: {
            ticks: { color: c.textColor },
            grid: { display: false }
          }
        }
      }
    });
  }

  // ROC-AUC Curves Comparison
  const rocCtx = document.getElementById('chart-tabular-roc');
  if (rocCtx) {
    chartInstances.tabularRoc = new Chart(rocCtx, {
      type: 'line',
      data: {
        labels: ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'],
        datasets: [
          {
            label: 'LightGBM Tuned (AUC = 0.942)',
            data: [0.0, 0.45, 0.68, 0.81, 0.88, 0.92, 0.95, 0.97, 0.98, 0.99, 1.0],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: true,
            tension: 0.3,
            borderWidth: 2
          },
          {
            label: 'Random Forest (AUC = 0.885)',
            data: [0.0, 0.35, 0.55, 0.70, 0.79, 0.84, 0.89, 0.93, 0.96, 0.98, 1.0],
            borderColor: '#059669',
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false,
            tension: 0.3
          },
          {
            label: 'Baseline Logistic (AUC = 0.764)',
            data: [0.0, 0.20, 0.38, 0.52, 0.65, 0.74, 0.80, 0.86, 0.91, 0.96, 1.0],
            borderColor: '#dc2626',
            borderWidth: 1.5,
            borderDash: [3, 3],
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
            position: 'bottom',
            labels: { color: c.textColor, boxWidth: 12, padding: 15 }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'False Positive Rate (FPR)', color: c.textColor },
            ticks: { color: c.textColor },
            grid: { color: c.gridColor }
          },
          y: {
            title: { display: true, text: 'True Positive Rate (TPR)', color: c.textColor },
            ticks: { color: c.textColor },
            grid: { color: c.gridColor }
          }
        }
      }
    });
  }
}

/**
 * 2. TEXT / NLP ANALYSIS CHARTS
 */
function initTextCharts() {
  const c = getChartColors();

  // Model Performance Comparison across F1, Precision, Recall
  const f1Ctx = document.getElementById('chart-text-models');
  if (f1Ctx) {
    chartInstances.textModels = new Chart(f1Ctx, {
      type: 'bar',
      data: {
        labels: ['TF-IDF + Naive Bayes', 'Bi-LSTM + Word2Vec', 'DistilBERT Base', 'Fine-tuned PhoBERT'],
        datasets: [
          {
            label: 'Accuracy (%)',
            data: [76.5, 83.2, 91.4, 95.8],
            backgroundColor: 'rgba(37, 99, 235, 0.8)',
            borderRadius: 4
          },
          {
            label: 'Macro F1-Score (%)',
            data: [74.8, 82.7, 90.9, 95.6],
            backgroundColor: 'rgba(5, 150, 105, 0.8)',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: c.textColor } }
        },
        scales: {
          x: { ticks: { color: c.textColor }, grid: { display: false } },
          y: { min: 50, max: 100, ticks: { color: c.textColor }, grid: { color: c.gridColor } }
        }
      }
    });
  }

  // Token Length Distribution
  const lenCtx = document.getElementById('chart-text-lengths');
  if (lenCtx) {
    chartInstances.textLengths = new Chart(lenCtx, {
      type: 'line',
      data: {
        labels: ['0-20', '21-40', '41-60', '61-80', '81-100', '101-140', '141-200', '200+'],
        datasets: [{
          label: 'Mật độ độ dài mẫu (Tokens)',
          data: [450, 1420, 2100, 1750, 890, 420, 180, 45],
          borderColor: '#7c3aed',
          backgroundColor: 'rgba(124, 58, 237, 0.15)',
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { title: { display: true, text: 'Số lượng tokens', color: c.textColor }, ticks: { color: c.textColor }, grid: { color: c.gridColor } },
          y: { title: { display: true, text: 'Số văn bản', color: c.textColor }, ticks: { color: c.textColor }, grid: { color: c.gridColor } }
        }
      }
    });
  }
}

/**
 * 3. IMAGE / COMPUTER VISION CHARTS
 */
function initImageCharts() {
  const c = getChartColors();

  // Training & Validation Loss Curve
  const lossCtx = document.getElementById('chart-image-loss');
  if (lossCtx) {
    chartInstances.imageLoss = new Chart(lossCtx, {
      type: 'line',
      data: {
        labels: Array.from({ length: 15 }, (_, i) => `Epoch ${i + 1}`),
        datasets: [
          {
            label: 'Train Loss',
            data: [1.85, 1.42, 1.10, 0.84, 0.65, 0.52, 0.41, 0.33, 0.28, 0.23, 0.20, 0.18, 0.16, 0.15, 0.14],
            borderColor: '#2563eb',
            borderWidth: 2,
            tension: 0.25
          },
          {
            label: 'Validation Loss',
            data: [1.90, 1.48, 1.18, 0.91, 0.72, 0.59, 0.49, 0.43, 0.38, 0.35, 0.34, 0.33, 0.32, 0.32, 0.31],
            borderColor: '#059669',
            borderWidth: 2,
            tension: 0.25
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: c.textColor } }
        },
        scales: {
          x: { ticks: { color: c.textColor }, grid: { color: c.gridColor } },
          y: { title: { display: true, text: 'Cross-Entropy Loss', color: c.textColor }, ticks: { color: c.textColor }, grid: { color: c.gridColor } }
        }
      }
    });
  }

  // Model Latency vs Top-1 Accuracy
  const perfCtx = document.getElementById('chart-image-models');
  if (perfCtx) {
    chartInstances.imagePerf = new Chart(perfCtx, {
      type: 'bar',
      data: {
        labels: ['Custom CNN (Baseline)', 'ResNet-50', 'EfficientNet-B2', 'Vision Transformer (ViT-B/16)'],
        datasets: [
          {
            label: 'Top-1 Accuracy (%)',
            data: [73.4, 88.6, 92.1, 94.7],
            backgroundColor: 'rgba(37, 99, 235, 0.8)',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { ticks: { color: c.textColor }, grid: { display: false } },
          y: { min: 60, max: 100, ticks: { color: c.textColor }, grid: { color: c.gridColor } }
        }
      }
    });
  }
}
