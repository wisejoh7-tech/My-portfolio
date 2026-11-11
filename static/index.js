// Dark Mode Toggle
function toggleMode() {
    document.body.classList.toggle("light-mode");
}

// Dropdowns toggle (used on skills & projects page)
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

    // Mobile Navbar Toggle
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");
    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", () => {
            menuToggle.classList.toggle("active");
            navLinks.classList.toggle("active");
        });

        // Close menu when clicking outside
        document.addEventListener("click", (e) => {
            if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
                navLinks.classList.remove("active");
                menuToggle.classList.remove("active");
            }
        });
    }

    // Scroll Navbar Shrink
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 50) {
                navbar.classList.add("shrink");
            } else {
                navbar.classList.remove("shrink");
            }
        });
    }

    // Initialise Chart.js if elements exist
    const accElem = document.getElementById('accuracyChart');
    if (accElem && typeof Chart !== 'undefined') {
        const ctx = accElem.getContext('2d');
        new Chart(ctx, {
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
                responsive: true,
                plugins: { legend: { labels: { color: 'white' } } },
                scales: {
                    y: { beginAtZero: true, ticks: { color: 'white' } },
                    x: { ticks: { color: 'white' } }
                }
            }
        });
    }

    const userElem = document.getElementById('userGrowthChart');
    if (userElem && typeof Chart !== 'undefined') {
        const ctx2 = userElem.getContext('2d');
        new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                datasets: [{
                    label: 'Active Users',
                    data: [150, 230, 300, 400, 480],
                    backgroundColor: '#38bdf8'
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { labels: { color: 'white' } } },
                scales: {
                    y: { beginAtZero: true, ticks: { color: 'white' } },
                    x: { ticks: { color: 'white' } }
                }
            }
        });
    }
});

// Generic Helper for ML Prediction Forms
async function runPrediction(endpoint, formId, resultId) {
    const form = document.getElementById(formId);
    const resultBox = document.getElementById(resultId);
    if (!form || !resultBox) return;

    resultBox.style.display = 'block';
    resultBox.innerHTML = '<p style="color:#38bdf8;">Analyzing patient/user parameters...</p>';

    const formData = new FormData(form);
    const payload = {};
    formData.forEach((value, key) => {
        payload[key] = value;
    });

    try {
        const resp = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await resp.json();
        if (!resp.ok || !data.success) {
            resultBox.innerHTML = `<p style="color:#ef4444;">Error: ${data.error || 'Failed to complete prediction'}</p>`;
            return;
        }

        let outputHtml = `<div style="padding:15px; background:rgba(56,189,248,0.15); border:1px solid #38bdf8; border-radius:10px; margin-top:15px;">`;
        if (data.probability !== undefined) {
            outputHtml += `<p><strong>Predicted Risk / Probability:</strong> <span style="color:#38bdf8; font-size:1.2em;">${data.probability}%</span></p>`;
        }
        if (data.risk_level) {
            outputHtml += `<p><strong>Assessment:</strong> <span style="color:#f59e0b;">${data.risk_level}</span></p>`;
        }
        if (data.purchase_probability !== undefined) {
            outputHtml += `<p><strong>Purchase Probability:</strong> <span style="color:#38bdf8; font-size:1.2em;">${data.purchase_probability}%</span></p>`;
            outputHtml += `<p><strong>Customer Intent:</strong> <span style="color:#f59e0b;">${data.intent}</span></p>`;
        }
        if (data.strategy) {
            outputHtml += `<p><strong>Recommended Strategy:</strong> ${data.strategy}</p>`;
        }
        if (data.recommendation) {
            outputHtml += `<p><strong>Clinical Recommendation:</strong> ${data.recommendation}</p>`;
        }
        outputHtml += `</div>`;
        resultBox.innerHTML = outputHtml;
    } catch (err) {
        resultBox.innerHTML = `<p style="color:#ef4444;">Connection error: ${err.message}</p>`;
    }
}
