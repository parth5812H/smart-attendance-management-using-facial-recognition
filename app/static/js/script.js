:root {
    --bg: #f5f7ff;
    --panel: #ffffff;
    --primary: #3d5afe;
    --primary-strong: #1f39d7;
    --secondary: #edf1ff;
    --text: #1e2430;
    --muted: #6d7582;
    --success: #1bbf73;
    --danger: #f15156;
    --border: #e2e8f0;
    --shadow: 0 12px 30px rgba(27, 32, 61, 0.08);
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: Arial, sans-serif;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.topbar {
    background: #0f172a;
    color: white;
    padding: 18px 0;
}

.topbar-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.brand {
    font-size: 1.4rem;
    font-weight: 700;
}

nav {
    display: flex;
    gap: 20px;
}

nav a {
    color: white;
    text-decoration: none;
    opacity: 0.9;
}

.main-content {
    padding-top: 32px;
    padding-bottom: 40px;
}

.hero {
    margin-bottom: 24px;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--primary);
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 10px;
}

h1, h2, h3 {
    margin: 0 0 12px;
}

.subtitle {
    color: var(--muted);
    max-width: 640px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
    margin-bottom: 30px;
}

.card {
    background: var(--panel);
    border-radius: 18px;
    padding: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}

.stat-card {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.stat-card span {
    color: var(--muted);
    font-size: 0.9rem;
}

.stat-card strong {
    font-size: 2.2rem;
    color: var(--primary-strong);
}

.table-section {
    margin-top: 28px;
}

.section-header {
    margin-bottom: 18px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    text-align: left;
    padding: 12px 10px;
    border-bottom: 1px solid var(--border);
}

th {
    background: #f8fafc;
}

.form-card {
    max-width: 760px;
    margin: 0 auto;
}

.student-form {
    display: grid;
    gap: 20px;
}

.field-row {
    display: grid;
    gap: 8px;
}

label {
    font-weight: 600;
}

input[type="text"], input[type="file"] {
    width: 100%;
    padding: 12px 14px;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: white;
    font-size: 1rem;
}

.primary-btn, .secondary-btn {
    border: none;
    border-radius: 12px;
    padding: 12px 18px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.primary-btn {
    background: var(--primary);
    color: white;
}

.secondary-btn {
    background: var(--secondary);
    color: var(--primary);
}

.primary-btn:hover, .secondary-btn:hover {
    transform: translateY(-1px);
}

.flash-container {
    margin-bottom: 18px;
}

.flash {
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.flash-success {
    background: rgba(27, 191, 115, 0.12);
    color: #0f766e;
}

.flash-error {
    background: rgba(241, 81, 86, 0.12);
    color: #b91c1c;
}

.camera-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0b1220;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 20px;
}

#video {
    width: 100%;
    max-width: 640px;
    height: auto;
    display: block;
    background: black;
}

.recognition-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}

.result-box {
    padding: 14px 16px;
    border: 1px solid var(--border);
    background: #f8fbff;
    border-radius: 12px;
    color: var(--text);
    min-height: 50px;
}

.result-box.success {
    border-color: rgba(27, 191, 115, 0.5);
    background: rgba(27, 191, 115, 0.08);
    color: #166534;
}

.result-box.error {
    border-color: rgba(241, 81, 86, 0.5);
    background: rgba(241, 81, 86, 0.08);
    color: #991b1b;
}

@media (max-width: 680px) {
    nav {
        gap: 10px;
        font-size: 0.9rem;
    }

    .topbar-inner {
        flex-direction: column;
        gap: 12px;
    }
}
