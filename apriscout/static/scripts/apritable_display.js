document.addEventListener('DOMContentLoaded', () => {
  const defaultButton = document.querySelector('.category-button[data-category="all"]');
  if (defaultButton) defaultButton.click();
});

document.querySelectorAll('.category-button').forEach(button => {
  button.addEventListener('click', () => {

    const category = button.dataset.category;

    document.querySelectorAll('tbody tr').forEach(row => {
      const categories = row.dataset.categories ? row.dataset.categories.split(',') : [];

      if (category === 'all' || categories.includes(category)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });

    // Highlight active button
    document.querySelectorAll('.category-button').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
  });
});
