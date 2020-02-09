$( document ).ready(function() {

    // Temporarily disable form Enter keypress
    $("#answer-form").keydown(function(e) {
        if (e.keyCode == 13) { e.preventDefault(); return false; }
    });

    // Get review data
    $.ajax({
        headers: { "X-CSRFToken": CSRF_TOKEN },
        url: AVAILABLE_REVIEWS_URL,
        method: 'GET',
        success: function(data) {

            // Redirect if no reviews
            if (data['reviews'].length == 0) { window.location.replace(PROFILE_URL); }

            // Page elements
            var questionH4   = $('#question-text'),
                answerInput  = $('#answer-input'),
                submitButton = $('#submit-answer-btn'),
                lessonButton = $('#lesson-btn'),
                mainDiv      = $('#main-div'),
                correctSpan  = $('#correct-answer');

            // Reroute Enter keypress on form to submitButton click
            $("#answer-form").keydown(function(e) {
                if (e.keyCode == 13) { e.preventDefault(); submitButton.click(); return false; }
            });

            var get_random_index = function(arr) {
                /* Return random index of array */
                return Math.floor(Math.random() * arr.length);
            };
            
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
                review['is_done'] = false;
            }

            // Initialize cyclical review process
            var pageState = {
                'review_index': 0,
                'answer_visible': false,
                'details_enabled': false,
                'answer_submitted': false
            }
            questionH4.text(reviews[0]['chosen_qna']['question']);

            var get_current_review_values = function() {
                var currentReview = reviews[pageState['review_index']];
                return {
                    'current_review' : currentReview,
                    'question'       : currentReview['chosen_qna']['question'],
                    'correct_answer' : currentReview['chosen_qna']['answer'],
                    'user_answer'    : answerInput.val()
                };
            };

            var get_next_review_index = function() {
                /* Get next review index that hasn't been done, or -1 if all done */
                start = 1 + pageState['review_index'];
                for (let i = start; i < reviews.length; i++) { 
                    if (!reviews[i]['is_done']) { return i; }
                }
                for (let i = 0;     i < start;          i++) { 
                    if (!reviews[i]['is_done']) { return i; }
                }
                return -1;
            };

            var lessonButtonClick = function(e) {
                /* Hide/show lesson details */
                e.preventDefault();
                if (!pageState['details_enabled']) { return false; }
                var lessonDiv = $('#lesson-div');
                if (lessonDiv.hasClass('d-none')) {
                    lessonDiv.removeClass('d-none');
                    //
                    // TODO: display real lesson details here
                    //
                    lessonDiv.html('<p>This feature coming soon :^)</p>');
                } else {
                    lessonDiv.addClass('d-none');
                    lessonDiv.html('');
                }
            };

            var postReviews = function(isExit) {
                /* POST reviews to the server to save progress in database */
                $.ajax({
                    headers: { "X-CSRFToken": CSRF_TOKEN },
                    url: SAVE_REVIEWS_URL,
                    method: 'POST',
                    data: {'reviews': JSON.stringify(reviews)},
                    dataType: 'json',
                    isExit: isExit,
                    success: function(data) {
                        if (!isExit) { window.location.replace(window.location.origin + data['redirect']); }
                    },
                    error: function(err) {
                        console.log('Error: ');
                        console.log(err);
                    }
                });

                // Now overwrite this function so you can only call it once
                postReviews = function(isExit) { return false; }
            };

            var colorClasses = ['color-2', 'color-correct', 'color-incorrect'];
            var pageActions = {
                'set_color_class': 
                    function(colorClass) {
                        for (cc of colorClasses) { mainDiv.removeClass(cc); }
                        mainDiv.addClass(colorClass);
                    },
                'show_answer': 
                    function() {
                        var text = 'Answer: ' + get_current_review_values()['correct_answer'];
                        correctSpan.text(text);
                        correctSpan.removeClass('ghost');
                        pageState['answer_visible'] = true;
                    },
                'hide_answer': 
                    function() {
                        correctSpan.text('');
                        correctSpan.addClass('ghost');
                        pageState['answer_visible'] = false;
                    },
                'enable_details': 
                    function() { 
                        lessonButton.removeClass('disabled');
                        lessonButton.click(lessonButtonClick);
                        pageState['details_enabled'] = true; 
                    },
                'disable_details': 
                    function() { 
                        lessonButton.addClass('disabled');
                        lessonButton.off('click');
                        $('#lesson-div').html('');
                        $('#lesson-div').addClass('d-none');
                        pageState['details_enabled'] = false;
                    },
                'update_review': 
                    function(isCorrect) {
                        review = get_current_review_values()['current_review'];
                        if (isCorrect) {
                            review['is_done'] = true;
                        } else {
                            review['was_ever_incorrect'] = true;
                        }
                    },
                'update_question':
                    function(text='') {
                        if (text === '') { questionH4.text(get_current_review_values()['question']); }
                        else { questionH4.text(text); }
                    },
                'clear_answer_input':
                    function() {
                        answerInput.val('');
                        answerInput.focus();
                    }
            }

            var correct_actions = function() {
                /* Change page when correct answer is submitted */
                var isCorrect = true;
                pageState['answer_submitted'] = true;
                pageActions['set_color_class']('color-correct');
                pageActions['update_review'](isCorrect);
                pageActions['enable_details']();
            };

            var incorrect_actions = function() {
                /* Change page when incorrect answer is submitted */
                var isCorrect = false;
                pageState['answer_submitted'] = true;
                pageActions['set_color_class']('color-incorrect');
                pageActions['show_answer']();
                pageActions['update_review'](isCorrect);
                pageActions['enable_details']();
            };

            var next_actions = function() {
                /* Change page when user moves to next review */
                pageState['review_index'] = get_next_review_index();
                if (pageState['review_index'] < 0) { 
                    // Submit results to the server for processing and redirection
                    submitButton.off('click');
                    pageActions['update_question']('Done! Processing your reviews...');
                    postReviews();
                } else {
                    // Update page with next review question stuff
                    pageActions['update_question']();
                    pageActions['set_color_class']('color-2');
                    pageActions['hide_answer']();
                    pageActions['disable_details']();
                    pageActions['clear_answer_input']();
                    pageState['answer_submitted'] = false;
                }
            };

            // Hook up submit button functionality
            submitButton.click(function(e) {
                e.preventDefault();
                if (pageState['answer_submitted']) {
                    console.log('Next review');
                    next_actions();
                } else {
                    crv = get_current_review_values();
                    if (crv['user_answer'] == crv['correct_answer']) {
                        console.log('Correct!');
                        correct_actions();
                    } else {
                        console.log('Incorrect. You dumb as hell');
                        console.log(crv['correct_answer']);
                        incorrect_actions();
                    }
                }

                console.log('Page state:');
                console.log(pageState);
            });

            // Before exiting, send server your review progress for processing
            $( window ).on('beforeunload', function() { 
                console.log('sup bruh');
                console.log(reviews);
                postReviews(isExit=true); 
            });
        },
        failure: function(data) {

            // Show error message
            console.log('Failed to load reviews. What a disappointment!'); 
            window.location.redirect(PROFILE_URL);
        }
    });

});