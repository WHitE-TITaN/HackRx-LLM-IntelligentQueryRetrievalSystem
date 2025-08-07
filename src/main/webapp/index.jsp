<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<%
    String defaultToken = System.getenv("default_token");
    if (defaultToken == null) {
        defaultToken = ""; // fallback if env var is missing
    }
%>
<!DOCTYPE html>
<html>
<head>
    <title>HackRx LLM</title>
</head>
<body>
    <h1>Hello! How are you?</h1>

    <form id="userInteraction">
        <label for="fileLink">Text Input</label><br>
        <input type="text" id="fileLink" name="textInput" placeholder="Enter Link here"><br>

        <label for="Question">Questions</label><br>
        <input type="text" id="Question" name="questionInput" placeholder="Enter Questions here"><br>

        <input type="hidden" id="default_token" value="<%= defaultToken %>"><br>
        <button id="submitButton" type="submit">Submit</button>
    </form>

    <script>
        window.addEventListener("DOMContentLoaded", () => {
            document.getElementById("userInteraction").addEventListener("submit", async function (event) {
                event.preventDefault(); // prevent default form submission

                const link = document.getElementById("fileLink").value;
                const question = document.getElementById("Question").value;
                const token = document.getElementById("default_token").value;

                const data = {
                    documents: link,
                    query: question
                };

                try {
                    const response = await fetch("api/v1", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer " + token
                        },
                        body: JSON.stringify(data)
                    });

                    const result = await response.text();
                    console.log("Response status:", response.status);
                    console.log("Token sent:", token);
                    document.body.innerHTML += `<pre>${result}</pre>`;
                } catch (err) {
                    console.error("Fetch error:", err);
                }
            });
        });
    </script>
</body>
</html>
