import { APIs } from "./constraints.js";



let brainData = null;

async function get_json() {
    try {

        const response = await fetch(APIs.JSON, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            // response.error isn't a thing; use statusText
            console.error(`Response failed: ${response.statusText}`);
            return;
        }

        // 3. await the parsing, and it's lowercase .json(), not .JSON()
        const data = await response.json();

        // 4. Access the 'json' key you sent from FastAPI
        const js = data["json"];

        if (!js) {
            console.error("The 'json' key is missing from the response.");
            return;
        }

        console.log(`JSON found! ID check: ${js["id"]}`);
        return js;
        
    } catch (err) {
        console.error("Network or parsing error:", err);
    }
}


get_json().then(js => {
    if (js) {
        window.brainData = js; 
    }
});




  let selectedStudent = null;
  let currentPage = 'brain';
  
  // ──────────────────────────────────────────────
  // Helpers
  // ──────────────────────────────────────────────

  function getAllStudents() {
    const out = [];
    // Ensure we grab the dictionary from the array
    const periodsContainer = brainData.brain.classes.students[0]; 
  
    Object.entries(periodsContainer).forEach(([period, studentArrays]) => {
      studentArrays.forEach(stu => {
        // stu is ["First", "Last"]
        const fullName = `${stu[0]} ${stu[1]}`.trim(); 
        out.push({ name: fullName, period });
      });
    });
    return out;
  }

  function SinglegetAllStudents() {
    const out = [];
    const periods = brainData.brain.classes.students;
    periods.forEach(periodObj => {
      Object.entries(periodObj).forEach(([period, names]) => {
        names.forEach(name => out.push({ name, period }));
      });
    });
    return out;
  }
  
  function avatarColor(name) {
    const colors = ['#7c6af7','#4fd1c5','#f6ad55','#68d391','#fc8181','#63b3ed','#f687b3'];
    let h = 0;
    for (let c of name) h = (h * 31 + c.charCodeAt(0)) & 0xffff;
    return colors[h % colors.length];
  }
  
  function initials(name) {
    return name.slice(0, 2).toUpperCase();
  }
  
  function stars(rating) {
    let s = '';
    for (let i = 1; i <= 5; i++) {
      s += `<span class="star ${i <= rating ? 'filled' : 'empty'}">${i <= rating ? '★' : '☆'}</span>`;
    }
    return s;
  }
  
function emotionClass(e) {
    if (!e) return 'Neutral';
    if (e.toLowerCase().includes('friend')) return 'Friendly';
    if (e.toLowerCase().includes('enthu')) return 'Enthusiastic';
    if (e.toLowerCase().includes('mix') || e.toLowerCase().includes('super')) return 'Mixed';
    return 'Neutral';
  }
  
