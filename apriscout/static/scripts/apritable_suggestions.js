const allPokemon = JSON.parse(document.getElementById("pokemon-data").textContent);
const input = document.getElementById("add-pokemon-search");
const suggestions = document.getElementById("add-pokemon-suggestions");
const hiddenIdInput = document.getElementById("pokemon_id");

let currentFocus = -1;


function closeSuggestions() {
  suggestions.innerHTML = "";
  suggestions.classList.remove("show");
  currentFocus = -1;
}


input.addEventListener("input", () => {
  const query = input.value.toLowerCase();
  closeSuggestions();

  if (!query) return;

  const matches = allPokemon
    .filter(p => p.name.toLowerCase().includes(query))
    .slice(0, 8);

  if (matches.length === 0) {
    suggestions.classList.remove("show");
    return;
  }

  matches.forEach(p => {
    const li = document.createElement("li");
    const pokemonName = p.name.charAt(0).toUpperCase() + p.name.slice(1)
    li.innerHTML = `<img src="/static/${p.sprite}" alt="${pokemonName}"> ${pokemonName}`;
    li.addEventListener("click", () => {
      input.value = pokemonName;
      hiddenIdInput.value = p.id;
      closeSuggestions();
    });
    suggestions.appendChild(li);
  });

  suggestions.classList.add("show");
});


input.addEventListener("keydown", (e) => {
  const items = suggestions.querySelectorAll("li");
  if (!items.length) return;

  if (e.key === "ArrowDown") {
    currentFocus = (currentFocus + 1) % items.length;
    items.forEach(i => i.classList.remove("active"));
    items[currentFocus].classList.add("active");
    e.preventDefault();
  } else if (e.key === "ArrowUp") {
    currentFocus = (currentFocus - 1 + items.length) % items.length;
    items.forEach(i => i.classList.remove("active"));
    items[currentFocus].classList.add("active");
    e.preventDefault();
  } else if (e.key === "Enter") {
    e.preventDefault();
    if (currentFocus >= 0 && currentFocus < items.length) {
      items[currentFocus].click();
    }
  }
});

document.addEventListener("click", (e) => {
  if (!e.target.closest("#pokemon-search") && !e.target.closest("#suggestions")) {
    closeSuggestions();
  }
});
