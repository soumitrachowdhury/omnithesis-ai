const API_ENDPOINT = '/generate-report';
const STATUS_ENDPOINT = (jobId) => `/report-status/${jobId}`;
const STAGE_KEYS = ['research', 'domain', 'curation', 'feasibility', 'writing', 'editing'];
const STAGE_LABELS = {
  research: 'Research',
  domain: 'Domain Analysis',
  curation: 'Curation',
  feasibility: 'Feasibility',
  writing: 'Writing',
  editing: 'Editing',
};

const STAGE_HELPER_TEXT = {
  research: [
    'Searching ArXiv...',
    'Searching Semantic Scholar...',
    'Finding candidate papers...',
    'Filtering for relevance...',
  ],
  domain: [
    'Reading the field overview...',
    'Identifying core concepts...',
    'Summarizing active trends...',
    'Connecting ideas to the topic...',
  ],
  curation: [
    'Ranking by relevance...',
    'Checking paper quality...',
    'Prioritizing stronger sources...',
    'Removing weak matches...',
  ],
  feasibility: [
    'Comparing topic difficulty to your background...',
    'Checking skill gaps...',
    'Drafting learning advice...',
    'Sizing up the research load...',
  ],
  writing: [
    'Composing the report structure...',
    'Synthesizing the research notes...',
    'Drafting the executive summary...',
    'Building the report sections...',
  ],
  editing: [
    'Polishing transitions...',
    'Tightening the language...',
    'Checking flow and readability...',
    'Final pass in progress...',
  ],
};

const form = document.getElementById('report-form');
const topicInput = document.getElementById('research-topic');
const pythonSkillInput = document.getElementById('python-skill');
const mlExperienceInput = document.getElementById('ml-experience');
const generateButton = document.getElementById('generate-button');
const retryButton = document.getElementById('retry-button');
const downloadButton = document.getElementById('download-pdf');
const reportPanel = document.getElementById('report-panel');
const reportOutput = document.getElementById('report-output');
const errorPanel = document.getElementById('error-panel');
const errorMessage = document.getElementById('error-message');
const progressMessage = document.getElementById('progress-message');
const progressTimer = document.getElementById('progress-timer');
const progressSteps = Array.from(document.querySelectorAll('.progress-step'));

const defaultStageStatusTexts = Object.fromEntries(
  progressSteps.map((step) => {
    const stageKey = step.dataset.stage;
    const status = step.querySelector('.progress-step__status');
    return [stageKey, status ? status.textContent.trim() : ''];
  }),
);

let currentJobId = null;
let activeRequest = null;
let pollAbortController = null;
let pollTimeoutId = null;
let reportMarkdown = '';

function setStatusMessage(message) {
  progressMessage.textContent = message;
}

function formatDuration(totalSeconds) {
  const safeSeconds = Math.max(Number(totalSeconds) || 0, 0);
  const minutes = Math.floor(safeSeconds / 60);
  const seconds = safeSeconds % 60;
  return `${minutes}:${String(seconds).padStart(2, '0')}`;
}

function updateTimerDisplay(elapsedSeconds = 0, remainingSeconds = 0) {
  progressTimer.textContent = `Elapsed ${formatDuration(elapsedSeconds)} · Remaining about ${formatDuration(remainingSeconds)}`;
}

function showPanel(panel) {
  panel.classList.remove('is-hidden');
  panel.classList.add('is-visible');
}

function hidePanel(panel) {
  panel.classList.add('is-hidden');
  panel.classList.remove('is-visible');
}

function stopPolling() {
  if (pollTimeoutId) {
    clearTimeout(pollTimeoutId);
    pollTimeoutId = null;
  }

  if (pollAbortController) {
    pollAbortController.abort();
    pollAbortController = null;
  }
}

function resetTracker() {
  progressSteps.forEach((step) => {
    step.classList.remove('is-active', 'is-complete', 'is-pending');
    const stageKey = step.dataset.stage;
    const status = step.querySelector('.progress-step__status');
    if (status) {
      status.textContent = defaultStageStatusTexts[stageKey] || status.textContent;
    }
  });

  setStatusMessage('Waiting for a topic.');
  updateTimerDisplay(0, 0);
}

function setStepStatus(stageKey, message) {
  const step = progressSteps.find((entry) => entry.dataset.stage === stageKey);
  if (!step) {
    return;
  }

  const status = step.querySelector('.progress-step__status');
  if (status && message) {
    status.textContent = message;
  }
}

function getLiveStageMessage(stageKey, elapsedSeconds = 0) {
  const messages = STAGE_HELPER_TEXT[stageKey] || ['Working...'];
  const index = Math.min(Math.floor(Number(elapsedSeconds || 0) / 4), messages.length - 1);
  return messages[index];
}

