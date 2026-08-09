/* ==========================================================================
   LIFE CARE DASHBOARD FRONTEND LOGIC (ES6)
   ========================================================================== */

const API_BASE = '/api';

// Global App State
let state = {
  user: null,
  activeTab: 'dashboard',
  currentReportType: 'daily',
  charts: {
    water: null,
    sleep: null
  }
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  const savedUser = localStorage.getItem('life_care_user');
  if (savedUser) {
    try {
      state.user = JSON.parse(savedUser);
      showMainApp();
    } catch (e) {
      localStorage.removeItem('life_care_user');
    }
  }

  // Set default dates in inputs
  const todayStr = new Date().toISOString().split('T')[0];
  document.getElementById('current-date-display').innerText = new Date().toLocaleDateString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric', year: 'numeric'
  });

  const startDateElem = document.getElementById('med-start-date');
  const endDateElem = document.getElementById('med-end-date');
  const apptDateElem = document.getElementById('appt-date');

  if (startDateElem) startDateElem.value = todayStr;
  if (endDateElem) endDateElem.value = todayStr;
  if (apptDateElem) apptDateElem.value = todayStr;

  renderTimeInputs();
});

// ----------------- AUTHENTICATION -----------------
function switchAuthTab(tab) {
  document.getElementById('tab-login-btn').classList.toggle('active', tab === 'login');
  document.getElementById('tab-register-btn').classList.toggle('active', tab === 'register');
  document.getElementById('login-form').classList.toggle('hidden', tab !== 'login');
  document.getElementById('register-form').classList.toggle('hidden', tab !== 'register');
  hideAuthError();
}

function showAuthError(msg) {
  const errBox = document.getElementById('auth-error-msg');
  errBox.innerText = msg;
  errBox.classList.remove('hidden');
}

function hideAuthError() {
  document.getElementById('auth-error-msg').classList.add('hidden');
}

async function handleLogin(e) {
  e.preventDefault();
  hideAuthError();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (data.success) {
      state.user = data.user;
      localStorage.setItem('life_care_user', JSON.stringify(data.user));
      showMainApp();
    } else {
      showAuthError(data.message || 'Login failed.');
    }
  } catch (err) {
    showAuthError('Server connection error. Please ensure server is running.');
  }
}

async function handleRegister(e) {
  e.preventDefault();
  hideAuthError();
  const name = document.getElementById('reg-name').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    if (data.success) {
      state.user = data.user;
      localStorage.setItem('life_care_user', JSON.stringify(data.user));
      showMainApp();
    } else {
      showAuthError(data.message || 'Registration failed.');
    }
  } catch (err) {
    showAuthError('Server connection error.');
  }
}

function demoLogin(email, password) {
  document.getElementById('login-email').value = email;
  document.getElementById('login-password').value = password;
  handleLogin(new Event('submit'));
}

function handleLogout() {
  localStorage.removeItem('life_care_user');
  state.user = null;
  document.getElementById('main-app').classList.add('hidden');
  document.getElementById('auth-container').classList.remove('hidden');
}

function showMainApp() {
  document.getElementById('auth-container').classList.add('hidden');
  document.getElementById('main-app').classList.remove('hidden');

  // Set Nav User Info
  document.getElementById('nav-user-name').innerText = state.user.name;
  document.getElementById('nav-user-email').innerText = state.user.email;
  document.getElementById('nav-user-avatar').innerText = state.user.name.charAt(0).toUpperCase();

  navigateTo('dashboard');
}

