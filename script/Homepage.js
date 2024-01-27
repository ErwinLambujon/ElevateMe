document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll('.buttons input[type="button"]');
    buttons.forEach((btn) => {
        if (btn.value === "Home") {
            btn.classList.add("button-clicked");
        }
    });

    function handleButtonClick() {
        buttons.forEach((btn) => {
            btn.addEventListener("click", function () {
                buttons.forEach((b) => {
                    if (b !== this) {
                        b.classList.remove("button-clicked");
                        b.classList.add("button1");
                    }
                });

                if (!this.classList.contains("button-clicked")) {
                    this.classList.remove("button1");
                    this.classList.add("button-clicked");
                } else {
                    this.classList.remove("button-clicked");
                    this.classList.add("button1");
                }
            });
        });
    }

    handleButtonClick();
});

const popupButton = document.getElementById("pop-up");
const overlay = document.getElementById("overlay");
const popup = document.getElementById("popup");
const closeButton = document.getElementById("closeButton");


popupButton.addEventListener("click", function () {
    overlay.style.display = "block";
    popup.style.display = "block";
});

closeButton.addEventListener("click", function () {
    overlay.style.display = "none";
    popup.style.display = "none";
});

const generateForm = document.getElementById("generate-form");
const saveButton = document.querySelector(".Saving");
const psLine = document.getElementById("ps-form"); // Assuming the ID is 'ps-form'

function toggleDiagram(diagramId) {

    const field3Input = document.getElementById("field3");
    const field3 = document.getElementById("field3_head");
    if (diagramId === "venn-2") {
        field3Input.disabled = true;
        field3Input.hidden = true;
        field3.hidden = true;
    } else if (diagramId === "venn-3") {
        field3Input.disabled = false;
        field3Input.hidden = false;
        field3.hidden = false;
    }
}

