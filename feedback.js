/* ============================================================
   Feedback button & modal — feedback.js
   ============================================================ */

function initFeedback({ feedbackBtn, feedbackModal, feedbackClose, feedbackForm, feedbackThanks }) {
  let selectedRating = null;

  function openModal() {
    feedbackModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    feedbackModal.classList.remove('active');
    document.body.style.overflow = '';
    setTimeout(() => {
      feedbackForm.hidden = false;
      feedbackThanks.hidden = true;
      feedbackForm.reset();
      selectedRating = null;
      feedbackModal.querySelectorAll('.rating-btn').forEach(b => b.classList.remove('selected'));
    }, 300);
  }

  function selectRating(value) {
    selectedRating = value;
  }

  function getSelectedRating() {
    return selectedRating;
  }

  function submitFeedback(e) {
    if (e) e.preventDefault();
    feedbackForm.hidden = true;
    feedbackThanks.hidden = false;
    setTimeout(closeModal, 2000);
  }

  feedbackBtn.addEventListener('click', openModal);
  feedbackClose.addEventListener('click', closeModal);

  feedbackModal.addEventListener('click', (e) => {
    if (e.target === feedbackModal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && feedbackModal.classList.contains('active')) closeModal();
  });

  feedbackModal.querySelectorAll('.rating-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      selectRating(parseInt(btn.dataset.value, 10));
      feedbackModal.querySelectorAll('.rating-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    });
  });

  feedbackForm.addEventListener('submit', submitFeedback);

  return { openModal, closeModal, selectRating, getSelectedRating, submitFeedback };
}

if (typeof module !== 'undefined') {
  module.exports = { initFeedback };
}
