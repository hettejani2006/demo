let glossLink = "https://raw.githubusercontent.com/Abrar822/Json.A/refs/heads/main/gloss_Cosmic_Tales.json";
let data = [];

async function fetcher() {
  let response = await fetch(glossLink);
  data = await response.json();
  data = data.glossary;
}

function createCard(card, idx) {
  let term = data[idx].term;
  let definition = data[idx].definition;

  card.innerHTML = `
    <div class="term">${term} <i class="fa-solid fa-chevron-down"></i></div>
    <div class="defin">${definition}</div>
  `;
}

function glossaryGenerator() {
  const container = document.querySelector(".glossaryContainer .container");

  data.forEach((_, i) => {
    let card = document.createElement("div");
    card.classList.add("card");
    container.append(card);
    createCard(card, i);
  });

  const terms = document.querySelectorAll(".term");
  terms.forEach(term => {
    term.addEventListener("click", () => {
      const defin = term.nextElementSibling;
      const icon = term.querySelector("i");

      // Close others
      document.querySelectorAll(".defin").forEach(d => {
        if (d !== defin) {
          d.classList.remove("toggle");
          d.previousElementSibling.querySelector("i").classList.remove("rotate");
        }
      });

      // Toggle this one
      defin.classList.toggle("toggle");
      icon.classList.toggle("rotate");
    });
  });
}

async function executor() {
  await fetcher();
  glossaryGenerator();
}
executor();