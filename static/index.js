// Dark Mode Toggle
function toggleMode(){
    document.body.classList.toggle("light-mode");
}

// Skills dropdown toggle (used on skills page)
document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('skillsToggle');
    const list = document.getElementById('skillsList');
    if (btn && list) {
        btn.addEventListener('click', function () {
            list.classList.toggle('hidden');
            btn.textContent = list.classList.contains('hidden') ? 'Show Skill Categories ▾' : 'Hide Skill Categories ▴';
        });
    }
    const pbtn = document.getElementById('projectsToggle');
    const plist = document.getElementById('projectsList');
    if (pbtn && plist) {
        pbtn.addEventListener('click', function () {
            plist.classList.toggle('hidden');
            pbtn.textContent = plist.classList.contains('hidden') ? 'Show Machine Learning Projects ▾' : 'Hide Machine Learning Projects ▴';
        });
    }
});

// Chart.js Example - Model Accuracy
const ctx = document.getElementById('accuracyChart').getContext('2d');
const accuracyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
            label: 'Model Accuracy %',
            data: [82, 85, 87, 88, 89],
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.2)',
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive:true,
        plugins: {legend: {labels:{color:'white'}}},
        scales: {
            y: {beginAtZero:true, ticks:{color:'white'}},
            x: {ticks:{color:'white'}}
        }
    }
});

// Chart.js Example - User Growth
const ctx2 = document.getElementById('userGrowthChart').getContext('2d');
const userGrowthChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mar','Apr','May'],
        datasets: [{
            label:'Active Users',
            data:[150, 230, 300, 400, 480],
            backgroundColor:'#38bdf8'
        }]
    },
    options: {
        responsive:true,
        plugins: {legend: {labels:{color:'white'}}},
        scales: {
            y: {beginAtZero:true, ticks:{color:'white'}},
            x: {ticks:{color:'white'}}
        }
    }
});