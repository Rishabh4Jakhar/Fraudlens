function filterFeatures(type) {
  const cards = document.querySelectorAll('.features__card');
  const buttons = document.querySelectorAll('.features-page__types-btn');

  buttons.forEach(btn => btn.classList.remove('active'));
  
  const activeBtn = [...buttons].find(btn => btn.textContent.toLowerCase().includes(type));
  if (activeBtn) activeBtn.classList.add('active');

  cards.forEach(card => {
    const title = card.querySelector('h4').textContent.toLowerCase();

    if (type === 'all') {
      card.style.display = 'flex';
      card.classList.remove('hidden');
      card.classList.remove('active-card');
    } else if (title.includes(type)) {
      card.style.display = 'flex';
      card.classList.remove('hidden');
      card.classList.add('active-card');
    } else {
      card.style.display = 'none';
      card.classList.remove('active-card');
    }
  });
}
