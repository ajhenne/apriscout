// clickable apriball data
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("div-table-ball")) {
        e.target.classList.toggle("uncollected");
    }
})

// save apriball states
document.getElementById("apritable-save").addEventListener("click", () => {
    const updates = [];
    document.querySelectorAll(".div-table-ball").forEach(img => {
        if (img.dataset.pokemonId) {
            updates.push({
                pokemon_id: img.dataset.pokemonId,
                ball: img.dataset.ball,
                collected: !img.classList.contains("uncollected")
            });
        }
    });

    fetch(window.location.pathname + "/update_collection", {
        method: "POST",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify({ updates }),
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
})

// collect apriballs when adding pokemon
document.querySelector(".add-aprimon-form").addEventListener("submit", (e) => {
    const selectedBalls = [];
    document.querySelectorAll(".div-add-cell img").forEach(img => {
        if(!img.classList.contains("uncollected")) {
            selectedBalls.push(img.dataset.ball);
        }
    });

    hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.id = "selected_balls";
    hidden.name = "balls";
    hidden.value = JSON.stringify(selectedBalls);
    e.target.appendChild(hidden);
});