// ----------------- NAVIGATION -----------------
function navigateTo(tabId) {
  state.activeTab = tabId;

  // Update Navigation UI
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabId);
  });

  document.querySelectorAll('.tab-view').forEach(view => {
    view.classList.toggle('hidden', view.id !== `view-${tabId}`);
    view.classList.toggle('active', view.id === `view-${tabId}`);
  });

  // Update Page Title
  const titles = {
    dashboard: ['Overview Dashboard', 'Summary of your health tracking metrics'],
    water: ['Hydration Tracker', 'Track your daily water intake and keep streaks glowing'],
    sleep: ['Sleep Studio', 'Log sleeping hours, evaluate quality, and maintain rest habits'],
    activity: ['Activity Hub', 'Monitor daily steps, exercise duration, and workout logs'],
    mood: ['Mood Lounge', 'Log daily emotional states and view history trends'],
    medicines: ['Medication Manager', 'Manage prescribed medicines and mark daily doses taken'],
    appointments: ['Medical Appointments', 'View and schedule clinic checkups and doctor visits'],
    reports: ['Health Reports & Badges', 'Comprehensive analytics, health score, and achievements'],
    profile: ['User Profile Settings', 'Update account details and security settings']
  };

  if (titles[tabId]) {
    document.getElementById('page-title').innerText = titles[tabId][0];
    document.getElementById('page-subtitle').innerText = titles[tabId][1];
  }

  // Load Tab Specific Data
  switch (tabId) {
    case 'dashboard': loadDashboard(); break;
    case 'water': loadWaterTab(); break;
    case 'sleep': loadSleepTab(); break;
    case 'activity': loadActivityTab(); break;
    case 'mood': loadMoodTab(); break;
    case 'medicines': loadMedicinesTab(); break;
    case 'appointments': loadAppointmentsTab(); break;
    case 'reports': loadReport(state.currentReportType); break;
    case 'profile': loadProfileTab(); break;
  }
}

// ----------------- DASHBOARD -----------------
async function loadDashboard() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/dashboard/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    // Water Metric
    const water = data.water || { cups: 0, goal: 8 };
    document.getElementById('dash-water-cups').innerText = water.cups;
    document.getElementById('dash-water-goal').innerText = water.goal;
    const waterPct = Math.min(100, Math.round((water.cups / water.goal) * 100));
    document.getElementById('dash-water-bar').style.width = `${waterPct}%`;

    // Sleep Metric
    const sleep = data.sleep || { hours: 0, quality: 'No Record' };
    document.getElementById('dash-sleep-hours').innerText = sleep.hours;
    document.getElementById('dash-sleep-quality').innerText = sleep.quality || 'No Record';

    // Activity Metric
    const activity = data.activity || { steps: 0, duration: 0 };
    document.getElementById('dash-steps').innerText = activity.steps.toLocaleString();

    // Mood Metric
    const mood = data.mood || { mood: 'Not Logged' };
    document.getElementById('dash-mood-val').innerText = mood.mood;

    const moodEmojis = {
      happy: '😊', excited: '🤩', normal: '🙂', tired: '🥱', stressed: '😰', sad: '😢', angry: '😡'
    };
    document.getElementById('dash-mood-emoji').innerText = moodEmojis[mood.mood.toLowerCase()] || '✨';

    // Next Appointment
    const apptBox = document.getElementById('dash-appointment-box');
    if (data.next_appointment) {
      const appt = data.next_appointment;
      apptBox.innerHTML = `
        <div class="dash-appt-card">
          <h4>${appt.title}</h4>
          <p><i class="fa-solid fa-user-doctor"></i> Dr. ${appt.doctor} - ${appt.clinic}</p>
          <p><i class="fa-regular fa-clock"></i> ${appt.date} at ${appt.time}</p>
          <span class="badge-pill bg-emerald mt-2">${appt.status}</span>
        </div>
      `;
    } else {
      apptBox.innerHTML = `<p class="text-muted">No upcoming appointments scheduled.</p>`;
    }

    // Today's Medicines Doses
    const medsRes = await fetch(`${API_BASE}/medicines/${state.user.user_id}`);
    const medsData = await medsRes.json();
    const medsBox = document.getElementById('dash-medicines-box');
    if (medsData.success && medsData.medicines.length > 0) {
      const todayStr = new Date().toISOString().split('T')[0];
      let html = '<div class="dash-meds-list">';
      medsData.medicines.forEach(m => {
        const takenArr = (m.taken && m.taken[todayStr]) ? m.taken[todayStr] : new Array(m.times_per_day).fill(false);
        const takenCount = takenArr.filter(Boolean).length;
        html += `
          <div class="dash-med-item">
            <div>
              <strong>${m.medicine_name}</strong> (${m.dose})
              <div class="text-sm text-muted">${takenCount} of ${m.times_per_day} doses taken today</div>
            </div>
            <button class="btn-secondary btn-sm" onclick="navigateTo('medicines')">View</button>
          </div>
        `;
      });
      html += '</div>';
      medsBox.innerHTML = html;
    } else {
      medsBox.innerHTML = `<p class="text-muted">No active prescribed medicines.</p>`;
    }

  } catch (e) {
    console.error('Error loading dashboard:', e);
  }
}

