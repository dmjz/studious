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

            // Page elements
            var questionH4   = $('#question-text'),
                answerInput  = $('#answer-input'),
                submitButton = $('#submit-answer-btn'),
                lessonButton = $('#lesson-btn'),
                mainDiv      = $('#main-div'),
                correctSpan  = $('#correct-answer');

            // Send Enter keypress on form to submitButton click
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

            lessonButton.click(function() {
                //
                // TODO: display real lesson details here
                //
                var lessonDiv = $('#lesson-div');
                if (lessonDiv.hasClass('ghost')) {
                    console.log('Show lesson div');
                    lessonDiv.removeClass('ghost');
                    lessonDiv.html('<p>Placeholder for real lesson details here</p>');
                } else {
                    console.log('Show lesson div');
                    lessonDiv.html('');
                    lessonDiv.addClass('ghost');
                }
            });

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
                        lessonButton.prop("disabled", false);
                        pageState['details_enabled'] = true; 
                    },
                'disable_details': 
                    function() { 
                        lessonButton.prop("disabled", true);
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
            }

            var correct_actions = function() {
                /* Change page when correct answer is submitted */
                var isCorrect = true;
                pageState['answer_submitted'] = true;
                pageActions['set_color_class']('color-correct');
                pageActions['update_review'](isCorrect);
            };

            var incorrect_actions = function() {
                /* Change page when incorrect answer is submitted */
                var isCorrect = false;
                pageState['answer_submitted'] = true;
                pageActions['set_color_class']('color-incorrect');
                pageActions['show_answer']();
                pageActions['update_review'](isCorrect);
            };

            var next_actions = function() {
                /* Change page when user moves to next review */
                pageState['review_index'] = get_next_review_index();
                if (pageState['review_index'] < 0) { 
                    // Submit results to the server for processing and redirection
                    submitButton.off('click');
                    submitButton.prop('disabled', false);
                    pageActions['update_question']('Done! Processing your reviews...');
                    //
                    // TODO: submit stuff to server now
                    //
                } else {
                    // Update page with next review question stuff
                    pageActions['update_question']();
                    pageActions['set_color_class']('color-2');
                    pageActions['hide_answer']();
                    pageActions['disable_details']();
                    pageState['answer_submitted'] = false;
                }
            };

            // Hook up submit button functionality
            submitButton.click(function() {
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
        },
        failure: function(data) {

            // Show error message
            console.log('Failed to load reviews. What a disappointment'); 
        }
    });

});