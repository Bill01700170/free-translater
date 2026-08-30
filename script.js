async function translateText() {
    const text = document.getElementById("textInput").value;
    const fromLanguage = document.getElementById("fromLanguage").value;
    const toLanguage = document.getElementById("toLanguage").value;
    const translation = document.getElementById("translation");

    if (text.trim() === "") {
        translation.textContent = "Please enter something to translate.";
        return;
    }

    translation.textContent = "Translating... 🤖";

    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                fromLanguage: fromLanguage,
                toLanguage: toLanguage
            })
        });

        const data = await response.json();

        if (data.error) {
            translation.textContent = "Error: " + data.error;
            return;
        }

        translation.textContent = data.translation;

    } catch (error) {
        translation.textContent =
            "Could not connect to the translation server.";
        console.error(error);
    }
}