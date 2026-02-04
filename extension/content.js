document.addEventListener("mouseup", () => {
    const selectedText = window.getSelection().toString().trim();
    if (!selectedText) return;

    const existing = document.getElementById("bangla-tooltip");
    if (existing) existing.remove();

    fetch("https://bangla-translation-browser-extension.onrender.com/translate", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "X-API-KEY": "32504085-f55a-464a-814d-570a24729f63"
        },
        body: JSON.stringify({ text: selectedText })
    })
    .then(res => res.json())
    .then(data => {
        const tooltip = document.createElement("span");
        tooltip.id = "bangla-tooltip";
        tooltip.innerText = `${data.bangla}`;
        tooltip.style.background = "#ffffaa";
        tooltip.style.color = "#000";
        tooltip.style.border = "1px solid #ccc";
        tooltip.style.padding = "2px 4px";
        tooltip.style.borderRadius = "4px";
        tooltip.style.fontSize = "12px";
        tooltip.style.position = "absolute";
        tooltip.style.zIndex = 9999;

        const range = window.getSelection().getRangeAt(0);
        const rect = range.getBoundingClientRect();
        tooltip.style.top = `${rect.bottom + window.scrollY + 2}px`;
        tooltip.style.left = `${rect.left + window.scrollX}px`;

        document.body.appendChild(tooltip);
        setTimeout(() => tooltip.remove(), 5000);
    })
    .catch(err => console.error(err));
});
