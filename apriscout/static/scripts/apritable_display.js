// Default category.
document.addEventListener('DOMContentLoaded', () => {
  const defaultButton = document.querySelector('.category-button[data-category="all"]');
  if (defaultButton) defaultButton.click();
});


// Category selection.
document.querySelectorAll('.category-button').forEach(button => {
  button.addEventListener('click', () => {

    const category = button.dataset.category;

    document.querySelectorAll('.div-table-row').forEach(row => {
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

// Add category.
document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-category-button");
  const inputWrapper = document.getElementById("new-category-input-wrapper");
  const inputField = document.getElementById("new-category-input");
  const confirmBtn = document.getElementById("confirm-new-category");

  addBtn.addEventListener("click", () => {
    addBtn.style.display = "none";
    inputWrapper.style.display = "inline-flex";
    inputField.focus();
  });

  const username = document.body.dataset.username;

  const submitCategory = () => {
    const name = inputField.value.trim();
    if (!name) return;
    fetch(`/${username}/add_category`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name })
    }).then(res => {
      if (res.ok) {
        location.reload();
      } else {
        alert("Failed to create category.");
      }
    });
  };

  confirmBtn.addEventListener("click", submitCategory);
  inputField.addEventListener("keypress", (e) => {
    if (e.key === "Enter") submitCategory();
  });
});
