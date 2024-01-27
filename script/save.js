let cardCounter = 1;

function deleteCard(containerId, cardId) {
    const cardElement = document.getElementById(containerId).querySelector('#' + cardId);
    if (cardElement) {
        cardElement.remove();
    }
}

function createCard(containerId, text) {
    // Increment the cardCounter for a unique ID
    const cardId = 'card' + cardCounter++;

    // Create card elements
    const card = document.createElement("div");
    card.className = "card";
    card.id = cardId;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "checkbox";

    const cardText = document.createElement("div");
    cardText.className = "card-text";
    cardText.contentEditable = true;

    // Set text content only if the 'text' parameter is not empty
    if (text.trim() !== "") {
        cardText.textContent = text;
    }

    // Create a container div for buttons
    const buttonContainer = document.createElement("div");
    buttonContainer.className = "button-container";

    const editButton = document.createElement("button");
    editButton.className = "edit-button";
    editButton.textContent = "Edit";
    
    // Set a data attribute to store the cardId
    editButton.dataset.cardId = cardId;
    editButton.onclick = function () {
        showEditCardModal(containerId, cardId);
    };

    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.textContent = "Delete";
    // Set a data attribute to store the cardId
    deleteButton.dataset.cardId = cardId;
    deleteButton.onclick = function () {
        deleteCard(containerId, cardId);
    };

    // Append elements to the card
    card.appendChild(checkbox);
    card.appendChild(cardText);
    card.appendChild(editButton);
    card.appendChild(deleteButton);

    // Append the card to the cards container
    const cardsContainer = document.getElementById(containerId);
    cardsContainer.appendChild(card);
}


function editCard(containerId, cardId) {
    // Get the current card text
    const currentText = document.getElementById(cardId).getElementsByClassName('card-text')[0].innerText;

    // Set the initial value of the modal input
    document.getElementById('editCardText').value = currentText;

    // Show the edit card modal
    document.getElementById('editCardModal').style.display = 'block';
}

function closeEditCardModal() {
  
    document.getElementById('editCardModal').style.display = 'none';
}

function confirmEditCard() {
    // Get the edited text from the input field
    const editedText = document.getElementById('editCardText').value;

    // Update the card text with the edited text
    const containerId = document.getElementById('editCardModal').dataset.containerId;
    const cardId = document.getElementById('editCardModal').dataset.cardId;
    const cardTextElement = document.getElementById(containerId).querySelector('#' + cardId + ' .card-text');
    
    if (cardTextElement) {
        cardTextElement.innerText = editedText;
    }

    // Server Logic, Update it here?

    closeEditCardModal();
}
function getCurrentCardText(containerId, cardId) {
    const cardTextElement = document.getElementById(containerId).querySelector('#' + cardId + ' .card-text');
    return cardTextElement ? cardTextElement.innerText : '';
}

function showEditCardModal(containerId, cardId) {
    const modal = document.getElementById('editCardModal');
    modal.style.display = 'block';
    modal.dataset.containerId = containerId;
    modal.dataset.cardId = cardId;  
    const currentCardText = getCurrentCardText(containerId, cardId);
    document.getElementById('editCardText').value = currentCardText;
}

/* function getCurrentCardText() {
    
    const containerId = document.getElementById('editCardModal').dataset.containerId;
    const firstCardText = document.getElementById(containerId).getElementsByClassName('card-text')[0].innerText;
    return firstCardText;
}  */


function closeAddCardModal() {
    const modal = document.getElementById('addCardModal');
    modal.style.display = 'none';
}

function confirmAddCard() {
    const modal = document.getElementById('addCardModal');
    const containerId = modal.dataset.containerId;
    const newCardText = document.getElementById('newCardText').value;

    // Add the new card
    createCard(containerId,  newCardText);

    // Close the modal
    closeAddCardModal();
}

function showAddCardModal(containerId) {
    const modal = document.getElementById('addCardModal');
    modal.style.display = 'block';
    modal.dataset.containerId = containerId;

    // Reset the value of the textarea to trigger the placeholder
    document.getElementById('newCardText').value = '';

    // If you still want to set a placeholder dynamically, you can do it here
    // document.getElementById('newCardText').placeholder = "Enter Problem Statement Here";
}

//show history popup
    function closePopup() {
        document.getElementById('showHistoryPopupVenn3').style.display = 'none';
        document.getElementById('showHistoryPopupVenn2').style.display = 'none';
    }






























// Additional functions or modifications can be added as needed
/* mogana nani ang mga functions but need siya unique IDs para eh pasapasa pang edit og pang delete. Let me know if naa sayup
*/
/* function createCard(containerId, text) {
    // Increment the cardCounter for a unique ID
    const cardId = 'card' + cardCounter++;

    // Create card elements
    const card = document.createElement("div");
    card.className = "card";
    card.id = cardId;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "checkbox";

    const cardText = document.createElement("div");
    cardText.className = "card-text";
    cardText.contentEditable = true;
    cardText.textContent = text;

    const editButton = document.createElement("button");
    editButton.className = "edit-button";
    editButton.textContent = "Edit";
    // Set a data attribute to store the cardId
    editButton.dataset.cardId = cardId;
    editButton.onclick = function () {
        showEditCardModal(containerId, cardId);
    };

    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.textContent = "Delete";
    // Set a data attribute to store the cardId
    deleteButton.dataset.cardId = cardId;
    deleteButton.onclick = function () {
        deleteCard(containerId, cardId);
    };

    // Append elements to the card
    card.appendChild(checkbox);
    card.appendChild(cardText);
    card.appendChild(editButton);
    card.appendChild(deleteButton);

    // Append the card to the cards container
    const cardsContainer = document.getElementById(containerId);
    cardsContainer.appendChild(card);
}
 */