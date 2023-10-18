let currentQuestion = -1;
let correctAnswers = 0;


//////////////////// Function to start the game ////////////////////

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

///////////// Function to calculate the score //////////////////////////
function calculateScore() {
    return correctAnswers;
}

// End game 
function endGame() {
    currentQuestion = countries.length;
    displayQuestion();
    const score = calculateScore();  
        document.getElementById('scoreValue').innerText = score;
        $('#scoreModal').modal('show');
}



function displayQuestion() {
    if (currentQuestion < countries.length) {
        const country = countries[currentQuestion];
        document.getElementById('country-name').innerText = 'What is the capital of the country: ' + country.name;
    } else {
        document.getElementById('country-name').innerText = 'Quiz completed!';
        document.getElementById('capital-input').disabled = true;
        document.getElementById('answer-count').innerText = 'Correct Answers: ' + correctAnswers;
        $('#scoreModal').modal('show');
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
    } else {
        const wrongAnswerModal = new bootstrap.Modal(document.getElementById('wrongAnswerModal'));
        document.getElementById('correctAnswer').innerText = country.capital;
        wrongAnswerModal.show();
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


