$( document ).ready(function() {

    // Get review data
    $.ajax({
        headers: { "X-CSRFToken": CSRF_TOKEN },
        url: AVAILABLE_REVIEWS_URL,
        method: 'GET',
        success: function(data) {

            // Elements
            var questionH4  = $('#question-text'),
                answerInput = $('#answer-input'),
                submitButton = $('#submit-answer-btn'),
                lessonButton = $('#lesson-btn');

            var get_random_index = function(arr) {
                /* Return random index of array */
                return Math.floor(Math.random() * arr.length);
            }
            
            var shuffle = function(arr) {
                /* Shuffle array in place */
                var n       = 2*arr.length,
                    temp    = 0,
                    swap    = 0;
                for (let i = 0; i < n; i++) {
                    swap = get_random_index(arr);
                    temp = arr[swap];
                    arr[swap] = arr[0];
                    arr[0] = temp;
                }
            };

            // Shuffle reviews and select random question, answer per review
            var reviews = data['reviews'];
            shuffle(reviews);
            for (let indReview = 0; indReview < reviews.length; indReview++) {
                review = reviews[indReview];
                qnaPairs = review['qna_pairs'];
                qna = qnaPairs[get_random_index(qnaPairs)];
                review['chosen_qna'] = { 
                    'question': qna[0], 
                    'answer': qna[1] 
                };

                // Also add some structure required to track user submissions
                review['was_ever_incorrect'] = false;
                review['was_answered'] = false;
            }

            // Initialize cyclical review process
            var pageState = {
                'review_index': 0,
                'answer_visible': false,
                'details_available': false,
                'can_change_state': true
            }
            questionH4.text(pageState['review_index']);

            // Hook up submit button functionality
            submitButton.click(function() {
                var currentReview = reviews[pageState['review_index']];
                var userAnswer = answerInput.val();
                var correctAnswer = currentReview['chosen_qna']['answer'];
                if (userAnswer == correctAnswer) {
                    console.log('Correct!');
                } else {
                    console.log('You dumb');
                    console.log(correctAnswer);
                }
            });
        },
        failure: function(data) {

            // Show error message
            console.log('Now you fucked up'); 
        }
    });

});