// ----------------- WATER TRACKER -----------------
async function loadWaterTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/water/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    const today = data.today;
    document.getElementById('water-cups-count').innerText = today.cups;
    document.getElementById('water-goal-count').innerText = today.goal;
    document.getElementById('water-percent-display').innerText = `${today.progress}%`;
    document.getElementById('water-wave-fill').style.height = `${today.progress}%`;
    document.getElementById('water-streak-badge').innerText = `🔥 ${today.streak} Days Streak`;

    let advice = "Stay hydrated! Water keeps your muscles and mind active.";
    if (today.progress >= 100) advice = "🎉 Outstanding! You reached your 8-cup daily water goal!";
    else if (today.progress >= 50) advice = "✅ Great progress! You're past halfway to your daily target.";
    else if (today.cups > 0) advice = "💧 Good start! Drink another cup to keep your momentum going.";
    document.getElementById('water-advice-msg').innerText = advice;

    // Render History Chart
    renderWaterChart(data.history || []);
  } catch (e) {
    console.error('Error loading water tab:', e);
  }
}

async function addWaterCup() {
  try {
    const res = await fetch(`${API_BASE}/water/${state.user.user_id}/add`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      loadWaterTab();
    }
  } catch (e) {
    console.error('Error adding cup:', e);
  }
}

function renderWaterChart(history) {
  const ctx = document.getElementById('waterHistoryChart');
  if (!ctx) return;

  const labels = history.slice(-7).map(h => h.date);
  const cupsData = history.slice(-7).map(h => h.cups);

  if (state.charts.water) state.charts.water.destroy();

  state.charts.water = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Cups Drank',
        data: cupsData,
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6, 182, 212, 0.2)',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, max: 10 } }
    }
  });
}

// ----------------- SLEEP STUDIO -----------------
async function loadSleepTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/sleep/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    document.getElementById('sleep-streak-badge').innerText = `🔥 ${data.streak} Days Streak`;
    const statusBox = document.getElementById('sleep-status-display');

    if (data.today) {
      const rec = data.today;
      let msg = "Maintaining a consistent sleep schedule improves mental focus.";
      if (rec.hours >= 7) msg = "Great job! You got a healthy amount of restful sleep 😴✨";
      else msg = "You slept less than recommended (7-8 hours). Try to sleep earlier tonight!";

      statusBox.innerHTML = `
        <div class="sleep-summary-card">
          <h4>${rec.hours} Hours Logged (${rec.quality})</h4>
          <p class="mt-2 text-muted">${msg}</p>
        </div>
      `;
    } else {
      statusBox.innerHTML = `<p class="text-muted">No sleep recorded for today yet.</p>`;
    }

    renderSleepChart(data.history || []);
  } catch (e) {
    console.error('Error loading sleep tab:', e);
  }
}

