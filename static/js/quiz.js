let currentQuestion = -1;
let correctAnswers = 0;

function startGame() {
    currentQuestion = -1;
    correctAnswers = 0;
    document.getElementById('quiz-title').style.display = 'block';
    document.getElementById('answer-count').style.display = 'block';
    document.getElementById('question').style.display = 'block';
    document.getElementById('capital-input').disabled = false;
    document.getElementById('answer-count').innerText = 'Correct Answers: 0';
    document.getElementById('quiz-title').innerText = 'Guess the Capitals';
    document.querySelector('button[onclick="startGame()"]').style.display = 'none';
    document.querySelector('button[onclick="endGame()"]').style.display = 'block';
    nextQuestion();
}
function calculateScore() {
    // Assuming correctAnswers is a variable keeping track of correct answers
    return correctAnswers;
}


function endGame() {
    currentQuestion = countries.length;
    displayQuestion();
    const score = calculateScore();  // Calculate the actual score
        document.getElementById('scoreValue').innerText = score;
        $('#scoreModal').modal('show');  // Show the modal with the score
}



function displayQuestion() {
    if (currentQuestion < countries.length) {
        const country = countries[currentQuestion];
        document.getElementById('country-name').innerText = 'Country: ' + country.name;
    } else {
        document.getElementById('country-name').innerText = 'Quiz completed!';
        document.getElementById('capital-input').disabled = true;
        document.getElementById('answer-count').innerText = 'Correct Answers: ' + correctAnswers;
        // Display the score modal
        $('#scoreModal').modal('show');
        // Set the score value in the modal
        document.getElementById('scoreValue').innerText = correctAnswers;
    }
}

function submitAnswer() {
    const userAnswer = document.getElementById('capital-input').value.toLowerCase();
    const country = countries[currentQuestion];
    const correctAnswer = country.capital.toLowerCase();
    if (userAnswer === correctAnswer) {
        correctAnswers++;
        document.getElementById('answer-count').innerText = 'Correct Answers: ' + correctAnswers;
    }
    nextQuestion();
}



function nextQuestion() {
    currentQuestion++;
    if (currentQuestion < countries.length) {
        document.getElementById('capital-input').value = '';
        displayQuestion();
        document.getElementById('submit-button').style.display = 'block';
    } else {
        displayQuestion();
        document.getElementById('submit-button').style.display = 'none';
    }
}

function sendScoreViaEmail() {
    const score = parseInt(document.getElementById('scoreValue').innerText);
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const url = '{% url "save_score" %}';

    const formData = new FormData();
    formData.append('score', score);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Score sent via email successfully!');
        } else {
            alert('Failed to send score via email.');
        }
    })
    .catch(error => console.error('Error:', error));
}

