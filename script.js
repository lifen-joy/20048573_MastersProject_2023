// When the form is submitted, send an AJAX request to the server to check the text
$('#text-form').submit(function(event) {
    event.preventDefault();
    var formData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: '/',
        data: formData,
        success: function(data) {
            // Clear any previous recommendations and display the new ones
            $('#recommendation-list').empty();
            for (var i = 0; i < data.recommendations.length; i++) {
                var recommendation = data.recommendations[i];
                var li = $('<li>').addClass('recommendation');
                var h3 = $('<h3>').text(recommendation['word']);
                var p1 = $('<p>').text('Tone: ' + recommendation['tone']);
                var p2 = $('<p>').text('Inclusive alternative: ' + recommendation['alt word']);
                var p3 = $('<p>').text('Context: ' + recommendation['context']);
                var p4 = $('<p>').text('Definition: ' + recommendation['definition']);
                var p5 = $('<p>').text('Reason: ' + recommendation['reason']);
                li.append(h3, p1, p2, p3, p4, p5);
                $('#recommendation-list').append(li);
            }
            // Display the input text
            $('#input-text').text(data.input_text);
            // Show the recommendations section
            $('#recommendations').show();
        }
    });
});

//Reference list

