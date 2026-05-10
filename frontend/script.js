const API_BASE = "http://localhost:8000";


function addMessage(text, type) {

    const div = document.createElement("div");

    div.className = "message " + type;

    div.innerText = text;

    document.getElementById("messages").appendChild(div);

    const messages = document.getElementById("messages");
    messages.scrollTop = messages.scrollHeight;
}

async function processData() {

    const files = document.getElementById("pdfUpload").files;

    const youtube = document.getElementById("youtubeLink").value;

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    formData.append("youtube", youtube);

    const statusBox = document.getElementById("statusBox");

    statusBox.className = "status-box processing";

    statusBox.innerHTML = `
        <div class="loader"></div>
        <span>Processing documents...</span>
    `;

    try {

        const res = await fetch(`${API_BASE}/process`, {
            method: "POST",
            body: formData
        });

        await res.json();

        statusBox.className = "status-box success";

        statusBox.innerHTML = `
            ✅ Documents processed successfully!
        `;

    } catch (error) {

        statusBox.className = "status-box error";

        statusBox.innerHTML = `
            ❌ Error processing documents.
        `;

        console.error(error);
    }
}


async function askQuestion() {

    const questionInput = document.getElementById("question");

    const question = questionInput.value.trim();

    if (!question) return;

    questionInput.value = "";

    addMessage(question, "user");

    const thinkingDiv = document.createElement("div");

    thinkingDiv.className = "message bot";

    thinkingDiv.innerText = "Thinking...";

    document.getElementById("messages").appendChild(thinkingDiv);

    thinkingDiv.scrollIntoView({
        behavior: "smooth"
    });

    try {

        const res = await fetch(`${API_BASE}/query`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question
            })
        });

        const data = await res.json();

        thinkingDiv.remove();

        addMessage(data.answer, "bot");

        if (data.latency) {
            addMessage(
                `⏱ Response generated in ${data.latency.toFixed(2)} seconds`,
                "bot"
            );
        }

    } catch (error) {

        thinkingDiv.remove();

        addMessage("Error getting response.", "bot");

        console.error(error);
    }
}

function handleKey(event) {

    if (event.key === "Enter") {

        askQuestion();
    }
}