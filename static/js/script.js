// Toggle visibility of the custom URL input box based on the selected radio button
document.querySelectorAll('input[name="url-type"]').forEach((radio) => {
    radio.addEventListener('change', () => {
        const customUrlBox = document.getElementById('custom-url-box');
        if (document.getElementById('custom-url').checked) {
            customUrlBox.style.display = 'block';
        } else {
            customUrlBox.style.display = 'none';
        }
    });
});

// Ensure the correct visibility of custom URL input on page load
window.addEventListener('DOMContentLoaded', () => {
    const customUrlBox = document.getElementById('custom-url-box');
    if (document.getElementById('custom-url').checked) {
        customUrlBox.style.display = 'block';
    } else {
        customUrlBox.style.display = 'none';
    }
});


// Toggle visibility of the custom URL input box based on the selected radio button
// document.querySelectorAll('input[name="url-type"]').forEach((radio) => {
//     radio.addEventListener('change', () => {
//         const customUrlBox = document.getElementById('custom-url-box');
//         if (document.getElementById('custom-url').checked) {
//             customUrlBox.style.display = 'block';
//         } else {
//             customUrlBox.style.display = 'none';
//         }
//     });
// });

// Handle the shorten button click
document.getElementById('btn-short').addEventListener('click', async () => {
    const userURL = document.getElementById('input').value.trim();
    const isCustom = document.getElementById('custom-url').checked;
    const customURL = document.getElementById('custom-input').value.trim();

    if (!userURL) {
        alert('Please enter a valid URL.');
        return;
    }

    // Build the payload
    const payload = { original_url: userURL };
    if (isCustom) {
        if (!customURL) {
            alert('Please enter a custom URL.');
            return;
        }
        payload.custom_short_url = customURL;
    }
    // alert(payload);
    console.log(payload)
    try {
        // Replace this with your actual API endpoint
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("API Error:", errorText); // Log response body for more details
            throw new Error('Failed to shorten the URL');
        }

        const data = await response.json();
        console.log(data)
        const shortURL = data.short_url; // Make sure this matches your API's response structure

        // Update the result section
        const resultDiv = document.getElementById('result');
        const shortURLLink = document.getElementById('short-url');

        shortURLLink.href = shortURL;
        shortURLLink.textContent = shortURL;

        resultDiv.style.display = 'block';
    } catch (error) {
        console.error(error);
        alert('Error: Unable to shorten the URL.');
    }
});

// Handle the copy button
document.getElementById('copy-btn').addEventListener('click', () => {
    const shortURL = document.getElementById('short-url').textContent;

    navigator.clipboard.writeText(shortURL)
        .then(() => {
            alert('Shortened URL copied to clipboard!');
        })
        .catch((error) => {
            console.error(error);
            alert('Failed to copy the URL.');
        });
});
