$(function() {
    // Handle form submission
    $('#text-form').submit(function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the text input value from the form
        var text = $('#text-input').val();

        // Send a POST request to the Flask app to check the text for offensive words
        $.ajax({
            url: '/check',
            method: 'POST',
            data: { text: text },
            success: function(response) {
                // Clear any previous results
                $('#result').empty();

                // Display the results
                if (response.status === 'success') {
                    $('#result').addClass('success');
                    $('#result').text(response.message);
                } else if (response.status === 'warning') {
                    $('#result').addClass('warning');
                    $('#result').text(response.message);

                    // Add the offensive words and suggestions to the result message
                    var html = '';
                    for (var i = 0; i < response.offensive_words.length; i++) {
                        html += '<p><strong>' + response.offensive_words[i] + '</strong>: ' + response.suggestions[i] + '</p>';
                    }
                    $('#result').append(html);
                }
            },
            error: function(xhr, status, error) {
                console.log('Error:', error);
            }
        });
    });
});
