document.addEventListener("DOMContentLoaded", () => {
    // Attach event listener to the survey form submission
    const surveyForm = document.getElementById("surveyForm");

    if (surveyForm) {
        surveyForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Prevent default form submission

            // Collect survey data from form inputs
            const formData = new FormData(surveyForm);
            const surveyData = {};

            formData.forEach((value, key) => {
                surveyData[key] = value;
            });

            console.log("Submitting survey data:", surveyData);

            try {
                // Send the survey data to the server
                const response = await fetch("/submit_survey", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(surveyData),
                });

                if (response.ok) {
                    const data = await response.json();

                    if (data.redirect_url) {
                        // Redirect to the recommendations page
                        window.location.href = data.redirect_url;
                    } else {
                        console.error("No redirect URL provided in response:", data);
                        alert("Submission successful, but redirection failed.");
                    }
                } else {
                    console.error("Failed to submit survey. Server responded with status:", response.status);
                    alert("Failed to submit survey. Please try again later.");
                }
            } catch (error) {
                console.error("Error submitting survey:", error);
                alert("An error occurred while submitting the survey. Please try again later.");
            }
        });
    } else {
        console.warn("Survey form not found on the page.");
    }
});