function renderTrackerFromJob(job) {
  const stageIndex = STAGE_KEYS.indexOf(job.stage);
  const stageState = job.stage_state;
  const isCompleted = job.status === 'completed';
  const currentStageIndex = stageIndex >= 0 ? stageIndex : -1;

  progressSteps.forEach((step, index) => {
    step.classList.remove('is-active', 'is-complete', 'is-pending');

    if (isCompleted || (stageState === 'completed' && index <= currentStageIndex)) {
      step.classList.add('is-complete');
      return;
    }

    if (stageState === 'running' && index === currentStageIndex) {
      step.classList.add('is-active');
      return;
    }

    if (index < currentStageIndex) {
      step.classList.add('is-complete');
      return;
    }

    step.classList.add('is-pending');
  });

  if (stageIndex >= 0) {
    const liveMessage = job.stage_state === 'running'
      ? getLiveStageMessage(job.stage, job.elapsed_seconds)
      : job.message;

    setStepStatus(job.stage, liveMessage);
    if (stageState === 'running') {
      setStatusMessage(`Running ${STAGE_LABELS[job.stage] || job.stage}...`);
    } else if (stageState === 'completed') {
      setStatusMessage(`${STAGE_LABELS[job.stage] || job.stage} complete.`);
    }
  }

  updateTimerDisplay(job.elapsed_seconds, job.estimated_remaining_seconds);

  if (job.status === 'queued') {
    setStatusMessage('Queued. Waiting for the first stage.');
  }

  if (job.status === 'completed') {
    setStatusMessage('Report generation complete.');
    updateTimerDisplay(job.elapsed_seconds, 0);
  }
}

function buildBackgroundSummary() {
  const parts = [];
  const pythonSkill = pythonSkillInput.value.trim();
  const mlExperience = mlExperienceInput.value.trim();

  if (pythonSkill) {
    parts.push(`Python skill level: ${pythonSkill}`);
  }

  if (mlExperience) {
    parts.push(`ML experience: ${mlExperience}`);
  }

  return parts.join('; ');
}

function setLoading(isLoading) {
  generateButton.disabled = isLoading;
  generateButton.textContent = isLoading ? 'Generating...' : 'Generate Report';
  form.querySelectorAll('input, select').forEach((field) => {
    field.disabled = isLoading;
  });
}

function showError(message) {
  errorMessage.textContent = message;
  showPanel(errorPanel);
  hidePanel(reportPanel);
}

function hideError() {
  hidePanel(errorPanel);
}

function renderReport(markdown) {
  reportMarkdown = markdown;
  reportOutput.innerHTML = window.marked.parse(markdown);
  showPanel(reportPanel);
}

async function sleep(ms, signal) {
  return new Promise((resolve, reject) => {
    const timeoutId = window.setTimeout(() => {
      if (signal) {
        signal.removeEventListener('abort', onAbort);
      }
      resolve();
    }, ms);

    function onAbort() {
      clearTimeout(timeoutId);
      reject(new DOMException('Aborted', 'AbortError'));
    }

    if (signal) {
      signal.addEventListener('abort', onAbort, { once: true });
    }
  });
}

async function pollJobStatus(jobId) {
  stopPolling();
  pollAbortController = new AbortController();

  while (currentJobId === jobId) {
    const response = await fetch(STATUS_ENDPOINT(jobId), {
      signal: pollAbortController.signal,
    });

    if (!response.ok) {
      throw new Error(`Status request failed with status ${response.status}.`);
    }

    const job = await response.json();
    renderTrackerFromJob(job);

    if (job.status === 'completed') {
      stopPolling();
      renderReport(job.report || '# No report returned');
      setLoading(false);
      return;
    }

    if (job.status === 'failed') {
      stopPolling();
      showError(job.error ? `The ${job.stage || 'pipeline'} step did not complete. Try generating the report again.` : 'The pipeline did not complete. Try generating the report again.');
      setLoading(false);
      return;
    }

    await sleep(2000, pollAbortController.signal);
  }
}

async function generateReport(event) {
  event.preventDefault();

  const topic = topicInput.value.trim();
  if (!topic) {
    showError('Enter a research topic before generating a report.');
    return;
  }

  hideError();
  hidePanel(reportPanel);
  setLoading(true);
  stopPolling();
  resetTracker();

  const payload = {
    topic,
    python_skill_level: pythonSkillInput.value || null,
    ml_experience: mlExperienceInput.value || null,
    additional_background: buildBackgroundSummary() || null,
  };

  try {
    activeRequest = new AbortController();
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: activeRequest.signal,
    });

    if (!response.ok) {
      let detail = `The report request failed with status ${response.status}.`;
      try {
        const errorData = await response.json();
        detail = errorData?.detail || errorData?.message || detail;
      } catch {
        // Keep the fallback message.
      }
      throw new Error(detail);
    }

    const data = await response.json();
    currentJobId = data.job_id;
    setStatusMessage(data.message || 'Report generation started.');
    updateTimerDisplay(0, 0);
    await pollJobStatus(currentJobId);
  } catch (error) {
    stopPolling();

    const message = error?.name === 'AbortError'
      ? 'The report request was cancelled.'
      : error?.message || 'The pipeline did not complete. Try generating the report again.';

    showError(message);
    setStatusMessage('Waiting for a topic.');
    setLoading(false);
  } finally {
    activeRequest = null;
    currentJobId = null;
  }
}

function retryLastRequest() {
  hideError();
  form.requestSubmit();
}

function printReport() {
  window.print();
}

form.addEventListener('submit', generateReport);
retryButton.addEventListener('click', retryLastRequest);
downloadButton.addEventListener('click', printReport);

resetTracker();
