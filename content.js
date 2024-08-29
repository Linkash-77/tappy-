// content.js

function injectAIButton() {
    const posts = document.querySelectorAll('.linkedin-post-class'); // Adjust this selector

    posts.forEach(post => {
        const aiButton = document.createElement('button');
        aiButton.textContent = 'AI Comment';
        aiButton.className = 'ai-comment-button';

        post.appendChild(aiButton);

        aiButton.addEventListener('click', function() {
            const postText = post.querySelector('.post-text-class').innerText; // Adjust selector to fetch the post text
            fetch('https://your-flask-api-url.com/process', { // Replace with your actual API URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: postText }),
            })
            .then(response => response.json())
            .then(data => {
                // Display the summary and sentiment
                alert(`Summary: ${data.summary}\nSentiment: ${data.sentiment} (${data.percentage}%)`);
                // You can also add the summary and sentiment as a comment or display it in a different way
            })
            .catch(error => console.error('Error:', error));
        });
    });
}

document.addEventListener('DOMContentLoaded', injectAIButton);