async function handleLogSleep(e) {
  e.preventDefault();
  const sleep_time = document.getElementById('sleep-start-time').value;
  const wake_time = document.getElementById('sleep-wake-time').value;
  const quality = document.querySelector('input[name="sleep-quality"]:checked').value;

  try {
    const res = await fetch(`${API_BASE}/sleep/${state.user.user_id}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sleep_time, wake_time, quality })
    });
    const data = await res.json();
    if (data.success) {
      loadSleepTab();
    } else {
      alert(data.message || 'Error saving sleep.');
    }
  } catch (err) {
    console.error('Error saving sleep:', err);
  }
}

function renderSleepChart(history) {
  const ctx = document.getElementById('sleepHistoryChart');
  if (!ctx) return;

  const labels = history.slice(-7).map(h => h.date);
  const hoursData = history.slice(-7).map(h => h.hours);

  if (state.charts.sleep) state.charts.sleep.destroy();

  state.charts.sleep = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Sleep Hours',
        data: hoursData,
        backgroundColor: '#6366f1',
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, max: 14 } }
    }
  });
}

// ----------------- ACTIVITY HUB -----------------
async function loadActivityTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/activity/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    document.getElementById('activity-streak-badge').innerText = `🔥 ${data.streak} Days Streak`;

    if (data.today) {
      document.getElementById('act-steps').value = data.today.steps;
      document.getElementById('act-duration').value = data.today.duration;
    }

    // Client-side statistics: uses the existing backend history without changing the backend.
    const history = data.history || [];
    const stepsValues = history.map(x => Number(x.steps) || 0);
    const durationValues = history.map(x => Number(x.duration) || 0);
    const avg = arr => arr.length ? Math.round(arr.reduce((a,b) => a+b, 0) / arr.length) : 0;
    const max = arr => arr.length ? Math.max(...arr) : 0;
    const activityStats = document.getElementById('activity-statistics');
    if (activityStats) {
      activityStats.innerHTML = `
        <div class="stat-mini"><span class="stat-label">Average Steps</span><span class="stat-value">${avg(stepsValues).toLocaleString()}</span></div>
        <div class="stat-mini"><span class="stat-label">Highest Steps</span><span class="stat-value">${max(stepsValues).toLocaleString()}</span></div>
        <div class="stat-mini"><span class="stat-label">Avg. Exercise</span><span class="stat-value">${avg(durationValues)} min</span></div>
        <div class="stat-mini"><span class="stat-label">Best Day</span><span class="stat-value">${max(stepsValues).toLocaleString()} steps</span></div>`;
    }

    const todaySteps = Number((data.today || {}).steps || 0);
    const todayDuration = Number((data.today || {}).duration || 0);
    const stepsPct = Math.min(100, Math.round(todaySteps / 8000 * 100));
    const exercisePct = Math.min(100, Math.round(todayDuration / 30 * 100));
    const goals = document.getElementById('activity-goals');
    if (goals) {
      goals.innerHTML = `
        <div class="goal-item"><div class="goal-row"><strong>Steps</strong><span>${todaySteps.toLocaleString()} / 8,000</span></div><div class="goal-progress"><span style="width:${stepsPct}%"></span></div></div>
        <div class="goal-item"><div class="goal-row"><strong>Exercise</strong><span>${todayDuration} / 30 min</span></div><div class="goal-progress"><span style="width:${exercisePct}%"></span></div></div>
        <p class="text-sm text-muted">${stepsPct >= 100 && exercisePct >= 100 ? '🎉 Great job! You reached both daily activity goals.' : '💪 Keep going! A little more movement can help you reach today’s goals.'}</p>`;
    }

    // Render Table History
    const container = document.getElementById('activity-history-table');
    if (data.history && data.history.length > 0) {
      let html = `
        <table class="data-table">
          <thead>
            <tr><th>Date</th><th>Steps</th><th>Duration</th></tr>
          </thead>
          <tbody>
      `;
      data.history.slice(-10).reverse().forEach(row => {
        html += `
          <tr>
            <td>${row.date}</td>
            <td><strong>${row.steps.toLocaleString()}</strong></td>
            <td>${row.duration} mins</td>
          </tr>
        `;
      });
      html += `</tbody></table>`;
      container.innerHTML = html;
    } else {
      container.innerHTML = `<p class="text-muted">No activity history recorded.</p>`;
    }
  } catch (e) {
    console.error('Error loading activity:', e);
  }
}

async function handleLogActivity(e) {
  e.preventDefault();
  const steps = document.getElementById('act-steps').value;
  const duration = document.getElementById('act-duration').value;

  try {
    const res = await fetch(`${API_BASE}/activity/${state.user.user_id}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ steps, duration })
    });
    const data = await res.json();
    if (data.success) {
      loadActivityTab();
    }
  } catch (e) {
    console.error('Error saving activity:', e);
  }
}

