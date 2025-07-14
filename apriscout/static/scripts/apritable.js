const allPokemon = JSON.parse(document.getElementById("pokemon-data").dataset.pokemon);
const searchInput = document.getElementById("pokemon_search");
const suggestionsList = document.getElementById("suggestions");
const pokemonIdInput = document.getElementById("pokemon_id");

let currentFocus = -1;

function closeSuggestions() {
  suggestionsList.innerHTML = "";
  currentFocus = -1;
}

function highlightSuggestion(index) {
  const items = suggestionsList.getElementsByClassName("suggestion-item");
  if (!items) return;
  // Remove existing highlights
  for (const item of items) {
    item.classList.remove("suggestion-active");
  }
  if (index >= 0 && index < items.length) {
    items[index].classList.add("suggestion-active");
    // Scroll into view if needed
    items[index].scrollIntoView({ block: "nearest" });
  }
}

searchInput.addEventListener("input", function () {
  const query = this.value.toLowerCase();
  suggestionsList.innerHTML = "";
  pokemonIdInput.value = "";
  currentFocus = -1;
  if (!query) return;

  const matches = allPokemon.filter(p => p.name.toLowerCase().includes(query)).slice(0, 10);

  for (const match of matches) {
    const li = document.createElement("li");
    li.textContent = match.name;
    li.dataset.id = match.id;
    li.className = "suggestion-item";
    li.addEventListener("click", () => {
      searchInput.value = match.name;
      pokemonIdInput.value = match.id;
      closeSuggestions();
    });
    suggestionsList.appendChild(li);
  }
});

searchInput.addEventListener("keydown", function(e) {
  const items = suggestionsList.getElementsByClassName("suggestion-item");
  if (!items.length) return;

  if (e.key === "ArrowDown") {
    currentFocus++;
    if (currentFocus >= items.length) currentFocus = 0;
    highlightSuggestion(currentFocus);
    e.preventDefault();
  } else if (e.key === "ArrowUp") {
    currentFocus--;
    if (currentFocus < 0) currentFocus = items.length - 1;
    highlightSuggestion(currentFocus);
    e.preventDefault();
  } else if (e.key === "Enter") {
    e.preventDefault();
    if (currentFocus > -1) {
      items[currentFocus].click();
      currentFocus = -1;
    }
  }
});

document.addEventListener("click", function (e) {
  if (!e.target.closest("#pokemon_search") && !e.target.closest("#suggestions")) {
    closeSuggestions();
  }
});
