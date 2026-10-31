// Active Quiz Engine Script
document.addEventListener('DOMContentLoaded', () => {
  const quizContainer = document.getElementById('quiz-engine-container');
  if (!quizContainer) return;

  const attemptId = quizContainer.dataset.attemptId;
  const questionId = quizContainer.dataset.questionId;
  const isPracticeMode = quizContainer.dataset.mode === 'PRACTICE';
  const timeLimitSec = parseInt(quizContainer.dataset.timeLimit || '0', 10);
  const saveUrl = quizContainer.dataset.saveUrl;
  const submitUrl = quizContainer.dataset.submitUrl;
  const csrfToken = quizContainer.dataset.csrf;

  // Track elapsed time
  const timerStorageKey = `quiz_time_elapsed_${attemptId}`;
  let elapsedSec = parseInt(sessionStorage.getItem(timerStorageKey) || '0', 10);

  const timerDisplay = document.getElementById('quiz-timer-display');
  const timerBadge = document.getElementById('quiz-timer-badge');

  let timerInterval = null;

  if (timeLimitSec > 0) {
    // Exam mode countdown
    function updateCountdown() {
      elapsedSec++;
      sessionStorage.setItem(timerStorageKey, elapsedSec);

      const remaining = timeLimitSec - elapsedSec;
      if (remaining <= 0) {
        clearInterval(timerInterval);
        if (timerDisplay) timerDisplay.textContent = '00:00';
        autoSubmitQuiz('Time has expired! Submitting your exam automatically.');
        return;
      }

      const mins = Math.floor(remaining / 60);
      const secs = remaining % 60;
      if (timerDisplay) {
        timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }

      // Visual warning when under 2 minutes
      if (remaining <= 120 && timerBadge) {
        timerBadge.classList.remove('bg-secondary', 'bg-dark');
        timerBadge.classList.add('bg-danger', 'text-white');
      }
    }

    updateCountdown();
    timerInterval = setInterval(updateCountdown, 1000);
  } else {
    // Practice mode elapsed counter
    function updateElapsed() {
      elapsedSec++;
      sessionStorage.setItem(timerStorageKey, elapsedSec);
      const mins = Math.floor(elapsedSec / 60);
      const secs = elapsedSec % 60;
      if (timerDisplay) {
        timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
    }
    updateElapsed();
    timerInterval = setInterval(updateElapsed, 1000);
  }

  // Answer selection
  const options = document.querySelectorAll('.quiz-option');
  options.forEach(opt => {
    opt.addEventListener('click', () => {
      const optionId = opt.dataset.optionId;
      options.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');

      const radio = opt.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;

      // Asynchronous auto-save
      saveAnswerState(optionId, null);
    });
  });

  // Flag for review button
  const flagBtn = document.getElementById('flag-question-btn');
  if (flagBtn) {
    flagBtn.addEventListener('click', () => {
      const isCurrentlyFlagged = flagBtn.dataset.flagged === 'true';
      const newFlagState = !isCurrentlyFlagged;
      flagBtn.dataset.flagged = newFlagState.toString();

      if (newFlagState) {
        flagBtn.classList.remove('btn-outline-warning');
        flagBtn.classList.add('btn-warning');
        flagBtn.innerHTML = '<i class="bi bi-flag-fill me-1"></i> Flagged for Review';
      } else {
        flagBtn.classList.remove('btn-warning');
        flagBtn.classList.add('btn-outline-warning');
        flagBtn.innerHTML = '<i class="bi bi-flag me-1"></i> Mark for Review';
      }

      saveAnswerState(null, newFlagState);
    });
  }

  // Check Answer Button (Practice Mode)
  const checkAnswerBtn = document.getElementById('practice-check-btn');
  if (checkAnswerBtn) {
    checkAnswerBtn.addEventListener('click', () => {
      const selected = document.querySelector('.quiz-option.selected');
      if (!selected) {
        alert('Please select an option first.');
        return;
      }
      const optionId = selected.dataset.optionId;
      saveAnswerState(optionId, null, true);
    });
  }

  // Submit confirmation handler
  const confirmSubmitBtn = document.getElementById('confirm-final-submit-btn');
  if (confirmSubmitBtn) {
    confirmSubmitBtn.addEventListener('click', () => {
      autoSubmitQuiz();
    });
  }

  function saveAnswerState(optId, isFlagged, triggerExplanation = false) {
    const payload = { question_id: questionId };
    if (optId !== null) payload.option_id = optId;
    if (isFlagged !== null) payload.is_flagged = isFlagged;

    fetch(saveUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      if (data.success && isPracticeMode && (triggerExplanation || data.explanation)) {
        revealPracticeExplanation(data);
      }
      // Update palette button status if present
      const curPalette = document.querySelector(`.palette-btn[data-qid="${questionId}"]`);
      if (curPalette) {
        if (data.is_answered) curPalette.classList.add('answered');
        if (data.is_flagged) curPalette.classList.add('flagged');
        else curPalette.classList.remove('flagged');
      }
    })
    .catch(err => console.error('Auto-save error:', err));
  }

  function revealPracticeExplanation(data) {
    const explanationCard = document.getElementById('practice-explanation-card');
    if (!explanationCard) return;

    options.forEach(opt => {
      const optId = opt.dataset.optionId;
      if (optId == data.correct_option_id) {
        opt.classList.add('correct-reveal');
      } else if (opt.classList.contains('selected') && !data.is_correct) {
        opt.classList.add('incorrect-reveal');
      }
    });

    const expText = document.getElementById('practice-explanation-text');
    if (expText && data.explanation) {
      expText.textContent = data.explanation;
    }
    explanationCard.classList.remove('d-none');
  }

  function autoSubmitQuiz(message) {
    if (message) alert(message);
    sessionStorage.removeItem(timerStorageKey);

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = submitUrl;

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    const timeInput = document.createElement('input');
    timeInput.type = 'hidden';
    timeInput.name = 'time_spent';
    timeInput.value = elapsedSec;
    form.appendChild(timeInput);

    document.body.appendChild(form);
    form.submit();
  }
});
