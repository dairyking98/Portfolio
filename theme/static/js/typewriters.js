// Typewriter Collection Display Script

let typewritersData = [];
let currentView = 'list';
let filteredData = [];

// Load JSON data
async function loadTypewriters() {
    try {
        const response = await fetch('/typewriters.json');
        if (!response.ok) {
            throw new Error('Failed to load typewriters data');
        }
        typewritersData = await response.json();
        filteredData = [...typewritersData];
        initializeViews();
    } catch (error) {
        console.error('Error loading typewriters:', error);
        document.getElementById('table-body').innerHTML = 
            '<tr><td colspan="100">Error loading data. Please ensure typewriters.json exists.</td></tr>';
    }
}

// Initialize views
function initializeViews() {
    setupViewSwitching();
    renderListView();
    renderPivotView();
    setupSearch();
    setupSorting();
}

// View switching
function setupViewSwitching() {
    const listBtn = document.getElementById('list-view-btn');
    const pivotBtn = document.getElementById('pivot-view-btn');
    const listView = document.getElementById('list-view');
    const pivotView = document.getElementById('pivot-view');
    
    listBtn.addEventListener('click', () => {
        currentView = 'list';
        listBtn.classList.add('active');
        pivotBtn.classList.remove('active');
        listView.classList.add('active');
        pivotView.classList.remove('active');
    });
    
    pivotBtn.addEventListener('click', () => {
        currentView = 'pivot';
        pivotBtn.classList.add('active');
        listBtn.classList.remove('active');
        pivotView.classList.add('active');
        listView.classList.remove('active');
        renderPivotView();
    });
}

// List View - only show specified columns
const LIST_VIEW_COLUMNS = [
    'Typewriter Brand',  // Make
    'Model',
    'Year',
    'Serial No',         // Serial
    'Typeface',
    'Pitch',
    'Layout',
    'Notes',
    'Link'               // Generated link column
];

// Generate URL slug from text
function slugify(text) {
    if (!text) return '';
    return String(text)
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')  // Remove special characters
        .replace(/[\s_-]+/g, '-')  // Replace spaces and underscores with hyphens
        .replace(/^-+|-+$/g, '');   // Remove leading/trailing hyphens
}

// Generate machine page link
// Only generates links for machines with serial numbers (pages without serials are handled by plugin)
function generateMachineLink(tw) {
    const make = tw['Typewriter Brand'];
    const model = tw['Model'];
    const serial = tw['Serial No'];
    
    // Only generate link if make, model, and serial exist (serial is required)
    if (!make || !model || !serial) {
        return null;
    }
    
    // Generate URL: /typewriters/{make}-{model}-{serial}/
    const makeSlug = slugify(make);
    const modelSlug = slugify(model);
    const serialSlug = slugify(serial);
    
    if (!makeSlug || !modelSlug || !serialSlug) {
        return null;
    }
    
    return `/typewriters/${makeSlug}-${modelSlug}-${serialSlug}/`;
}

// List View
function renderListView() {
    const table = document.getElementById('typewriters-table');
    const thead = document.getElementById('table-head');
    const tbody = document.getElementById('table-body');
    
    if (filteredData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="100">No typewriters found.</td></tr>';
        return;
    }
    
    // Use only the specified columns for display (excluding Link which is generated)
    const displayColumns = LIST_VIEW_COLUMNS.filter(col => col !== 'Link');
    
    // Create header (add Link column)
    thead.innerHTML = '<tr>' + 
        displayColumns.map(col => `<th>${formatColumnName(col)}</th>`).join('') + 
        '<th>Link</th>' +
        '</tr>';
    
    // Create rows
    tbody.innerHTML = filteredData.map(tw => {
        const link = generateMachineLink(tw);
        const linkCell = link 
            ? `<td><a href="${link}" class="machine-link">View Page</a></td>`
            : '<td><span class="empty">—</span></td>';
        
        return '<tr>' + 
            displayColumns.map(col => {
                const value = tw[col] !== undefined ? tw[col] : '';
                return `<td>${formatValue(value)}</td>`;
            }).join('') + 
            linkCell +
            '</tr>';
    }).join('');
    
    updateTableCount();
}

function formatColumnName(name) {
    // Convert column names to readable format
    const replacements = {
        'Typewriter Brand': 'Make',
        'Serial No': 'Serial',
        'Electric/Manual': 'Type',
        'New Rubber?': 'Rubber',
        'Sale Price': 'Sale',
        'Purchase Price': 'Purchase',
        'From Where & Who': 'Source'
    };
    return replacements[name] || name;
}