// ----------------- MOOD LOUNGE -----------------
async function loadMoodTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/mood/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    document.getElementById('mood-streak-badge').innerText = `🔥 ${data.streak} Days Streak`;

    const container = document.getElementById('mood-history-list');
    const emojis = { happy: '😊', excited: '🤩', normal: '🙂', tired: '🥱', stressed: '😰', sad: '😢', angry: '😡' };
    const history = data.history || [];

    // Mood statistics are calculated from the existing history returned by the backend.
    const counts = {};
    history.forEach(item => {
      const key = String(item.mood || 'unknown').toLowerCase();
      counts[key] = (counts[key] || 0) + 1;
    });
    const total = history.length;
    const positive = (counts.happy || 0) + (counts.excited || 0);
    const positivePct = total ? Math.round(positive / total * 100) : 0;
    const mostFrequent = total ? Object.entries(counts).sort((a,b) => b[1] - a[1])[0][0] : '—';
    const stats = document.getElementById('mood-statistics');
    if (stats) {
      stats.innerHTML = `
        <div class="stat-mini"><span class="stat-label">Happy</span><span class="stat-value">${counts.happy || 0}</span></div>
        <div class="stat-mini"><span class="stat-label">Normal</span><span class="stat-value">${counts.normal || 0}</span></div>
        <div class="stat-mini"><span class="stat-label">Positive %</span><span class="stat-value">${positivePct}%</span></div>
        <div class="stat-mini"><span class="stat-label">Most Frequent</span><span class="stat-value capitalize">${mostFrequent}</span></div>`;
    }

    const insight = document.getElementById('mood-insight');
    if (insight) {
      if (!total) insight.textContent = 'Start logging your mood daily to discover patterns over time.';
      else if (positivePct >= 70) insight.textContent = '🌟 Most of your recent logs are positive. Keep doing things that support your wellbeing.';
      else if (positivePct < 30) insight.textContent = '💙 Your positive-mood percentage is low lately. Consider rest, a short walk, or an enjoyable activity.';
      else insight.textContent = '🙂 Your mood has been mixed recently. Keep tracking it to understand your patterns better.';
    }

    if (history.length > 0) {
      let html = '<div class="history-grid">';
      data.history.slice(-12).reverse().forEach(item => {
        html += `
          <div class="mood-history-card">
            <span class="mood-card-emoji">${emojis[item.mood.toLowerCase()] || '✨'}</span>
            <div class="mood-card-info">
              <strong class="capitalize">${item.mood}</strong>
              <div class="text-sm text-muted">${item.date}</div>
            </div>
          </div>
        `;
      });
      html += '</div>';
      container.innerHTML = html;
    } else {
      container.innerHTML = `<p class="text-muted">No mood logs yet.</p>`;
    }
  } catch (e) {
    console.error('Error loading mood tab:', e);
  }
}

