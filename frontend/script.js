const BACKEND_URL = "http://127.0.0.1:5000";

// Upload image
document.getElementById("uploadForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById("image");
    formData.append("image", fileInput.files[0]);

    fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            localStorage.setItem("filepath", data.filepath);
        })
        .catch(error => console.error("Error:", error));
});

// Process image
document.getElementById("processForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const filepath = localStorage.getItem("filepath");
    if (!filepath) {
        alert("Please upload an image first!");
        return;
    }

    const operation = document.getElementById("operation").value;
    const cutoff = document.getElementById("cutoff") ? document.getElementById("cutoff").value : null;
    const gamma = document.getElementById("gamma") ? document.getElementById("gamma").value : null;
    const kernel_size = document.getElementById("kernel_size") ? document.getElementById("kernel_size").value : null;

    const params = {};
    if (cutoff) params.cutoff = parseInt(cutoff);
    if (gamma) params.gamma = parseFloat(gamma);
    if (kernel_size) params.kernel_size = parseInt(kernel_size);

    fetch(`${BACKEND_URL}/process`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filepath, operation, params }),
    })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const resultImage = document.getElementById("resultImage");
            resultImage.src = url;
            resultImage.style.display = "block";
        })
        .catch(error => console.error("Error:", error));
});

// Update parameters based on selected operation
document.getElementById("operation").addEventListener("change", function() {
    const operation = this.value;
    const paramsDiv = document.getElementById("params");
    
    // Clear previous parameters
    paramsDiv.innerHTML = "<h3>Parameters (Optional)</h3>";

    // Add relevant parameters for selected operation
    switch (operation) {
        case "highpass":
        case "lowpass":
            paramsDiv.innerHTML += `
                <label for="cutoff">Cutoff:</label>
                <input type="number" id="cutoff" name="cutoff">
            `;
            break;
        case "power_law":
            paramsDiv.innerHTML += `
                <label for="gamma">Gamma:</label>
                <input type="number" step="0.1" id="gamma" name="gamma">
            `;
            break;
        case "mean_filter_algorithm":
        case "median_filter_algorithm":
            paramsDiv.innerHTML += `
                <label for="kernel_size">Kernel Size:</label>
                <input type="number" id="kernel_size" name="kernel_size">
            `;
            break;
        case "logarithmic":
            paramsDiv.innerHTML += `
                <label for="c">C:</label>
                <input type="number" step="0.1" id="c" name="c">
            `;
            break;
        default:
            break;
    }
});