function formatValue(value) {
    if (value === null || value === undefined || value === '') {
        return '<span class="empty">—</span>';
    }
    if (typeof value === 'number') {
        if (value % 1 === 0) {
            // Don't add commas to years (4-digit numbers typically)
            if (value >= 1000 && value <= 2100) {
                return String(value);
            }
            return value.toLocaleString();
        }
        return value.toFixed(2);
    }
    // For string values that might be years
    const str = String(value);
    if (/^\d{4}$/.test(str)) {
        return str; // Don't add commas to 4-digit years
    }
    return str;
}

// Search functionality
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        filteredData = typewritersData.filter(tw => {
            return Object.values(tw).some(val => 
                String(val).toLowerCase().includes(query)
            );
        });
        renderListView();
    });
}

// Sorting
function setupSorting() {
    const sortSelect = document.getElementById('sort-select');
    sortSelect.addEventListener('change', (e) => {
        const sortValue = e.target.value;
        if (!sortValue) {
            // Reset to original order
            filteredData = [...typewritersData];
            renderListView();
            return;
        }
        
        const [sortBy, direction] = sortValue.split('|');
        const ascending = direction === 'asc';
        
        filteredData.sort((a, b) => {
            let aVal = a[sortBy] || '';
            let bVal = b[sortBy] || '';
            
            // Handle Year column - extract first 4 digits if it's a date string
            if (sortBy === 'Year') {
                const aYear = String(aVal).match(/\d{4}/);
                const bYear = String(bVal).match(/\d{4}/);
                if (aYear && bYear) {
                    const result = parseInt(aYear[0]) - parseInt(bYear[0]);
                    return ascending ? result : -result;
                }
            }
            
            // Try numeric comparison
            const aNum = parseFloat(aVal);
            const bNum = parseFloat(bVal);
            if (!isNaN(aNum) && !isNaN(bNum)) {
                const result = aNum - bNum;
                return ascending ? result : -result;
            }
            
            // String comparison
            const result = String(aVal).localeCompare(String(bVal));
            return ascending ? result : -result;
        });
        renderListView();
    });
}

function updateTableCount() {
    const countEl = document.getElementById('table-count');
    if (countEl) {
        countEl.textContent = filteredData.length;
    }
}

// Pivot View
function renderPivotView() {
    const groupBy = document.getElementById('pivot-group').value;
    const metric = document.getElementById('pivot-metric').value;
    const chartDiv = document.getElementById('pivot-chart');
    
    // Group data
    const groups = {};
    typewritersData.forEach(tw => {
        const groupKey = tw[groupBy] || 'Unknown';
        if (!groups[groupKey]) {
            groups[groupKey] = [];
        }
        groups[groupKey].push(tw);
    });
    
    // Calculate metrics
    const pivotData = Object.entries(groups).map(([key, items]) => {
        let value = 0;
        if (metric === 'count') {
            value = items.length;
        } else if (metric === 'value') {
            value = items.reduce((sum, item) => {
                const val = parseFloat(item.Value) || 0;
                return sum + val;
            }, 0);
        } else if (metric === 'purchase') {
            value = items.reduce((sum, item) => {
                const val = parseFloat(item['Purchase Price']) || 0;
                return sum + val;
            }, 0);
        }
        return { key, value, items };
    }).sort((a, b) => b.value - a.value);
    
    // Render chart
    const maxValue = Math.max(...pivotData.map(d => d.value));
    
    chartDiv.innerHTML = '<div class="pivot-list">' +
        pivotData.map(item => {
            const percentage = (item.value / maxValue) * 100;
            const formattedValue = metric === 'count' 
                ? item.value 
                : '$' + item.value.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0});
            
            return `
                <div class="pivot-item">
                    <div class="pivot-header">
                        <span class="pivot-label">${item.key}</span>
                        <span class="pivot-value">${formattedValue}</span>
                    </div>
                    <div class="pivot-bar-container">
                        <div class="pivot-bar" style="width: ${percentage}%"></div>
                    </div>
                    <div class="pivot-details">
                        <small>${item.items.length} machine${item.items.length !== 1 ? 's' : ''}</small>
                    </div>
                </div>
            `;
        }).join('') +
        '</div>';
}

// Update pivot view when controls change
document.addEventListener('DOMContentLoaded', () => {
    loadTypewriters();
    
    const pivotGroup = document.getElementById('pivot-group');
    const pivotMetric = document.getElementById('pivot-metric');
    
    if (pivotGroup) {
        pivotGroup.addEventListener('change', renderPivotView);
    }
    if (pivotMetric) {
        pivotMetric.addEventListener('change', renderPivotView);
    }
    
    // Update last updated time
    const lastUpdated = document.getElementById('last-updated');
    if (lastUpdated) {
        const now = new Date();
        lastUpdated.textContent = now.toLocaleDateString() + ' ' + now.toLocaleTimeString();
    }
});

