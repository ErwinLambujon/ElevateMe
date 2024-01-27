document.addEventListener('DOMContentLoaded', function () {
    // Function to get CSRF token
    function getCSRFToken() {
        let csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            return csrfToken.content;
        }
        console.error('CSRF Token not found in the meta tag.');
        return null;
    }

    function displayFiveHMWs(data) {
        var hmwContainer = document.querySelector(".generatedHMW-container");

        hmwContainer.innerHTML = '';

        var csrfToken = getCSRFToken();

        var checkboxes = [];


        if (data.fiveHMWs) {
            var formElement = document.createElement('form');
            formElement.action = "/generate-elevator-pitch/";
            formElement.method = "post";
            formElement.id = "form";

            var csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            formElement.appendChild(csrfInput);

            let whysID = 0;
            data.fiveHMWs.forEach(function (item) {

                var hmwCardDiv = document.createElement('div');
                hmwCardDiv.classList.add('hmwCards');
                hmwCardDiv.id = whysID;

                var checkboxInput = document.createElement('input');
                checkboxInput.type = 'checkbox';
                checkboxInput.classList.add('checkbox');
                checkboxInput.name = 'checkbox_group';
                checkboxInput.value = item.statement;
                checkboxes.push(checkboxInput)

                var cardTextDiv = document.createElement('div');
                cardTextDiv.classList.add('card-text');
                cardTextDiv.contentEditable = true;
                cardTextDiv.textContent = item.statement;

                cardTextDiv.addEventListener('input', function () {
                    checkboxInput.value = cardTextDiv.textContent;
                });

                hmwCardDiv.appendChild(checkboxInput);
                hmwCardDiv.appendChild(cardTextDiv);

                formElement.appendChild(hmwCardDiv);
                whysID++;
            });

            let genHmwButtonContainer = document.createElement('div');
            genHmwButtonContainer.classList.add('genHmwButton-container');

            var generateElevatorbutton = document.createElement('button');
            generateElevatorbutton.type = 'submit';
            generateElevatorbutton.name = "checkbox_group"
            generateElevatorbutton.classList.add('generateElevatorPitch-button');
            generateElevatorbutton.textContent = 'Elevator Pitch';

            genHmwButtonContainer.appendChild(generateElevatorbutton);
            formElement.appendChild(genHmwButtonContainer);

            hmwContainer.appendChild(formElement);

            var showButton = document.createElement('button');
            showButton.classList.add('showElevator-button'); // Adjust the class name as needed
            showButton.textContent = 'Show Button';

            showButton.addEventListener('click', function () {
                showPopup()
            });

            let showButtonContainer = document.createElement('div');
            showButtonContainer.classList.add('genHmwButton-container'); // Corrected class name here
            showButtonContainer.appendChild(showButton)

            formElement.addEventListener('submit', function (event) {
                if (!checkboxes.some(checkbox => checkbox.checked)) {
                    event.preventDefault();
                    alert('Please select at least one checkbox.');
                }
            });

            hmwContainer.appendChild(showButtonContainer);
        }
    }

    function fetchAndPopulateData(value) {
        var csrfToken = getCSRFToken();

        $.ajax({
            url: `/generated-5-hmws/${value}/`,
            type: 'post',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data)
                displayFiveHMWs(data);

                sessionStorage.setItem('fiveHMWsData', JSON.stringify(data));
            },
            error: function (error) {
                console.error('Error fetching data:', error);
            }
        });
    }

    var generateHMWsButton = document.querySelector('.generateWhys-Button');
    generateHMWsButton.addEventListener('click', function () {
        var contextValue = generateHMWsButton.getAttribute('data-context');
        fetchAndPopulateData(contextValue);
    });

    var savedData = sessionStorage.getItem('fiveHMWsData');
    if (savedData) {
        displayFiveHMWs(JSON.parse(savedData));
    }

    function showPopup() {
        var popupContainer = document.getElementById('popupContainer');
        popupContainer.style.display = 'block';
    }

    var close_button = document.getElementById('closeButton')
    close_button.addEventListener('click', function () {
        popupContainer.style.display = 'none';
    })

});

document.addEventListener('DOMContentLoaded', function () {
    var showHistoryButton = document.querySelector('.showHistory-button');
    var showHistoryPopup = document.getElementById('showHistoryWhys');
    var closePopupButton = document.getElementById('closePopup');

    function getCSRFToken() {
        var csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            console.log('CSRF Token:', csrfToken.content);
            return csrfToken.content;
        }
        console.error('CSRF Token not found in the meta tag.');
        return null;
    }
    function getSelectedAndWhys() {
        var csrfToken = getCSRFToken();

        $.ajax({
            url: `/get-problem-statemen-and-whys/`,
            type: 'post',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                displayProblemStatementAndWhys(data);
                },
            error: function (error) {
                console.error('Error fetching data:', error);
            }
        });
    }

    function displayProblemStatementAndWhys(data) {
        var showHistoryWhysContainer = document.getElementById('showHistoryWhys');
        showHistoryWhysContainer.className = 'popup'

        if(data.ranked_ps && data.fiveWhys) {
            showHistoryWhysContainer.innerHTML = '';

            var h1 = document.createElement('h1');
            h1.textContent = 'Potential Root Problem History';
            showHistoryWhysContainer.appendChild(h1);

            var selectedProbStatement = document.createElement('div');
            selectedProbStatement.className = 'selectedProbStatement';
            showHistoryWhysContainer.appendChild(selectedProbStatement)

            var h2Selected = document.createElement('h2');
            h2Selected.textContent = 'Selected Problem Statement';
            selectedProbStatement.appendChild(h2Selected);

            var textareaSelected = document.createElement('p');
            textareaSelected.id = 'selectedField1';
            textareaSelected.name = 'field1';
            textareaSelected.placeholder = data.ranked_ps;
            textareaSelected.readOnly = true;
            textareaSelected.textContent = data.ranked_ps;
            selectedProbStatement.appendChild(textareaSelected);

            var whyHistory = document.createElement('div');
            whyHistory.className = 'whyHistory'
            showHistoryWhysContainer.appendChild(whyHistory)

            var h2Why = document.createElement('h2');
            h2Why.textContent = 'Why’s Statement';
            whyHistory.appendChild(h2Why)

            data.fiveWhys.forEach(function (item) {
                console.log(item)
                var whysTextArea = document.createElement('p');
                whysTextArea.id = 'field2';
                whysTextArea.name = 'field2';
                whysTextArea.placeholder = item;
                whysTextArea.readOnly = true;
                whysTextArea.textContent = item;
                whyHistory .appendChild(whysTextArea);
            })

            var closeButtondiv = document.createElement('div');
            closeButtondiv.className = "closeButton-container";
            showHistoryWhysContainer.appendChild(closeButtondiv)

            var closeButton = document.createElement('button');
            closeButton.textContent = 'Close';
            closeButton.className = 'button-input';
            closeButton.id = "close"
            closeButton.type = "button";

            closeButton.addEventListener('click', function () {
                showHistoryWhysContainer.style.display = "none";
            })

            closeButtondiv.appendChild(closeButton)
        }
    }

    showHistoryButton.addEventListener('click', function () {
        getSelectedAndWhys()
        showHistoryPopup.style.display = 'block';
    });

    closePopupButton.addEventListener('click', function () {
        showHistoryPopup.style.display = 'none';
    });
});

function closePopup() {
    var popup = document.getElementById('showHistoryWhys');
    popup.style.display = 'none';
}