async function logMood(moodValue) {
  try {
    const res = await fetch(`${API_BASE}/mood/${state.user.user_id}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mood: moodValue })
    });
    const data = await res.json();
    if (data.success) {
      loadMoodTab();
    }
  } catch (e) {
    console.error('Error logging mood:', e);
  }
}

// ----------------- MEDICINES -----------------
async function loadMedicinesTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/medicines/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    // Notifications
    const notifArea = document.getElementById('medication-notifications');
    if (data.notifications && data.notifications.length > 0) {
      let nHtml = '';
      data.notifications.forEach(n => {
        nHtml += `
          <div class="alert-box alert-warning">
            <i class="fa-solid fa-bell"></i>
            <div>
              <strong>${n.title}</strong>
              <div>${n.message}</div>
            </div>
          </div>
        `;
      });
      notifArea.innerHTML = nHtml;
    } else {
      notifArea.innerHTML = '';
    }

    // Medicines Grid
    const grid = document.getElementById('medicines-grid');
    if (data.medicines && data.medicines.length > 0) {
      let html = '';
      const todayStr = new Date().toISOString().split('T')[0];
      data.medicines.forEach(m => {
        const takenList = (m.taken && m.taken[todayStr]) ? m.taken[todayStr] : new Array(m.times_per_day).fill(false);
        
        let dosesChecklist = '<div class="doses-checklist">';
        m.times.forEach((tStr, idx) => {
          const isTaken = takenList[idx] || false;
          dosesChecklist += `
            <label class="dose-check-label ${isTaken ? 'taken' : ''}">
              <input type="checkbox" ${isTaken ? 'checked disabled' : ''} onchange="markDoseTaken(${m.medicine_id}, ${idx})">
              <span>Dose ${idx + 1} (${tStr}) - ${isTaken ? 'Taken ✓' : 'Pending'}</span>
            </label>
          `;
        });
        dosesChecklist += '</div>';

        html += `
          <div class="glass-card medicine-card">
            <div class="card-header">
              <h3><i class="fa-solid fa-capsules text-rose"></i> ${m.medicine_name}</h3>
              <button class="btn-link text-danger" onclick="deleteMedicine(${m.medicine_id})"><i class="fa-solid fa-trash"></i></button>
            </div>
            <div class="med-details mt-2">
              <div><strong>Dose:</strong> ${m.dose}</div>
              <div><strong>Schedule:</strong> ${m.times_per_day} times/day</div>
              <div><strong>Duration:</strong> ${m.start_date} to ${m.end_date}</div>
            </div>
            <h4 class="mt-4 text-sm font-semibold">Today's Dose Checklist:</h4>
            ${dosesChecklist}
          </div>
        `;
      });
      grid.innerHTML = html;
    } else {
      grid.innerHTML = `<p class="text-muted">No medicines added yet. Click "Add New Medicine" to add one.</p>`;
    }
  } catch (e) {
    console.error('Error loading medicines:', e);
  }
}

function renderTimeInputs() {
  const count = parseInt(document.getElementById('med-times-count').value) || 1;
  const container = document.getElementById('med-time-inputs-container');
  let html = '<label>Schedule Times (HH:MM)</label><div class="form-row flex-wrap">';
  for (let i = 0; i < count; i++) {
    html += `<input type="time" class="med-time-input flex-1" value="${12 + i}:00" required>`;
  }
  html += '</div>';
  container.innerHTML = html;
}

async function handleCreateMedicine(e) {
  e.preventDefault();
  const medicine_name = document.getElementById('med-name').value;
  const dose = document.getElementById('med-dose').value;
  const times_per_day = parseInt(document.getElementById('med-times-count').value);
  const timeElems = document.querySelectorAll('.med-time-input');
  const times = Array.from(timeElems).map(input => input.value);
  const start_date = document.getElementById('med-start-date').value;
  const end_date = document.getElementById('med-end-date').value;

  try {
    const res = await fetch(`${API_BASE}/medicines/${state.user.user_id}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ medicine_name, dose, times_per_day, times, start_date, end_date })
    });
    const data = await res.json();
    if (data.success) {
      closeModal('add-medicine-modal');
      loadMedicinesTab();
    } else {
      alert(data.message || 'Error creating medicine.');
    }
  } catch (err) {
    console.error('Error creating medicine:', err);
  }
}

