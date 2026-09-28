document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("contact-form");
    const button = document.getElementById("send-message-btn");
    console.log("helllo");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        button.disabled = true;
        button.innerText = "Sending...";

        const formData = new FormData(form);

        try {

            const response = await fetch("/send-message/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                },
                body: formData
            });

            const data = await response.json();
            console.log("data");

            if (data.success) {

                Swal.fire({
                    icon: "success",
                    title: "Message Sent!",
                    text: data.message,
                    confirmButtonText: "OK"
                });

                form.reset();

            } else {

                Swal.fire({
                    icon: "error",
                    title: "Oops!",
                    text: data.message,
                    confirmButtonText: "OK"
                });
            }

        } catch (error) {

            console.error("Error:", error);

            Swal.fire({
                icon: "error",
                title: "Something went wrong!",
                text: "Unable to send your message. Please try again.",
                confirmButtonText: "OK"
            });

        } finally {

            button.disabled = false;
            button.innerText = "Send Message";

        }

    });


    function getCSRFToken() {

        const csrfToken = document.querySelector(
            '[name=csrfmiddlewaretoken]'
        );

        return csrfToken ? csrfToken.value : "";

    }

});