function setPage(page) {
    currentPage = page;
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    const items = document.querySelectorAll('.nav-item');
    const map = ['brain','students','memory','assignments','periods','import'];
    const idx = map.indexOf(page);
    if (idx >= 0) items[idx]?.classList.add('active');
    render();
  }
  
  // ──────────────────────────────────────────────
  // Pages
  // ──────────────────────────────────────────────
  
  function renderBrain() {
    const b = brainData.brain;
    const students = getAllStudents();
    const avgRating = b.chat_history.length
      ? (b.chat_history.reduce((a, c) => a + c.rating, 0) / b.chat_history.length).toFixed(1)
      : '—';
  
    const periodCount = b.classes.students.reduce((a, p) => a + Object.keys(p).length, 0);
  
    return `
    <div class="page-header fade-in">
      <div>
        <div class="page-title"><span>//</span> BRAIN OVERVIEW</div>
        <div class="page-sub">Live snapshot of ${b.name}'s cognitive state</div>
      </div>
    </div>
  
    <div class="stats-row fade-in">
      <div class="stat-card" style="--accent-bar: var(--accent)">
        <div class="stat-label">Students</div>
        <div class="stat-value">${students.length}</div>
        <div class="stat-sub">across ${periodCount} period(s)</div>
      </div>
      <div class="stat-card" style="--accent-bar: var(--accent2)">
        <div class="stat-label">Chat Logs</div>
        <div class="stat-value">${b.chat_history.length}</div>
        <div class="stat-sub">conversations stored</div>
      </div>
      <div class="stat-card" style="--accent-bar: var(--warn)">
        <div class="stat-label">Avg Rating</div>
        <div class="stat-value">${avgRating}</div>
        <div class="stat-sub">out of 5.0</div>
      </div>
      <div class="stat-card" style="--accent-bar: var(--green)">
        <div class="stat-label">Assignments</div>
        <div class="stat-value">${b.student_assignments.length}</div>
        <div class="stat-sub">loaded from classroom</div>
      </div>
    </div>
  
    <div class="section-label fade-in">Identity</div>
    <div class="info-grid fade-in">
      <div class="info-cell">
        <div class="info-cell-label">Instance Name</div>
        <div class="info-cell-value">${b.name}</div>
      </div>
      <div class="info-cell">
        <div class="info-cell-label">Instance ID</div>
        <div class="info-cell-value" style="font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted2)">${brainData.id}</div>
      </div>
      <div class="info-cell">
        <div class="info-cell-label">Date of Activation</div>
        <div class="info-cell-value">${new Date(b.date_of_activation).toLocaleString()}</div>
      </div>
      <div class="info-cell">
        <div class="info-cell-label">Core Directive</div>
        <div class="info-cell-value" style="color: var(--muted2)">${b.core || '⚠ Not set'}</div>
      </div>
    </div>
  
    <div class="section-label fade-in">Recent Chat Activity</div>
    <div class="panel fade-in">
      <div class="panel-header">
        <div class="panel-title">CHAT_HISTORY [ ${b.chat_history.length} entries ]</div>
      </div>
      <div class="panel-body">
        <div class="chat-log">
          ${b.chat_history.map((c, i) => `
            <div class="chat-entry">
              <div class="ce-top">
                <span class="ce-num">#${String(i).padStart(3,'0')}</span>
                <span class="emotion-tag ${emotionClass(c.emotion)}">${c.emotion}</span>
                <div class="rating-stars">${stars(c.rating)}</div>
              </div>
              ${c.summary}
            </div>
          `).join('')}
        </div>
      </div>
    </div>
    `;
  }
  
  function renderStudents() {
    const students = getAllStudents();
    const b = brainData.brain;
  
    const detailHtml = selectedStudent ? (() => {
      const s = selectedStudent;
      return `
        <div class="panel fade-in">
          <div class="panel-header">
            <div class="panel-title">STUDENT_PROFILE :: ${s.name.toUpperCase()}</div>
            <span class="period-badge">${s.period}</span>
          </div>
          <div class="panel-body">
            <div class="info-grid" style="margin-bottom: 16px">
              <div class="info-cell">
                <div class="info-cell-label">Name</div>
                <div class="info-cell-value" style="text-transform: capitalize">${s.name}</div>
              </div>
              <div class="info-cell">
                <div class="info-cell-label">Period</div>
                <div class="info-cell-value">${s.period.replace('_', ' ').toUpperCase()}</div>
              </div>
              <div class="info-cell">
                <div class="info-cell-label">Assignments</div>
                <div class="info-cell-value" style="color: var(--muted2)">— (not yet linked)</div>
              </div>
              <div class="info-cell">
                <div class="info-cell-label">Memory Entries</div>
                <div class="info-cell-value" style="color: var(--muted2)">0</div>
              </div>
            </div>
            <div class="section-label">Memories</div>
            <div class="empty-state">
              <div class="es-icon">🧩</div>
              <div>No student-specific memories yet.</div>
              <div style="margin-top: 6px; font-size: 11px; color: var(--muted)">Memories will appear here once Pepper has per-student tracking enabled.</div>
            </div>
          </div>
        </div>
      `;
    })() : `
      <div class="panel fade-in">
        <div class="panel-body">
          <div class="empty-state">
            <div class="es-icon">👈</div>
            <div>Select a student to view their profile</div>
          </div>
        </div>
      </div>
    `;
  
    return `
    <div class="page-header fade-in">
      <div>
        <div class="page-title"><span>//</span> STUDENTS</div>
        <div class="page-sub">${students.length} students enrolled</div>
      </div>
    </div>
  
    <div class="two-col">
      <div class="panel fade-in">
        <div class="panel-header">
          <div class="panel-title">ROSTER</div>
        </div>
        <div class="panel-body">
          <div class="student-list">
            ${students.map(s => `
              <div class="student-item ${selectedStudent?.name === s.name ? 'selected' : ''}"
                   onclick="selectStudent('${s.name}', '${s.period}')">
                <div class="avatar" style="background: ${avatarColor(s.name)}">${initials(s.name)}</div>
                <div class="student-name" style="text-transform: capitalize">${s.name}</div>
                <span class="period-badge">${s.period.replace('_',' ')}</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
  
      <div>${detailHtml}</div>
    </div>
    `;
  }
  
  function renderMemory() {
    const b = brainData.brain;
    return `
    <div class="page-header fade-in">
      <div>
        <div class="page-title"><span>//</span> MEMORY LOG</div>
        <div class="page-sub">All conversation memories stored in Pepper's brain</div>
      </div>
    </div>
  
    <div class="section-label fade-in">Chat History [ ${b.chat_history.length} ]</div>
    <div class="memory-area fade-in">
      ${b.chat_history.length === 0
        ? `<div class="empty-state"><div class="es-icon">💤</div><div>No memories yet.</div></div>`
        : b.chat_history.map((c, i) => `
          <div class="memory-card">
            <div class="mc-top">
              <div style="display:flex; align-items:center; gap:8px">
                <span style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted)">#${String(i).padStart(3,'0')}</span>
                <span class="emotion-tag ${emotionClass(c.emotion)}">${c.emotion}</span>
              </div>
              <div class="rating-stars">${stars(c.rating)}</div>
            </div>
            <div class="memory-summary">${c.summary}</div>
            <div class="memory-idx">CHAT_HISTORY[${i}] · rating: ${c.rating}/5</div>
          </div>
        `).join('')
      }
    </div>
  
    <div class="section-label fade-in" style="margin-top: 8px">Long-term Memories [ ${b.memories.length} ]</div>
    <div class="empty-state fade-in" style="background: var(--surface); border: 1px solid var(--border); border-radius: 12px;">
      <div class="es-icon">🧠</div>
      <div>No long-term memories stored yet.</div>
      <div style="font-size: 11px; color: var(--muted); margin-top: 6px">brain.memories[ ] is currently empty</div>
    </div>
    `;
  }
  
  function renderAssignments() {
    return `
    <div class="page-header fade-in">
      <div>
        <div class="page-title"><span>//</span> ASSIGNMENTS</div>
        <div class="page-sub">Pulled from Google Classroom</div>
      </div>
      <button class="btn" onclick="alert('Google Classroom integration coming soon.')">⟳ Sync Classroom</button>
    </div>
  
    <div class="panel fade-in">
      <div class="panel-body">
        <div class="empty-state">
          <div class="es-icon">📚</div>
          <div>No assignments loaded.</div>
          <div style="font-size: 12px; color: var(--muted); margin-top: 8px">
            Connect your Google Classroom account to pull student_assignments into the brain.
          </div>
          <button class="btn" style="margin-top: 16px" onclick="alert('Google Classroom OAuth coming soon.')">Connect Classroom</button>
        </div>
      </div>
    </div>
    `;
  }
  
  function renderPeriods() {
    const periods = brainData.brain.classes.students;
    return `
    <div class="page-header fade-in">
      <div>
        <div class="page-title"><span>//</span> PERIODS</div>
        <div class="page-sub">Class period breakdown</div>
      </div>
    </div>
  
    ${periods.map(periodObj => Object.entries(periodObj).map(([period, names]) => `
      <div class="panel fade-in" style="margin-bottom: 16px">
        <div class="panel-header">
          <div class="panel-title">${period.replace('_',' ').toUpperCase()}</div>
          <span class="period-badge">${names.length} students</span>
        </div>
        <div class="panel-body">
          <div class="student-list">
          ${names.map(stu => {
            const fullName = `${stu[0]} ${stu[1]}`.trim();
            return `
              <div class="student-item" onclick="selectStudent('${fullName}', '${period}')">
                <div class="avatar" style="background: ${avatarColor(fullName)}">${initials(fullName)}</div>
                <div class="student-name" style="text-transform: capitalize">${fullName}</div>
              </div>
            `;
        }).join('')}
          </div>
        </div>
      </div>
    `).join('')).join('')}
    `;
  }
  
  function renderImport() {
    return `
    <div class="page-header fade-in">
      <div>
        <div class="page-title"><span>//</span> IMPORT BRAIN</div>
        <div class="page-sub">Load a brain.json file to update the dashboard</div>
      </div>
    </div>
  
    <div class="panel fade-in">
      <div class="panel-body">
        <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
          <div style="font-size: 28px; margin-bottom: 8px">🧠</div>
          <p><strong>Click to upload</strong> brain.json</p>
          <p style="margin-top: 4px">Drag and drop also supported</p>
        </div>
        <input type="file" id="fileInput" accept=".json" onchange="loadBrainFile(event)">
        <div style="font-size: 12px; color: var(--muted2)">
          Current brain: <span style="font-family: 'Space Mono', monospace; color: var(--accent)">${brainData.brain.name}</span>
          &nbsp;·&nbsp; ID: <span style="font-family: 'Space Mono', monospace; font-size: 10px; color: var(--muted2)">${brainData.id}</span>
        </div>
      </div>
    </div>
    `;
  }
  
  // ──────────────────────────────────────────────
  // Actions
  // ──────────────────────────────────────────────
  function selectStudent(name, period) {
    selectedStudent = { name, period };
    if (currentPage !== 'students') currentPage = 'students';
    render();
  }
  
  function loadBrainFile(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      try {
        const parsed = JSON.parse(ev.target.result);
        if (parsed.brain) {
          brainData = parsed;
          document.getElementById('instanceId').textContent = 'ID: ' + brainData.id.slice(0,8) + '…';
          setPage('brain');
        } else {
          alert('Invalid brain.json format — missing "brain" key.');
        }
      } catch {
        alert('Failed to parse JSON.');
      }
    };
    reader.readAsText(file);
  }
  
  // ──────────────────────────────────────────────
  // Render
  // ──────────────────────────────────────────────
  function render() {

    if (!brainData) return; 

    const el = document.getElementById('mainContent');
    const pages = {
        brain: renderBrain,
        students: renderStudents,
        memory: renderMemory,
        assignments: renderAssignments,
        periods: renderPeriods,
        import: renderImport
    };
    el.innerHTML = (pages[currentPage] || renderBrain)();
}
  


export function print(thing="\n"){
    console.log(thing);
}
window.selectStudent = selectStudent;
window.setPage = setPage;
window.loadBrainFile = loadBrainFile;
async function initApp() {
    const data = await get_json(); // Wait for the real data
    if (data) {
        brainData = data;
        // Now it's safe to set the ID and render
        // document.getElementById('instanceId').textContent = 'ID: ' + brainData.id.slice(0,8) + '…';
        // render(); 
    } else {
        document.getElementById('mainContent').innerHTML = `
            <div class="empty-state">Failed to connect to Pepper's Brain. Is the backend running?</div>
        `;
    }
}


document.addEventListener("DOMContentLoaded", ()=>{

    initApp();
    const pages = document.querySelectorAll('.nav-item');
    pages.forEach((e)=>{
        e.addEventListener("click", ()=>{
            print(e);
            setPage(e.dataset.role);
        })
    })
})
