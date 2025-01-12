document.getElementById("upload-form").onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    alert(result.message || result.error);
};

async function sendQuery() {
    const query = document.getElementById("query").value;
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query})
    });
    const result = await response.json();
    document.getElementById("response").innerText = result.response;
}