async function markDoseTaken(medId, doseIdx) {
  try {
    const res = await fetch(`${API_BASE}/medicines/${state.user.user_id}/mark_taken`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ medicine_id: medId, dose_index: doseIdx })
    });
    const data = await res.json();
    if (data.success) {
      loadMedicinesTab();
    }
  } catch (e) {
    console.error('Error marking dose taken:', e);
  }
}

async function deleteMedicine(medId) {
  if (!confirm('Are you sure you want to remove this medicine?')) return;
  try {
    const res = await fetch(`${API_BASE}/medicines/${state.user.user_id}/delete/${medId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      loadMedicinesTab();
    }
  } catch (e) {
    console.error('Error deleting medicine:', e);
  }
}

// ----------------- APPOINTMENTS -----------------
async function loadAppointmentsTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/appointments/${state.user.user_id}`);
    const data = await res.json();
    if (!data.success) return;

    const grid = document.getElementById('appointments-grid');
    if (data.appointments && data.appointments.length > 0) {
      let html = '';
      data.appointments.reverse().forEach(a => {
        const statusColors = {
          Upcoming: 'bg-emerald', Completed: 'bg-indigo', Missed: 'bg-amber', Cancelled: 'text-danger'
        };
        html += `
          <div class="glass-card appointment-card">
            <div class="card-header">
              <h3><i class="fa-solid fa-stethoscope text-cyan"></i> ${a.title}</h3>
              <select onchange="updateApptStatus('${a.appointment_id}', this.value)" class="status-select">
                <option value="Upcoming" ${a.status === 'Upcoming' ? 'selected' : ''}>Upcoming</option>
                <option value="Completed" ${a.status === 'Completed' ? 'selected' : ''}>Completed</option>
                <option value="Missed" ${a.status === 'Missed' ? 'selected' : ''}>Missed</option>
                <option value="Cancelled" ${a.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
              </select>
            </div>
            <div class="appt-details mt-3">
              <div><i class="fa-solid fa-user-doctor"></i> <strong>Doctor:</strong> ${a.doctor}</div>
              <div><i class="fa-solid fa-hospital"></i> <strong>Clinic:</strong> ${a.clinic}</div>
              <div><i class="fa-regular fa-calendar"></i> <strong>Date & Time:</strong> ${a.date} at ${a.time}</div>
              ${a.notes ? `<div class="mt-2 text-muted text-sm"><i class="fa-solid fa-note-sticky"></i> ${a.notes}</div>` : ''}
            </div>
            <div class="mt-4 flex justify-between align-center">
              <span class="badge-pill ${statusColors[a.status] || ''}">${a.status}</span>
              <button class="btn-link text-danger" onclick="deleteAppointment('${a.appointment_id}')"><i class="fa-solid fa-trash"></i> Delete</button>
            </div>
          </div>
        `;
      });
      grid.innerHTML = html;
    } else {
      grid.innerHTML = `<p class="text-muted">No appointments scheduled yet. Click "Schedule Appointment" to add one.</p>`;
    }
  } catch (e) {
    console.error('Error loading appointments:', e);
  }
}

async function handleCreateAppointment(e) {
  e.preventDefault();
  const title = document.getElementById('appt-title').value;
  const doctor = document.getElementById('appt-doctor').value;
  const clinic = document.getElementById('appt-clinic').value;
  const date = document.getElementById('appt-date').value;
  const time = document.getElementById('appt-time').value;
  const notes = document.getElementById('appt-notes').value;

  try {
    const res = await fetch(`${API_BASE}/appointments/${state.user.user_id}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, doctor, clinic, date, time, notes })
    });
    const data = await res.json();
    if (data.success) {
      closeModal('add-appointment-modal');
      loadAppointmentsTab();
    } else {
      alert(data.message || 'Error creating appointment.');
    }
  } catch (err) {
    console.error('Error creating appointment:', err);
  }
}

async function updateApptStatus(apptId, newStatus) {
  try {
    const res = await fetch(`${API_BASE}/appointments/${state.user.user_id}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ appointment_id: apptId, status: newStatus })
    });
    const data = await res.json();
    if (data.success) {
      loadAppointmentsTab();
    }
  } catch (e) {
    console.error('Error updating status:', e);
  }
}

