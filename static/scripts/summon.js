document.addEventListener('DOMContentLoaded', function() {
    const singleSummonButton = document.getElementById('single-summon-btn');
    const multiSummonButton = document.getElementById('multi-summon-btn');

    // Look for a button click
    singleSummonButton.addEventListener('click', function() {
        summonCharacter(false, singleSummonButton);  // false to indicate single summon
    });
    multiSummonButton.addEventListener('click', function() {
        summonCharacter(true, multiSummonButton);  // true to indicate a multi summon
    });

    // Disable and Enable button functions
    function disableButton(button) {
        button.disabled = true;
    }
    function enableButton(button) {
        button.disabled = false;
    }

    // Display randomly generated character within summon container, uses a route in app_blueprint
    function summonCharacter(isMultiSummon, summonButton) {
        const tableName = summonButton.getAttribute('data-table');
        const summonResultContainer = document.querySelector('.summons-pulled-container');
        const singleButton = document.getElementById('single-summon-btn');
        const multiButton = document.getElementById('multi-summon-btn');

        // Disable summon buttons (to prevent spamming)
        disableButton(singleButton);
        disableButton(multiButton);

        // Calls summon function (set as route in app_blueprint)
        fetch('/summon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tableName: tableName, multiSummon: isMultiSummon })  // also sends whether it is multi or not
        })
   
        // Deals with characters returned and displays in specified container
        .then(response => response.json())
        .then(data => {
            summonResultContainer.innerHTML = '';  // clear container
            data.characters.forEach(character => {
               
                // Identify class of summon for borders & potential animations (SSR)
                var characterClass = 'standard-pull';
                if (character.details.includes('SSR')) {
                    characterClass = 'ssr-pull'
                }
                else if (character.details.includes('SR'))
                {
                    characterClass = 'sr-pull'
                }
                else if (character.details.includes('R'))
                {
                    characterClass = 'r-pull'
                }

                // Place into summon container
                const img = document.createElement('img');  // create img element for character
                img.src = `/static/images/characters/${character.image_name}`;
                img.alt = character.name;
                img.classList.add(characterClass)  // apply character class
                summonResultContainer.appendChild(img);  // append character to container
            });
        })

        // Display errors in console
        .catch(error => console.error('Error:', error))

        // Enable summon buttons again
        .finally(() => {
            enableButton(singleButton);
            enableButton(multiButton);
        });
    }
});