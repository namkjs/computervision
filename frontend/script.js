const BACKEND_URL = "http://127.0.0.1:5000";

// Upload Image
document.getElementById("uploadForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("image");

    if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
    }

    formData.append("image", fileInput.files[0]);

    fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.filepath) {
                alert("Upload successful!");
                localStorage.setItem("filepath", data.filepath);
            } else {
                alert("Upload failed: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
});

// Process Image
document.getElementById("processForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const filepath = localStorage.getItem("filepath");
    if (!filepath) {
        alert("Please upload an image first!");
        return;
    }

    const operation = document.getElementById("operation").value;
    const params = {};

    // Get parameters and convert them to the correct type (number or string)
    document.querySelectorAll("#params input").forEach(input => {
        if (input.value) {
            if (input.type === "number") {
                params[input.name] = parseInt(input.value, 10);  // Convert to integer
            } else {
                params[input.name] = input.value;
            }
        }
    });

    console.log("Sending data:", { filepath, operation, params });

    fetch(`${BACKEND_URL}/process`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filepath, operation, params }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Processing error: " + response.statusText);
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const resultImage = document.getElementById("resultImage");
            resultImage.src = url;
            resultImage.style.display = "block";
        })
        .catch(error => console.error("Error:", error));
});

// Show dynamic parameters based on selected operation
document.getElementById("operation").addEventListener("change", function () {
    const operation = this.value;
    const paramsDiv = document.getElementById("params");
    paramsDiv.innerHTML = "";  // Clear previous parameters

    switch (operation) {
        case "highpass":
        case "lowpass":
            paramsDiv.innerHTML = `
                <label for="cutoff">Cutoff Frequency (Example: 30):</label>
                <input type="number" class="form-control" id="cutoff" name="cutoff" value="30">
            `;
            break;

        case "power_law":
            paramsDiv.innerHTML = `
                <label for="gamma">Gamma (Example: 1.0):</label>
                <input type="number" step="0.1" class="form-control" id="gamma" name="gamma" value="1.0">
            `;
            break;

        case "mean_filter_algorithm":
        case "median_filter_algorithm":
        case "dilation_opencv":
        case "dilation_algorithm":
        case "erosion_opencv":
        case "erosion_algorithm":
            paramsDiv.innerHTML = `
                <label for="kernel_size">Kernel Size (Example: 3):</label>
                <input type="number" class="form-control" id="kernel_size" name="kernel_size" value="3">
            `;
            break;

        case "adaptive_threshold":
            paramsDiv.innerHTML = `
                <label for="block_size">Block Size (Example: 11):</label>
                <input type="number" class="form-control" id="block_size" name="block_size" value="11">
                <label for="C">C (Example: 2):</label>
                <input type="number" class="form-control" id="C" name="C" value="2">
            `;
            break;

        case "kmeans_clustering":
            paramsDiv.innerHTML = `
                <label for="k">Number of Clusters (Example: 3):</label>
                <input type="number" class="form-control" id="k" name="k" value="3">
                <label for="max_iter">Max Iterations (Example: 100):</label>
                <input type="number" class="form-control" id="max_iter" name="max_iter" value="100">
                <label for="epsilon">Epsilon (Example: 0.2):</label>
                <input type="number" step="0.1" class="form-control" id="epsilon" name="epsilon" value="0.2">
            `;
            break;

        case "jpeg_compress":
            paramsDiv.innerHTML = `
                <label for="quality">JPEG Quality (Example: 90):</label>
                <input type="number" class="form-control" id="quality" name="quality" value="90">
            `;
            break;

        default:
            paramsDiv.innerHTML = `<p class="text-muted">No additional parameters required for this operation.</p>`;
            break;
    }
});
