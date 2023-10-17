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

function endGame() {
    currentQuestion = countries.length;
    displayQuestion();
}

function displayQuestion() {
    if (currentQuestion < countries.length) {
        const country = countries[currentQuestion];
        document.getElementById('country-name').innerText = 'Country: ' + country.name;
    } else {
        document.getElementById('country-name').innerText = 'Quiz completed!';
        document.getElementById('capital-input').disabled = true;
        document.getElementById('answer-count').innerText = 'Correct Answers: ' + correctAnswers;
    }
}

function submitAnswer() {
    const userAnswer = document.getElementById('capital-input').value.toLowerCase();
    const country = countries[currentQuestion];
    const correctAnswer = country.capital.toLowerCase();
    if (userAnswer === correctAnswer) {
        alert('Correct answer! The capital is ' + country.capital);
        correctAnswers++;
        document.getElementById('answer-count').innerText = 'Correct Answers: ' + correctAnswers;
    } else {
        alert('Incorrect answer. The capital is ' + country.capital);
    }
    nextQuestion();
}

function nextQuestion() {
    currentQuestion++;
    if (currentQuestion < countries.length) {
        document.getElementById('capital-input').value = '';
        displayQuestion();
        document.getElementById('submit-button').style.display = 'block'; // Display the submit button
    } else {
        displayQuestion();
        document.getElementById('submit-button').style.display = 'none'; // Hide the submit button
    }
}