class Dashboard {
    constructor() {
        this.trendsChart = null;
        this.typesChart = null;
        this.initializeCharts();
        this.updateStats();
        this.setupRefreshButton();
    }

    initializeCharts() {
        // Detection Trends Chart
        const trendsCtx = document.getElementById('trendsChart').getContext('2d');
        this.trendsChart = new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Detections',
                    data: [65, 59, 80, 81, 56, 55],
                    borderColor: '#4A90E2',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Monthly Detection Trends'
                    }
                }
            }
        });

        // Content Types Chart
        const typesCtx = document.getElementById('typesChart').getContext('2d');
        this.typesChart = new Chart(typesCtx, {
            type: 'doughnut',
            data: {
                labels: ['Text', 'Images', 'Combined'],
                datasets: [{
                    data: [300, 200, 100],
                    backgroundColor: ['#4A90E2', '#E24A90', '#90E24A']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    updateStats() {
        // Simulate real-time updates
        setInterval(() => {
            const stats = this.generateRandomStats();
            this.updateStatCards(stats);
            this.updateCharts(stats);
        }, 5000);
    }

    generateRandomStats() {
        return {
            totalScans: Math.floor(Math.random() * 2000) + 1000,
            threatsDetected: Math.floor(Math.random() * 200) + 100,
            accuracyRate: (Math.random() * (99.9 - 95.0) + 95.0).toFixed(1),
            responseTime: (Math.random() * (1.5 - 0.5) + 0.5).toFixed(2)
        };
    }

    updateStatCards(stats) {
        document.querySelector('.stat-card:nth-child(1) .stat-number').textContent = stats.totalScans.toLocaleString();
        document.querySelector('.stat-card:nth-child(2) .stat-number').textContent = stats.threatsDetected.toLocaleString();
        document.querySelector('.stat-card:nth-child(3) .stat-number').textContent = `${stats.accuracyRate}%`;
        document.querySelector('.stat-card:nth-child(4) .stat-number').textContent = `${stats.responseTime}s`;
    }

    updateCharts(stats) {
        // Update trends chart with new data point
        const trendsData = this.trendsChart.data.datasets[0].data;
        trendsData.push(stats.threatsDetected);
        trendsData.shift();
        this.trendsChart.update();

        // Update types chart
        const total = stats.totalScans;
        this.typesChart.data.datasets[0].data = [
            Math.floor(total * 0.5),
            Math.floor(total * 0.3),
            Math.floor(total * 0.2)
        ];
        this.typesChart.update();
    }

    setupRefreshButton() {
        const refreshBtn = document.createElement('button');
        refreshBtn.className = 'refresh-button';
        refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i>';
        refreshBtn.title = 'Refresh Dashboard';
        document.querySelector('.page-header .container').appendChild(refreshBtn);

        refreshBtn.addEventListener('click', () => {
            this.updateStatCards(this.generateRandomStats());
        });
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});