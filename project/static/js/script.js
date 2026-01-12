// Additional JavaScript functionality

// Export data functionality
function exportData(format = 'csv') {
    axios.get('/api/filtered-data')
        .then(response => {
            if (response.data.success) {
                const data = response.data.data;
                
                if (format === 'csv') {
                    exportToCSV(data);
                } else if (format === 'json') {
                    exportToJSON(data);
                }
            }
        })
        .catch(error => {
            console.error('Error exporting data:', error);
            alert('Failed to export data');
        });
}

function exportToCSV(data) {
    if (data.length === 0) {
        alert('No data to export');
        return;
    }
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => JSON.stringify(row[header])).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `campus_pulse_data_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function exportToJSON(data) {
    const jsonContent = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `campus_pulse_data_${new Date().toISOString().split('T')[0]}.json`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Auto-refresh functionality
let autoRefreshInterval = null;

function startAutoRefresh(interval = 30000) { // 30 seconds
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing dashboard data...');
        loadDashboardData();
    }, interval);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Initialize auto-refresh when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Start auto-refresh after 1 minute
    setTimeout(() => {
        startAutoRefresh(60000);
    }, 60000);
});

// Add export buttons to page
function addExportButtons() {
    const exportSection = document.createElement('div');
    exportSection.className = 'export-section mt-3';
    exportSection.innerHTML = `
        <button class="btn btn-outline-primary btn-sm me-2" onclick="exportData('csv')">
            <i class="fas fa-file-csv me-1"></i>Export CSV
        </button>
        <button class="btn btn-outline-secondary btn-sm" onclick="exportData('json')">
            <i class="fas fa-file-code me-1"></i>Export JSON
        </button>
    `;
    
    // Add to filter section
    const filterSection = document.querySelector('.filter-section');
    if (filterSection) {
        filterSection.appendChild(exportSection);
    }
}

// Call this after dashboard loads
setTimeout(addExportButtons, 1000);