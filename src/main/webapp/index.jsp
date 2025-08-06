<!DOCTYPE html>
<html>
  <head>
    <title>
      HackRx LLM
    </title>
  </head>
  <body>
    <h1>
      hello how are you
    </h1>
    <form id = "userIntraction">
      <label for="File Link">Text Input</label></br>
      <input type="text" id="fileLink" name="textInput" placeholder="Enter Link here"></br>
      <lable for="Question">Questions</lable></br>
      <input type="text" id="questionInput" name="questionInput" placeholder="Enter Questions here"></br>
      <button id="submitButton" type = "submit">Submit</button>
    </form>


    <script>
      document.getElementById("userIntraction").addEventListener("submit", async function(event) {
        event.preventDefault(); // stop default form submission

        const link = document.getElementById("fileLink").value;
        const question = document.getElementById("questionInput").value;
        // Construct JSON payload
        const data = {
          documents : link, 
          query: question
        };

        try {
          const response = await fetch("hackrx/run", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + System.getenv("default_token")
            },
            body: JSON.stringify(data)
          }); 

          const result = await response.text(); // assuming you return raw HTML or JSON
          document.body.innerHTML += `<pre>${result}</pre>`;
        } catch (err) {
          console.error("Fetch error:", err);
        }
      });
    </script>
    
  </body>
</html>
