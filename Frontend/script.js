// -------- PAGE NAVIGATION --------
function showPage(pageId) {

    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    document.getElementById(pageId).classList.add('active');

}


// -------- LANGUAGE HANDLING --------

let selectedLanguage = localStorage.getItem("userLanguage") || "en";

const langSelector = document.getElementById("global-lang");

if (langSelector) {
    langSelector.value = selectedLanguage;
}

function updateLang() {

    selectedLanguage = document.getElementById("global-lang").value;

    localStorage.setItem("userLanguage", selectedLanguage);

}



// -------- IMAGE PREVIEW --------

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");

if (imageInput) {

    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {

            preview.src = e.target.result;
            preview.style.display = "block";

        };

        reader.readAsDataURL(file);

    });

}



// -------- PREDICT DISEASE --------

async function predictDisease() {

    const fileField = document.querySelector('input[type="file"]');

    if (!fileField.files[0]) {

        alert("Please upload an image first!");
        return;

    }

    const formData = new FormData();
    formData.append("file", fileField.files[0]);

    const btn = document.getElementById("predictBtn");
    btn.innerText = "Analyzing...";

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/predict?lang=${selectedLanguage}`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        console.log("API RESPONSE:", data);

        displayResults(data);

    } catch (error) {

        console.error("FULL ERROR:", error);
        alert("Error: " + error.message);

    } finally {

        btn.innerText = "Predict Disease";

    }

}

document.getElementById("predictBtn").onclick = predictDisease;



// -------- DISPLAY RESULTS --------

function displayResults(data) {

    const resultArea = document.getElementById("resultArea");
    const cureList = document.getElementById("cureList");

    cureList.innerHTML = "";

    // Disease
    const disease = document.createElement("p");
    disease.innerHTML = "<b>Disease:</b> " + data.disease;
    cureList.appendChild(disease);

    // Disease Name
    const diseaseName = document.createElement("p");
    diseaseName.innerHTML = "<b>Disease Name:</b> " + data.disease_name;
    cureList.appendChild(diseaseName);

    // Index
    const index = document.createElement("p");
    index.innerHTML = "<b>Index:</b> " + data.index;
    cureList.appendChild(index);

    // Cure Title
    const cureTitle = document.createElement("h3");
    cureTitle.innerText = "Cure Steps:";
    cureList.appendChild(cureTitle);

    // Cure Steps
    data.cure.forEach(step => {

        const p = document.createElement("p");
        p.innerHTML = "• " + step;
        cureList.appendChild(p);

    });

    resultArea.classList.remove("hidden");
}
// -------- TEXT TO SPEECH --------

async function playAudio() {

   const cures = Array.from(
    document.querySelectorAll("#cureList p")
)
.map(p => p.innerText)
.join(". ");

const fullText = cures;

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/tts?text=${encodeURIComponent(fullText)}&lang=${selectedLanguage}`,
            { method: "POST" }
        );

        const data = await response.json();

        console.log("TTS RESPONSE:", data);

        if (!data.success) {
            alert("Audio generation failed");
            return;
        }

        const audioSrc = "data:audio/wav;base64," + data.audio_data;

        const audio = new Audio(audioSrc);
        audio.play();

    } catch (error) {

        console.error("TTS Error:", error);

    }
}

document.getElementById("listenBtn").onclick = playAudio;