async function deleteAppointment(apptId) {
  if (!confirm('Are you sure you want to delete this appointment?')) return;
  try {
    const res = await fetch(`${API_BASE}/appointments/${state.user.user_id}/delete/${apptId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      loadAppointmentsTab();
    }
  } catch (e) {
    console.error('Error deleting appointment:', e);
  }
}

// ----------------- REPORTS & BADGES -----------------
async function loadReport(type) {
  state.currentReportType = type;
  document.querySelectorAll('.seg-btn').forEach(btn => {
    btn.classList.toggle('active', btn.innerText.toLowerCase().includes(type));
  });

  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/reports/${state.user.user_id}?type=${type}`);
    const data = await res.json();
    if (!data.success) return;

    // Score & Status
    document.getElementById('report-score-num').innerText = data.score;
    document.getElementById('report-status-badge').innerText = data.overall_status.toUpperCase();

    // Challenges
    const challengesContainer = document.getElementById('report-challenges-list');
    if (data.challenges) {
      let cHtml = '';
      data.challenges.forEach(c => {
        cHtml += `
          <div class="challenge-item ${c.done ? 'completed' : ''}">
            <i class="fa-solid ${c.done ? 'fa-circle-check text-success' : 'fa-circle-notch text-muted'}"></i>
            <div>
              <strong>${c.name}</strong>
              <div class="text-sm text-muted">${c.val}</div>
            </div>
          </div>
        `;
      });
      challengesContainer.innerHTML = cHtml;
    }

    // Badges
    const badgesContainer = document.getElementById('report-badges-grid');
    if (data.badges && data.badges.length > 0) {
      let bHtml = '';
      data.badges.forEach(b => {
        bHtml += `
          <div class="badge-item">
            <div class="badge-icon">${b.icon}</div>
            <div class="badge-name">${b.name}</div>
          </div>
        `;
      });
      badgesContainer.innerHTML = bHtml;
    } else {
      badgesContainer.innerHTML = `<p class="text-muted">Complete daily health challenges to unlock badges!</p>`;
    }

  } catch (e) {
    console.error('Error loading report:', e);
  }
}

// ----------------- PROFILE -----------------
async function loadProfileTab() {
  if (!state.user) return;
  try {
    const res = await fetch(`${API_BASE}/auth/profile/${state.user.user_id}`);
    const data = await res.json();
    if (data.success) {
      document.getElementById('prof-name').value = data.user.name;
      document.getElementById('prof-email').value = data.user.email;
    }
  } catch (e) {
    console.error('Error loading profile:', e);
  }
}

async function handleUpdateProfile(e) {
  e.preventDefault();
  const name = document.getElementById('prof-name').value;
  const email = document.getElementById('prof-email').value;
  const old_password = document.getElementById('prof-old-pass').value;
  const new_password = document.getElementById('prof-new-pass').value;

  try {
    const res = await fetch(`${API_BASE}/auth/profile/${state.user.user_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, old_password, new_password })
    });
    const data = await res.json();
    if (data.success) {
      alert('Profile updated successfully!');
      state.user = data.user;
      localStorage.setItem('life_care_user', JSON.stringify(data.user));
      showMainApp();
    } else {
      alert(data.message || 'Error updating profile.');
    }
  } catch (err) {
    console.error('Error updating profile:', err);
  }
}

// ----------------- MODALS -----------------
function openModal(modalId) {
  document.getElementById(modalId).classList.remove('hidden');
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
}
